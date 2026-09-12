# INFO: IPPS Gap Analysis - Article Summaries (P3-S1)

**Doc ID**: IPPSGAP-IN03
**Goal**: Summaries of 11 LLM best practices articles read for deep mapping in P3-S1
**Source**: `e:\Dev\Delphios\knowledge\AI-Stuff\LLMBestPractices_2026-09-12`

**Depends on:**
- `__STRUT_IPPSGAP.md` step P3-S1
- `_INFO_PREFLIGHT_ANALYSIS.md [IPPSGAP-IN01]` for prior mapping context

## Summary

11 articles read in full from the LLM best practices knowledge base: 5 from ai-agents, 2 from prompt-engineering, 4 from knowledge-vaults. The `writing/glossary.md` file does not exist in the knowledge base. Each article summary below captures key claims, concrete recommendations, and IPPS-relevant patterns for the mapping step (P3-S2).

## Article Summaries

### ai-agents/structured-output.md

- Structured output constrains model output to a schema (JSON, XML, YAML) at generation time via native API support (OpenAI `response_format`, Anthropic tool-use schemas, Gemini `responseSchema`)
- Use structured output for any model call whose response feeds downstream code: classifications, extractions, function-call arguments, form fills, multi-field summaries. Skip for free-form generation
- Replaces fragile regex extraction from free-form text with a typed contract - response is guaranteed to parse
- IPPS relevance: TRACTFUL defines document types but has no machine-validation. GRUC CHECKS are manual, not automated schema validation. This article supports GAP-06 (output schema validation)

### ai-agents/system-prompts.md

- System prompt persists across every turn; user message is per-turn ask. Test: "would you write this rule every turn?" If yes, it belongs in system
- Standard skeleton: 1) Identity, 2) Capabilities, 3) Constraints, 4) Format - in that order. Model attends to first lines and last
- Hard cap: 200-800 tokens for most agents. If prompt grows, factor out examples to few-shot block, schema to tool definition, long instructions to referenced runbook
- Treat system prompt as code: commit to repo, review changes in PRs, tag versions, run eval set against every diff
- System prompt is recoverable - assume it will leak. No API keys, passwords, PII in system prompt. Credentials belong behind tool calls
- IPPS relevance: IPPS rules (agent-behavior.md, core-conventions.md) function as system prompts. The 4-block skeleton maps to IPPS rules structure. Version control of rules is already done via git. The "assume leak" principle is not addressed in IPPS (relates to GAP-01)

### ai-agents/role-framing.md

- Role framing narrows output distribution toward domain expert answers. Three-sentence opener: role, domain, audience
- "Expert/senior/principal" primes calibrated answers; persona primes ("pirate", "sassy") degrade accuracy. Do not mix correctness primes with tone primes
- Calibration rule: "When you do not know an answer, say so. Mark uncertain claims. Do not invent function names, file paths, or version numbers."
- Anti-sycophancy is a hard rule: "Do not flatter the user. Do not say 'great question.' If the user is wrong, say so plainly." Restate at end of system prompt (recency bias)
- Role fades in multi-turn loops - periodically inject role refresher
- IPPS relevance: IPPS agent-behavior.md already contains anti-sycophancy rules ("No acknowledgment phrases"). Calibration rule maps to SOCAS [VERIFIED]/[UNVERIFIED] labels. Role refresh maps to EDIRD phase context loading

### ai-agents/rag.md

- Most RAG failures are retrieval failures, not generation failures. Chunk on headings/paragraphs first, then enforce 200-800 token budget with 50-token overlap
- Hybrid retrieval: vector similarity + metadata filters + BM25 for rare keywords. Merge with reciprocal rank fusion
- Cross-encoder reranker in series: retrieve top 50 by vector, rerank with cross-encoder, keep top 5
- Golden set evaluation: recall@k (retrieval) and answer correctness (generation) tracked separately
- Inline citations required: pass chunk IDs into prompt, require model to cite them. Stale chunks filtered by `last_updated` metadata
- IPPS relevance: IPPS has no RAG equivalent. /prime workflow loads context but without retrieval, chunking, or citation discipline. This is a gap - IPPS agents load files directly but have no retrieval-quality framework

### ai-agents/mcp-servers.md

- MCP server exposes tools, resources, and prompts for durable integrations. Break-even point: roughly third reuse
- Group related tools under one server (one domain = one auth boundary). Tool names: verbs not nouns. Types: narrow with enums. Descriptions: what it does, what it returns, one example
- Tools are actions; resources are addressable data (URI-referenced, cached by client)
- Security: OAuth/token/mTLS at transport, strip secrets from outputs, per-tool rate limits, explicit allowlists per tool
- Every call gets a log line: tool, args, result_summary, duration_ms, error. Logs feed debugging, eval datasets, audit trails
- IPPS relevance: IPPS has MCP servers configured (playwright, playwriter) but no guidelines for when to create vs reuse, tool naming, or logging. The logging pattern supports IMP-10 (observability)

### prompt-engineering/reasoning-model-prompting.md

- Reasoning models run internal chain of thought before answering. Do not add "think step by step" - it duplicates into visible output and crowds out the answer
- Few-shot examples that walk through steps add noise to reasoning models. Show only input and final answer, skip intermediate reasoning
- Reasoning models do better with 1 example or none and sharper instruction. Replace example density with instruction precision
- Token budget: reasoning consumes `max_tokens` before visible output. Current Claude models use adaptive thinking via `effort` parameter, not fixed `budget_tokens`. Set `max_tokens` generously (64k+ at high effort)
- Use reasoning models for multi-step verifiable tasks; stay with chat models for single-step extraction/classification
- IPPS relevance: IPPS STRUT plan model hints ("Opus for analysis") align with reasoning model selection guidance. The "strip scaffolding" principle maps to APAPALAN (As Little As Necessary). The effort parameter guidance is relevant to /switch-model workflow

### prompt-engineering/prompt-caching-strategies.md

- Prompt caching cuts latency 50-80% and cost ~90% on cached portion. Cache key is the prefix - stable content first, mutable content last
- Standard layout: 1) System message/policy, 2) Few-shot examples, 3) Tool definitions, 4) Retrieved context, 5) Conversation history, 6) Current user query
- Timestamps/session IDs at top of prompt destroy cache. Move mutable content to bottom. Sort RAG chunks by stable key, not relevance score
- Caches scoped per model version. Pin model version, not floating alias. Model upgrade resets hit rate to zero
- Cache hit rate is first-class production metric. Track per endpoint, per prompt version, per model. Alert on sustained drop
- IPPS relevance: IPPS has no cache-awareness guidance (GAP-04). IPPS rules are loaded as stable system context (good for caching) but no explicit guidance on ordering. The model version pinning advice is relevant to /switch-model workflow

### knowledge-vaults/vault-frontmatter-schema.md

- Frontmatter is the spine of a vault: type, status, provenance, dates. Never optional, never partially filled
- Required fields are per type, declared in spec, enforced by auditor. Load-bearing fields (confidence, sources, alternatives_considered) are the ones hurried authors skip
- Absent key vs empty list mean different things to query engine. `counter_evidence: []` says "checked, none found"; missing `counter_evidence` says nothing
- Rigor frameworks add fields to base type, not parallel schema. Field groups that gate each other travel together
- Adding a field is cheap; making it required is a migration. Never backfill fabricated defaults
- IPPS relevance: IPPS document header blocks (Doc ID, Goal, Depends on) serve similar purpose to frontmatter but are markdown, not YAML. The per-type required fields pattern maps to TRACTFUL document type requirements. The "never backfill fabricated defaults" principle aligns with SOCAS anti-hallucination

### knowledge-vaults/linking-and-tags.md

- Vault value is in edges, not nodes. Relationships are always wikilinks; tags carry state, not meaning
- Free-floating descriptive tags banned. Tags: exactly one status tag per note, multiple nested domain tags allowed
- Naked link dumps (trailing list of bare links) are the most common way a vault looks connected while carrying no reasoning. Every link needs a sentence around it
- Block references for passage-level citations: `[[@source#^p-23]]` for page 23
- Orphans (no inbound/outbound links) are hygiene gate: link it or delete it. Clusters of orphans mean missing MOC, not missing links
- IPPS relevance: IPPS cross-references (Doc ID references like `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]`) serve the same purpose as wikilinks. IPPS has no orphan detection. The "every link needs context" principle maps to APAPALAN precision requirement

### knowledge-vaults/team-vaults.md

- Shared vaults need coordination without corruption. Git provides merge model, immutable history, and review gates that file replicators cannot
- Atomicity is concurrency discipline: two people editing two atoms never conflict; one 2000-word note three people touch is a merge hotspot
- Append-only convention: one bullet per line, newest at bottom, never reflow existing lines. Frontmatter keeps fixed field order for clean diffs
- Filenames are primary keys. Naming ledger prevents duplicate concepts. One maintainer owns taxonomy
- Renames are scope-freeze operations: state path list, get sign-off, commit rename and link updates together
- IPPS relevance: IPPS uses git for version control (aligned). ID-REGISTRY.md serves as naming ledger for topics (aligned). The append-only convention maps to IPPS Document History sections. The single-maintainer taxonomy model differs from IPPS collaborative model

### knowledge-vaults/vault-evolution.md

- Vaults outgrow designs. Governing rule: add, deprecate, migrate, never rebuild. Four moves cover every legitimate case
- Add new type: declare in spec, add template/schema, create folder, run auditor. No existing notes change - reversible by deleting spec block
- Making optional field required is the one move that touches existing notes. Run as migration: generate worklist, scope-freeze backfill, never fabricate values, re-run to prove zero
- Layer second framework rather than fork. Framework-specific rules trigger on prefixes. Never rebuild - severs backlinks, resets history, erases audit memory
- Deprecation: move notes to archive first, then remove type from spec. Record why in one line
- IPPS relevance: IPPS has no formal evolution protocol. The "never rebuild" principle is relevant to IPPS version migrations (V1 to V2 to V3 to V4 in _OldVersions/). The add/deprecate/migrate pattern could formalize IPPS spec changes. The "layer rather than fork" principle applies to PromptSystem sync model

## Document History

**[2026-09-12 17:35]**
- Initial article summaries created for P3-S1
- 11 articles read and summarized (glossary.md does not exist)
- Categories covered: ai-agents (5), prompt-engineering (2), knowledge-vaults (4)
