Compress this DevSystem workflow file while preserving ALL execution logic.

Primary (keep as-is): Step sequences with numbering, gate checks with checkboxes, context branching conditions (CONTEXT-SPECIFIC sections), MUST-NOT-FORGET lists, prerequisites, stuck detection thresholds, trigger definitions, mandatory re-read lists, output format specifications.

Secondary (compress):
- Step descriptions: Reduce multi-sentence steps to single imperative lines. "First, you should analyze the context to understand what documents exist" → "Analyze context - identify existing documents".
- BAD/GOOD pairs in workflow rules: Keep GOOD only unless BAD shows a non-obvious mistake.
- Prose paragraphs explaining workflow philosophy or mindset: Reduce to 1-line profile statement.
- Multiple code block examples showing similar patterns: Keep 1, reference pattern for rest.
- PowerShell/command blocks: Keep the command, drop surrounding explanation if the command is self-documenting.
- Context-specific sections with repetitive structure: Merge common patterns, note differences only.
- "When to Use" sections that restate the trigger: Drop.

Drop:
- Table of Contents sections.
- Example output sections that duplicate the Output Format section.
- Verification sections that exactly duplicate /verify workflow checks.
- Prose that restates what numbered steps already say.
- Comments in code blocks that restate the step description.

Formatting rules:
- Preserve all numbered step sequences exactly.
- Preserve all checkbox gate items verbatim.
- Preserve all conditional routing (if X → run Y, context A → steps, context B → steps).
- Preserve GLOBAL-RULES sections completely.
- Preserve all /workflow and @skills: references.
- Preserve all placeholder tokens ([SESSION_FOLDER], [WORKSPACE_FOLDER], etc.).
- Keep frontmatter (description, auto_execution_mode) exactly.
- Merge near-identical PowerShell blocks differing only in a parameter into one parameterized block.
- Do NOT add content not in the original.