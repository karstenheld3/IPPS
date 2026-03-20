Score this compressed workflow file on a 1-5 scale.

Score 5: ALL step sequences preserved in order with correct numbering. ALL gate checks with checkboxes intact. ALL context branches preserved. ALL prerequisites, triggers, and MUST-NOT-FORGET items present. Significant size reduction (>25%). Frontmatter intact.

Score 4: All execution paths preserved. Minor omissions: a redundant example removed, an explanatory sentence dropped, a "When to Use" section removed where trigger section covers it. No execution path changed. Size reduction >15%.

Score 3: Core execution logic preserved but some paths simplified: a context-specific section merged losing a minor distinction, a stuck detection detail dropped, or an output format field removed. Workflow would mostly execute correctly but might miss edge cases.

Score 2: Execution logic altered: steps reordered, gate checks missing items, context branches merged losing important routing, prerequisites incomplete, or MUST-NOT-FORGET items missing. Workflow would produce different results in multiple scenarios.

Score 1: Critical execution content missing: step sequences broken, gate checks removed, context branching lost, or GLOBAL-RULES dropped. Workflow would fail or produce wrong results.

Minimum acceptable score: 3.5

Check specifically:
- [ ] All numbered steps present and in order
- [ ] All gate check checkbox items preserved
- [ ] All context branches preserved (SESSION-MODE vs PROJECT-MODE, etc.)
- [ ] MUST-NOT-FORGET section complete
- [ ] All /workflow and @skills: references intact
- [ ] Frontmatter preserved
- [ ] All placeholder tokens preserved

Return: {"score": N, "justification": "...", "lost_items": ["..."], "size_reduction_percent": N}