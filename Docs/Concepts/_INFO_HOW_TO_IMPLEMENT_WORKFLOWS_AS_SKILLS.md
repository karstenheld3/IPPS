# INFO: Bundling Workflows with Skills

**Doc ID**: SKLWRKFL-IN01
**Goal**: Research how to migrate 44 Cascade workflows into a skill-based architecture without folder bloat, given that workflows are deprecated in Devin Local

## Summary

**Problem:** IPPS has 44 workflows and 20 skills. Devin Local does not support workflows - only skills. Naively migrating each workflow to its own skill = folder bloat + context bloat + detection ceiling exceeded.

**The core tension:** Workflows had near-zero context cost (filename listed as available command). Skills load name+description into agent context for every skill, even those never invoked. With 44+ skills, the detection ceiling (32-36) is exceeded and agent selection accuracy degrades.

**Breakthrough finding: `disable-model-invocation: true` eliminates context cost** [VERIFIED - Anthropic official docs]

Claude Code provides a frontmatter field that makes skills behave identically to workflows:

| Frontmatter | User can invoke | Agent can invoke | Description in context |
|---|---|---|---|
| (default) | Yes | Yes | Yes - always loaded |
| `disable-model-invocation: true` | Yes | No | **No - removed from context** |
| `user-invocable: false` | No | Yes | Yes - always loaded |

With `disable-model-invocation: true`:
- Skill appears in `/` autocomplete menu (type safety, discoverability)
- Description is NOT loaded into agent context (zero context cost)
- Full SKILL.md body loads ONLY when user types `/name` (progressive disclosure)
- Agent cannot auto-trigger it (workflow-equivalent behavior)
- Detection ceiling becomes irrelevant (agent never auto-selects these skills)

Source: https://code.claude.com/docs/en/skills#control-who-invokes-a-skill

**Devin CLI equivalent:** `triggers: ["user"]` prevents auto-invocation but descriptions may still be loaded. Not as strong as Claude Code's `disable-model-invocation`. [ASSUMED - Devin docs less explicit]

**Cascade:** Workflows already provide this behavior natively. Keep workflows.

**Recommended approach: Option F (User-Only Skills + Domain Knowledge Skills)**

All 44 procedure skills use `disable-model-invocation: true` / `triggers: ["user"]`:
- Zero context cost on Claude Code
- Minimal context cost on Devin CLI (~1300 tokens for descriptions) [ASSUMED]
- Full autocomplete and type safety on all platforms
- Detection ceiling irrelevant (only ~8-12 domain skills are model-triggered)

Combined with ~8-12 domain skills (model-triggered) for auto-discovery:
- `write-documents`, `session-management`, `deep-research`, `coding-conventions` etc.
- These provide routing when user doesn't know the exact command name
- Stays well under 32-skill detection ceiling for model-triggered skills

**Key findings:**

- **Claude Code**: `disable-model-invocation: true` removes skill from agent context entirely. User still gets `/` autocomplete. This is the workflow equivalent.
- **Devin CLI/Desktop**: `triggers: ["user"]` prevents auto-activation. Plugins bundle skills under namespaces (`/plugin:skill`). `devin migrate workflows` converts Cascade workflows to skills.
- **Detection ceiling at 32-36 skills**: Only applies to model-triggered skills. User-only skills bypass this. [VERIFIED - multiple sources]
- **Plugins**: Devin CLI and Claude Code both support plugin-based skill bundling with namespaces, reducing organizational bloat.
- **IPPS existing pattern**: `write-documents` (30 files, 12 verbs) and `session-management` (7 files, 5 ops) already work as domain routers.

**Alternatives considered (previous iterations):**

- **Option A (Router Only)**: Poor discoverability, no per-command autocomplete
- **Option B (Flat Many-Skills)**: Exceeds detection ceiling, massive duplication
- **Option C (Thin Wrapper + Shared Library)**: Exceeds ceiling with 55-60 folders
- **Option D (Argument Routing)**: Fragile parsing, no per-command description
- **Option E (Domain Router + Selective Wrappers)**: Good but unnecessarily complex now that Option F exists

## Community Voices and Evidence

**Detection ceiling and accuracy degradation:**
- Production benchmarks report **32-36 skills** as the ceiling before inconsistent selection [VERIFIED - enuno/claude-command-and-control]
- Optimal performance at **2-3 skills per task**, diminishing returns at 4+ [VERIFIED - same source]
- MCP tool research: accuracy falls from >90% to single digits as tool count grows. **25-50 tools** is the degradation zone. Learned retrieval showing 3-7 relevant tools matches accuracy of showing 50 [VERIFIED - Wasowski, Level Up Coding]
- "Give an assistant 150 tools at once, and it starts reaching for the wrong ones, like a person lost in an overly long menu" [VERIFIED - same source]

**Skill sprawl is a recognized problem:**
- **the-agency** (GitHub): 59 SKILL.md files, explicitly flags "skill sprawl". Recommends consolidating redundant skills (e.g., 7 `sandbox-*` skills into one with subcommands). Audit classified skills as: compliant, minor drift, major rework, retire. [VERIFIED - issue #289]
- **skill-fuse** (gaia-research): Tool that merges overlapping skills into one. "Agent skill merge is a real problem. You install shape, audit, and refactor as three separate commands - now every task juggles three /commands, three prompt budgets, three chances for the agent to pick the wrong one." SKILL.md acts as router, delegates to reference/ files. [VERIFIED - GitHub]
- **Shrivu Shankar** (blog.sshh.io): "Build skills for the class of task, not the instance. Some are specs (how to do a thing); others are principles (how to think about a class of things)." Warns against "one skill per task, ending up with a directory of one-shots nobody else can use."

**Community patterns for organizing skills:**
- **"Route, do not restate"** (Philip Hern, DEV Community): 5-layer architecture. AGENTS.md as thin router. Skills as on-demand runbooks. Reference files for catalogs. "Tell the agent explicitly when not to load the heavy stuff." Reduced token spend on routine edits.
- **CheesecakeLabs**: Real-world measurement: **69% reduction in startup tokens** (7,121 to 2,213) by moving task-specific content from rules into skills. "A project can have dozens of skills installed. The agent only pays the token cost for the ones it uses."
- **localskills.sh**: "Skills are cheap at rest - the ceiling is discoverability, not tokens. The real failure mode is vague descriptions that never match tasks. Write descriptions that name the trigger."
- **Cursor**: Recursive subfolder discovery. `.cursor/skills/shipping/deploy-staging/SKILL.md` - "Cursor walks the skills root recursively, so category folders work for grouping related skills. The skill's name comes from the folder that contains SKILL.md, not the category above it."
- **Claude Code mastery**: Trigger tables in CLAUDE.md that map task types to skills. Skill gates for security.
- **Anthropic best practices** (nyosegawa/skills): "SKILL.md as routing and workflow layer. Put schemas, API docs, examples, rubrics, long style guides, and domain notes in separate files." Orchestration skills "should be architected like small software systems, not long prompts."

**Migration guides:**
- **Claude Code power user tips**: "If you do something more than once a day, turn it into a skill." Skills replace legacy `.claude/commands/`.
- **Developers Digest** (Windsurf-to-Claude migration): "Windsurf Flows let you save and replay prompt sequences. Claude Code has Skills - markdown files with structured frontmatter that become slash commands."
- **claudecodeguides.com**: "Too many commands clutter the menu: organize with prefixes (review-, gen-, check-) or consolidate related commands into one command with argument-based branching."

**Enterprise anti-patterns:**
- **CEAD paper** (arxiv): "Micro-agent proliferation" mirrors micro-skill proliferation. "Start with business capabilities and risk boundaries, not with a target number of agents. Decompose only where there is a durable reason." A 32-agent swarm with no strong capability map performed worst.
- **Wasowski**: Dynamic tool assembly - "loading schemas on demand rather than upfront - show the agent a menu, not the whole kitchen" cuts payload by ~85% while improving accuracy.

## Platform Capabilities Comparison

**Devin Desktop (Cascade - legacy):**
- Workflows: `.devin/workflows/*.md`, invoked via `/name`. Cascade-only.
- Skills: `.devin/skills/<name>/SKILL.md`, progressive disclosure (name+description in prompt, body loaded on invoke).
- Both coexist: workflows for user-triggered procedures, skills for agent-discoverable capabilities.

**Devin Desktop (Devin Local):**
- Workflows: NOT supported.
- Skills: ONLY supported mechanism for reusable procedures. Same format as Devin CLI.
- Frontmatter: `name`, `description`, `argument-hint`, `model`, `subagent`, `agent`, `allowed-tools`, `permissions`, `triggers`.
- Subagent orchestration: One skill can invoke other skills as subagents. One level deep (no nesting).
- Source: https://docs.devin.ai/cli/extensibility/skills/creating-skills

**Claude Code:**
- Commands (`.claude/commands/*.md`) and skills (`.claude/skills/<name>/SKILL.md`) are merged - same feature.
- Subfolder organization: `.claude/commands/ci/build.md` creates `/build` (subfolder shown in help but NOT in command name).
- Plugin namespacing: `plugin-name:skill-name` colon syntax.
- Nested skills in monorepo subdirectories: supported, qualified as `subdir:skill-name`.
- Source: https://code.claude.com/docs/en/skills

**Agent Skills Standard (agentskills.io):**
- Open specification by Anthropic, adopted by Devin, Claude Code, Microsoft Agent Framework, Cursor, Codex.
- 1 skill = 1 directory with SKILL.md + optional scripts/, references/, assets/.
- Progressive disclosure: advertise (~100 tokens) -> load (<5000 tokens) -> read resources -> run scripts.
- No built-in subcommand or grouping concept.
- Source: https://agentskills.io/specification

## Current IPPS State

**20 skills** (file counts):
- Heavy: `write-documents` (30), `deep-research` (23), `travel-info` (14), `coding-conventions` (13), `llm-transcription` (12)
- Medium: `llm-computer-use` (9), `ms-playwright-mcp` (8), `pdf-tools` (8), `windsurf-auto-model-switcher` (8), `session-management` (7), `youtube-downloader` (7)
- Light: `drift-correction` (5), `google-account` (3), `playwriter-mcp` (3), `git` (2), `github` (2), `windows-desktop-control` (2), `edird-phase-planning` (1), `git-conventions` (1)
- Data-heavy: `llm-evaluation` (154, mostly model-sources JSON)

**44 workflows** (line counts range 13-495, median ~88 lines)

**Existing router patterns in IPPS:**
- `write-documents` SKILL.md lists 12 verbs with "Read template X, guide Y, rules Z" instructions per verb. Workflows like `/write-spec` currently invoke this skill via `@skills:write-documents`.
- `session-management` SKILL.md covers 5 lifecycle operations (init, work, save, resume, finalize).

## Approach Analysis

### Option A: Router Skill Pattern (Fewer Folders, Less Discoverable)

**Structure:**
```
.devin/skills/
  write-documents/   # 1 folder, 12 "subcommands"
    SKILL.md          # Routes based on user request
    INFO_TEMPLATE.md
    SPEC_TEMPLATE.md
    ...30 files
  session-mgmt/      # 1 folder, 5 "subcommands"
    SKILL.md
    ...
```

**Invocation:** `/write-documents` then user specifies "write a spec for X"

**Pros:**
- Minimal folders (~10-12 total)
- Knowledge collocated with router
- Already working in IPPS V4.2

**Cons:**
- No per-command autocomplete (user must know subcommands exist)
- Single skill description must cover all subcommands
- Agent auto-invocation less precise (broad description matches too many tasks)
- SKILL.md grows large as more subcommands added

**Token cost:** ~1000-1200 tokens for catalog (10-12 skills x ~100 tokens)

### Option B: Flat Many-Skills (Maximum Discoverability, Maximum Bloat)

**Structure:**
```
.devin/skills/
  write-spec/         # Each workflow = own skill folder
    SKILL.md
    SPEC_TEMPLATE.md   # Duplicated from write-documents
    SPEC_RULES.md      # Duplicated
  write-info/
    SKILL.md
    INFO_TEMPLATE.md   # Duplicated
    INFO_GUIDE.md      # Duplicated
    INFO_RULES.md      # Duplicated
  session-new/
    SKILL.md
    SESSION_TEMPLATE.md  # Duplicated from session-management
  ...44+ folders
```

**Invocation:** `/write-spec`, `/session-new`, `/commit`

**Pros:**
- Every command has its own `/slash-command` with autocomplete
- Agent can auto-invoke the precise skill for the task
- Each skill description is focused and specific

**Cons:**
- 44+ folders = significant directory bloat
- Shared knowledge duplicated across folders (templates, rules, guides)
- Maintenance nightmare: update APAPALAN_RULES.md in 12 places
- ~4400+ tokens for catalog

**Token cost:** ~4400 tokens (44 x ~100)

### Option C: Thin Wrapper + Shared Library (Exceeds Ceiling)

**Structure:**
```
.devin/skills/
  # === Domain skills (heavy, contain all knowledge) ===
  write-documents/           # 30 files: templates, guides, rules
    SKILL.md                 # Full router with verb mapping
    ...
  # === Command skills (thin, reference domain skills) ===
  write-spec/
    SKILL.md                 # ~10 lines: references write-documents resources
  write-info/
    SKILL.md                 # ~10 lines
  session-new/
    SKILL.md                 # ~10 lines
  ...
```

**Invocation:** `/write-spec`, `/session-new`, `/commit` (each has autocomplete)

**Pros:**
- Every command gets `/slash-command` autocomplete
- Knowledge lives in ONE place (domain skill), referenced by many
- Compatible with all platforms

**Cons:**
- **~55-60 folders exceeds 32-skill detection ceiling**
- Agent selection accuracy degrades with this many skills
- Cross-skill file references depend on agent correctly resolving relative paths

**Token cost:** ~5500-6000 tokens for catalog

### Option D: Argument-Based Routing

Same as Option A, but SKILL.md uses `argument-hint`.

**Pros:** Minimal folders, arguments visible in hint
**Cons:** Agent must parse free-text correctly. No per-subcommand description. Fragile.

**Token cost:** Same as A (~1000-1200)

### Option E: Domain Router + Selective Wrappers (Recommended)

Hybrid of A and C. Domain skills handle most routing internally. Thin wrappers ONLY for the highest-frequency commands where dedicated autocomplete and description add measurable value.

**Selection criteria for thin wrappers:** Command gets a wrapper ONLY if ALL conditions met:
1. Invoked >3x per week by user
2. Semantically distinct enough that a specific description improves agent selection
3. Not naturally discoverable through the domain skill's description

**Structure:**
```
.devin/skills/
  # === Domain skills (routers with knowledge) ===
  write-documents/           # Routes 12 verbs, 30 files
    SKILL.md                 # Verb mapping + routing table
    ...
  session-management/        # Routes 5 operations, 7 files
    SKILL.md
    ...
  quality-assurance/         # Routes: critique, reconcile, verify, improve
    SKILL.md
    ...
  development/               # Routes: build, solve, implement, test, bugfix, fix
    SKILL.md
    ...
  workspace-management/      # Routes: prime, cleanup, sync, remove, project-release
    SKILL.md
    ...

  # === Selective thin wrappers (high-frequency only) ===
  commit/                    # Daily use, distinct from git-conventions domain
    SKILL.md
  go/                        # Unique orchestrator, no domain parent
    SKILL.md
  research/                  # Distinct entry point vs deep-research domain
    SKILL.md
  verify/                    # Highest-frequency QA command
    SKILL.md

  # === Existing tool/platform skills (unchanged) ===
  pdf-tools/
  youtube-downloader/
  ms-playwright-mcp/
  ...
```

**Domain skill SKILL.md router pattern (example for `quality-assurance`):**
```yaml
---
name: quality-assurance
description: Review, verify, critique, and improve documents and code. Use when asked to review, verify, critique, reconcile, or improve any artifact.
triggers:
  - user
  - model
---

# Quality Assurance

Route by user intent:

- **Critique** (find flawed assumptions, logic errors): Read `CRITIQUE_PROCEDURE.md`
- **Reconcile** (pragmatic review of critique findings): Read `RECONCILE_PROCEDURE.md`
- **Verify** (verify work against specs/rules): Read `VERIFY_PROCEDURE.md`
- **Improve** (find and fix inconsistencies): Read `IMPROVE_PROCEDURE.md`

## MUST-NOT-FORGET
...
```

**Thin wrapper SKILL.md example (for `verify`):**
```yaml
---
name: verify
description: Verify work against specs, rules, and quality gates. Use after implementation or significant changes.
triggers:
  - user
---

Execute verify procedure from @skills:quality-assurance.

1. Read `quality-assurance/SKILL.md` for MUST-NOT-FORGET
2. Read `quality-assurance/VERIFY_PROCEDURE.md`
3. Follow the procedure
```

**Pros:**
- Stays UNDER 32-skill detection ceiling (~23-30 total)
- High-frequency commands get dedicated autocomplete
- Knowledge centralized in domain skills (no duplication)
- Agent descriptions are focused: domain skills broad ("review, verify, critique"), wrappers narrow ("verify work against specs")
- Progressive disclosure: domain skills loaded by agent auto-match, wrappers loaded by user `/command`
- Naming convention clear: domain = noun (capability area), wrapper = verb (specific action)

**Cons:**
- Less discoverable than full Option C for infrequent commands
- User must know domain skill name for non-wrapped commands
- Decision of "what gets a wrapper" requires maintenance

**Token cost:** ~2300-3000 tokens for catalog

## Proposed Architecture (Option F)

### Two tiers of skills

**Tier 1: Domain skills (model-triggered, ~8-12 skills)**
Agent auto-discovers these. Descriptions loaded in context. Provide routing for users who don't know the exact command name. Each has `triggers: ["user", "model"]` (default) or `disable-model-invocation: false` (default).

**Tier 2: Procedure skills (user-only, ~44 skills)**
One per workflow. Each has `disable-model-invocation: true` / `triggers: ["user"]`. Zero context cost on Claude Code, minimal on Devin CLI. User invokes via `/name` with autocomplete.

### Tier 1: Domain Skills (model-triggered)

**`write-documents` (existing, 30 files)** - Auto-match: "write a spec", "create INFO document", "document this"

**`session-management` (existing, 7 files)** - Auto-match: "start a session", "save progress"

**`deep-research` (existing, 23 files)** - Auto-match: "research this topic", "deep dive into"

**`coding-conventions` (existing, 13 files)** - Auto-match: "review code style", "check conventions"

**`drift-correction` (existing, 5 files)** - Auto-match: "check for drift", "correct drift"

**`git-conventions` (existing, 1 file)** - Auto-match: "commit this", "prepare commit"

**`quality-assurance` (NEW, ~5-8 files)** - Auto-match: "verify this", "critique", "improve", "review quality"

**`content-processing` (NEW, ~3-5 files)** - Auto-match: "transcribe this", "translate"

**`workspace-management` (NEW, ~3-5 files)** - Auto-match: "clean up", "sync files", "release"

**`development` (NEW, ~3-5 files)** - Auto-match: "build this", "implement", "fix bug", "run tests"

**`knowledge-management` (NEW, ~2-3 files)** - Auto-match: "record failure", "extract learnings"

Count: 11 domain skills in context (~1100 tokens)

### Tier 2: Procedure Skills (user-only, `disable-model-invocation: true`)

Each is a skill folder containing SKILL.md + the workflow procedure (either inline or as supporting file). The SKILL.md is minimal:

```yaml
---
name: verify
description: Verify work against specs, rules, and quality gates.
disable-model-invocation: true
---

# Verify Procedure

[full workflow content here, loaded ONLY when user types /verify]
```

**From `write-documents` domain:** `write-spec`, `write-info`, `write-impl-plan`, `write-test-plan`, `write-strut`, `write-tasks-plan`, `write-minto`, `propose-minto`, `conversation-start`, `conversation-update`, `conversation-draft`
**From `session-management` domain:** `session-new`, `session-save`, `session-load`, `session-finalize`, `session-archive`
**From `deep-research` domain:** `research`
**From `drift-correction` domain:** `drift-detect`, `drift-correct`
**From `git-conventions` domain:** `commit`
**From `coding-conventions` domain:** `rename`
**From `quality-assurance` domain:** `critique`, `reconcile`, `verify`, `improve`
**From `content-processing` domain:** `transcribe`, `translate`
**From `workspace-management` domain:** `prime`, `cleanup`, `sync`, `remove`, `project-release`
**From `development` domain:** `build`, `solve`, `implement`, `test`, `bugfix`, `fix`, `partition`
**From `knowledge-management` domain:** `fail`, `learn`
**Standalone:** `go`, `switch-model`

Count: 44 procedure skills (zero context cost on Claude Code)

### Existing Platform/Tool Skills (unchanged, model-triggered)

`pdf-tools`, `youtube-downloader`, `ms-playwright-mcp`, `playwriter-mcp`, `llm-computer-use`, `windows-desktop-control`, `git`, `github`, `google-account`, `travel-info`, `llm-evaluation`, `edird-phase-planning`

Count: 12 tool skills in context (~1200 tokens)

### Totals

- Model-triggered skills in context: **23** (11 domain + 12 tool) = ~2300 tokens
- User-only skills NOT in context: **44** (zero tokens on Claude Code)
- **Grand total: 67 skill folders**, but only **23 consume context tokens**
- Detection ceiling: 23 model-triggered skills, well under 32-36 limit
- 44 workflows fully absorbed (0 remaining)

## Cross-Platform Strategy

**The same SKILL.md serves all platforms** with platform-specific frontmatter:

```yaml
---
name: verify
description: Verify work against specs, rules, and quality gates.
# Claude Code: disable-model-invocation removes from context entirely
disable-model-invocation: true
# Devin CLI: triggers: ["user"] prevents auto-activation
triggers:
  - user
---
```

Both fields can coexist. Each platform reads only its own field.

**Per-platform behavior:**

- **Cascade**: Keep `.devin/workflows/*.md` (native format, proven, zero context cost). Skills for domain knowledge only. No migration needed.
- **Claude Code**: Use `.claude/skills/<name>/SKILL.md` with `disable-model-invocation: true`. Zero context cost. Full autocomplete. Alternatively `.claude/commands/<name>.md` for single-file skills (no folder needed).
- **Devin Local/CLI**: Use `.devin/skills/<name>/SKILL.md` with `triggers: ["user"]`. Description still loaded (~30 tokens each) but auto-invocation prevented.

**File reference approach:** Use tool calls (most portable):
```markdown
1. Read `.devin/skills/write-documents/SPEC_TEMPLATE.md` for document structure
2. Follow the template
```

**Plugin option for Devin CLI:** Bundle all procedure skills into a DevSystem plugin. Invoke as `/devsys:verify`, `/devsys:commit`. Reduces namespace clutter, enables `devin plugins install` distribution. [VERIFIED - Devin plugin system supports this]

## ACP (Agent Client Protocol) - Not Relevant

ACP has no concept of workflows, skills, slash commands, or direct-call syntax. The protocol is a wire-level standard (JSON-RPC 2.0 over stdio) for editor-to-agent communication. Its `session/prompt` method accepts free-form text content blocks - no structured field for command name, skill reference, or procedure invocation exists.

If a user types `/verify` in an ACP client (Zed, JetBrains), the editor passes that string as plain text in `session/prompt`. The agent interprets it however it wants. ACP v2 proposal adds plan variants and unified tool calls but introduces nothing related to commands or skills.

**Implication for this research:** ACP is not a factor in the skill vs workflow architecture decision. Cross-platform portability comes from file conventions (SKILL.md format, `.agents/` standard), not from protocol features. Each client implements its own command mechanism outside ACP.

Source: `e:\Dev\KarstensWorkspace\docs\AI-Standards\ACP-AgentClientProtocol_2026-06-12` [ACP-IN01 through ACP-IN14]

## Open Questions

1. **Devin CLI `triggers: ["user"]` context behavior** - Does this also remove descriptions from agent context (like Claude Code's `disable-model-invocation: true`)? Devin docs say "at session start, Devin sees a list of all available skills (name + description)" without specifying trigger-based filtering. Need testing. [ASSUMED descriptions still loaded]
2. **Dual frontmatter compatibility** - Can `disable-model-invocation: true` and `triggers: ["user"]` coexist in the same SKILL.md without errors on either platform? Need testing. [ASSUMED both fields are silently ignored by the other platform]
3. **Folder count mitigation** - 67 folders is significant. For Cascade (workflows + skills), this doesn't apply (workflows are flat files). For Devin Local, plugin bundling or subfolder organization may reduce visual noise.
4. **Claude Code bug #26251** - An issue reported that `disable-model-invocation: true` sometimes prevents the user from invoking via the Skill tool (model refuses to execute). May require testing on current Claude Code version.

## Exclusions

- **MCP-based skill composition**: Not researched. MCP tools could theoretically wrap skill invocation, but this adds infrastructure complexity without clear benefit over thin wrappers.
- **Devin Cloud Playbooks**: Different mechanism (Devin Cloud-specific), not relevant to local/desktop agent workflows.
- **.agents specification (AGENTS-1)**: The full `.agents/manifest.yaml` spec includes modes, policies, profiles, and activation types (instruction_only, mcp_tool, cli_shim). Not researched in depth since IPPS currently targets Devin Desktop and Claude Code, not the full `.agents` spec.

## Sources

- SKLWRKFL-IN01-SC-DVNAI-CRSKL: https://docs.devin.ai/cli/extensibility/skills/creating-skills - Skill format, frontmatter, subagent orchestration
- SKLWRKFL-IN01-SC-DVNAI-OVRVW: https://docs.devin.ai/cli/extensibility/skills/overview - Skill discovery, triggers, scope
- SKLWRKFL-IN01-SC-DVNAI-CSKLS: https://docs.devin.ai/desktop/cascade/skills - Cascade progressive disclosure, supporting files
- SKLWRKFL-IN01-SC-DVNAI-PRDSK: https://docs.devin.ai/product-guides/skills - Devin Cloud skills, one-at-a-time limitation
- SKLWRKFL-IN01-SC-DVNAI-DVNLC: https://docs.devin.ai/desktop/devin-local - Devin Local limitations, skill migration
- SKLWRKFL-IN01-SC-AGSKL-SPEC: https://agentskills.io/specification - Agent Skills open standard, directory structure, progressive disclosure
- SKLWRKFL-IN01-SC-AGSKL-IMPL: https://agentskills.io/client-implementation/adding-skills-support.md - Client implementation guide, discovery paths
- SKLWRKFL-IN01-SC-CLAUD-SKLS: https://code.claude.com/docs/en/skills - Claude Code skills, subfolder discovery, live change detection
- SKLWRKFL-IN01-SC-CLAUD-SLSH: https://code.claude.com/docs/en/slash-commands - Commands/skills merge, namespace syntax
- SKLWRKFL-IN01-SC-CLAUD-CMDS: https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md - Command organization patterns
- SKLWRKFL-IN01-SC-GHUB-AGNT: https://github.com/agentsfolder/spec - .agents specification, manifest.yaml, SKILL.yaml format
- SKLWRKFL-IN01-SC-GHUB-AGSK: https://github.com/agentskills/agentskills - Agent Skills repo, Anthropic-developed standard
- SKLWRKFL-IN01-SC-MSFT-AGSK: https://learn.microsoft.com/en-us/agent-framework/agents/skills - Microsoft Agent Framework skills adoption
- SKLWRKFL-IN01-SC-GHUB-DCUL: https://github.com/OnlyTerp/DevinCLI-Unlocked - Devin CLI community guide, subagent patterns
- SKLWRKFL-IN01-SC-GHUB-SBFLD: https://github.com/anthropics/claude-code/issues/44678 - Subfolder organization request for slash commands
- SKLWRKFL-IN01-SC-IPPS-DVDT: `e:\Dev\IPPS\Docs\INFO_HOW_DEVIN_WORKS.md` [DVDT-IN01] - Devin Desktop capabilities reference
- SKLWRKFL-IN01-SC-GHUB-AGNC: https://github.com/the-agency-ai/the-agency/issues/289 - 59 skills audit, skill sprawl, consolidation recommendations
- SKLWRKFL-IN01-SC-GHUB-FUSE: https://github.com/gaia-research/skill-fuse - Skill fusion tool, SKILL.md as router with reference/ delegation
- SKLWRKFL-IN01-SC-CRSR-SKLS: https://cursor.com/help/customization/skills - Cursor recursive subfolder discovery, category folders
- SKLWRKFL-IN01-SC-CKLB-BLOG: https://cheesecakelabs.com/blog/agent-skills-for-workflows-into-rules-file/ - 69% token reduction measurement, rules-to-skills migration
- SKLWRKFL-IN01-SC-LCSK-BLOG: https://localskills.sh/blog/skill-md-vs-claude-md-vs-agents-md - SKILL.md vs CLAUDE.md vs AGENTS.md decision guide
- SKLWRKFL-IN01-SC-DVTO-BLOG: https://dev.to/shrouwoods/an-efficient-cursor-directory-less-context-better-agents-kl0 - "Route, do not restate" pattern, 5-layer architecture
- SKLWRKFL-IN01-SC-GHUB-PRDN: https://github.com/enuno/claude-command-and-control - Production-grade skills, 32-36 detection ceiling, trigger tables
- SKLWRKFL-IN01-SC-GHUB-BPRC: https://github.com/nyosegawa/skills/blob/main/agent-skill-best-practices.md - Anthropic-aligned best practices, orchestration patterns
- SKLWRKFL-IN01-SC-GHUB-DSTL: https://github.com/distillation-labs/agentyc/blob/main/skills-guide.md - Anthropic skills guide, cross-platform deployment
- SKLWRKFL-IN01-SC-MDIM-WSKT: https://medium.com/@wasowski.jarek - MCP tool sprawl, 25-50 tool accuracy degradation, dynamic tool assembly
- SKLWRKFL-IN01-SC-ARXV-CEAD: https://arxiv.org/html/2605.08258v1 - CEAD paper, micro-agent proliferation anti-pattern
- SKLWRKFL-IN01-SC-SSHH-BLOG: https://blog.sshh.io/p/how-ai-productivity-fails - "Build skills for class not instance", skill encoding philosophy
- SKLWRKFL-IN01-SC-CLPW-TIPS: https://support.claude.com/en/articles/14554000-claude-code-power-user-tips - Claude Code power user patterns, skills for repeated workflows
- SKLWRKFL-IN01-SC-DVDG-MIGR: https://www.developersdigest.tech/blog/migrating-from-windsurf-to-claude-code - Windsurf-to-Claude migration guide
- SKLWRKFL-IN01-SC-CCGD-BLOG: https://claudecodeguides.com/how-to-create-custom-slash-command-claude-2026/ - Command organization, prefix naming
- SKLWRKFL-IN01-SC-GHUB-CCCM: https://github.com/epicurean-Paradox/claude-code-mastery - Trigger tables, skill gates, session drift mitigation
- SKLWRKFL-IN01-SC-BCLW-SOUL: https://www.betterclaw.io/blog/soul-md-agents-md-configuration-guide - Token budget guidelines, 400-500 token ceiling per always-on file
- SKLWRKFL-IN01-SC-SJNM-TOOL: https://github.com/sjnims/plugin-dev/commit/4a5bb09 - SlashCommand tool consolidated into Skill tool
- SKLWRKFL-IN01-SC-CLCD-SKLS: https://code.claude.com/docs/en/skills - disable-model-invocation removes description from context, invocation control table
- SKLWRKFL-IN01-SC-CLCD-DMOD: https://code.claude.com/docs/en/custom-skills - Commands merged into skills, disable-model-invocation for workflow equivalence
- SKLWRKFL-IN01-SC-DVNAI-PLGN: https://docs.devin.ai/cli/extensibility/plugins/overview - Devin CLI plugin system, namespaced skills, manifest, governance
- SKLWRKFL-IN01-SC-GHUB-SGNZ: https://github.com/SigNoz/agent-skills - Devin plugin example, /plugin:skill namespace pattern
- SKLWRKFL-IN01-SC-CLCD-PLGN: https://claude-code-playbook.pages.dev/en/docs/level-4/plugins - Claude Code plugin system, namespace rules
- SKLWRKFL-IN01-SC-GHUB-BG26: https://github.com/anthropics/claude-code/issues/26251 - Bug: disable-model-invocation blocks user invocation via Skill tool
- SKLWRKFL-IN01-SC-GHUB-IS19: https://github.com/anthropics/claude-code/issues/19141 - Clarification: user-invocable vs disable-model-invocation distinction
- SKLWRKFL-IN01-SC-DVDG-DMOD: https://www.developersdigest.tech/guides/disable-model-invocation - disable-model-invocation usage guide
- SKLWRKFL-IN01-SC-CLKF-PLGN: https://claudefa.st/blog/tools/mcp-extensions/plugins-distribution - Plugin distribution, marketplace, namespace rules
- SKLWRKFL-IN01-SC-IPPS-ACPR: `e:\Dev\KarstensWorkspace\docs\AI-Standards\ACP-AgentClientProtocol_2026-06-12` [ACP-IN01] - ACP protocol has no skill/workflow/command concept

## Document History

**[2026-08-04 17:50]**
- Added: ACP section - protocol has no concept of skills/workflows/commands, not a factor in architecture decision
- Added: ACP source reference

**[2026-08-04 17:30]**
- Added: Option F (User-Only Skills + Domain Knowledge Skills) as new recommendation
- Changed: Breakthrough finding - `disable-model-invocation: true` eliminates context cost (verified from Anthropic docs)
- Changed: Architecture now uses two tiers: model-triggered domain skills (23 in context) + user-only procedure skills (44 at zero cost)
- Added: Cross-Platform Strategy section with dual frontmatter approach
- Added: Plugin bundling option for Devin CLI distribution
- Added: 10 new sources (plugin systems, invocation control, bugs)

**[2026-08-04 16:40]**
- Added: Community Voices and Evidence section (16 new sources)
- Changed: Recommendation from Option C (Thin Wrapper) to Option E (Domain Router + Selective Wrappers)
- Changed: Detection ceiling (32-36 skills) now drives architecture decision
- Changed: Grand total from ~58-63 folders to 29 folders (under ceiling)
- Added: Option E with router pattern examples and thin wrapper selection criteria

**[2026-08-04 14:55]**
- Initial research: platform capabilities, approach analysis, workflow-to-skill mapping
