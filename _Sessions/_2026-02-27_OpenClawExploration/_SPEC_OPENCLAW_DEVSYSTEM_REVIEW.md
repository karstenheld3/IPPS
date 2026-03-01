# Devil's Advocate Review: OCLAW-SP01

**Reviewed**: 2026-03-01 17:20
**Target**: `_SPEC_OPENCLAW_DEVSYSTEM.md [OCLAW-SP01]`
**Context**: Specification for integrating IPPS DevSystem into OpenClaw workspaces

## Industry Research Findings

### 1. OpenClaw Workspace Injection [VERIFIED]

**Finding**: OpenClaw injects ONLY these specific files into system prompt:
- AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md, MEMORY.md

**Critical**: WORKFLOWS.md will NOT be auto-injected. Agent must explicitly read it.

**Source**: https://docs.openclaw.ai/concepts/system-prompt

### 2. Token Budget Concerns [VERIFIED]

**Finding**: GitHub issue #9157 reports "Workspace file injection wastes 93.5% of token budget"

**Risk**: Embedding full DevSystem rules in AGENTS.md could cause token bloat.

**Source**: https://github.com/openclaw/openclaw/issues/9157

### 3. Skills Folder Behavior [VERIFIED]

**Finding**: Workspace skills override managed/bundled skills when names collide.

**Implication**: Syncing skills/ from IPPS will work, but may override OpenClaw's bundled skills.

**Source**: https://docs.openclaw.ai/concepts/agent-workspace

### 4. Bootstrap File Limits

**Finding**: `agents.defaults.bootstrapMaxChars` and `agents.defaults.bootstrapTotalMaxChars` control injection limits.

**Risk**: Large AGENTS.md may be truncated if it exceeds limits.

### 5. Sub-Agent Prompt Mode

**Finding**: Sub-agents use `promptMode=minimal` which omits Skills, Memory Recall, Heartbeats.

**Risk**: Sub-agents spawned for session work may not have full DevSystem context.

## Critical Issues

### OCLAW-RV-001: WORKFLOWS.md Not Auto-Injected

**Severity**: [HIGH]
**Location**: OCLAW-FR-02, Section 7 (Key Mechanisms)

**Problem**: Spec assumes agent will read WORKFLOWS.md, but OpenClaw only auto-injects specific bootstrap files. WORKFLOWS.md is NOT in the injection list.

**Evidence**: OpenClaw docs list exactly 8 files for injection: AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md, MEMORY.md

**Impact**: Agent will not automatically know workflows exist. Must be told in AGENTS.md to read WORKFLOWS.md.

**Recommendation**: 
1. Add explicit instruction in AGENTS.md: "Read WORKFLOWS.md for available workflows"
2. Consider: Is WORKFLOWS.md even needed? Could workflows be embedded in AGENTS.md?

### OCLAW-RV-002: Token Budget Risk from Large AGENTS.md

**Severity**: [HIGH]
**Location**: OCLAW-DD-01, OCLAW-IG-01

**Problem**: Embedding "complete DevSystem rules" in AGENTS.md could exceed token limits. DevSystem rules (devsystem-core.md + devsystem-ids.md) are ~500+ lines.

**Evidence**: GitHub issue #9157 reports 93.5% token waste from workspace injection.

**Impact**: 
- AGENTS.md may be truncated
- Less context available for actual conversation
- Performance degradation

**Recommendation**:
1. Measure current AGENTS.md size (7.8 KB = ~2000 tokens)
2. Measure DevSystem rules size
3. Consider: Reference skills instead of embedding rules (e.g., "@write-documents" instead of full rules)
4. Set `bootstrapMaxChars` appropriately in openclaw.json

### OCLAW-RV-003: Sub-Agent Context Loss

**Severity**: [MEDIUM]
**Location**: OCLAW-FR-07 (Sub-Agent Session Spawning)

**Problem**: Sub-agents use `promptMode=minimal` which omits Skills, Memory Recall, Heartbeats. Sub-agents won't have full DevSystem context.

**Evidence**: OpenClaw docs: "minimal: omits Skills, Memory Recall..."

**Impact**: Sub-agents spawned for independent session work may not follow DevSystem conventions.

**Recommendation**:
1. Document this limitation in spec
2. Consider: Should session work be main-agent only?
3. Alternative: Pass critical rules via session NOTES.md

## High Priority Issues

### OCLAW-RV-004: Skills Folder Override Risk

**Severity**: [MEDIUM]
**Location**: OCLAW-FR-03, OCLAW-DD-03

**Problem**: Spec says sync entire skills/ folder from IPPS. This will override any OpenClaw bundled skills with same names.

**Evidence**: OpenClaw docs: "Workspace-specific skills. Overrides managed/bundled skills when names collide."

**Impact**: May break OpenClaw's built-in functionality if skill names collide.

**Recommendation**:
1. Audit IPPS skills/ for name collisions with OpenClaw bundled skills
2. Consider: Prefix IPPS skills with namespace (e.g., `ipps-write-documents/`)
3. Or: Only sync specific skills, not entire folder

### OCLAW-RV-005: Missing Fallback for WORKFLOWS.md

**Severity**: [MEDIUM]
**Location**: Section 7 (Workflow Lookup Pattern)

**Problem**: If WORKFLOWS.md doesn't exist or is empty, agent has no workflows. No fallback defined.

**Impact**: Agent will be stuck without workflow guidance.

**Recommendation**:
1. Define fallback behavior in AGENTS.md
2. Alternative: Embed minimal workflow list in AGENTS.md, use WORKFLOWS.md for extended definitions

### OCLAW-RV-006: Git Sync Direction Not Enforced

**Severity**: [MEDIUM]
**Location**: Section 9 (Deployment)

**Problem**: Spec says IPPS deploys TO OpenClaw, but git sync (Section 7.4 "Session Handover") implies bidirectional sync between laptop and VM.

**Ambiguity**: Which direction does git flow?
- IPPS -> OpenClaw workspace (deploy-to-all-repos)
- Laptop OpenClaw <-> VM OpenClaw (session handover)

**Impact**: Potential merge conflicts if both directions modify same files.

**Recommendation**:
1. Clarify: skills/ only flows IPPS -> OpenClaw (never reverse)
2. Clarify: _Sessions/ can flow both directions (git merge)
3. Document conflict resolution strategy

## Medium Priority Issues

### OCLAW-RV-007: deploy-to-all-repos.md Requires Modification

**Severity**: [LOW]
**Location**: Section 9.2

**Problem**: Spec shows PowerShell snippet for OpenClaw handling, but deploy-to-all-repos.md would need structural changes to support per-repo special rules.

**Impact**: Current deploy-to-all-repos.md may not support "never overwrite" semantics without modification.

**Recommendation**: Create separate implementation step for deploy-to-all-repos.md changes.

### OCLAW-RV-008: _Sessions Folder Naming Conflict

**Severity**: [LOW]
**Location**: OCLAW-FR-04

**Problem**: DevSystem uses `_Sessions/` but OpenClaw may have conventions for other underscore-prefixed folders.

**Impact**: Minor - unlikely to cause issues.

**Recommendation**: Verify OpenClaw doesn't use `_Sessions/` for anything else.

## Questions That Need Answers

1. **What are OpenClaw's bundled skill names?** - Need to check for collisions before syncing.

2. **What is `bootstrapMaxChars` default?** - Need to ensure AGENTS.md fits within limits.

3. **Can WORKFLOWS.md be added to injection list?** - Or is agent-side read the only option?

4. **How does OpenClaw handle agent.defaults.workspace git status?** - Does it auto-commit?

5. **What happens if sub-agent modifies session files while main agent is active?** - Concurrency risk?

## Recommendations Summary

| Issue | Severity | Action |
|-------|----------|--------|
| WORKFLOWS.md not auto-injected | HIGH | Add read instruction to AGENTS.md |
| Token budget risk | HIGH | Measure sizes, consider skill refs over embedding |
| Sub-agent context loss | MEDIUM | Document limitation, use NOTES.md for rules |
| Skills override risk | MEDIUM | Audit for name collisions |
| Missing workflow fallback | MEDIUM | Add fallback to AGENTS.md |
| Git sync direction | MEDIUM | Clarify in spec |

## Document History

**[2026-03-01 17:20]**
- Initial Devil's Advocate review
- Identified 8 issues (2 critical, 4 high/medium, 2 low)
- Research findings from OpenClaw docs

