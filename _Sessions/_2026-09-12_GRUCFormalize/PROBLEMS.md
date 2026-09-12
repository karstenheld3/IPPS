# Session Problems: GRUC Formalization

**Started**: 2026-09-12

## Open

- **GRUC-PR-0001**: CHECKS dual purpose may conflict with "invisible to executor" principle. Quality improvement checks are not process discipline - they are more like RULES. Need to resolve: should CHECKS remain invisible to executor, or does the new quality check category change this? (Resolution: CHECKS remain invisible to executor. Quality improvement checks are post-execution assessment, not pre-execution guidance. The invisibility principle holds because the working agent should not optimize for improvement tips during generation.)
- **GRUC-PR-0002**: verify.md currently includes SOCAS conceptual verification, fact-checking, privacy scans. Moving these out of verify.md means they need a new home. Options: (a) move to CHECKS, (b) move to critique.md, (c) keep in verify.md as "conceptual" beyond RULES. User wants verify.md ONLY against RULES, so these must move. SOCAS → critique.md (logic flaws), fact-check → improve.md or CHECKS, privacy → CHECKS or verify.md RULES.
- **GRUC-PR-0003**: critique.md currently does extensive research (5 topics, web search). Switching to GUIDES-only may reduce its effectiveness. Need to determine: does GUIDES contain enough direction for critique, or does critique need additional sources?
- **GRUC-PR-0004**: drift-detect.md currently builds DoD from SPEC/IMPL/TASKS sources. Switching to CHECKS-only means CHECKS must contain all the DoD items currently extracted from sources. This is a significant content creation effort.
- **GRUC-PR-0005**: improve.md currently reads RULES for Phase 2 (fix violations). If improve.md only consults CHECKS, where do rule violations go? Options: (a) improve.md still reads RULES for Phase 2 only, (b) rule violations move to CHECKS, (c) verify.md handles all rule violations and improve.md only does Phase 3+4.
- **GRUC-PR-0006**: EXAMPLE files need a home. Per-skill? Per-domain? Where do they live in the folder structure?

## Resolved

(none yet)

## Deferred

(none yet)
