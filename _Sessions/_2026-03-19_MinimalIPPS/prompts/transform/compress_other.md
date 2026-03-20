Compress this DevSystem file while preserving ALL functional content.

Classify each section of the file:

Primary (keep as-is):
- All behavioral rules, constraints, and conditions
- All ID formats, schemas, and structural contracts
- All command syntax and parameter definitions
- All MUST/MUST NOT/NEVER statements
- All conditional logic (if X then Y)
- All cross-references to other files (/workflow, @skills:)
- All configuration blocks
- All safety/warning notes

Secondary (compress):
- BAD/GOOD example pairs: Keep GOOD only unless BAD shows a non-obvious mistake. Keep at most 1 BAD+GOOD per rule.
- Multiple examples of the same pattern: Keep 1 comprehensive example.
- Verbose explanations where the rule is self-documenting: Reduce to 1 sentence or drop.
- Prose paragraphs restating what structured content already says.
- Setup/install scripts: Keep commands, drop defensive coding and interactive menus.
- Troubleshooting sections: Keep non-obvious fixes only.
- Historical data (specific dates, test results, session findings).

Drop:
- Table of Contents sections.
- Section introductions that announce what follows.
- Completion checklists that restate earlier steps.
- Duplicate content that exists verbatim in another referenced file.
- Purely decorative elements (--- dividers between sections, empty sections).

Formatting rules:
- Preserve all markdown headers at their original level.
- Preserve all IDs, formats, and schemas exactly.
- Preserve all placeholder tokens ([WORKSPACE_FOLDER], etc.).
- Preserve frontmatter if present.
- Use single-line entries where multi-line adds no information.
- Do NOT add content not in the original.
- Do NOT change the meaning of any instruction.