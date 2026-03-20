Compress this DevSystem template file while preserving the COMPLETE structural contract.

Primary (keep as-is): Header block format (Doc ID, Goal, Target file, Depends on), all section headings with their nesting level, all ID format patterns (FR-XX, DD-XX, EC-XX, TC-XX, etc.), all placeholder patterns showing required fields, MUST-NOT-FORGET sections, checkbox items, field definitions with their descriptions.

Secondary (compress):
- Full worked examples embedded in templates: Keep the structure/skeleton, remove filled-in content that merely illustrates. If a template has both a skeleton AND a full example section, drop the full example.
- BAD/GOOD pairs inside templates: Drop - these belong in the corresponding RULES file.
- Verbose placeholder descriptions: "[Single sentence describing what to specify]" → keep the bracket placeholder, drop the meta-description.
- Section descriptions that say "fill this with X": Reduce to 1-line comment or drop if the section heading is self-explanatory.
- Example JSON/code blocks: Keep the schema/structure, reduce example data to 1 row/entry.
- Concurrent blocks explanation + Auth System example in STRUT: Keep rules (4 lines), compress example to minimal.

Drop:
- "Template Instructions" HTML comment blocks (one-time guidance).
- Multiple examples showing the same template filled differently.
- Explanatory prose between template sections that won't appear in the output document.
- Table of Contents if sections are already well-headed.

Formatting rules:
- Preserve ALL section headings at exact markdown level.
- Preserve ALL ID format patterns exactly (e.g., `[TOPIC]-IP[NN]`, `[PREFIX]-IP01-EC-01`).
- Preserve ALL placeholder tokens in brackets.
- Preserve ALL checkbox patterns.
- Preserve header block structure completely (Doc ID, Goal, Dependencies, etc.).
- Preserve Document History section format.
- Keep at least 1 minimal example per distinct content type (JSON, code, ASCII diagram).
- Do NOT add content not in the original.