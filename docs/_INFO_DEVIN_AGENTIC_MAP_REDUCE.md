# INFO: Devin Agentic MapReduce

**Doc ID**: AGNTMAPR-IN01
**Goal**: Document the Agentic MapReduce architecture as implemented by Devin, covering the 5-stage pipeline, design rationale, Security Swarm application, and evaluation results
**Timeline**: Created 2026-07-21, Updated 2 times (2026-07-21)

## Summary

- Agentic MapReduce is a 5-stage pipeline (Plan, Shard, Map, Reduce, Verify) for whole-codebase reasoning tasks where completeness is required [VERIFIED]
- Agents are placed only where reasoning is needed (Plan, Map, Reduce, Verify); selection/sharding is deterministic with no model in the loop [VERIFIED]
- Coverage is guaranteed by construction: a deterministic pass produces a finite work queue, every shard is assigned, scan completes only when queue is exhausted [VERIFIED]
- Cost tracks relevant code volume, not total repo size; re-runs only process files changed since last scanned commit [VERIFIED]
- Security Swarm is the first production implementation: 72% recall on 50 real Common Vulnerabilities and Exposures (CVE) entries across 14 languages at $90.23/scan average [VERIFIED]
- Outperforms Claude Security (68% at $131.87), Codex Security (48%, no cost data), Cursor Security (26% at $4.60) [VERIFIED]
- The Reduce stage enables cross-shard attack chain composition that no isolated worker could discover (e.g., unauthenticated ID leak + ID-gated Remote Code Execution (RCE) = P0 unauthenticated RCE) [VERIFIED]
- Evaluation uses post-training-cutoff CVEs pinned to pre-fix commits, ensuring hits reflect code reasoning not memorization [VERIFIED]

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Architecture Overview](#2-architecture-overview)
   - [2.1 Design Rationale](#21-design-rationale-how-each-decision-eliminates-a-failure-mode)
   - [2.2 Classic vs Agentic MapReduce](#22-classic-mapreduce-vs-agentic-mapreduce)
3. [Pipeline Stages](#3-pipeline-stages)
4. [Security Swarm Implementation](#4-security-swarm-implementation)
5. [Evaluation Methodology](#5-evaluation-methodology)
6. [Results](#6-results)
7. [Applicability Beyond Security](#7-applicability-beyond-security)
8. [Next Steps](#8-next-steps)
9. [Sources](#9-sources)
10. [Document History](#10-document-history)

## 1. Problem Statement

Whole-codebase tasks (security scanning, code-quality enforcement, breaking-change detection) share a defining property: **the result is only trustworthy if the entire codebase was considered.**

A single search-driven agent pointed at a large repo (50k+ files) fails in three specific ways:

- **Budget spent finding work, not doing it.** According to [Zhang et al., FastContext (2026)](https://arxiv.org/abs/2606.14066), reading and searching consumed 56.2% of tool-use turns and 46.5% of main-agent tokens across 300 SWE-bench Multilingual trajectories (GPT-5.4-high with Mini-SWE-Agent). Selection dominates analysis.
- **Context becomes a shared bottleneck.** A long-running agent carries discoveries from one part of the repo while reasoning about the next. Unrelated evidence competes for attention and context budget as the run grows.
- **No explicit coverage boundary.** A search-driven agent stops when it decides it's done, not when a finite work queue has been exhausted. There is no guarantee every relevant file was considered.

These issues scale with repo size, making the single-agent approach structurally unsuitable for whole-codebase tasks.

## 2. Architecture Overview

[Agentic MapReduce](https://devin.ai/blog/agentic-map-reduce) adapts the classic distributed systems pattern (shard a large input, map over every shard in parallel, reduce results into one answer) for agent reasoning.

**Key inversion from classic MapReduce:** Where classic MapReduce processes the entire input using handwritten instructions, Agentic MapReduce uses an agent to decide what matters for the current codebase. Then a deterministic pass finds every instance of it.

**Design principle:** Put agents where reasoning is required (synthesizing the decomposition function, inspecting the shards, and the reduction). Everything else is deterministic.

```
┌────────────┐      ┌────────────┐      ┌────────────┐      ┌────────────┐      ┌────────────┐
│   1 PLAN   │      │  2 SHARD   │      │   3 MAP    │      │  4 REDUCE  │      │  5 VERIFY  │
│  (Agentic) │ ──>  │(Deterministic) ──> │  (Agentic) │ ──>  │  (Agentic) │ ──>  │  (Agentic) │
└────────────┘      └────────────┘      └────────────┘      └────────────┘      └────────────┘
     │                    │                    │                    │                    │
  Agent writes      Selectors run         One worker per       Dedupes, chains,    Reproduces in
  selectors for     over ALL files;       batch in parallel;   prioritizes across   sandbox per
  this repo         matches bucketed      focused context      all shards           finding
```

- **Plan** - Agent studies repo, authors selectors (patterns identifying relevant code). Agentic: yes
- **Shard** - Selectors run deterministically over entire repo; matches bucketed. Agentic: no
- **Map** - One agent per batch, in parallel, does per-shard reasoning. Agentic: yes
- **Reduce** - Agent groups, dedupes, synthesizes per-shard outputs into final answer. Agentic: yes
- **Verify** - Agent reproduces findings in sandbox against running build. Agentic: yes

### 2.1 Design Rationale: How Each Decision Eliminates a Failure Mode

Each failure mode from single-agent whole-codebase scanning (section 1) maps to a specific architectural decision:

```
 Failure Mode                 Architectural Decision              Guarantee
┌───────────────────────┐    ┌───────────────────────────┐    ┌─────────────────────────┐
│ Budget spent FINDING  │    │ Plan once, then run       │    │ Tokens spent on relevant │
│ work, not doing it    │ -> │ selectors deterministically│ -> │ code only, not searching │
│ (56% of tool-use)     │    │ (no model in selection)   │    │ through the rest         │
├───────────────────────┤    ├───────────────────────────┤    ├─────────────────────────┤
│ Context is a shared   │    │ Bounded batches with      │    │ Each worker starts fresh, │
│ bottleneck (grows     │ -> │ independent workers,      │ -> │ no cross-contamination   │
│ with discoveries)     │    │ no shared state           │    │ between unrelated code   │
├───────────────────────┤    ├───────────────────────────┤    ├─────────────────────────┤
│ No explicit coverage  │    │ Deterministic pass over   │    │ Finite work queue;       │
│ boundary (agent       │ -> │ ALL files produces finite │ -> │ complete only when queue  │
│ decides when "done")  │    │ work queue before mapping │    │ is exhausted             │
└───────────────────────┘    └───────────────────────────┘    └─────────────────────────┘
```

**Why Shard is deterministic:** If an agent decided which files to inspect, it would reintroduce failure mode 1 (budget spent finding work) and failure mode 3 (no coverage guarantee). Deterministic selection ensures every file is evaluated, cheaply, without model tokens.

**Why Map uses independent workers:** If workers shared context, they would reintroduce failure mode 2 (context bottleneck). Fresh context per shard means each worker's reasoning capacity is spent entirely on its bounded assignment.

**Why Reduce exists as a separate stage:** Independent workers cannot see cross-shard relationships (attack chains, cascading breaking changes). The Reducer operates on compressed conclusions rather than full transcripts, keeping cost proportional to findings rather than to codebase size.

### 2.2 Classic MapReduce vs Agentic MapReduce

```
                    Classic MapReduce              Agentic MapReduce
                    ─────────────────              ─────────────────
 What is fixed:     Map/Reduce functions           The codebase (input)
                    (written by programmer)

 What varies:       The input data                 The decomposition strategy
                                                   (written by planner agent)

 Selection:         Process ALL input              Agent decides what matters,
                    (no filtering)                 then deterministic pass finds it

 Map function:      Deterministic transform        Agentic reasoning per shard
                    (same input = same output)     (judgment, not computation)

 Key inversion:     Human writes instructions,     Agent writes instructions,
                    machine executes on data       machine executes on codebase,
                                                   agents reason on results
```

The critical insight: classic MapReduce assumes the programmer knows what computation to apply. Agentic MapReduce assumes the agent must first discover what matters for this specific codebase, then systematize that discovery into a deterministic pass.

## 3. Pipeline Stages

### 3.1 Plan

The planner studies the repo and produces **selectors**: relevance tests concrete enough to run deterministically over the whole codebase with no model in the loop. Reasoning is spent once, when the selectors are authored.

A selector's language depends on the task and the codebase:
- Tree-sitter query over syntax nodes
- Compiler query over symbols and types
- Traversal of an import or call graph
- Comparison of generated API schemas
- Lexical pattern for a repository-specific convention

**Selector examples by task:**

- **Security Scanning** - Select route declarations, auth boundaries, deserialization entry points, calls to dangerous APIs
- **Breaking-Change Detection** - Compare exported symbols or generated API schemas, then select affected consumers
- **Code-Quality Enforcement** - Identify functions exceeding complexity threshold, pattern-match deprecated API usage, flag unhandled error paths

### 3.2 Shard

The selectors run deterministically over **every** file in the repository. Files that match nothing are dropped from consideration. The remaining matches are packed into **bounded batches**.

This stage is fully deterministic (no model). It produces the finite work queue that guarantees coverage.

Example: 7 files emit signals, grouped into 3 bounded batches; the rest are dropped.

### 3.3 Map

Each batch gets its own worker agent (child Devin session), running in parallel from a fresh, focused context. A worker:
1. Receives its batch's signals and rule provenance
2. Reads the real code it needs to reach a verdict
3. Emits structured results: zero or more findings with severity and confidence

Workers run independently. No shared state between them. Each reasons from a focused context for one bounded shard only.

```
               Shard Stage                          Map Stage (parallel)
┌─────────────────────────────┐      ┌──────────────────────────────────────┐
│  Entire Repo (N files)      │      │                                      │
│  ┌───┐┌───┐┌───┐┌───┐┌───┐  │      │  ┌─────────┐                         │
│  │ . ││ x ││ . ││ x ││ x │  │      │  │Worker 1 │ Batch 1 → 2 findings    │
│  └───┘└───┘└───┘└───┘└───┘  │      │  └─────────┘                         │
│  ┌───┐┌───┐┌───┐┌───┐┌───┐  │      │  ┌─────────┐                         │
│  │ x ││ . ││ . ││ x ││ . │  │ ──>  │  │Worker 2 │ Batch 2 → 0 findings    │
│  └───┘└───┘└───┘└───┘└───┘  │      │  └─────────┘                         │
│                             │      │  ┌─────────┐                         │
│  x = match, . = dropped     │      │  │Worker 3 │ Batch 3 → 1 finding     │
└─────────────────────────────┘      └──────────────────────────────────────┘
 7 matches → 3 bounded batches         3 workers run in parallel, fresh context
```

### 3.4 Reduce

A Reducer session aggregates results, consuming **only outputs from workers that produced findings** (zero-finding workers are ignored). The Reducer:
1. Consumes structured outputs (conclusions, not full transcripts)
2. Deduplicates overlapping results
3. Reconciles local conclusions
4. Applies global prioritization
5. Identifies cross-shard relationships no isolated worker could see

**Cross-shard composition example (Security):**

```
 Worker Findings                    Reducer                         Output
┌───────────────────────┐      ┌─────────────────────┐      ┌───────────────────────┐
│ W1: ID leak      (P2) │ ──>  │                     │      │ CHAIN:                │
│ W3: ID-gated RCE (P2) │ ──>  │  Dedupe + Compose   │ ──>  │  Unauth RCE      (P0) │
├───────────────────────┤      │  Attack Chains      │      ├───────────────────────┤
│ W1: IDOR /orders (P2) │ ──>  │                     │      │ DEDUPED:              │
│ W2: IDOR /orders (P2) │ ──>  │                     │      │  IDOR /orders: 1x (-) │
└───────────────────────┘      └─────────────────────┘      └───────────────────────┘
                                                              (-) = not exploitable
```

- Worker A finds: Unauthenticated ID leak (P2)
- Worker B finds: ID-gated RCE (P2)
- Reducer chains: Unauthenticated RCE (P0)

The duplicate report is collapsed (e.g., two workers both reporting Insecure Direct Object Reference (IDOR) on `/api/orders` becomes one finding marked "not exploitable" if context shows it's benign).

### 3.5 Verify

The orchestrator fans out once more over serious findings. One sandboxed Devin session per finding reproduces it against a running build. Each finding is recorded as:
- **Confirmed** - Reproduced successfully
- **False Positive** - Could not reproduce, dismissed
- **Inconclusive** - Reproduction attempted but outcome unclear

```
 Serious Findings            Sandboxed Sessions              Classification
┌────────────────────┐      ┌────────────────────────┐      ┌──────────────────┐
│ Unauth RCE    (P0) │ ──>  │ Session 1: reproduce   │ ──>  │ ● Confirmed      │
│ SQLi in search(P1) │ ──>  │ Session 2: reproduce   │ ──>  │ ● Confirmed      │
│ SSRF in proxy (P1) │ ──>  │ Session 3: reproduce   │ ──>  │ ● Inconclusive   │
│ Open redirect (P2) │ ──>  │ Session 4: reproduce   │ ──>  │ ● False Positive │
└────────────────────┘      └────────────────────────┘      └──────────────────┘
                             one session per finding          Confirmed → fix PR
                             against running build
```

Confirmed findings can be handed back to Devin to fix, opening a remediation PR.

## 4. Security Swarm Implementation

[Devin Security Swarm](https://devin.ai/blog/security-swarm-eval) is powered by Agentic MapReduce. Security scanning is the first production application because the task shape maps exactly:
- Vulnerability report only trustworthy if entire codebase considered
- Real bugs are sparse relative to the code hiding them
- Most severe bugs chain exploits across multiple files

### 4.1 Security-Specific Pipeline

**Plan (Threat Model):**
A Devin session studies the repo and writes **rules** for this codebase: patterns for its routes, data layer, auth wrappers, and deserialization sinks. Surfaced as an editable **threat model**. On interactive scans, the user can adjust rules before the swarm fans out.

**Shard (Signals and Batches):**
Rules run deterministically over the entire repo. Every match emits a signal. Files matching nothing are dropped. Remaining files bucketed into bounded batches.

**Map (The Swarm):**
One child Devin session per batch, in parallel, each from a fresh focused context containing:
- Its batch's signals
- The rule provenance behind them

Each worker reads real code, clears a false-positive gate, and reports findings with severity, confidence, and preconditions, accounting for every file it was handed.

**Reduce (Triage and Chains):**
A reducer session:
- Processes workers' conclusions (not their transcripts)
- Deduplicates findings
- Attributes ownership
- Triages into **P0/P1/P2** severity
- Composes **attack chains** across shards with global view

**Verify (Runtime Proof):**
One sandboxed session per serious finding, reproducing against a running build. Classification: Confirmed, False Positive, or Inconclusive.

## 5. Evaluation Methodology

### 5.1 Dataset Construction

- **50 vulnerabilities** across **14 languages** (Go, Rust, Python, Ruby, Java, C#, JavaScript, C, Swift, Dart, Elixir, PHP, and others)
- Vulnerability classes: RCE, SQL injection, path traversal, Server-Side Request Forgery (SSRF), auth bypass, memory-safety bugs, denial-of-service, unsafe deserialization
- Repo sizes range from small (`smallbitvec`: 60 KB, 10 files) to large (`libcrux`: 92 MB, 1,754 files)

**Software categories covered:**

- **Crypto** - `jose-swift`, `ruby-jwt/jwe`, `libcrux`
- **Parsers and Codecs** - `yyjson`, `cowlib`, `wire`, `nokogiri`
- **Web Servers and Frameworks** - `bandit`, `plug`, `puma`, `wsgidav`
- **Template Engines** - `twig`, `liquidjs`, `scriban`
- **Infrastructure** - `kopia`, `dex`, `filebrowser`, `opentelemetry-operator`, `anchor`

### 5.2 Anti-Contamination Design

Every vulnerability was selected for **recency**: all advisories published after the training cutoffs of the models tested. The patch, CVE, and write-ups explaining the bug were never in training data.

Each case is pinned to the **exact commit before its fix landed** (the parent of the fix commit), so the bug is provably present.

Additional vetting:
- Verified agents did not look up CVEs during their investigations
- Confirmed "unpatched" commits actually contain the flaw
- Excluded cases where the bug lives in a vendor dependency rather than the project's own source

### 5.3 Grading Methodology

**Recall-based scoring:** A scanner gets credit only if it surfaces a finding identifying the **same underlying vulnerability** (same root cause, same code area). Unrelated extra findings count neither for nor against.

**Match criteria:** Finding must land on the same root cause in the same place, with Common Weakness Enumeration (CWE) and file path as hints. Exact wording or line numbers not required (two researchers can write up the same bug differently).

**Strict rule:** The specific target vulnerability must be found, not just any real bug in the right file. This keeps results comparable across runs and over time.

### 5.4 "Right Area, Different Defect" Pattern

The strict bar surfaces a recurring pattern: a run opens the exact file, finds a genuine vulnerability, but reports a **different** bug.

Example: `facil.io` - Target is an infinite loop in JSON parser triggered by bare `i`/`I` (Infinity) token. Runs found the right file and flagged real defects (depth-counter underflow, over-read in number parsing) but not the specific target. Both genuine flaws; neither the graded one.

This means **recall understates actual detection capability**. The recall numbers are a floor, not a ceiling.

## 6. Results

- **Devin Security** - Recall: 72% | Avg Cost/Scan: $90.23
- **Claude Security** - Recall: 68% | Avg Cost/Scan: $131.87
- **Codex Security** - Recall: 48% | Avg Cost/Scan: (no data)
- **Cursor Security** - Recall: 26% | Avg Cost/Scan: $4.60

**Key findings:**
- Security Swarm achieves highest recall AND lower cost than the next-best performer
- Does not sit on the usual cost-recall tradeoff curve (usually more findings = more compute)
- This is the result the Agentic MapReduce architecture was built to produce: cost tracks relevant code volume, not total repo size

**Cost efficiency mechanism:**
- No single agent searches the entire repo while carrying ever-growing unrelated discoveries
- Each worker reasons from a focused context for one bounded shard
- The Reducer compounds savings by reasoning over compressed conclusions rather than full transcripts
- Re-runs only process files changed since last scanned commit (incremental)

## 7. Applicability Beyond Security

The architecture fits any task where a verdict is only trustworthy if the whole codebase was in view. Explicitly mentioned applications:

- **Security Scanning** - First production use (Security Swarm)
- **Code-Quality Enforcement** - Functions exceeding complexity, deprecated API usage, unhandled error paths
- **Breaking-Change Detection** - Compare exported symbols/API schemas, select affected consumers, group under the API change that caused them, produce migration plan

The pattern generalizes to any task requiring:
1. Whole-codebase coverage guarantee
2. Sparse relevant signals in a large codebase
3. Cross-file relationship reasoning
4. Bounded per-unit reasoning cost

## 8. Next Steps

1. Monitor for additional Agentic MapReduce applications beyond security (code quality, breaking changes)
2. Track dataset evolution as CVEs fall inside training cutoffs (Cognition plans to retire and replace them)
3. Evaluate whether IPPS workflows could benefit from the Plan-Shard-Map-Reduce pattern for multi-file operations
4. Watch for public availability of the selector language/format for custom pipelines

## 9. Sources

**Primary Sources:**
- `AGNTMAPR-IN01-SC-DVNAI-AGMR`: https://devin.ai/blog/agentic-map-reduce - Agentic MapReduce architecture, pipeline stages, design rationale, Security Swarm overview [VERIFIED]
- `AGNTMAPR-IN01-SC-DVNAI-SWEV`: https://devin.ai/blog/security-swarm-eval - Evaluation methodology, dataset construction, grading, benchmark results [VERIFIED]
- `AGNTMAPR-IN01-SC-ARXIV-FCTX`: https://arxiv.org/abs/2606.14066 - Zhang et al., FastContext (2026). Agent trajectory analysis showing 56.2% tool-use turns spent on reading/searching [VERIFIED]

## 10. Document History

**[2026-07-21 00:31]**
- Added: Section 2.1 Design Rationale (failure mode → decision → guarantee mapping with diagram)
- Added: Section 2.2 Classic vs Agentic MapReduce structural comparison
- Added: Explanations for WHY Shard is deterministic, WHY Map uses independent workers, WHY Reduce is separate

**[2026-07-21 00:30]**
- Added: 4 Unicode box-drawing diagrams (pipeline flow, shard/map parallel execution, reduce composition, verify classification)

**[2026-07-21 00:30]**
- Initial research document created from two Devin blog posts (2026-07-01)
- Covered: Architecture, 5-stage pipeline, Security Swarm, evaluation methodology, results
