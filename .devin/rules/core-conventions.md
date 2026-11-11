---
trigger: always_on
---

# Core Conventions

Universal formatting and writing conventions for all documents.

## Text Style (Exception: transcribed or external documents)

- Use ASCII "double quotes" or 'single quotes'. Never use Non-ASCII quotes unless explicitly asked.
- Expect international readers who are not native speakers. Write the explicit claim, not a figurative stand-in: rewrite idioms, slang, and region-dependent phrases as the claim they carry; keep established precise terms (MECT-WC-10 in @skills:write-documents `MECT_WRITING_RULES.md`)
- No emojis in documentation (see Document Rule Exceptions below)
- Avoid Markdown tables; use unnumbered lists with indented properties (see Document Rule Exceptions below)
- Use Unicode box-drawing characters for structures:
  - Trees and flows: `├─>` `└─>` `│` (2-space indentation compatible)
  - Boxes and diagrams (non-UI): `┌─` `├─` `└─` `│` `─` `┐` `┤` `┘`
  - UI mockups: Same Unicode characters (SPEC-DG-06), not ASCII `+` `-` `|`
- Arrow symbol `→` must have spaces around it: `A → B` not `A→B`
- Never use `▼` (U+25BC); use `v` instead
- Try to fit single statements/decisions/objects on a single line
- Format workflow references as inline code: `/verify`, `/go`, `/implement`
- Inline enumerations use `N)` format, not `(N)`: `1) first, 2) second, 3) third`
- URLs must always include the scheme (`https://` or `http://`). Never write bare domains: `msn.com` → `https://msn.com`

## Encoding

- Always assume UTF-8 encoding.
- When writing in non-English languages, use native special characters (e.g., German Umlaute: ae → ä, oe → ö, ue → ü, ss → ß). Never substitute with ASCII approximations.
- When non-UTF-8 encoding is detected, document in workspace or session NOTES.md: 1) file path, 2) detected encoding (e.g., ISO-8859-1, Windows-1252), 3) how to preserve the encoding (e.g., which PowerShell `[System.IO.File]::` encoding parameters). Test the PowerShell snippet on a copy of the file before recording 3)

## Authoritative Literals

Some values are **lexical, not semantic** - every character matters. Addresses, IBANs, reference numbers, registration codes, and official names must be reproduced exactly as recorded. GenAI systematically introduces format drift on these values.

- Values marked `[LITERAL]` MUST be copied character-for-character: no Unicode substitution (`o` stays `o`, not `º`; comma stays comma, not dash), no abbreviation or expansion, no reformatting of punctuation, spacing, or casing
- Source of truth for new literals: official documents (government registrations, contracts, bank confirmations) - never secondary documents. Outbound communication (emails, letters, forms) copies from the `[LITERAL]`-marked source
- Corruption categories with BAD/GOOD examples: @skills:write-documents `APAPALAN_RULES.md` APAPL-PR-13

**Marking format** - tag values in-place where they are already defined (no separate section, no duplication); optional source after colon:
```
- **Street**: Rua da Liberdade, 42, 3.o Esq. [LITERAL: registration certificate 2026-01-15]
- **IBAN**: DE89370400440532013000 [LITERAL]
- **Tax ID**: 123456789 (obtained 2026-03-10) [LITERAL]
```

## Date and Time Format

- **In documents**: `YYYY-MM-DD HH:MM` - `2026-03-19 14:30`
- **In logging**: `YYYY-MM-DD HH:MM:SS` - `2026-03-19 14:30:23`
- **In filenames**: `YYYY-MM-DD` prefix - `2026-03-19_ServerMigration.md`, `2026-03-19_14-30_MeetingNotes.md`
- **In temp file names**: `_HHmmss` suffix - `.tmp_fix_quotes_143022.ps1`
- **In session folders**: `YYYY-MM-DD` prefix - `_2026-03-19_FixAuthBug/`
- **In Document History**: `[YYYY-MM-DD HH:MM]` - `**[2026-03-19 14:30]**`
- **For months**: `YYYY-MM` - `2026-03`

Never use locale-dependent formats (`03/19/2026`, `19.03.2026`, `March 19, 2026`).

## Document Structure

- Place Table of Contents after header block (or after MUST-NOT-FORGET if present)
- No `---` markers between sections
- One empty line between sections
- Most recent changes at top in changelog sections

## Header Block

All documents start with (exceptions below):

```
# [Document Type]: [Title]

**Doc ID**: [TOPIC]-[TYPE][NN]
**Goal**: Single sentence describing purpose
**Target file**: `/path/to/file.py` (or list for multiple)

**Depends on:**
- `_SPEC_[X].md [TOPIC-SP01]` for [what it provides]

**Does not depend on:**
- `_SPEC_[Y].md [TOPIC-SP02]` (explicitly exclude if might seem related)
```

- Doc ID is required for all documents except the exceptions below. Optional fields, omit if not applicable: Target file, Depends on, Does not depend on
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`

**Exceptions** (no Header Block):
1. Publishing documents (articles, reports, ebooks, blog posts, whitepapers) - the reader sees only title and content; no Header Block, no Doc ID
2. Prompts, workflows, skills - use the header and sections defined in their templates and rules (`PROMPTS_RULES.md`, `WORKFLOW_RULES.md`, `SKILL_RULES.md`)

## Document History Section

Always at document end, reverse chronological order:

```
## Document History

**[2026-01-12 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Fixed: Modal OK button signature

**[2026-01-12 10:00]**
- Initial specification created
```

**Action prefixes:** Added, Changed, Fixed, Removed, Moved

**Exception:** LLM-consumed instruction files (rules, workflows, skills, standalone prompts) have no history section - see WF-CT-07 and SK-CT-06.

## Document Rule Exceptions

Documents may opt-in to use Markdown tables or emojis by adding a PromptSystem tag as the **first line** of the document (before the title):

```html
<PromptSystem MarkdownTablesAllowed=true EmojisAllowed=true APAPALAN=true MECT=true />
```

- `MarkdownTablesAllowed=true`, `EmojisAllowed=true` - allow Markdown tables / emojis in this document. Use for comparison documents, feature matrices, compatibility charts, status dashboards
- `APAPALAN=true`, `MECT=true` - APAPALAN / MECT rules apply. Defined in `@skills:write-documents` and `@skills:coding-conventions`

**Table formatting rule:** When tables are allowed, align columns with spaces for human readability. No bold, italic, or other formatting inside table cells.
- GOOD: `| Model      | Workers | TPM   |` above `|------------|---------|-------|`
- BAD: `|Model|Workers|TPM|` (no spacing), `| **Model** | Workers |` (bold in cells)

**Allowed emojis (when enabled):** ✅ (yes, supported, pass, enabled), ❌ (no, unsupported, fail, disabled), ⚠️ (warning, partial, caution), ★ ☆ ⯪ (filled, outlined, half-filled rating star)

**Usage pattern:** Emoji first, then textual equivalent: `- **MCP** - ✅ Yes`, `- **Hooks** - ❌ No`, `- **Data** - ⚠️ Partial (read-only)`, `- **Docs** - ★★★★⯪ (4.5)`

**Tables ALWAYS allowed, no opt-in tag needed:** documents whose primary purpose is to be read as prose (not reference/lookup) - Minto Pyramid articles (output of `/write-article` or `/propose-article` using MINTO), blog posts, essays, whitepapers, publication-ready reports.

## Presenting Decisions

When [ACTOR] must choose between options (design decisions, open questions, a/b/c problem resolutions), present every decision in this format. Bare option labels ("Outcome A", "option c", "confirm or override") without this structure count as a failed presentation.

```text
# [Decision ID]: [Question as a plain sentence]

**Problem**: What is wrong or undecided today, observable by the user
**Context**: Why the problem exists - the constraint, spec clause, or prior finding that created it
**Review**: Clickable links to the files and sections the user needs to decide, e.g. `path/to/file.md` section "Heading" (line N)

**Options**
- **1) [Short name]** (recommended - only one option carries this)
  - What: The concrete change or behaviour
  - Why it works: The mechanism or evidence that makes it solve the problem
  - Implication: Cost, side effects, what breaks or must be reverse-updated
  - Why recommended: One sentence, only on the recommended option
- **2) [Short name]**
  - What / Why it works / Implication
```

Rules:
- Exactly one recommendation per decision, stated on the option itself, never in a separate summary
- List every viable option, including "do nothing" when it is viable; omit options only when they violate a spec clause and say which clause
- Present only decisions where options differ in cost, quality, scope, or user-facing behaviour. Engineering choices with no user-visible trade-off are NOT presented - the agent decides and records them
- Close with the exact reply format expected: `DD-04 2, DD-05 1`
- Fixed points (constraints no option can change) go under Context, not as pseudo-options
- Review links are mandatory, so [ACTOR] never searches: each file as a clickable path (`tools-and-skills.md` Chat Output) plus section heading and line number. Never raw HTML (stripped, dead links). Do not wrap the decision block in a code fence: paths in code fences are not clickable
- If no file backs the decision, write `Review: none (decision is self-contained)`; never omit the line

## Confirmation Keywords

`[CONFIRMATION_KEYWORDS]`: yes, confirm, confirmed, do, execute, apply

Workflows that require user confirmation before executing changes MUST accept any of these keywords. Non-confirmation keywords: no, cancel, abort, stop.

Workflows reference this list as `@rules:core-conventions.md [CONFIRMATION_KEYWORDS]` instead of inlining keyword lists.

## Skill References

Reference skills using `@skills:skill-name` format. The skill name must match a folder in `[AGENT_FOLDER]/skills/`. GOOD: `@skills:write-documents`. BAD: `(write-documents skill)`, `write-documents skill`, `the writing skill`

## APAPALAN Writing Principle

**APAPALAN** = As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)

All written output - documents, code comments, log messages, commit messages, communications - follows this principle. Precision always wins when the two conflict. Full rules: @skills:write-documents `APAPALAN_RULES.md`.

**Minimal subset (always apply):**
- **APAPL-PR-07**: Be specific - no "handles errors appropriately", say "retry 3 times with exponential backoff"
- **APAPL-PR-09**: Consistent patterns - same concept = same format everywhere
- **APAPL-BR-02**: Sacrifice grammar for brevity - drop articles, filler, verbose constructions
- **APAPL-NM-01**: One name per concept - no synonyms, no polysemy
- **APAPL-NM-05**: Use standard terms - don't invent new names for known concepts
- **APAPL-ST-01**: Goal first - reader knows WHY before HOW

## Transcription Output

Transcribed content MUST contain only the original document's content. No processing metadata, agent annotations, or workflow artifacts. **Text Style rules do NOT apply to transcribed content.** Transcriptions preserve the original exactly - including curly quotes, typos, unusual punctuation, and formatting choices. Only markdown structural elements (headers, lists, emphasis) are agent-created.

**Prohibited in transcription output:** source filename, path, or URL; page counts, figure counts, or statistics; transcription date or processing timestamps; verification status or progress markers; agent notes or processing comments.

**Store metadata separately:** If tracking is needed, create a companion `[FILENAME]_meta.json` or add to session NOTES.md.
