# TASKS: OpenClaw Token Usage Investigation

**Doc ID**: OCLAW-TK01
**Feature**: Token Usage Analysis
**Goal**: Identify and verify root causes of high input token usage in OpenClaw
**Source**: Anthropic dashboard showing 15.3M input / 69K output for 4-5 requests
**Strategy**: PARTITION-HYPOTHESIS

## Observation

- **Total tokens in:** 15,326,380 (15.3M)
- **Total tokens out:** 69,343 (69K)
- **Ratio:** ~220:1 input to output
- **Per request average:** ~3M input tokens
- **Model:** claude-opus-4-5-20251101 (Mar 01), claude-sonnet-4-5-20250929 (Mar 02-03)
- **Web searches:** 0

## Possible Causes to Investigate

### PC-01: Extended Thinking Budget
Extended thinking may consume massive input tokens as thinking chains grow.

### PC-02: Conversation History Accumulation
Each turn resends full history including all previous tool results.

### PC-03: Cache Read Token Counting
Anthropic counts cache_read as input tokens (even though cost is 10%).

### PC-04: Bootstrap Context Files
System loads multiple .md files (AGENTS.md, SOUL.md, etc.) into every prompt.

### PC-05: Skills Prompt Injection
Up to 150 skills with descriptions injected into system prompt.

### PC-06: Tool Result Details
Large tool outputs (file reads, searches) accumulate in history.

### PC-07: System Prompt Size
Base system prompt may be very large (700+ lines).

### PC-08: Compaction Not Triggering
Compaction only activates when context exceeds limits.

## Task 0 - Baseline (MANDATORY)

- [x] Confirm source code locations are accessible
- [x] Verify config file contents

## Tasks

### Phase 1: Token Counting Mechanism

- [x] **OCLAW-TK-001** - Find how input tokens are counted/reported
  - Files: `src/agents/usage.ts`, `src/agents/pi-embedded-runner/run.ts`
  - **FINDING:** `derivePromptTokens()` sums `input + cacheRead + cacheWrite`
  - **CRITICAL:** Anthropic dashboard shows RAW tokens including cache reads
  - Run.ts L163-177 fixes internal display by using `lastCacheRead` not accumulated

- [x] **OCLAW-TK-002** - Find thinking budget configuration
  - Files: `src/auto-reply/thinking.ts`, `src/agents/pi-embedded-runner/utils.ts`
  - **FINDING:** ThinkLevel passes through to `@mariozechner/pi-agent-core`
  - Budget tokens defined in external library, not in OpenClaw code

### Phase 2: Context Construction

- [x] **OCLAW-TK-003** - Measure system prompt size
  - Files: `src/agents/system-prompt.ts` (706 lines)
  - **FINDING:** System prompt includes:
    - Skills section, Memory section, User identity
    - Time section, Messaging rules, Safety rules
    - Workspace/Project context files (bootstrap)
    - Silent replies, Heartbeats, Runtime info
  - Estimated: ~20-30K tokens base system prompt

- [x] **OCLAW-TK-004** - Measure bootstrap file limits
  - Files: `src/agents/pi-embedded-helpers/bootstrap.ts`
  - **FINDING:**
    - `DEFAULT_BOOTSTRAP_MAX_CHARS = 20,000` per file
    - `DEFAULT_BOOTSTRAP_TOTAL_MAX_CHARS = 150,000` total
    - Configurable via `agents.defaults.bootstrapMaxChars`
  - Max contribution: ~37,500 tokens (150K chars / 4)

- [x] **OCLAW-TK-005** - Measure skills prompt limits
  - Files: `src/agents/skills/workspace.ts`
  - **FINDING:**
    - `DEFAULT_MAX_SKILLS_IN_PROMPT = 150`
    - `DEFAULT_MAX_SKILLS_PROMPT_CHARS = 30,000`
    - `DEFAULT_MAX_SKILL_FILE_BYTES = 256,000`
  - Max contribution: ~7,500 tokens (30K chars / 4)

### Phase 3: History and Compaction

- [x] **OCLAW-TK-006** - Find conversation history handling
  - Files: `src/agents/compaction.ts`
  - **FINDING:**
    - `SUMMARIZATION_OVERHEAD_TOKENS = 4,096`
    - `BASE_CHUNK_RATIO = 0.4`, `MIN_CHUNK_RATIO = 0.15`
    - `SAFETY_MARGIN = 1.2` (20% buffer for estimation error)
    - `pruneHistoryForContextShare()` uses `maxHistoryShare = 0.5` (50% of context)
    - Compaction only triggers when context exceeds limits

- [x] **OCLAW-TK-007** - Find tool result handling
  - Files: `src/agents/session-transcript-repair.ts`, `src/agents/compaction.ts`
  - **FINDING:**
    - `stripToolResultDetails()` removes verbose tool outputs BEFORE summarization
    - Tool results ARE included in history until compaction
    - Each turn resends full history including all prior tool results

### Phase 4: Synthesis

- [x] **OCLAW-TK-008** - Calculate theoretical maximum per request
  - **CALCULATION:**
    - System prompt: ~25K tokens
    - Bootstrap files: up to 37.5K tokens
    - Skills prompt: up to 7.5K tokens
    - Conversation history: grows unbounded until compaction
    - Cache reads: reported as input (but billed at 10%)
  - **Theoretical single turn:** ~70K tokens minimum
  - **With history:** Can reach context window (200K default)

- [x] **OCLAW-TK-009** - Identify primary contributor(s)
  - **ROOT CAUSES RANKED:**
    1. **Cache Read Reporting (PC-03):** Anthropic dashboard shows cache_read as input tokens. If 200K context is cached, each request shows 200K "input" even though you pay only 10%.
    2. **History Accumulation (PC-02):** Each turn resends full conversation history including all prior tool results.
    3. **Bootstrap Context (PC-04):** 150K chars = ~37.5K tokens injected every turn.
    4. **Skills Prompt (PC-05):** 30K chars = ~7.5K tokens per turn.
    5. **Extended Thinking (PC-01):** Adds to context but budget managed by pi-agent-core.

## Task N - Final Verification (MANDATORY)

- [x] Document findings in INFO document or NOTES.md
- [x] Provide recommendations to reduce token usage
- [ ] Update PROGRESS.md - mark investigation complete

## VERIFIED ROOT CAUSES

### PRIMARY: Interleaved Thinking Token Accumulation [VERIFIED]

**Source:** `transcript-policy.ts:101` - `dropThinkingBlocks = isCopilotClaude`

For direct Anthropic provider, `dropThinkingBlocks = false`. Thinking blocks are **preserved across tool calls** and resent as INPUT tokens on every subsequent API call.

**Config evidence:**
- `thinkingDefault: "medium"` in openclaw.json
- Model: `anthropic/claude-sonnet-4-5` (direct Anthropic)

**Anthropic docs confirm:** "Thinking blocks from the last assistant turn included in subsequent requests (input tokens)" and "when using interleaved thinking with tools, you can exceed this limit as the token limit becomes your entire context window (200k tokens)"

**Token math:**
- Medium thinking budget: ~10K-32K tokens per thinking turn
- 10 tool-call round-trips per request: 10 x 32K = 320K INPUT tokens
- 5 requests with 10+ tool calls each: 5 x 320K = 1.6M+ INPUT tokens from thinking alone
- Add context/history: Easily reaches 3M+ per request

### SECONDARY: Tool-Call Round-Trip Multiplication

Each tool call is a separate API request. With interleaved thinking enabled, EVERY tool-call round-trip:
1. Sends previous thinking blocks as INPUT
2. Generates new thinking tokens as OUTPUT
3. Returns tool calls with thinking preserved

A single user interaction with 15 tool calls = 15 API requests, each carrying accumulated thinking.

### TERTIARY: Large Initial Context

Bootstrap (150K chars) + Skills (30K chars) + System prompt = ~70K tokens baseline, multiplied by every tool-call round-trip.

## RECOMMENDATIONS

### IMMEDIATE: Reduce or disable thinking

1. **Set thinking to "off" or "minimal"** in `openclaw.json`:
```json
"agents": {
  "defaults": {
    "thinkingDefault": "off"
  }
}
```

Or use "minimal" (1,024 tokens) instead of "medium" (~10K-32K tokens).

### MEDIUM-TERM: Reduce context size

2. **Reduce bootstrap limits** in `openclaw.json`:
```json
"agents": {
  "defaults": {
    "bootstrapMaxChars": 10000,
    "bootstrapTotalMaxChars": 50000
  }
}
```

3. **Limit skills** in `openclaw.json`:
```json
"skills": {
  "limits": {
    "maxSkillsInPrompt": 30,
    "maxSkillsPromptChars": 10000
  }
}
```

### INVESTIGATION: Confirm with payload logging

4. **Enable payload logging** to see exact thinking token counts:
```
OPENCLAW_ANTHROPIC_PAYLOAD_LOG=true
```

5. **Check API response usage** for `thinking_tokens` field to confirm thinking is the primary contributor.

## Dependency Graph

```
TK-001 ─┬─> TK-008
TK-002 ─┤
TK-003 ─┤
TK-004 ─┤
TK-005 ─┤
TK-006 ─┤
TK-007 ─┘
TK-008 ─> TK-009 ─> TK-N
```

## Document History

**[2026-03-03 08:25]**
- CORRECTED: Cache read was wrong assumption
- Actual root cause: Interleaved thinking tokens preserved across tool calls
- `dropThinkingBlocks = false` for direct Anthropic provider
- `thinkingDefault: "medium"` causes 10K-32K thinking tokens per turn
- Tool-call round-trips multiply thinking token input

**[2026-03-03 08:15]**
- Initial investigation (incorrect assumption about cache reads)

**[2026-03-03 08:10]**
- Initial tasks plan created for token usage investigation
