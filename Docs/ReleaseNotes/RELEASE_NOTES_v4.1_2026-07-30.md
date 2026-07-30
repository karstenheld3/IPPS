# Release Notes: v4.1 (2026-07-30)

## Summary

Minor release spanning 22 commits from V4.0 (2026-07-01) through V4.1. Theme: conversation intelligence, agent ecosystem research, and write-documents quality refinement. Introduces ghostwriting capability via humanizing rules and a new `/conversation-draft` workflow.

## Highlights

- **Conversation Humanizing Rules** - 6 rules (CV-HM-01 through CV-HM-06) for ghostwriting emails and messages in the user's voice, based on forensic linguistics research
- **`/conversation-draft`** - New workflow for drafting emails, WhatsApp messages, or other text AS the user
- **Agent Ecosystem Research** - 5 new INFO documents covering Codex, Claude Code, Devin MapReduce, agent comparison, and human writing patterns
- **Write-Documents Quality** - SPEC rules/template overhaul, INFO template reconciliation, new WORKFLOW_RULES file
- **LLM Evaluation** - Claude Fable 5, Mythos 5, Sonnet 5 models added to registry

## New Workflows (1)

- `/conversation-draft` - Draft emails, WhatsApp messages, or other text AS the user

## Removed Workflows

None.

## New Skills / Skill Changes

- **write-documents**:
  - `CONVERSATION_HUMANIZING_RULES.md` - 6 rules for ghostwriting in user's voice (CV-HM-01 through CV-HM-06)
  - `WORKFLOW_RULES.md` - New file for workflow authoring conventions
  - `SPEC_RULES.md` - Overhauled specification writing rules
  - `SPEC_TEMPLATE.md` - Updated template aligned with new rules
  - `CONVERSATION_RULES.md` - Added CV-HM-* index, CV-ST-01 section ordering, CV-LN-04 absolute links
  - `CONVERSATION_TEMPLATE.md` - Humanizing Settings section, MNF items
  - `SKILL.md` - Updated with new file references
  - INFO template fixes: unnumber meta-sections, fix source claim scope, add [UNVERIFIED], Timeline relaxation
- **session-management**:
  - `cascade-delete.ps1` - Cascade session deletion helper
  - `cascade-search.ps1` - Cascade session search helper
- **llm-evaluation** - Added Claude Fable 5, Mythos 5, Sonnet 5 to model registry; reorganized historical screenshots into date-prefixed folders
- **llm-transcription** - Synced model registry and pricing from llm-evaluation
- **deep-research** - Added site-specific rule for gesetze-im-internet.de

## New Research Documents

- `Docs/FurtherResearch/_INFO_HOW_CODEX_WORKS.md` - OpenAI Codex agent architecture
- `Docs/FurtherResearch/_INFO_HOW_CLAUDE_CODE_WORKS.md` - Anthropic Claude Code architecture
- `Docs/FurtherResearch/_INFO_DEVIN_AGENTIC_MAP_REDUCE.md` (AGNTMAPR-IN01) - Devin's 5-stage whole-codebase reasoning pipeline
- `Docs/FurtherResearch/_INFO_AGENT_COMPARISON.md` - Cross-agent feature comparison
- `Docs/FurtherResearch/_INFO_HUMAN_WRITING_PATTERNS.md` (HMNWRTPTN-IN01) - Forensic linguistics research for humanizing rules
- `Docs/INFO_AGENTIC_PROBLEMS.md` (AGNTPROB-IN01) - Categorized failure patterns in AI-assisted development
- `Docs/Concepts/_INFO_APAPALAN_PRINCIPLE.md` - APAPALAN writing principle deep dive
- `Docs/Concepts/_INFO_MECT_PHILOSOPHY.md` - MECT communication philosophy deep dive
- `Docs/INFO_HOW_DEVIN_WORKS.md` - Updated with Devin Desktop 3.6.22 features

## DevSystem Version Changes

**V4.1**:
- Bumped from V4.0 to V4.1 (minor: no breaking changes, new capabilities)
- Added SOP 7 (post-release version bump procedure)
- Added `.claude/commands/` for Claude Code compatibility (workflow symlinks)
- Date verification rule added to `agent-behavior.md`
- MECT deliberate redundancy concept and APAPALAN signal boundary added

## Rules Changes

- `agent-behavior.md` - Date verification rule: always verify dates via web search, never rely on training data
- `core-conventions.md` - MECT deliberate redundancy concept
- `tools-and-skills.md` - Updated skill registry

## Infrastructure

- Removed obsolete `Windsurf.bat` and `WindsurfNext.bat` (renamed to `Devin.bat` / `DevinNext.bat` in v4.0)
- Excluded `_PrivateSessions/` from git tracking
- Excluded `skills/llm-evaluation/model-sources/` from git and deployment
- Fixed commit workflow git noise (CRLF warnings, rename summaries) causing Cascade hangs

## Failures Logged (6)

- `GLOB-FL-034` - Private path leaked into reusable template
- `GLOB-FL-035` - Ignored "draft" verb semantics, created file instead of presenting
- `GLOB-FL-036` - Wrote rule examples violating existing rules (locale dates, ASCII Umlauts)
- `GLOB-FL-037` - Point-fixes without requirement propagation
- `GLOB-FL-038` - Deleted file without confirmation, misread "no keep"
- `GLOB-FL-039` - Incomplete sync: missed devsystem-core.md Workflow Reference

## Statistics

- **Commits**: 22
- **Files Added**: 59
- **Files Modified**: 42
- **Files Deleted**: 107 (mostly reorganization of llm-evaluation screenshots)
- **New Topics Registered**: AGNTPROB, AGNTMAPR, HMNWRTPTN
- **Workflows**: 43 (was 42)

## Document History

**[2026-07-30 16:58]**
- Initial release notes created
