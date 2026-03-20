Score this compressed file on a 1-5 scale.

Score 5: ALL functional content preserved - rules, constraints, conditions, formats, commands, schemas, cross-references. Significant size reduction (>25%). An agent reading this compressed version would behave identically to one reading the original.

Score 4: All critical functional content preserved. Minor omissions limited to: redundant examples, verbose explanations of self-documenting rules, historical data. Agent behavior unchanged. Size reduction >15%.

Score 3: Core functional content preserved but some operational detail lost: an edge case condition dropped, a format variant removed, or a troubleshooting scenario missing. Agent could operate correctly in common cases but might miss specific scenarios.

Score 2: Significant functional content lost: rules missing, conditional logic simplified losing branches, format specifications incomplete, or command parameters dropped. Agent behavior would change in multiple scenarios.

Score 1: Critical content missing: core rules dropped, structural contracts broken, command syntax incomplete, or cross-references removed. Agent would malfunction or produce wrong results.

Minimum acceptable score: 3.5

Check specifically:
- [ ] All MUST/MUST NOT/NEVER statements preserved
- [ ] All conditional logic preserved
- [ ] All ID formats and schemas intact
- [ ] All cross-references preserved
- [ ] All command syntax complete
- [ ] No meaning changed in any instruction
- [ ] Frontmatter preserved if present

Return: {"score": N, "justification": "...", "lost_items": ["..."], "size_reduction_percent": N}