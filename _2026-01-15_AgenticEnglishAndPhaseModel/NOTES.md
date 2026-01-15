# Session Notes

## Session Info

- **Started**: 2026-01-15
- **Goal**: Define Agentic English vocabulary and IPPS Phase Model specifications

## IMPORTANT: Cascade Agent Instructions

- Use lists, not Markdown tables
- No emojis in documentation
- No `---` markers between sections
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Use box-drawing characters for trees: `├─>` `└─>` `│`
- Instruction tokens use brackets: `[VERB]`, `[PLACEHOLDER]`, `[LABEL]`
- Context states use no brackets: `COMPLEXITY-HIGH`, `HOTFIX`, `SINGLE-PROJECT`
- Document History at end, reverse chronological order

## Key Decisions

- Instruction tokens (brackets) vs Context states (no brackets) syntax distinction
- Five-phase model: DISCOVERY, DESIGN, IMPLEMENT, IMPROVE, DELIVER
- Complexity levels map to semantic versioning: LOW=patch, MEDIUM=minor, HIGH=major

## Important Findings

- Agentic English provides controlled vocabulary for agent-human communication
- Phase model synthesizes Agile, ITIL, PRINCE2, Shape Up, Double Diamond, Scrum, SDLC

## Workflows to Run on Resume

- `/prime` to load context
- Review `_SPEC_AGENTIC_ENGLISH.md` and `_SPEC_IPPS_PHASE_MODEL.md`
