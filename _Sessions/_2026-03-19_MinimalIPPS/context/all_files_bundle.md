## [build.md]
<!-- lines: 41, tokens: ~257 -->
---
description: BUILD workflow - create software, features, systems
auto_execution_mode: 1
---

# Build Workflow

Entry point for BUILD workflow - creating software, features, systems.

## Required Skills

- @edird-phase-planning for phase gates and planning
- @session-management for session setup
- @write-documents for document templates

## MUST-NOT-FORGET

- Run `/session-new` at workflow start
- Run `/session-finalize` when done
- Follow @edird-phase-planning gates between phases

## Usage

```
/build "Add user authentication API"
```

## Workflow

1. Run `/session-new` with feature name
2. Invoke @edird-phase-planning skill
3. Follow phases: EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER
4. Check gates before each transition
5. Run `/session-finalize` when done

## BUILD-Specific Rules

- **UI work**: Visual reference (screenshot/video) is MANDATORY
- **UI work**: Max 100 lines before visual verification
- **Artifacts**: SPEC, IMPL, TEST documents required (depth per complexity)
- **Gate bypass forbidden**: Must list actual artifact paths as evidence


## [core-conventions.md]
<!-- lines: 169, tokens: ~1709 -->
---
trigger: always_on
---

# Core Conventions

Universal formatting and writing conventions for all documents.

## Text Style (Exception: transcribed or external documents)

- Use ASCII "double quotes" or 'single quotes'. Never use Non-ASCII quotes unless explicitly asked.
- No emojis in documentation (see Document Rule Exceptions below)
- Avoid Markdown tables; use unnumbered lists with indented properties (see Document Rule Exceptions below)
- Use Unicode box-drawing characters for structures:
  - Trees and flows: `├─>` `└─>` `│` (2-space indentation compatible)
  - Boxes and diagrams (non-UI): `┌─` `├─` `└─` `│` `─` `┐` `┤` `┘`
  - UI diagrams and designs: Keep ASCII `+` `-` `|` for compatibility and easy manual editing
- Never use `▼` (U+25BC); use `v` instead
- Try to fit single statements/decisions/objects on a single line
- Format workflow references as inline code: `/verify`, `/go`, `/recap`

## Date and Time Format

- **In documents**: `YYYY-MM-DD HH:MM` - Example: `2026-03-19 14:30`
- **In logging**: `YYYY-MM-DD HH:MM:SS` - Example: `2026-03-19 14:30:23`
- **In filenames**: `YYYY-MM-DD` prefix - Example: `2026-03-19_ServerMigration.md`, `2026-03-19_14-30_MeetingNotes.md`
- **In session folders**: `YYYY-MM-DD` prefix - Example: `_2026-03-19_FixAuthBug/`
- **In Document History**: `[YYYY-MM-DD HH:MM]` - Example: `**[2026-03-19 14:30]**`

Never use locale-dependent formats (`03/19/2026`, `19.03.2026`, `March 19, 2026`).

## Document Structure

- Place Table of Contents after header block (or after MUST-NOT-FORGET if present)
- No `---` markers between sections
- One empty line between sections
- Most recent changes at top in changelog sections

## Header Block

All documents start with:

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

- Doc ID is required for all documents
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Omit optional fields if not applicable: Target file, Depends on, Does not depend on

## Document History Section

Always at document end, reverse chronological order:

```
## Document History

**[2026-01-12 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Changed: Placeholder standardized to `{itemId}` (camelCase)
- Fixed: Modal OK button signature

**[2026-01-12 10:00]**
- Initial specification created
```

**Action prefixes:** Added, Changed, Fixed, Removed, Moved

## Document Rule Exceptions

Documents may opt-in to use Markdown tables or emojis by adding a DevSystem tag as the **first line** of the document (before the title).

**Syntax:**
```html
<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />
```

**Attributes:**
- `MarkdownTablesAllowed=true` - Allow Markdown tables in this document
- `EmojisAllowed=true` - Allow emojis in this document

**Table formatting rule:** When tables are allowed, format with aligned columns using spaces for human readability. No bold, italic, or other formatting inside table cells.
```markdown
| Model           | Workers | TPM   |
|-----------------|---------|-------|
| gpt-5-nano      | 120+    | ~402K |
| claude-4-5-opus | 60+     | ~473K |
```
- BAD: `|Model|Workers|TPM|` (no spacing)
- BAD: `| **Model** | Workers |` (bold in cells)

**Allowed emojis (when enabled):**
- ✅ - Yes, supported, pass, enabled
- ❌ - No, unsupported, fail, disabled
- ⚠️ - Warning, partial, caution
- ★ - Filled star (rating)
- ☆ - Outlined star (rating)
- ⯪ - Half-filled star (rating)

**Usage pattern:** Emoji first, then textual equivalent
```markdown
- **MCP** - ✅ Yes
- **Hooks** - ❌ No
- **Data** - ⚠️ Partial (read-only)
- **Quality** - ★★★☆☆ (3)
- **Docs** - ★★★★⯪ (4.5)
```

**When to use exceptions:**
- Comparison documents where tables improve readability
- Feature matrices and compatibility charts
- Status dashboards

## Skill References

Reference skills using `@skills:skill-name` format. The skill name must match a folder in `[AGENT_FOLDER]/skills/`.

- `@skills:write-documents` - Document writing skill
- `@skills:coding-conventions` - Coding conventions skill
- `@skills:deep-research` - Deep research skill

**BAD:** `(write-documents skill)`, `write-documents skill`, `the writing skill`
**GOOD:** `@skills:write-documents`

## APAPALAN Writing Principle

**APAPALAN** = As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)

All written output - documents, code comments, log messages, commit messages, communications - follows this principle. Full rules in `APAPALAN_RULES.md` (@skills:write-documents skill).

**Why:** Imprecise writing causes wrong assumptions. Verbose writing wastes attention. Precision prevents misunderstanding; brevity respects the reader's time. Precision always wins when the two conflict.

**Minimal subset (always apply):**
- **AP-PR-07**: Be specific - no "handles errors appropriately", say "retry 3 times with exponential backoff"
- **AP-PR-09**: Consistent patterns - same concept = same format everywhere
- **AP-BR-02**: Sacrifice grammar for brevity - drop articles, filler, verbose constructions
- **AP-NM-01**: One name per concept - no synonyms, no polysemy
- **AP-NM-05**: Use standard terms - don't invent new names for known concepts
- **AP-ST-01**: Goal first - reader knows WHY before HOW

## Temporary Files (.tmp prefix)

Files starting with `.tmp` are temporary helper scripts created during operations. They should be deleted after use. Example: `.tmp_fix_quotes.ps1`

## Transcription Output

Transcribed content MUST contain only the original document's content. No processing metadata, agent annotations, or workflow artifacts.

**IMPORTANT: Text Style rules do NOT apply to transcribed content.**
Transcriptions preserve the original exactly - including curly quotes, typos, unusual punctuation, and formatting choices. Only markdown structural elements (headers, lists, emphasis) are agent-created.

**Prohibited in transcription output:**
- Source filename, path, or URL
- Page counts, figure counts, or statistics
- Transcription date or processing timestamps
- Verification status or progress markers
- Agent notes or processing comments

**Store metadata separately:** If tracking is needed, create a companion `[FILENAME]_meta.json` or add to session NOTES.md.


## [skills/llm-evaluation/prompts/answer-from-text.md]
<!-- lines: 15, tokens: ~72 -->
# Answer from Text

Based on the provided text, answer the following question.

Rules:
- Answer ONLY using information from the provided text
- If the answer is not in the text, respond: "Cannot answer from provided text"
- Be concise - one sentence if possible
- Quote relevant passages when helpful

Question: {question}

Text:
{text}



## [skills/llm-evaluation/prompts/compare-image-transcription.md]
<!-- lines: 64, tokens: ~450 -->
# Compare Image Transcription Semantic Capture

Evaluate how well these two transcriptions capture the **same underlying visual content**. Both are attempting to represent the same original figure - judge whether they convey equivalent semantic understanding.

## Transcription A

The following contains ASCII art and `<transcription_notes>` metadata:

{transcription_a}

## Transcription B

The following contains ASCII art and `<transcription_notes>` metadata:

{transcription_b}

## What to Compare

Each transcription contains:
- **ASCII art** (```` ```ascii ... ``` ````) - structural representation using text characters
- **transcription_notes** (`<transcription_notes>...</transcription_notes>`) - metadata including:
  - Mode (Structural/Shading)
  - Dimensions
  - What ASCII captures vs misses
  - Colors and their meanings
  - Layout description
  - Reconstruction hints

## Evaluation Criteria

**Do both transcriptions convey the same semantic understanding?**

1. **Structural Elements (35 points)**
   - Same components identified? (boxes, nodes, connections)
   - Same hierarchy or flow depicted?
   - Same labels and annotations present?

2. **Visual Information Preserved (25 points)**
   - Same colors documented?
   - Same visual details noted as missing from ASCII?
   - Same reconstruction hints provided?

3. **Relationships and Layout (25 points)**
   - Same spatial arrangement described?
   - Same directional flow captured?
   - Same groupings or regions identified?

4. **Completeness (15 points)**
   - Both capture similar level of detail?
   - Neither omits significant elements the other includes?

## Scoring Guide

- **90-100**: Both capture identical semantic content, only superficial wording differs
- **70-89**: Same core understanding, minor interpretive differences
- **50-69**: Similar overall, but one captures details the other misses
- **30-49**: Different interpretations of the same visual
- **0-29**: Fundamentally different understanding of the source image

## Output

JSON only, example format:

{{"score": 85, "differences": ["color description differs", "layout interpretation varies"]}}


## [skills/llm-evaluation/prompts/judge-answer.md]
<!-- lines: 24, tokens: ~168 -->
# Judge Answer

You are an evaluation judge. Score how well the model answer matches the reference answer.

Scoring criteria (0-5):
- **5**: Perfect match - contains all key information, no errors
- **4**: Good - minor omissions or phrasing differences, core facts correct
- **3**: Acceptable - some key information present, some missing
- **2**: Poor - significant errors or omissions, partially correct
- **1**: Very poor - mostly incorrect or irrelevant
- **0**: Wrong - completely incorrect or no relevant content

Question: {question}
Reference Answer: {reference_answer}
Model Answer: {model_answer}

Respond with ONLY a JSON object:
```json
{
  "score": <0-5>,
  "rationale": "<brief explanation>"
}
```



## [skills/llm-evaluation/prompts/summarize-text.md]
<!-- lines: 17, tokens: ~85 -->
# Summarize Text

Summarize the following text concisely while preserving key information.

Include:
- Main topic or purpose
- Key facts and figures
- Important names, dates, locations
- Conclusions or outcomes

Output format: 2-3 paragraphs of plain text

Do not:
- Include minor details
- Add information not in the source
- Use bullet points (prose only)



## [skills/llm-evaluation/prompts/transcribe-page.md]
<!-- lines: 16, tokens: ~85 -->
# Transcribe Page

Transcribe this page exactly as shown. Preserve:
- All text content
- Document structure (headings, lists, tables)
- Numbers, dates, names exactly as written
- Any visible annotations or handwriting

Output format: Markdown

Do not:
- Add commentary or interpretation
- Summarize or paraphrase
- Skip any visible content
- Correct apparent typos (preserve original)


