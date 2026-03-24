---
name: coding-conventions
description: Coding style rules for Python and PowerShell. Apply when writing, editing, reviewing, or debugging code.
---

# Coding Conventions

All code MUST follow `MECT_CODING_RULES.md` (precision, brevity, consistency, naming, documentation). Read before writing or reviewing code.

## Files

- MECT_CODING_RULES.md - Code quality (MECT + APAPALAN for code)
- PYTHON-RULES.md - Python (formatting, imports, naming, comments)
- JSON-RULES.md - JSON (field naming, 2-space indent)
- WORKFLOW-RULES.md - Workflow documents (structure, token optimization)
- AGENT-SKILL-RULES.md - Agent skill development (structure, setup, token optimization)

## Logging Files (read when writing/reviewing logging/output code)

- LOGGING-RULES.md - General rules, philosophy, type overview (read first)
- LOGGING-RULES-APP-LEVEL.md - System/debug logging (LOG-AP rules)
- LOGGING-RULES-SCRIPT-LEVEL.md - Script output for QA/automation (LOG-SC rules)
- LOGGING-RULES-USER-FACING.md - End-user output via console/SSE (LOG-UF rules)

## Tools

reindent.py - Convert Python indentation: `python reindent.py folder/ --to 2 --recursive [--dry-run]` or `python reindent.py script.py --to 2`