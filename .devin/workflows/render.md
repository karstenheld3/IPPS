---
description: Render Markdown files to HTML and PDF
auto_execution_mode: 1
---

# Render Workflow

Turn one or more Markdown files into self-contained HTML and A4 PDF files using the renderings skill.

**Goal**: `.html` and `.pdf` artifacts in a `_EXPORT_gitignore` subfolder (or a user-chosen folder), readable without an editor, with working TOC links, page numbers, and bookmarks.

**Why**: Deliverables and review copies must open anywhere. Browser print dialogs and ad hoc viewers give inconsistent results; the skill gives one command with a shared visual language.

## Required Skills

- @skills:renderings for `render.py`, templates, options, troubleshooting

## MUST-NOT-FORGET

- Use the venv Python from `[SKILL_TOOLS_FOLDER]\llm-venv`; never system Python
- Choose the template before running: parallel language streams → `columns` with `--options` matching the marker lines; otherwise `document`
- Default output folder is `_EXPORT_gitignore` relative to the input's parent (session folder, workspace root, or the folder containing the inputs). Only use a different folder when the user explicitly provides `--output-dir` or names a target
- Never pass `--overwrite` on existing deliverables unless the user asked to replace them
- Report the artifact list (path, pages, size) back to the user
- Run `/verify` after workflow complete

## Prerequisites

- `render.py --list-templates` prints template names → proceed
- Exit code 2 mentioning `playwright install` → follow `SETUP.md` in the skill, then retry

# EXECUTION

## Steps

1. Resolve the inputs from the prompt: explicit files, a folder, or a glob. Determine the output folder: if the user specified `--output-dir` or named a target folder, use that; otherwise default to `_EXPORT_gitignore` under the input's parent directory (e.g. `[SESSION_FOLDER]/_EXPORT_gitignore/`, or `[WORKSPACE]/_EXPORT_gitignore/`, or `<input-folder>/_EXPORT_gitignore/`)
2. Inspect one input: if it contains marker lines that start language or version streams (headings like `### XX (Original)` or bold lines like `**XX (Original)**`), use `--template columns` and build `--options` per the skill's Procedure 2; otherwise use the default `document` template
3. Run `render.py` with `--output-dir <resolved folder>` and `--format both` unless the user asked for one format; add `--lang` for non-English documents, `--paper Letter` or `--landscape` when requested
4. Read the report: any `FAILED` line → fix the cause (encoding, missing browser, template option) and rerun only the failed inputs
5. Open one HTML in the browser preview and check one PDF page (page counter, header, tables) before reporting

## Stuck Detection

If 3 consecutive attempts fail:
1. Document in PROBLEMS.md
2. Ask user for guidance

# FINALIZATION

## Verification

Run `/verify` to check:
1. Every requested input has its `.html` and `.pdf` artifact
2. Report lines show page counts and no `FAILED`
3. Columns output: one card per section, one column per language, no empty columns where the source has content

## Output

- Artifacts in `_EXPORT_gitignore` (default) or the user-specified `--output-dir`
- Artifact list with paths, page counts, sizes in the chat response
