---
name: renderings
description: Apply when rendering Markdown files to HTML or PDF, including multilingual documents with parallel language columns. Provides render.py and HTML templates that render Markdown in the browser and print via headless Chromium.
compatibility: Python venv at [SKILL_TOOLS_FOLDER]/llm-venv with playwright installed. Chromium via `python -m playwright install chromium-headless-shell` (see SETUP.md).
---

# Renderings Skill

Two-step renderer: `render.py` injects Markdown into an HTML template that carries its own CSS and JavaScript Markdown renderer (step 1, Markdown → HTML), then prints that HTML with headless Chromium (step 2, HTML → PDF). Everything about layout lives in the template; Python only injects and prints.

**References** (loaded on demand):
- [SETUP.md](SETUP.md) - venv check, browser install, verification
- [templates/document.html](templates/document.html) - single reading column
- [templates/columns.html](templates/columns.html) - parallel streams (languages, versions) as aligned columns per section
- [templates/shared/tokens.css](templates/shared/tokens.css) - palette, fonts, type scale, base element rules
- [templates/shared/render-common.js](templates/shared/render-common.js) - shared template helpers (front matter, anchors, task lists, code classes, page header, done signal)

## MUST-NOT-FORGET

1. Run with the venv Python: `& "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\python.exe" [AGENT_FOLDER]\skills\renderings\render.py ...`
2. Pick the template first: documents with parallel language streams (`### DE (Original)` style markers) → `columns` with `--options`; everything else → `document`
3. Output goes next to the input unless `--output-dir` is given; existing files are skipped unless `--overwrite`
4. Relative image paths break when `--output-dir` differs from the input folder (a warning is printed)
5. Templates must set `body[data-rendered="true"]` when done; `render.py` waits for it before printing. A template that never sets it fails after `--render-timeout` seconds
6. Output HTML is self-contained (no external scripts, fonts, or styles); do not add CDN links to templates

## Intent Lookup

**User wants to...**
- **Render one or more Markdown files to HTML and PDF** → Procedure 1
- **Render a whole folder** → Procedure 1 with a folder or glob input, `--recursive` for subfolders
- **Render a multilingual document side by side** → Procedure 2
- **Only HTML, or only PDF** → `--format html` or `--format pdf` (`--keep-html` keeps the intermediate file)
- **Letter paper or landscape** → `--paper Letter`, `--landscape`
- **Wide tables print too small or wrap too much** → `--options "landscapeTables=7"` (tables with 7+ columns get their own landscape page) or `--options "tableFont=condensed"` (see Template Catalog)
- **Create a new layout** → Procedure 3

## Core Procedures

### 1. Render documents

```
1. Resolve inputs: files, folders (*.md), or globs
2. Run: python render.py <inputs> --output-dir <folder>            (template 'document', HTML and PDF)
3. Read the report lines: html size | pdf pages size | seconds; DONE line with ok/failed/skipped counts
4. Exit code 0 = all ok or skipped, 1 = some inputs failed (others rendered), 2 = setup or argument error
```

### 2. Render parallel language columns

```
1. Identify the marker line that starts each language stream in the source, e.g. `### DE (Original)`, `### EN (Translation)`, `### PT (Tradução)`
2. Run with the columns template and matching options:
   python render.py file.md --template columns --options "columns=DE:DE,EN:EN,PT:PT; markers=^###\s*DE\s*\(Original\),^###\s*EN\s*\(Translation\),^###\s*PT\s*\(Tradu; scope=document; sectionLevels=1-4; wideColumns=4"
3. For documents organized as dated entries whose language blocks start with bold markers (`**DE (Original)**`), use scope=entry:
   --options "columns=DE:DE,EN:EN,PT:PT; markers=^\*\*DE \(Original\)\*\*,^\*\*EN \(Translation\)\*\*,^\*\*PT \(Tradu; scope=entry; entryLevel=2; sectionLevels=3-4"
4. Check the first PDF page: one card per section, one column per language, wide tables stacked
```

Options (`;`-separated `key=value` pairs, override the template's `<meta name="render-options">`):
- `columns` - ordered `key:Label` pairs; one column per pair; roles by position: first ink, second accent, others muted
- `markers` - one regular expression per column matching the line that starts that stream (commas separate patterns; avoid commas inside patterns)
- `scope` - `document` (markers appear once) or `entry` (entries delimited by `entryLevel` headings, markers inside each entry)
- `entryLevel` - heading level that delimits entries (default 2)
- `sectionLevels` - heading levels that split each stream into sections, `low-high` (default `1-4`); section i of every stream forms one card
- `wideColumns` - tables with at least this many columns make their card stack the languages vertically (default 4)

Options of the `document` template (same `--options` syntax):
- `tableFont` - `default` or `condensed`; `condensed` renders tables in the condensed font stack (`Arial Narrow`, `Roboto Condensed`, `Bahnschrift SemiCondensed`, falling back to the sans stack when none is installed)
- `landscapeTables` - `0` (off, default) or N; tables with N or more columns print on their own A4 landscape page

### 3. Write a new template

```
1. Copy templates/document.html to templates/<name>.html
2. Keep the placeholders: {{TITLE}}, {{LANG}}, {{MARKDOWN}} and the includes {{FILE:shared/tokens.css}}, {{FILE:shared/markdown-it.min.js}}, {{FILE:shared/render-common.js}}
3. Keep the render script's last call finishRendering() - it sets data-rendered after fonts are ready
4. Put layout in the template's own <style>: @page size and margins, margin boxes for header/footer, column CSS
5. Test: python render.py sample.md --template templates/<name>.html --output-dir out --overwrite
```

Placeholder contract:
- `{{MARKDOWN}}` - replaced by a JSON string literal of the Markdown (with `<` escaped), read via `JSON.parse(document.getElementById("source").textContent)`
- `{{TITLE}}` - HTML-escaped document title (first `# ` heading, front matter `title:`, or file stem; `--title` overrides for a single input)
- `{{LANG}}` - `--lang` value (default `en`)
- `{{FILE:relative/path}}` - inlined file content from the templates folder (one level, no recursion, no `..`)
- `--paper` / `--landscape` inject a final `@page { size: ... }` rule before `</head>`

## CLI Reference

```
render.py <inputs...> [--format html|pdf|both] [--template NAME|PATH] [--options TEXT] [--output-dir DIR]
          [--paper A4|Letter] [--landscape] [--lang xx] [--title TEXT] [--render-timeout S]
          [--keep-html] [--overwrite] [--recursive] [--quiet] [--list-templates]
```

- `inputs` - files, folders (`*.md` inside), or glob patterns; dotfiles skipped; duplicates removed
- `--format` - default `both`; `pdf` alone writes a temporary HTML that is removed after a successful print unless `--keep-html`
- `--template` - `document` (default) or `columns`, or a path to any template file
- `--render-timeout` - seconds to wait for `data-rendered` (default 30)
- `--list-templates` - prints available template names and exits

## Template Catalog

- **document** - single column, A4 portrait, margins 20/18/22/18 mm, static title header on pages 2+, "Page N of M" footer, GitHub-compatible heading ids (TOC links work), task lists, code blocks unwrapped up to 110 characters per line then soft-wrapped, language label on fenced code, code line box measured from the monospace font so box-drawing diagrams have no row gaps, headings wrap anywhere (long file-name titles stay inside the page)
  - Tables: full width, repeated header rows, words break only when a single word is wider than its column; tables with 6+ columns start one size smaller; a table wider than the page steps its font down (13 / 12 / 11 px, 8.5 / 8 / 7.5 pt) until it fits; a table that still does not fit gets a horizontal scrollbar on screen, is clipped in PDF, and is reported as `WARNING: N tables wider than the page ...` on the file's report line. Opt-ins: `tableFont=condensed`, `landscapeTables=N`
  - Color: accent only on links; list markers and checkboxes use the text color
- **columns** - one card per section with N language columns, combined section title colored per column, block and table-row height alignment across columns, wide-table cards stacked vertically in print, landscape when more than 3 columns, single-column fallback with a notice when no marker matches

Both templates: no external resources, `-webkit-print-color-adjust: exact`, PDF bookmarks from headings (`outline=True`), tagged PDF.

## Gotchas

- **Browser revision mismatch** - Playwright Python pins one Chromium build; a build installed by another tool (Node Playwright MCP) has a different revision. `render.py` falls back to the newest installed `chromium-*` build, then to system Chrome, then exits 2 with the install command. Run the SETUP.md install once to remove the fallback
- **Running section titles** - Chromium does not support CSS `string-set`; the page header shows the document title, not the current section
- **Variable fonts** - Chromium embeds variable fonts (e.g. Cascadia) as Type3 outlines in PDF; the code font stack starts with static Consolas, JetBrains Mono, DejaVu Sans Mono for clean embedding
- **Markers inside code fences** are ignored by the columns template; markers must be plain lines
- **Commas in marker regexes** are not possible (comma separates patterns); use `\s` or character classes instead
- **`<PromptSystem .../>` lines** are removed before rendering; other raw HTML passes through unchanged
- **Single newlines** render as line breaks (`breaks: true`) so header blocks keep their lines; hard-wrapped paragraphs therefore also break per source line
- **No hyphenation** - the Playwright Chromium build ships without hyphenation dictionaries; `hyphens: auto` would have no effect, so table fitting relies on font size, not on breaking words
- **Braille art** - Consolas has no Braille glyphs; they fall back to the next monospace font with a different advance width and drift against box-drawing characters in the same block
- **Screen screenshots show colored fringes** on thin box-drawing lines (Windows ClearType sub-pixel rendering); the PDF has none

## Vendored Library

- `templates/shared/markdown-it.min.js` - markdown-it 14.1.0, MIT license (`templates/shared/markdown-it.LICENSE.txt`). Update by replacing the file with a newer `dist/markdown-it.min.js` and adjusting this line

## Quick Config

```powershell
$py = "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\python.exe"
$render = "[AGENT_FOLDER]\skills\renderings\render.py"
& $py $render "docs\*.md" --output-dir "docs\rendered" --overwrite
& $py $render "report_DE-EN-PT.md" --template columns --options "columns=DE:DE,EN:EN,PT:PT; markers=^###\s*DE,^###\s*EN,^###\s*PT" --lang de
```
