Score this compressed skill document on a 1-5 scale.

Score 5: ALL commands/tools with complete parameter lists preserved. ALL capability boundaries (when to use/not use) intact. ALL MUST-NOT-FORGET items present. ALL configuration blocks preserved. ALL safety warnings intact. Significant size reduction (>25%).

Score 4: All operational content preserved. Minor omissions: a redundant example removed, a troubleshooting tip for obvious issue dropped, historical test data removed. Agent could use the skill identically. Size reduction >15%.

Score 3: Core capability preserved but some operational detail lost: a parameter description shortened losing a constraint, an edge case in troubleshooting dropped, or a configuration variant removed. Agent could use the skill for common cases but might struggle with unusual scenarios.

Score 2: Significant capability information lost: command parameters missing, configuration blocks incomplete, capability boundaries unclear, or essential setup steps removed. Agent would fail to use the skill correctly in multiple scenarios.

Score 1: Critical capability missing: commands dropped, MUST-NOT-FORGET items removed, safety warnings deleted, or the skill's core purpose unclear. Agent could not use the skill.

Minimum acceptable score: 3.5

Check specifically:
- [ ] All commands/tools listed with parameters
- [ ] MUST-NOT-FORGET section complete
- [ ] When to use / when NOT to use preserved
- [ ] All configuration blocks intact
- [ ] All safety/warning notes preserved
- [ ] Skill frontmatter preserved
- [ ] At least 1 example per distinct operation

Return: {"score": N, "justification": "...", "lost_items": ["..."], "size_reduction_percent": N}