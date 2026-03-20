Compress this DevSystem skill document while preserving ALL technical capability information.

Primary (keep as-is): MUST-NOT-FORGET lists, tool action/parameter lists, architecture descriptions, capability boundaries (when to use / when NOT to use), command syntax with all parameters, API/CLI reference tables, configuration snippets, intent lookup tables, safety warnings.

Secondary (compress):
- Multiple usage examples showing the same command with different parameters: Keep 1 comprehensive example per command, drop variations.
- Setup/installation scripts with verbose state-checking logic: Keep the essential commands (download, extract, configure), drop defensive coding (null checks, backup logic, interactive menus, colored output).
- Uninstall scripts: Compress to command list with 1-line descriptions. Drop interactive menu PowerShell logic entirely.
- Troubleshooting sections with obvious fixes: Keep non-obvious fixes, drop "restart the application" type advice.
- Section introductions that restate the heading.
- "Common Patterns" sections that reassemble earlier individual commands.
- Historical test results or session-specific findings (dates, worker counts, specific model scores).
- Completion checklists that restate the setup steps.

Drop:
- Table of Contents sections.
- "Sources" sections listing GitHub URLs (keep only if URL is needed for installation).
- Case study narratives (Section 7 in AGENT-SKILL-RULES.md) - reduce to bullet-point lessons.
- Token optimization advice that duplicates WORKFLOW-RULES.md.
- Full PowerShell interactive menu scripts in UNINSTALL files - replace with flat command list.

Formatting rules:
- Preserve all command syntax exactly (flags, parameters, paths).
- Preserve all MUST-NOT-FORGET items verbatim.
- Preserve all "when to use / when NOT to use" boundaries.
- Preserve all configuration JSON/YAML blocks.
- Preserve all @skills: and /workflow references.
- Preserve all warning/safety notes (NEVER, CRITICAL, WARNING).
- Preserve skill frontmatter (name, description) exactly.
- Keep 1 example per distinct operation type.
- Do NOT add content not in the original.