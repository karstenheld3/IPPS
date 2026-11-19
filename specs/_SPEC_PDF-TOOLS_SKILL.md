# SPEC: PDF Tools Skill

**Doc ID**: PDFTOOLS-SP01
**Feature**: pdf-tools-skill
**Goal**: Specify what the `pdf-tools` skill provides so that an agent processes PDFs with Poppler, QPDF, Ghostscript, 7-Zip, and the skill scripts through command lines that do not fail.
**Timeline**: Created 2026-11-19, Updated 1 time
**Target file(s)**:
- `PromptSystemV4.7/skills/pdf-tools/SKILL.md`
- `PromptSystemV4.7/skills/pdf-tools/GHOSTSCRIPT.md`
- `PromptSystemV4.7/skills/pdf-tools/POPPLER.md` (added by a parallel change set, see Document History)
- `PromptSystemV4.7/skills/pdf-tools/SETUP.md`
- `PromptSystemV4.7/skills/pdf-tools/convert-pdf-to-jpg.py`
- `PromptSystemV4.7/skills/pdf-tools/compress-pdf.py`
- `PromptSystemV4.7/skills/pdf-tools/downsize-pdf-images.py`
- `PromptSystemV4.7/skills/pdf-tools/_test/test-pdf-tools.py`

## MUST-NOT-FORGET

- PowerShell splits an unquoted argument that starts with `-` at the first `.` and leaves `$variables` inside it unexpanded: every example quotes such arguments or passes an argument array
- Every `powershell` fence in a guide that has an example test (`SKILL.md`, `GHOSTSCRIPT.md`, and `POPPLER.md` once its test exists) is executed by the test suite; a documented command line that fails fails the suite
- Exit codes do not prove success: QPDF exits 3 for success with warnings, Ghostscript exits 0 after `**** Error`; success means the output file exists and has the expected page count
- The tools live outside the repository in `[SKILL_TOOLS_FOLDER]`; the skill never installs or modifies them except through `SETUP.md`
- `[PROMPTSYSTEM_FOLDER]` is the source; `[AGENT_FOLDER]` holds a mirror of the skill folder

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [User Actions](#11-user-actions)
12. [UX Design](#12-ux-design)
13. [Logging Requirements](#13-logging-requirements)
14. [Technical Constraints](#14-technical-constraints)
15. [Document History](#15-document-history)

## 1. Scenario

**Problem:** An agent using the skill could not run Ghostscript: every call ended with "Device 'pdfwrite' requires an output file but no file was specified". The skill had no Ghostscript guide and none of its command examples was tested. Cause: PowerShell splits unquoted `-option=value` arguments at the first `.`, so `-dCompatibilityLevel=1.4` reached Ghostscript as an extra input file before `-sOutputFile=`.

**Solution:**
- One skill that covers the PDF command line tools Poppler (12 tools), QPDF (3 tools), Ghostscript, 7-Zip, and 3 scripts
- Examples written so that PowerShell passes every argument unchanged, with helpers that check the result
- A test suite that builds its own PDFs, tests every tool and script, and executes every documented example
- Known tool defects and exit code traps documented and guarded by tests

**What we don't want:**
- Long `gswin64c.exe` command lines typed inline in the agent terminal
- Documentation claims that no test or source backs
- Success judged by exit code alone
- Examples that need private files, network access, or a manual step
- Test suite files in `_agentwork/` (agent work is deleted by `/cleanup`) or outside version control
- A separate research document for Ghostscript: findings live in `GHOSTSCRIPT.md`

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Agent                                                                          │
│  reads SKILL.md and GHOSTSCRIPT.md, runs the examples in PowerShell             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Skill folder  [PROMPTSYSTEM_FOLDER]/skills/pdf-tools/ (mirror: [AGENT_FOLDER]) │
│  ├─> SKILL.md         tool guide, setup block, rules, exit codes, known defects │
│  ├─> GHOSTSCRIPT.md   Ghostscript guide, quoting rules, helper, recipes         │
│  ├─> SETUP.md         installation of the tools                                 │
│  ├─> 3 scripts        convert-pdf-to-jpg, compress-pdf, downsize-pdf-images     │
│  └─> _test/           test-pdf-tools.py  (kept, versioned)                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Tool folder  [SKILL_TOOLS_FOLDER]  (outside the repository)                    │
│  ├─> poppler/  12 PDF tools     ├─> qpdf/  qpdf, fix-qdf, zlib-flate            │
│  ├─> gs/       gswin64c.exe     ├─> 7z/    7z.exe                               │
│  └─> llm-venv/ Python           └─> _pdf_output/, _pdf_to_jpg_converted/        │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Test sandbox  [WORKSPACE_FOLDER]/_agentwork/.tmp_pdftools_test/  (agent work)  │
│  fixtures and one folder per test case, rebuilt on every run                    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Context

The skill belongs to the PromptSystem skill set (`[AGENT_FOLDER]/skills/`). Other parts use it: transcription (PDF pages to images), document processing, and any workflow that reads or shrinks PDFs. The agent runs on Windows in PowerShell (Cascade terminal tool) and calls the tools by relative path `../.tools/...` from `[WORKSPACE_FOLDER]`.

Terms: DPI (dots per inch), AES (Advanced Encryption Standard), RC4 (a weak legacy cipher), NSIS (Nullsoft Scriptable Install System, the format of the Ghostscript installer), QDF (QPDF's text-editable PDF form), PS and EPS (PostScript and Encapsulated PostScript), XMP (Extensible Metadata Platform), TSV (tab-separated values), FR, NFR, DD, IG, TC (requirement, non-functional requirement, design decision, implementation guarantee, test case IDs of the document system).

Related standards: the agent folder standard (`_test/` role, `_agentwork/` deletion, `.tmp_` rebuildable content), the terminal hang prevention rules (long commands run through the supervised runner, no `2>&1`), and the privacy gate (skill files hold generic values only).

## 3. Domain Objects

### Tool

A **Tool** is a command line program in `[SKILL_TOOLS_FOLDER]` that the skill documents.

- Poppler 24.08.0: `pdfinfo`, `pdftotext`, `pdftoppm`, `pdftocairo`, `pdftohtml`, `pdftops`, `pdfimages`, `pdffonts`, `pdfseparate`, `pdfunite`, `pdfattach`, `pdfdetach`
- QPDF 12.3.0: `qpdf`, `fix-qdf`, `zlib-flate`
- Ghostscript 10.06.0: `gswin64c` (console build)
- 7-Zip 24.08: `7z`
- Python (venv) with `pdf2image` and `Pillow` for `convert-pdf-to-jpg.py`

### Skill script

A **Skill script** is a Python program in the skill folder that wraps tools behind a stable interface.

- `convert-pdf-to-jpg.py` - PDF pages to JPG files for vision analysis (Poppler)
- `compress-pdf.py` - automatic compression with strategy escalation (Ghostscript, QPDF, Poppler analysis)
- `downsize-pdf-images.py` - fixed-DPI or preset image downsampling (Ghostscript)

### Guide document

A **Guide document** is a markdown file the agent reads: `SKILL.md` (entry point), tool family guides (`GHOSTSCRIPT.md`; `POPPLER.md`, added by a parallel change set), `SETUP.md` (installation). Guides with executable examples have one example test each; at the time of writing these are `SKILL.md` and `GHOSTSCRIPT.md`, and `POPPLER.md` names its test `test_doc_examples_poppler_md`, which the suite does not yet contain.

### Example block

An **Example block** is a fenced code block with language `powershell` in `SKILL.md` or `GHOSTSCRIPT.md`. A block whose first line is `# setup` is a prelude shared by all other blocks of the same file. Templates and syntax lines use language `text` and are not executed.

### Helper

A **Helper** is a PowerShell function defined in a setup block and used by examples.

- `Invoke-Gs` - runs Ghostscript with array arguments, throws on non-zero exit or on `**** Error` and `Unrecoverable` in the output
- `Invoke-Qpdf` - runs QPDF, accepts exit codes 0 and 3, throws otherwise
- `Get-PdfPages` - returns the page count from `pdfinfo`

### Fixture set

A **Fixture set** is the group of PDFs and files the suite builds before the tests.

- `input.pdf` - 3 pages Letter, 2 noisy 800 x 800 images, standard fonts, metadata (title, author, subject, keywords), one link, one named destination
- `input2.pdf` - pages 3 and 1 of `input.pdf`
- `encrypted.pdf` - AES-256, user password `userpw`, owner password `ownerpw`
- `damaged.pdf` - `input.pdf` with a wrong `startxref` offset
- `notes.txt` - small attachment text

### Test suite

The **Test suite** is `_test/test-pdf-tools.py`: standard library only, tests registered by decorator, one result line per test, exit code 1 when a test fails.

### Sandbox

The **Sandbox** is `[WORKSPACE_FOLDER]/_agentwork/.tmp_pdftools_test/` (override with `--work-dir`, name must start with `.tmp_`): fixtures plus one folder per test case. Agent work, deleted by `/cleanup`.

### Known behavior

A **Known behavior** is a tool quirk the skill documents and a test guards: when the tool changes, the test fails and the documentation must change.

## 4. Functional Requirements

**PDFTOOLS-FR-01: Tool inventory and locations**
- `SKILL.md` lists every tool of the Tool object with version and location relative to `[WORKSPACE_FOLDER]` (`../.tools/...`)
- A "Choose the tool" list maps each task (compress, render, text, facts, merge/split/encrypt/repair, embedded files, archives) to the tools that do it
- `SETUP.md` installs every listed tool and verifies it; its final step runs the test suite

**PDFTOOLS-FR-02: convert-pdf-to-jpg.py**
- Input: one PDF; options `--output <dir>`, `--dpi <n>` (default 120), `--pages <1|1-3|all>` (default all)
- Output: `[output]/[PDF_FILENAME]/[PDF_FILENAME]_page[NNN].jpg`, JPEG quality 90, one subfolder per PDF; default output `[SKILL_TOOLS_FOLDER]/_pdf_to_jpg_converted/`
- Exit 1 with an `ERROR` line for a missing file, an unreadable PDF, or a missing Poppler
- Works for file names with spaces and umlauts

**PDFTOOLS-FR-03: compress-pdf.py**
- Input: one PDF; options `--compression high|medium|low` (default medium), `--output <file.pdf>`
- Targets: high 50 percent reduction, medium 25 percent, low 10 percent; strategies escalate from the preset of the level to a more aggressive one; already optimized PDFs with low level start with structure-only optimization
- Prints an analysis (pages, size, images, optimized, JPEG2000, DPI, potential) before compressing, then one result line per attempt, then the final size and reduction
- Output: `--output` path (missing folders are created) or `[SKILL_TOOLS_FOLDER]/_pdf_output/[PDF_FILENAME]_compressed.pdf`; the result can be larger than the input for optimized PDFs
- Exit 1 for a missing input, a missing tool, or when every attempt fails; exit 2 for an invalid level

**PDFTOOLS-FR-04: downsize-pdf-images.py**
- Input: one PDF; options `--output <dir>`, `--dpi <n>` (default 150), `--preset screen|ebook|printer|prepress` (overrides `--dpi`)
- Presets: screen 72 DPI, ebook 150, printer 300, prepress 300; without preset the DPI selects the Ghostscript preset (up to 72 screen, up to 150 ebook, up to 300 printer, above prepress)
- Output: `[output]/[PDF_FILENAME]_[DPI]dpi.pdf`; prints original size, new size, and reduction
- Exit 1 for a missing input or a Ghostscript failure; exit 2 for an invalid preset

**PDFTOOLS-FR-05: Poppler coverage (in `SKILL.md` or in `POPPLER.md`)**
- Each of the 12 tools has a purpose line, a tested example, and its key options
- Documented behavior: output naming (`[prefix]-[page].[ext]`, zero padding to the width of the page count, `-singlefile`), stdout output with `-`, default resolutions (150 DPI for `pdftoppm` and `pdftocairo`, 72 for `pdftotext`), password options `-upw` and `-opw`
- Documented exit codes: 1 cannot open the PDF, 2 cannot write the output, 99 command line error; PDFs with owner-only restrictions open normally
- `pdfseparate` requires a page number pattern for multi-page input

**PDFTOOLS-FR-06: QPDF coverage in SKILL.md**
- Tested examples for: check and inspection, merge, page ranges (`1-3`, `3,1`, `z`, `r1`, `:odd`), rotate, split, encrypt (AES-256), decrypt, restricted encryption, repair, `--replace-input`, linearize, optimize, attachments, overlay, argument files, QDF editing with `fix-qdf`, `zlib-flate` through process redirection
- Documented exit codes: 0 success, 2 error (nothing written), 3 success with warnings; `--is-encrypted` exits 2 for a plain file
- Documented refusal of RC4 without `--allow-weak-crypto`

**PDFTOOLS-FR-07: Ghostscript guide**
- `GHOSTSCRIPT.md` holds: the root cause of the "requires an output file" error, the quoting rules, a setup block with `Invoke-Gs`, three safe calling methods (quoted tokens, argument array, argument file), recipes, quirks and messages, and sources with verification labels
- Recipes: size reduction by preset, reaching a size limit, explicit DPI and strategy flags, grayscale, page ranges and merge and A4 fit, rendering to PNG and JPEG, text extraction, title and author, passwords, font embedding, removing images or text
- `SKILL.md` carries a MUST-NOT-FORGET hint to read the guide first, a Ghostscript section with a minimal safe call, and the preset list

**PDFTOOLS-FR-08: 7-Zip coverage in SKILL.md**
- Tested examples for add, list, test, extract with paths, extract flat, password archives (AES-256), hash
- Notes: `-y` and `-bd` always, quote every `-o`, `-p`, `-m`, `-sc` argument; 7z extracts the NSIS installer of Ghostscript, `7za.exe` does not

**PDFTOOLS-FR-09: PowerShell argument safety**
- Every example passes arguments that start with `-` and contain `=` as quoted strings or inside an argument array
- No example uses `2>&1`; error output goes to a file
- `@file` argument files are quoted (`'@args.txt'`)
- `SKILL.md` states the rule in MUST-NOT-FORGET with the observable symptoms

**PDFTOOLS-FR-10: Result verification**
- After each tool call the examples check the output: file exists, page count via `Get-PdfPages` or `pdfinfo`, or size comparison
- `SKILL.md` and `GHOSTSCRIPT.md` state which tools return success exit codes after errors and how to detect the error

**PDFTOOLS-FR-11: Executable examples**
- Each `powershell` block runs in a fresh folder holding the fixture set, after the prelude of its file, with PowerShell errors and non-zero exit codes of native commands treated as failure
- Relative tool paths in examples resolve to the real tool folder when run by the suite
- Blocks that are templates use language `text`

**PDFTOOLS-FR-12: Known behavior and defects**
- Documented and guarded by tests: `pdfdetach -savefile` fails with exit 99; qpdf refuses RC4; qpdf repair gives exit 3; Ghostscript exit 0 with empty output on a password error; Ghostscript default paper is Letter; base-14 fonts stay unembedded without `/NeverEmbed [ ]`; pdfmark `DOCINFO` must follow the input file; Poppler warns about unembedded fonts
- When a guarded behavior changes after a tool update, the test fails with a message naming the document to update

**PDFTOOLS-FR-13: Test suite**
- Builds its fixtures from an embedded PostScript source with Ghostscript and derives the other fixtures with QPDF; no stored binary fixtures
- Runs in a sandbox; the sandbox folder is deleted at the start only when its name starts with `.tmp_`
- Options: `--filter` (names containing any text), `--keep` (keep case folders), `--verbose` (full failure output), `--work-dir`
- Prints `PASS`, `FAIL`, or `SKIP` per test with duration, a summary line, and the failed names; exit code 1 when a test failed; case folders of passing tests are deleted, those of failing tests stay
- Needs no network and installs nothing

**PDFTOOLS-FR-14: Test coverage**
- At least one test per tool and per script, per documented option group, and per documented error behavior; the coverage list is in `_TEST_PDFTOOLS.md [PDFTOOLS-TP01]`
- A self-test proves that the example runner reports a failing script and a failing native command, and that `Invoke-Gs` throws on a missing password

**PDFTOOLS-FR-15: Special path characters**
- Tools and scripts handle spaces, umlauts, `!`, parentheses, `;`, `&`, `,`, `'`, `#` in file and folder names when the name is one argument
- A `%` in a Ghostscript output name is written `%%`

**PDFTOOLS-FR-16: Folder standard**
- `SKILL.md` lists its agent-created folders (`.tmp_jpgs/`, `_download_gitignore/compressed/`, `_test/`, `_agentwork/.tmp_pdftools_test/`) with role, parent, creator, content
- The test suite lives in `_test/` of the skill folder: kept, versioned, mirrored; its sandbox is agent work

## 5. Non-Functional Requirements

**PDFTOOLS-NFR-01: Performance - suite runtime**
- The full suite finishes within 3 minutes on the development machine (measured 75 s for 53 tests)
- Verification: runtime line in the summary; a run above 3 times the measured value is analyzed, not repeated

**PDFTOOLS-NFR-02: Reliability - determinism**
- Fixtures are generated from one embedded source; no test depends on the current date, the network, or a file outside the sandbox and the tool folder
- Verification: two consecutive full runs give the same PASS count

**PDFTOOLS-NFR-03: Safety - side effects**
- The suite writes only into the sandbox; the sandbox is deleted only when its folder name starts with `.tmp_`
- Examples write only into the current folder; the scripts write into their `--output` target; no test touches `[SKILL_TOOLS_FOLDER]/_pdf_output/` or `_pdf_to_jpg_converted/`
- Verification: after a run the workspace root and the tool folder hold no new files

**PDFTOOLS-NFR-04: Localization - encoding**
- All files are UTF-8; tests include file names with umlauts and special characters
- Verification: `test_ghostscript_special_characters_in_paths`, the script tests with umlaut names

**PDFTOOLS-NFR-05: Portability - platform**
- Target: Windows, PowerShell 7.3 or newer (examples rely on native argument passing; the suite sets the native error preference), tested with PowerShell 7.5.0
- Windows PowerShell 5.1 is not covered by the example runner

**PDFTOOLS-NFR-06: Observability - suite output**
- A failing test prints its first 700 characters of detail (all with `--verbose`) and keeps its case folder for inspection
- Verification: a forced failure shows the message and the kept folder

**PDFTOOLS-NFR-07: Maintainability - structure**
- One test file, test names `test_[tool]_[aspect]`, one guide per tool family, no duplicate statements between `SKILL.md` and `GHOSTSCRIPT.md` beyond the minimal safe call and the preset list

## 6. Design Decisions

**PDFTOOLS-DD-01:** Quote every `-option=value` argument or pass an argument array. Rationale: PowerShell issue 6291 splits unquoted tokens at `.`; quoting is the documented workaround; tested with PowerShell 7.5.0.

**PDFTOOLS-DD-02:** Provide helpers instead of repeating checks in every example (`Invoke-Gs`, `Invoke-Qpdf`, `Get-PdfPages`). Rationale: one place enforces output checking, exit code policy, and no `2>&1`.

**PDFTOOLS-DD-03:** Execute every documented example in the suite. Rationale: the user requirement is that the agent never meets an error with a documented command line; only execution proves it.

**PDFTOOLS-DD-04:** Generate fixtures at run time from PostScript, Ghostscript, and QPDF. Rationale: no binary files in version control, no private data, reproducible on every machine.

**PDFTOOLS-DD-05:** Keep the suite in `_test/` of the skill folder. Rationale: it is versioned, mirrored with the skill, found next to what it tests, and not deleted by `/cleanup`; `_agentwork/` content is deleted. The sandbox stays agent work.

**PDFTOOLS-DD-06:** Standard library only in the suite; it calls the tools through argument lists. Rationale: no install step, and Python argument lists avoid shell quoting in the tests that are not about quoting.

**PDFTOOLS-DD-07:** Known behaviors are guarded by tests that fail when the behavior changes. Rationale: documentation of tool quirks goes stale silently after a tool update.

**PDFTOOLS-DD-08:** Ghostscript gets its own guide file; `SKILL.md` keeps a hint and a minimal call. Rationale: user request; the Ghostscript material is large and error-prone.

**PDFTOOLS-DD-09:** Research findings go into `GHOSTSCRIPT.md` with verification labels and sources, not into a separate INFO file. Rationale: user request for no extra file.

**PDFTOOLS-DD-10:** The skill scripts keep Python argument lists and are not rewritten. Rationale: they are immune to the PowerShell problem and pass their tests unchanged.

**PDFTOOLS-DD-11:** Scope of deployment: the skill folder is mirrored to `[AGENT_FOLDER]` on its own. Rationale: a full mirror also copies unrelated pending changes.

## 7. Implementation Guarantees

**PDFTOOLS-IG-01:** Every behavior claim in `SKILL.md` and `GHOSTSCRIPT.md` is backed by a test, a documentation source, or both, and carries a label where it is a finding.

**PDFTOOLS-IG-02:** A run of the full suite leaves no file outside the sandbox.

**PDFTOOLS-IG-03:** The suite exit code is 1 if and only if at least one test failed.

**PDFTOOLS-IG-04:** After a successful run from the source folder and from the mirror, the skill folder and its mirror are byte-identical.

**PDFTOOLS-IG-05:** No example needs a file that the fixture set does not provide.

## 8. Key Mechanisms

- **Argument safety**: examples pass tool arguments as strings in arrays or as quoted tokens, so PowerShell never parses `-name=value` as a parameter; Ghostscript options always precede the input file
- **Result check**: helpers combine exit code, error text scan, and output verification; the guides state which tools need which check
- **Example runner**: the suite reads the fenced blocks of a guide, builds one script per block (strict error settings, native non-zero exit is an error, prelude first, relative tool path replaced), runs it in a fresh copy of the fixture set, and fails the guide test with the block position and output tail
- **Fixture pipeline**: embedded PostScript, rendered by Ghostscript to `input.pdf`; QPDF derives `input2.pdf`, `encrypted.pdf`; a byte edit derives `damaged.pdf`
- **Known-behavior guard**: tests assert the quirk itself (for example exit 99 of `pdfdetach -savefile`); a fixed quirk fails the test and names the document to update
- **Sandbox lifecycle**: delete if the name starts with `.tmp_`, build fixtures, run, delete passing case folders, keep failing ones

## 9. Action Flow

Suite run:

```
python _test/test-pdf-tools.py [--filter ...]
├─> resolve skill, workspace, and tool folders from the file location
├─> delete and recreate the sandbox (only a .tmp_ folder name)
├─> build fixtures: input.pdf, input2.pdf, encrypted.pdf, damaged.pdf, notes.txt
│   └─> on error: print "FIXTURES FAILED" and the traceback, exit 1
├─> for each selected test, in definition order
│   ├─> create a case folder with a copy of the fixtures
│   ├─> run tool calls through argument lists
│   ├─> check output files, sizes, page counts, text, exit codes
│   └─> print PASS, FAIL, or SKIP; delete the case folder when PASS
└─> print summary and failed names, exit 1 if any FAIL
```

Example block test:

```
test_doc_examples_[guide]
├─> extract powershell fences, collect '# setup' blocks as prelude
└─> for each other block
    ├─> case folder with fixtures
    ├─> script = strict settings + prelude + block, tool paths resolved
    ├─> run with pwsh -File equivalent
    └─> exit code 0 and no PowerShell error text -> pass; else record position and output tail
```

Agent use of the skill:

```
Agent needs a PDF operation
├─> SKILL.md: Choose the tool, MUST-NOT-FORGET
├─> Ghostscript involved: GHOSTSCRIPT.md, paste setup block, call Invoke-Gs
├─> run the example adapted to real file names, quoted arguments only
└─> verify: output exists, Get-PdfPages, size, no error text
```

## 10. Data Structures

Fixture inventory:

```
input.pdf      3 pages, Letter, 2 images 800 x 800, fonts Helvetica and Courier, link, named destination ChapterTwo
input2.pdf     2 pages: page 3 and page 1 of input.pdf
encrypted.pdf  AES-256, user password userpw, owner password ownerpw, 3 pages
damaged.pdf    3 pages recoverable, wrong startxref offset, qpdf exits 3 on repair
notes.txt      one line of text
```

Suite output lines:

```
Sandbox: E:\dev\IPPS\_agentwork\.tmp_pdftools_test
PASS test_qpdf_encrypt_and_decrypt (0.4s)
FAIL test_poppler_exit_codes (1.0s)
     [first 700 characters of the failure detail]
SKIP test_sevenzip_extracts_nsis_installer_like_setup_md (0.0s)
     installer not present: [SKILL_TOOLS_FOLDER]/_installer/gs10060w64.exe

SUMMARY: 52 PASS, 1 FAIL, 1 SKIP in 75s
FAILED: test_poppler_exit_codes
```

## 11. User Actions

N/A: command line skill without a user interface.

## 12. UX Design

N/A: command line skill without a user interface. The architecture diagram in section 1 and the flows in section 9 describe the structure.

## 13. Logging Requirements

**Applicable logging types:**
- [x] User-Facing (UF) - the three skill scripts print progress to the console
- [ ] App-Level (AP) - no server
- [x] Script-Level (SC) - the test suite is a verification script

**User-Facing logging (scripts):**
- **Audience**: the agent or user running a script
- **Goal**: know what is processed, with which settings, and what the result is
- **Key operations**: analysis (compress), each attempt (compress), each page file (convert), size before and after (compress, downsize)

**Expected output for convert-pdf-to-jpg.py:**
```
Converting 'input.pdf' pages 1-2 at 60 DPI...
  OK: input_page001.jpg
  OK: input_page002.jpg
Done. 2 file(s) created in 'jpgs'
```

**Expected output for compress-pdf.py (shape):**
```
Analyzing PDF...
  Pages: 3
  Size: 0.03 MB
  ...
Attempt 1: Aggressive (72 DPI)...
  Result: 0.02 MB (31.2% reduction)
Done: 'compressed/input-high.pdf'.
  Original: 0.03 MB
  Final: 0.02 MB
  Reduction: 31.2%
  Strategy: Aggressive (72 DPI)
```

**Script-Level logging (suite):**
- **Audience**: maintainer or agent verifying the skill
- **Goal**: all failure information in the output alone: which test, which expectation, the tool output
- **Key operations**: fixture build, each test, summary
- Output shape: see section 10

## 14. Technical Constraints

- PowerShell splits an unquoted argument that starts with `-` at the first `.` (PowerShell issue 6291, open since 2018) [VERIFIED]; with 7.5.0 it also leaves `$variables` inside such an argument unexpanded [TESTED]
- Ghostscript processes arguments left to right; an option applies to the files named after it; a positional argument opens the output device [VERIFIED in `Use.rst`]
- Ghostscript uses US Letter unless `-sPAPERSIZE` or `-dDEVICEWIDTHPOINTS` and `-dDEVICEHEIGHTPOINTS` say otherwise [VERIFIED]
- Ghostscript exits 0 after errors such as a missing password and writes an empty output [TESTED with 10.06.0]
- QPDF exits 3 when it succeeded with warnings; a damaged input always gives 3 [TESTED with 12.3.0]
- QPDF 12 refuses RC4 encryption without `--allow-weak-crypto` [TESTED]
- `pdfdetach -savefile` fails with exit 99 in the Poppler 24.08.0 Windows build [TESTED]
- Poppler prints font warnings to stderr for PDFs with unembedded standard fonts [TESTED]
- `convert-pdf-to-jpg.py` needs the Python modules `pdf2image` and `Pillow`; the suite uses the interpreter that runs it
- The tool folder is shared by workspaces and lies outside the repository; tests must not change it
- Tool binaries are Windows x64; the skill does not support other platforms

## 15. Document History

**[2026-11-19 09:35]**
- Changed: guide references independent of the parallel `POPPLER.md` change set (FR-05, Guide document, MUST-NOT-FORGET); added Terms
- Open: when the parallel change set is finished, update FR-01 (tool inventory location), FR-05 (Poppler coverage moved to `POPPLER.md`), and add the example test for `POPPLER.md` to `_TEST_PDFTOOLS.md` (proposed TC-56)

**[2026-11-19 09:20]**
- Initial specification created

**[2026-11-19 09:10]**
- Moved: from `_PrivateSessions_gitignore/_2026-11-19_PdfToolsSkill/_SPEC_PDFTOOLS.md` to `specs/_SPEC_PDF-TOOLS_SKILL.md`
