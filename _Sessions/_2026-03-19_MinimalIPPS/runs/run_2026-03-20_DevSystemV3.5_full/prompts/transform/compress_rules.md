Compress this DevSystem rule file while preserving ALL functional content.

Primary (keep as-is): Behavioral constraints, gate conditions, phase definitions, ID format specifications, verb/state/placeholder definitions, folder structure diagrams, workflow reference tables, checkbox-based checklists.

Secondary (compress):
- BAD/GOOD example pairs: Keep only the GOOD example unless the BAD is non-obvious. For ambiguous rules, keep 1 BAD + 1 GOOD (single-line each).
- Verbose explanations of WHY a rule exists: Reduce to one sentence or drop if the rule is self-explanatory.
- Lists of standard pairs/opposites (open/close, read/write): Drop entirely - readers know these.
- Philosophy sections that restate goals covered in individual rules: Drop or reduce to 1-line summary.
- Multi-line format examples when a single-line pattern suffices: Collapse to `Format: X` one-liner.

Drop:
- Redundant restatements of the same principle in different words.
- Section introductions that just announce what follows ("This section covers...").
- Table of Contents sections (these are navigational, not functional).
- Verbose rationale paragraphs when the rule name is self-documenting.

Formatting rules:
- Preserve all markdown headers at their original level.
- Preserve all rule IDs exactly (LOG-GN-01, AP-PR-07, etc.).
- Preserve all code blocks that define formats, schemas, or required syntax.
- Preserve all conditional logic (if X then Y, when A do B).
- Preserve all MUST/MUST NOT/NEVER constraints verbatim.
- Use single-line entries where multi-line adds no information.
- Keep cross-references to other files/skills/workflows intact.
- Do NOT add new content, commentary, or summaries not in the original.