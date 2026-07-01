# Release Notes: v4.0 (2026-07-01)

## Summary

Major release spanning 46 commits from V3.8 (2026-06-05) through V4.0. Theme: drift prevention, structured argumentation (AMINTON), and quality infrastructure maturation. Two new core concepts (GRUC, AMINTON) bring the system to ten integrated specifications.

## Highlights

- **GRUC (Guides, Rules, Checks)** - Drift-prevention technique with three file types separated by lifecycle position. GUIDE consumed before execution, RULES during verification, CHECKS during post-execution audit. Prevents gaming by keeping CHECKS invisible during work.
- **AMINTON (Agentic MINTO Notation)** - Tree notation for Minto Pyramid articles enabling machine verification of argument completeness. Full workflow pipeline: `/propose-minto` (generate candidates) and `/write-minto` (develop article).
- **Drift Detection and Correction** - `/drift-detect` and `/drift-correct` workflows for post-execution process audit using CHECKS files.
- **10 Core Concepts** - README updated from 8 to 10 integrated specifications with GRUC and AMINTON.
- **42 Workflows** - Up from 39, adding Minto, drift, and utility workflows.

## New Core Concepts

- **GRUC** - `Docs/Concepts/_INFO_GRUC_GUIDES_RULES_CHECKS.md`
- **AMINTON** - `Docs/Concepts/_INFO_AGENTIC_MINTO_ARTICLES.md`

## New Workflows (7)

- `/propose-minto` - Generate 3 scored AMINTON argument candidates from research material
- `/write-minto` - Develop full Minto Pyramid article from draft (tree-first, then prose)
- `/drift-detect` - Post-execution drift detection, persist gaps to __DRIFT_ file
- `/drift-correct` - Close drift gaps identified by /drift-detect
- `/detect-ai` - AI writing detection workflow (removed before final release)
- `/fix` - Fix any problem by reading relevant DevSystem knowledge
- `/cleanup` - Delete temporary files and artifacts left by workflows

## Removed Workflows

None.

## New Skills / Skill Changes

- **write-documents** - Added MINTO guide, rules, and templates:
  - `MINTO_GUIDE.md` - Strategic decisions for Minto article writing (tree-first sequencing)
  - `MINTO_RULES.md` - Structural verification rules (DS, AQ, TI, ME, AS, CL categories)
  - `MINTO-DRAFT_TEMPLATE.md` - Template for `__MINTO-DRAFT_[Article].md` scaffolding
  - `MINTO_TEMPLATE.md` - Template for `_MINTO_[Article].md` final article
  - `INFO_GUIDE.md`, `INFO_RULES.md` - GRUC files for INFO documents
  - `SK-CT-06` - No Document History in skill resource files
- **drift-correction** - New skill folder with CHECKS files for workflow process audit
- **deep-research** - Refined summary structure, Goals/Questions section, per-topic summaries, prevent Google AI answer extraction

## DevSystem Version Changes

**V4.0**:
- Bumped from V3.8 to V4.0 (major: new core concepts, breaking workflow additions)
- `devsystem-core.md` Workflow Reference updated to 42 entries (was 25)
- `devsystem-ids.md` overhauled: 7-14 char topics, nested IDs for `T##_`/`S##_` folders
- Agent behavior rule: no-humor clause added (prevents whimsical content in reusable files)
- Verify workflow: added Minto Documents section with template structure checks
- Improve workflow: added Minto Documents context detection
- Critique workflow: added Minto attack vectors (magnet failure, circular evidence, false MECE)

## Key Refactoring

- **AQUASE -> MINTO -> AMINTON**: Argument notation renamed twice for clarity. Final name: AMINTON (Agentic MINTO Notation)
- **DRAFT-MINTO -> MINTO-DRAFT**: Draft filename pattern standardized to `__MINTO-DRAFT_[Article].md`
- **follow-instructions -> adp -> drift-detect/drift-correct**: Agent drift prevention workflow split into detect + correct pair

## README Changes

- Core Concepts: 8 -> 10 (added GRUC, AMINTON)
- "How they work together" table: 10 entries
- Workflows Reference: 42 entries (added propose-minto, write-minto, and others)
- Skills Reference: write-documents updated to include MINTO

## Workspace Files

- `README.md` - Major update: 10 concepts, 42 workflows, GRUC/AMINTON sections
- `SOPS.md` - SOP 6 added for workflow add/edit/remove
- `ID-REGISTRY.md` - Added topics: FINRESAI, RUSESCPOL, AIDET, and others
- `deploy-to-all-repos.md` - Mandatory sync step added, ghost adp skill removed
- `NOTES.md` - DevSystem version bumped to V4.0
- `FAILS.md` - Multiple entries added during development

## Migration Notes

- No breaking changes to existing linked repos
- New files deployed via `/deploy-to-all-repos`: 4 Minto files + updated rules/workflows
- `workflows/project-release.md` protected by NeverOverwrite in SharePoint-GPT-Middleware
- Old `AQUASE` references no longer exist; all renamed to `AMINTON`
