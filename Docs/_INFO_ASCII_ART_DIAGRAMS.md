# INFO: ASCII Art Diagrams

**Doc ID**: ASCIIART-IN01
**Goal**: Define what to do, what to avoid, which constraints apply, and which diagram type to choose when drawing text diagrams for humans, LLMs, and image generators, with one worked example per type
**Timeline**: Created 2026-09-10, Updated 2 times (2026-09-10 - 2026-09-10)

**Note**: This is the deep research reference document. Operational GRUC files (GUIDES, RULES, CHECKS, EXAMPLES) in `skills/write-documents/` are distilled from this. Not loaded during writing workflows.

## Summary

- Text diagrams have three audiences with different needs: humans (Unicode box-drawing, visual polish), LLMs (Unicode box-drawing, explicit labels), image generators (Unicode box-drawing plus a prose prompt that names every element) [VERIFIED: DevSystem rules, gpt-image-2 field reports]
- Pure ASCII (`+ - | > < ^ v`) renders identically on every OS, font, and encoding; Unicode box-drawing is single-cell width but Unicode arrows `→ ↓ ▼` have East-Asian ambiguous width and break alignment in CJK fonts [VERIFIED: webreactiva ascii-flow skill, core-conventions.md]
- Never mix ASCII line chars (`- |`) with Unicode line chars (`─ │`) in one diagram; joints do not connect and stroke weights differ [VERIFIED]
- Width limit: 70 chars for Markdown/mobile, 80-120 for documents, 180 hard max; height is cheap, width is not [VERIFIED: transcribe.md F1, IETF 72-col rule, X-FRI skill]
- Image generators degrade above 6 modules per image; compress to 3-6 boxes, 3-5 bullets each, one dominant flow direction [VERIFIED: gpt-image-2 tests by lihuanyu.com]
- Image generators need a prose prompt alongside the ASCII: intent, audience, style, layout direction, element list, negative constraints ("do not invent components") [VERIFIED: ChatGPT image docs, bradsjm diagram prompt spec]
- One concept per box, labels of 1-3 words, detail in a legend below the art, spaces never tabs, verticals in the same column on every row [VERIFIED: all three ASCII skills agree]
- Pick the encoding before drawing: tree for hierarchy, flow for sequence, layers for tiers, swimlane for actors, state machine for cycles; a wrong encoding is the most common readability failure [VERIFIED: webreactiva]
- Charts: horizontal bars beat vertical bars in text (labels stay readable, bar length = one char per unit); avoid pie charts entirely, use proportion bars [ASSUMED: derived from monospace constraints]
- Every diagram needs a title line, a legend line, and a self-verification pass (all verticals aligned, arrowheads touch boxes, box interiors equal width, readable without the original) [VERIFIED: transcribe.md F2b]
- Width mismatch is a mixing problem, not a glyph problem: a line made of one glyph family only (braille + `⠀`, block eighths, Tier 2 digit fonts) cannot misalign against itself. This admits braille plots (2 x 4 dots per cell), block sparklines (8 levels per cell), and 3 x 3 digit fonts, provided labels sit on separate lines [VERIFIED: plotille, drawille, Textual Sparkline and Digits source]
- Depth (boxes on boxes) is faked by five techniques: occlusion (front box interrupts back border), offset stack, shadow column, dimmed page under modal, isometric face. Each states which border wins [ASSUMED: synthesized from asciiflow, PlantUML, TUI conventions]
- Braille and block charts need numbers shipped alongside for all consumers; the visual is supplementary, the numbers carry the fact [VERIFIED: transcribe.md F2b]

## Table of Contents

1. [Audiences and Purpose](#1-audiences-and-purpose)
2. [Character Sets](#2-character-sets)
3. [Universal Constraints](#3-universal-constraints)
4. [Anti-Patterns](#4-anti-patterns)
5. [Diagram Type Selection](#5-diagram-type-selection)
6. [Architecture Diagrams](#6-architecture-diagrams)
7. [UX Design Diagrams](#7-ux-design-diagrams)
8. [Charts](#8-charts)
9. [Other Diagram Types](#9-other-diagram-types)
10. [ASCII Art as Image-Generation Prompt](#10-ascii-art-as-image-generation-prompt)
11. [Verification Checklist](#11-verification-checklist)
12. [Next Steps](#12-next-steps)
13. [Sources](#13-sources)
14. [Document History](#14-document-history)

## 1. Audiences and Purpose

A text diagram is read by one of three consumers. Decide which one before drawing; the choice fixes character set, width, and label density.

- **Human reader** (SPEC, INFO, README, terminal output)
  - Wants: visual polish, clear boundaries, scannable layout
  - Use: Unicode box-drawing (DevSystem default per `core-conventions.md`, SPEC-DG-01/06, INFO-FT-03)
  - Width: 80-120 chars
- **LLM reader** (transcriptions, prompts, agent context, code comments)
  - Wants: explicit semantics, stable alignment, no ambiguous glyphs
  - Use: Unicode box-drawing (Tier 2), every node labeled, inline legend; Tier 1 only for ASCII-only pipelines
  - Width: 80-120 chars, max 180
- **Image generator** (ChatGPT / gpt-image, Gemini, Midjourney via text)
  - Wants: a compressed structure (3-6 modules), one flow direction, short labels, plus a prose prompt describing intent, style, and constraints
  - Use: Unicode box-drawing (Tier 2) as the structural skeleton, prose as the instruction; the art alone is not enough (see Section 10)
  - Width: 70-100 chars; anything wider is compressed away by the model

All three consumers use Tier 2 (Unicode box-drawing) as the default. Tier 1 (pure ASCII) is the fallback for ASCII-only pipelines (code comments, chat, git diffs, e-mail). When in doubt, use Tier 2.

**Why diagrams at all** (INFO_GUIDES.md Section 4): prefer a diagram over prose when 3+ components interact, when hierarchy exists, or when flow branches. Below that threshold a list is shorter and more precise.

## 2. Character Sets

Four tiers, from default to specialized. Tier 2 (Unicode box-drawing) is the default for all consumers. Choose one tier per diagram and never mix line characters across tiers.

### 2.1 Tier 1: Pure ASCII

```
Lines:      -  |  +  =
Corners:    +
Diagonals:  /  \
Arrows:     ->  <-  <->  v  ^  >>  <<
Brackets:   [ ]  ( )  { }  < >
Emphasis:   ===  ***  ###  ...
Fill:       #  *  =  .  :  (density: @ # % * + = - : .)
```

- Renders identically everywhere: any OS, font, terminal, encoding, e-mail, git diff, code comment
- Zero mojibake risk, zero width ambiguity
- Mandatory for: ASCII-only pipelines only (code comments, chat, git diffs, e-mail, legacy terminals)
- Weakness: `+` corners and `-` lines read as "engineering sketch"; acceptable, since semantics matter more than polish for these consumers

### 2.2 Tier 2: Unicode Box-Drawing

```
Light:      ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
Heavy:      ━ ┃ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋
Double:     ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬
Rounded:    ╭ ╮ ╰ ╯ (with ─ │)
Flow tree:  ├─>  └─>  │
```

- Single-cell width in every monospace font; alignment holds across platforms
- DevSystem default for all documents and all consumers (SPEC, INFO, UI mockups, LLM prompts, image-generation prompts)
- Use light set by default; heavy or double only to emphasize one container (e.g., the system boundary); rounded for UI mockups when the target UI has rounded corners
- Weakness: fails in proportional fonts and some CJK terminals; use Tier 1 for ASCII-only pipelines

### 2.3 Tier 3: Arrows, Blocks, Geometry

```
Arrows:     → ← ↑ ↓ ↔ ⇒ ▶ ◀ ▲ ▼
Blocks:     █ ▓ ▒ ░ ▌ ▐ ▀ ▄
Bullets:    • ◦ ▪ ■ □ ● ○ ◆ ◇ × ✓
```

- East-Asian **ambiguous width**: `→ ← ↑ ↓ ▲ ▼ ◀ ▶` are one cell in Western locales, two cells in CJK fonts. A single arrow mid-line shifts everything right of it
- Rule: use sparingly, only at the end of a connector where a shift cannot cascade, or prefer ASCII heads `> < ^ v`
- DevSystem rule: never `▼`, use `v`; `→` only in prose with spaces around it, never inside a diagram grid
- Blocks (`█ ▓ ▒ ░`) are safe single-width and useful for bar charts for all consumers

### 2.4 Tier 4: Line-Pure Glyph Sets (Braille, Block Eighths, Digit Fonts)

The width problem of Tiers 2-3 is a **mixing** problem: a glyph is only misaligned relative to other glyphs on the same line. A line that consists of one glyph family only cannot misalign against itself. This unlocks three high-resolution families for charts and pictures, on the condition that **no other character class appears on the same line**.

```
Braille (U+2800-U+28FF):   ⠀ ⡀ ⣀ ⣠ ⣰ ⣸ ⣼ ⣾ ⣿   2 x 4 dots per cell
                           ⠉ ⠒ ⠤ ⣀   horizontal levels (top to bottom)
                           ⠁ ⠂ ⠄ ⡀   single dots, left column
Block eighths (U+2581-88):  ▁ ▂ ▃ ▄ ▅ ▆ ▇ █   8 vertical levels per cell
Block left-eighths:         ▏ ▎ ▍ ▌ ▋ ▊ ▉ █   8 horizontal levels per cell
Shades:                     ░ ▒ ▓ █            4 density levels
Quadrants:                  ▖ ▗ ▘ ▝ ▞ ▚ ▜ ▛ ▙ ▟   2 x 2 blocks per cell
```

- **Braille**: 2x4 dots per cell = 8x the resolution of a character grid. Used by [plotille](https://github.com/tammoippen/plotille) and [drawille](https://github.com/asciimoo/drawille) for line plots, scatter, histograms, and pixel images. Dot bit layout per cell: rows top to bottom `1 4 / 2 5 / 3 6 / 7 8` = bits `0x01 0x08 / 0x02 0x10 / 0x04 0x20 / 0x40 0x80`, code point = `0x2800 + bits`. The empty cell `⠀` (U+2800) is a real glyph, not a space: use it for padding so the line stays braille-only
- **Block eighths**: 8 levels per cell, 1 row = a sparkline ([Textual Sparkline](https://textual.textualize.io/widgets/sparkline/) uses exactly `▁▂▃▄▅▆▇█`); stack rows for a taller area chart (Dolphie dashboard style)
- **Digit fonts**: 3x3-cell glyphs built from Tier 2 line-drawing pieces ([Textual Digits](https://textual.textualize.io/widgets/digits/)); a digit line contains only box-drawing glyphs and spaces, so it stays aligned

**Line-purity rule**: inside one rendered line, use exactly one of: Tier 1, Tier 2 (+ spaces), braille (+ `⠀`), block eighths (+ spaces). Labels, axis numbers, legends go on **separate lines** above or below the art, never left or right of it. Fonts that render braille narrower or wider than Latin cells exist; braille-only lines stay internally consistent regardless.

```
GOOD (labels on their own lines, art lines are braille-only):

requests/s, last 60 s                               peak 1,240
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠤⠒⠒⠊⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀
⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠤⠤⠥⠒⠊⠍⠠⠀⠂⠐⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠂⠠⠀⠄⠐⠀⠁
0 s                                                        60 s

BAD (label on the same line as braille; cell width may differ by font):

1,240 ⢀⣀⣀⣀ peak
```

### 2.5 ASCII Dialects

Tier 1 has stylistic dialects. Pick one per document.

```
Plain:      +-------+      Rounded (PlantUML):   ,-------.      Double:    +=======+
            | Box   |                            | Box   |                 | Box   |
            +-------+                            `-------'                 +=======+

Dashed:     + - - - +      Fragment (PlantUML):  ______________      Actor:   ,-.
            ' Box   '                            ! OPT / [cond]                `-'
            + - - - +                            !__/                          /|\
                                                 !  ...                         |
                                                 !~~~~~~~~~~~~~~                / \
```

- **Plain** `+ - |` is the default; renders everywhere, easiest to align
- **Rounded** `` , . ` ' `` softens corners for UI mockups; used by [PlantUML ASCII output](https://plantuml.com/ascii-art). Costs: backtick and `'` look like quotes in prose; do not mix with Plain in one diagram
- **Double** `=` for emphasis (system boundary, active state) or a second line style in the legend
- **Dashed** `- -` or `. .` for optional, external, or planned elements
- **Fragment** `!` left border with `~~~` separators (PlantUML) for alt/loop blocks in sequence diagrams
- **Actor** stick figure for sequence and use-case diagrams; 3 chars wide

### 2.5.1 Dialect Mapping

Same box in every available style. Pick one per document; do not mix styles within a diagram.

```
Plain (Tier 1):

  Normal      Dotted       Dashed
  +-------+   +.......+    + - - - +
  | Box   |   : Box   :    ' Box   '
  +-------+   +.......+    + - - - +

  Double      Rounded
  +=======+   ,-------.
  | Box   |   | Box   |
  +=======+   `-------'

Unicode (Tier 2):

  Normal      Dotted       Dashed
  ┌───────┐   ┌┄┄┄┄┄┄┄┐   ┌╌╌╌╌╌╌╌┐
  │ Box   │   ┆ Box   ┆   ╎ Box   ╎
  └───────┘   └┄┄┄┄┄┄┄┘   └╌╌╌╌╌╌╌┘

  Double      Heavy        Rounded
  ╔═══════╗   ┏━━━━━━━┓   ╭───────╮
  ║ Box   ║   ┃ Box   ┃   │ Box   │
  ╚═══════╝   ┗━━━━━━━┛   ╰───────╯
```

- **Dotted** `.` `:` (ASCII) or `┄` `┆` U+2504/2506 (Unicode, triple dash) for optional, external, or planned elements
- **Dashed** `- -` `'` (ASCII) or `╌` `╎` U+254C/254E (Unicode, double dash) for a lighter alternative to dotted
- **Heavy** `┏ ━ ┓ ┃` emphasizes one container (e.g., system boundary); use sparingly, one per diagram
- **Rounded** `╭ ╮ ╰ ╯` for UI mockups where the target UI has rounded corners
- Unicode dotted and dashed reuse normal light corners `┌ ┐ └ ┘`; no dedicated dotted/dashed corner glyphs exist

### 2.6 Decision Rule

```
Diagram lives in code comment/chat/e-mail?  ──yes──>  Tier 1 only
        │
        no
        v
Chart or picture needs sub-cell resolution?  ──yes──>  Tier 4 (braille or block eighths), line-pure
        │
        no
        v
                                                Tier 2 light
                                                (Tier 4 blocks allowed for charts)
```

Never on the same line: `-` next to `─`, `|` next to `│`, `+` next to `┼`, braille next to anything but braille. Stroke weights differ, junctions will not join, cell widths may differ.

## 3. Universal Constraints

Apply to every diagram regardless of type or consumer.

### 3.1 Grid Discipline

- **Spaces only, never tabs.** A tab renders as 2, 4, or 8 columns depending on the viewer; tabs guarantee misalignment
- **Boxes first, connectors second.** Fix box positions and widths, then route lines
- **Verticals stay in one column.** A `|` that drifts one column reads as broken. Count columns, do not eyeball
- **Compute centers before connecting.** `center_col = left_border_col + floor(total_width / 2)`. Attach vertical connectors at the computed column
- **Equal interior width per box row.** Pad shorter labels with spaces so `| login  |` and `| verify |` match
- **Same character count on every line of a box or table.** Verify with a column counter, not by eye
- **No trailing whitespace.** Editors strip it and shift the art
- **Straight lines only.** No diagonals except for explicit tree branches, Venn-style overlaps, or isometric faces (Section 3.6 E)
- **Text never touches a frame.** Min 1 space between text and `│` on both sides: `│ text │`, never `│text│`. Applies to labels, kind tags, buttons, and values
- **Frames never touch.** Nested boxes: 1-space gutter between outer and inner border on every side (`│ ┌───┐ │`). Adjacent boxes in one row: 3-5 spaces (2 min). Stacked boxes: 1 blank line or a connector row. Exception: TUI dashboard panels (Section 8.15) abut edge-to-edge to fill a fixed terminal width

### 3.2 Size

- **Width**: 70 chars for Markdown that may render on mobile or in side panes; 80-120 for documents and LLM prompts; 180 absolute max (transcribe.md F1)
- **Height**: cheap. Stack vertically before widening horizontally
- **Aspect ratio**: monospace cells are about 2:1 (taller than wide). Compensate by doubling horizontal gaps: 3-5 chars between adjacent boxes, 1 blank line between box rows
- **Padding**: 1 space between text and border (`| text |`); 2 spaces for UI mockups where whitespace is part of the design
- **Elements**: 3-7 primary elements per diagram (transcribe.md F0). Above 7, split into two diagrams or group into named clusters. Image generators degrade above 6 modules

### 3.3 Labels and Semantics

- **One concept per box.** Multi-concept boxes force wide boxes and break layout
- **Labels of 1-3 words**, action-oriented for flows (`Validate`, `Retry`), noun for components (`Auth Service`)
- **Label every node, region, and outcome.** `[DATABASE]`, `(pending)`, `RETRY LOOP`. LLMs understand explicit labels better than visual patterns (transcribe.md F1 MAXIMIZE SEMANTICS)
- **Mark states explicitly**: `(ACTIVE)` vs `(inactive)`, `(BEFORE)` vs `(AFTER)`
- **Branch labels are single words**: `Yes`, `No`, `Hit`, `Miss`, `Error`, `Empty`. Sentence-length labels go into prose below
- **UX text fidelity** (SPEC-DG-05): button and menu text in UI mockups matches the implementation 1:1. No `[Auth]` when the button says `[SharePoint (Managed Identity)]`
- **Detail lives in the legend**, not in the box. Legend is one or two lines directly under the art: `Legend: === main flow  --- log output  [S] = Server`

### 3.4 Structure of a Complete Diagram

Every diagram has four parts. Diagrams for LLM or image-generator consumption include all four; human-facing SPEC diagrams may omit part 4.

```
1. Title line      [DIAGRAM TYPE - WHAT IT SHOWS]
2. Art block       the grid itself
3. Legend line     symbol meanings, states, colors
4. Notes           what the art cannot show: colors, icons, proportions, data values
```

Example skeleton:

```
[COMPONENT DIAGRAM - ORDER SERVICE AND ITS DEPENDENCIES]

┌─────────────┐       ┌───────────────┐       ┌────────────┐
│ Web Client  │──────>│ Order Service │──────>│ Orders DB  │
│ [BROWSER]   │       │ [API]         │       │ [POSTGRES] │
└─────────────┘       └───────────────┘       └────────────┘
                             │
                             v
                      ┌───────────────┐
                      │ Payment API   │
                      │ [EXTERNAL]    │
                      └───────────────┘

Legend: ───> synchronous HTTP call  [TYPE] = component kind
Notes: Payment API is a third-party system outside the trust boundary (draw dashed in the image)
```

### 3.5 Direction

Choose one dominant flow direction per diagram and keep it:

- **Left-to-right**: request journeys, data movement, pipelines, user journeys, timelines
- **Top-to-bottom**: layered stacks, deployment hierarchies, call chains, decision trees, file trees
- **Radial**: hub-and-spoke only; hard in text, prefer a star with the hub in the center row
- **Return paths**: draw below the forward path or omit and state in legend (`<-- response omitted`)

### 3.6 Depth: Boxes on Top of Boxes

A character grid has no z-axis. Depth is faked by five techniques; each states its rule for which border wins where two boxes meet.

**A. Occlusion** - the front box interrupts the back box's border. The back box's hidden edge is simply not drawn. Reader infers "front" from the unbroken outline.

```
┌────────────────┐
│ Back           │
│      ┌────────────────┐
│      │ Front          │
└──────│                │
       └────────────────┘
```

Rule: the front box has all four edges complete; the back box loses every segment the front box covers. Never draw both borders through each other.

**B. Offset stack (deck of cards)** - identical boxes shifted 1 row and 2 columns each. Shows "many of the same" (instances, replicas, pages).

```
    ┌─────────────┐
  ┌─────────────┐ │
┌─────────────┐ │ │
│ Worker      │ │─┘
│ [PROCESS]   │─┘
└─────────────┘

or with a count instead of a stack:

┌─────────────┐
│ Worker  x3  │
│ [PROCESS]   │
└─────────────┘
```

Rule: top-left card is the front; max 3 visible layers; more = write the count.

**C. Shadow** - a dark edge on the right and bottom of a box. Front box in a modal-over-page situation.

```
Tier 1 (fallback)           Tier 2 (default)
+----------------+          ┌────────────────┐
| Confirm delete |#         │ Confirm delete │▓
|                |#         │                │▓
|  [Delete] [No] |#         │  [Delete] [No] │▓
+----------------+#         └────────────────┘▓
 ################            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
```

Rule: shadow is 1 char wide, right and bottom only, drawn with `#` (Tier 1) or `▓` (Tier 2). Block shades are fixed single-width in every monospace font (Section 2.3), so `▓` beside `│` is safe; braille beside `│` is not.

**D. Modal over dimmed page** - the page content behind a modal is replaced by `.` or `░` to show it is inactive; the modal is drawn complete on top.

```
┌────────────────────────────────────────────────────────────┐
│ . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  │
│ . . . . . . ┌────────────────────────────────┐ . . . . . . │
│ . . . . . . │ Cancel job 42?             [x] │ . . . . . . │
│ . . . . . . ├────────────────────────────────┤ . . . . . . │
│ . . . . . . │ Keeps 7 finished items.        │ . . . . . . │
│ . . . . . . │            [Cancel job] [Keep] │ . . . . . . │
│ . . . . . . └────────────────────────────────┘ . . . . . . │
│ . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  │
└────────────────────────────────────────────────────────────┘
```

Rule: dim pattern is `. ` (dot space) or `░`; never draw the underlying controls, they are not interactive while the modal is open.

**E. Isometric (2.5D)** - a box with a visible top and right face. Use for deployment nodes, storage volumes, physical devices. Costs 3 extra columns and 1 extra row per box. Left: Tier 1 (fallback). Right: Tier 2 (default, rounded corners).

```
      +-----------+          ╭───────────╮
     /           /|         /           /│
    +-----------+ |        ┌───────────┐ │
    | Node A    | |        │ Volume    │ │
    | [VM]      | +        │ [DISK]    │ ╯
    |           |/         │           │/
    +-----------+          ╰───────────╯
```

Rule: light comes from top-left; the top face uses `/` on the left edge and the right face a single column of `|` (Tier 1) or `│` (Tier 2) closed by `+` or `╯`. The diagonal `/` is ASCII in both tiers; the box-drawing diagonals `╱ ╲` have poor font coverage. Do not mix isometric and flat boxes in one row.

**Overlap without depth** (asciiflow style) - when two regions genuinely overlap (Venn-like, shared ownership), both borders are drawn and cross. Say so in the legend, otherwise readers assume a drawing error.

```
┌──────────────┐
│ Team A       │
│      ┌───────┼──────┐
│      │ both  │      │
└──────┼───────┘      │
       │       Team B │
       └──────────────┘

Legend: crossing borders = shared region, both teams own "both"
```

## 4. Anti-Patterns

Each BAD/GOOD pair shows one failure. Generic example data throughout.

### 4.1 Mixed Character Tiers

**BAD** (ASCII lines meet Unicode corners; joints do not connect):
```
┌--------┐
| Title  |
└--------┘
```

**GOOD** (one tier):
```
+--------+          ┌────────┐
| Title  |    or    │ Title  │
+--------+          └────────┘
```

### 4.2 Drifting Verticals

**BAD** (connector shifted one column at row 3):
```
┌────────┐
│ Input  │
└────────┘
    │
     v
┌────────┐
│ Output │
└────────┘
```

**GOOD** (center column 4 held on every row):
```
┌────────┐
│ Input  │
└────────┘
    │
    v
┌────────┐
│ Output │
└────────┘
```

### 4.3 Sentence Labels

**BAD**:
```
┌────────────────────────────────────────────────────────────┐
│ Validate the incoming request against the JSON schema and  │
│ reject it with 400 if any required field is missing        │
└────────────────────────────────────────────────────────────┘
```

**GOOD**:
```
┌──────────────────┐
│ Validate Request │
│ [SCHEMA]         │
└──────────────────┘
        │ Invalid
        v
┌──────────────────┐
│ Reject 400       │
└──────────────────┘

Notes: validation = JSON schema; any missing required field rejects
```

### 4.4 Box Maze

**BAD** (nested boxes for a linear list; 3 levels of borders, zero added meaning):
```
┌──────────────────────────────────────────────┐
│ Pipeline                                     │
│ ┌──────────────────────────────────────────┐ │
│ │ Stage 1                                  │ │
│ │ ┌──────────────────────────────────────┐ │ │
│ │ │ Read file                            │ │ │
│ │ └──────────────────────────────────────┘ │ │
│ └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

**GOOD** (linear = flow, not nesting):
```
[PIPELINE - 3 STAGES]

┌───────────┐     ┌───────────┐     ┌───────────┐
│ Read file │────>│ Transform │────>│ Write out │
└───────────┘     └───────────┘     └───────────┘
```

### 4.5 Wrong Encoding

**BAD** (a cyclic state machine drawn as a tree hides the cycle):
```
Idle
└─> Running
    └─> Paused
        └─> Running
            └─> Idle
```

**GOOD** (state machine with explicit loop):
```
[STATE MACHINE - JOB LIFECYCLE]

           start              pause
┌──────┐  ──────>  ┌─────────┐  ──────>  ┌────────┐
│ Idle │           │ Running │           │ Paused │
└──────┘  <──────  └─────────┘  <──────  └────────┘
   ^       stop         │         resume
   │                    │ finish
   └────────────────────┘
```

### 4.6 Decorative Boxes Around Lists

**BAD** (SPEC-CT-07: box wastes ~600 chars for a checklist):
```
┌──────────────────────────────────────┐
│ Gate: EXPLORE -> DESIGN              │
│  [ ] Scope defined                   │
│  [ ] Workflow type chosen            │
└──────────────────────────────────────┘
```

**GOOD**:
```
### Gate: EXPLORE -> DESIGN
- [ ] Scope defined
- [ ] Workflow type chosen
```

### 4.7 Unlabeled Nodes and Missing Legend

**BAD** (reader must guess what shapes and line styles mean):
```
( A )════( B )────( C )
```

**GOOD**:
```
[DATA FLOW - INGEST TO REPORT]

(Ingest)═════>(Store)─────>(Report)
 [JOB]         [DB]         [VIEW]

Legend: ═══> bulk write  ───> query  ( ) = process/store
```

### 4.8 Too Wide

**BAD** (150 chars, 9 boxes in one row; wraps on mobile, compressed by image models):
```
┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐
│ A  │─>│ B  │─>│ C  │─>│ D  │─>│ E  │─>│ F  │─>│ G  │─>│ H  │─>│ I  │
└────┘  └────┘  └────┘  └────┘  └────┘  └────┘  └────┘  └────┘  └────┘
```

**GOOD** (snake layout, 70 chars, or split into two diagrams):
```
┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐
│ A  │─>│ B  │─>│ C  │─>│ D  │─>│ E  │
└────┘  └────┘  └────┘  └────┘  └────┘
                                  │
  ┌───────────────────────────────┘
  │
  v
┌────┐  ┌────┐  ┌────┐  ┌────┐
│ F  │─>│ G  │─>│ H  │─>│ I  │
└────┘  └────┘  └────┘  └────┘
```

### 4.9 Data Duplicated in Chart and Text

**BAD**: chart shows `Revenue 2,450` and the paragraph below repeats "Revenue was 2,450". Judge rules (llm-transcription `judge.md`) penalize this.

**GOOD**: values appear once, in the chart; prose interprets ("Category A holds more than half").

### 4.10 Unicode Arrows Inside the Grid

**BAD** (`→` is double-width in CJK fonts; right side shifts):
```
│ Client │ → │ Server │
```

**GOOD**:
```
│ Client │──>│ Server │
```

## 5. Diagram Type Selection

Pick the type from the question the reader must answer. Wrong type = unreadable diagram even with perfect alignment.

```
[DIAGRAM TYPE SELECTOR]

What is the question?
│
├── "What are the parts and how do they connect?"    ──> 6.1 Component diagram
├── "Which part sits on top of which?"               ──> 6.2 Layer diagram
├── "Where does each part run?"                      ──> 6.3 Deployment / process topology
├── "Where does the data go?"                        ──> 6.4 Data flow diagram
├── "Who calls whom, in what order?"                 ──> 6.5 Sequence diagram
├── "What states exist and what moves between them?" ──> 6.6 State machine
├── "What happens after this event?"                 ──> 6.7 Event flow tree
├── "What are the stages of processing?"             ──> 6.8 Pipeline
├── "What depends on what?"                          ──> 6.9 Dependency graph
├── "What are the entities and their relations?"     ──> 6.10 Entity relationship
├── "What does the screen look like?"                ──> 7.1-7.8 UX mockups
├── "How does the user move between screens?"        ──> 7.9 Screen flow
├── "What changes?"                                  ──> 7.10 BEFORE / AFTER
├── "How big / how much / how does it trend?"        ──> 8.x Charts
├── "What contains what?"                            ──> 9.1 Tree
├── "Which decision leads where?"                    ──> 9.3 Decision tree / flowchart
├── "Who does which step?"                           ──> 9.4 Swimlane
└── "When does what happen?"                         ──> 8.4 Timeline / Gantt
```

Selection rules:

- **Hierarchy without cycles** = tree. **Any cycle** = state machine or graph, never a tree (Section 4.5)
- **Order matters** = sequence or pipeline. **Order does not matter** = component diagram
- **More than one actor** = swimlane or sequence. **One actor** = flowchart
- **Comparison of 2-4 options on 3+ criteria** = list with indented properties (DevSystem: no Markdown tables); a matrix diagram only when both axes are short enumerations (Section 8.6)
- **A quantity** = chart, never a diagram

### 5.1 Visual Encoding Taxonomy

The [ASCII Diagrams corpus](https://asciidiagrams.github.io/) (diagrams mined from Chromium, Linux, LLVM, TensorFlow source comments) tags every diagram with its visual encoding. The tags are a compact vocabulary for naming what a diagram does; use them in the title line or notes.

- **Connection :: Graph :: Directed** - boxes and arrows, flow has a direction (6.1, 6.3, 6.4, 6.9)
- **Connection :: Graph :: Undirected** - lattice or mesh, no arrowheads (Myers diff edit graph, adjacency)
- **Connection :: Tree** - one root, indented branches (6.7, 9.1)
- **Geometry :: Nested** - boxes inside boxes with meaning in containment (CSS box model, 6.1 boundaries)
- **Geometry :: Grid** - cells in rows and columns (8.6, 9.6, tile layouts)
- **Sequential :: Aligned** - events on a shared axis, alignment carries timing (6.5, 8.4)
- **Multiples** - the same diagram repeated for 2-3 scenarios side by side (BEFORE/AFTER, config A vs B)
- **Annotation** - callouts `<-- 2 (encapsulates 3, 4, 5)` pointing into the art
- **Legend** - symbol table under the art
- **Math Notation** - fractions as `-----` bars, sums, formulas laid out in 2D

Two patterns from the corpus worth copying:

```
Multiples (two scenarios, same shape, side by side):

  Independent screens             Mirrored screens
  ┌─────────┐  ┌─────────┐        ┌─────────┐  ┌─────────┐
  │ HDMI    │  │ VGA     │        │ HDMI    │  │ VGA     │
  └─────────┘  └─────────┘        └─────────┘  └─────────┘
       ^            ^                  ^            ^
       │            │                  │            │
  ┌────┴────┐  ┌────┴────┐        ┌────┴────────────┴────┐
  │ CRTC 1  │  │ CRTC 2  │        │        CRTC 1        │
  └─────────┘  └─────────┘        └──────────────────────┘

Annotation into nested geometry:

   ___________
  │     1     │
  │___________│
  │ 3 │ 4 │ 5 │  <── 2 (encapsulates 3, 4 and 5)
  │___│___│___│
  │   7   │ 8 │  <── 6 (encapsulates 7 and 8)
  │_______│___│

  r0 encapsulates 1, 2 and 6
```

## 6. Architecture Diagrams

All examples: Tier 2 light, 3-7 elements, title, legend. Swap to Tier 1 glyphs only for ASCII-only pipelines (Section 2.6).

### 6.1 Component Diagram

Question: what are the parts, what kind is each part, how do they connect. C4 "container" level. Group by trust boundary or domain using a dashed outer box.

```
[COMPONENT DIAGRAM - WEB SHOP, CONTAINER LEVEL]

┌─[ Trust boundary: company network ]─────────────────────────────────┐
│                                                                     │
│  ┌──────────────┐      ┌──────────────────┐      ┌───────────────┐  │
│  │ Web Frontend │─────>│ Shop API         │─────>│ Shop DB       │  │
│  │ [SPA]        │      │ [SERVICE]        │      │ [POSTGRES]    │  │
│  └──────────────┘      └──────────────────┘      └───────────────┘  │
│                               │                                     │
│                               │ publish                             │
│                               v                                     │
│                        ┌──────────────────┐      ┌───────────────┐  │
│                        │ Order Queue      │─────>│ Fulfilment    │  │
│                        │ [BROKER]         │      │ [WORKER]      │  │
│                        └──────────────────┘      └───────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTPS
                               v
                        ┌──────────────────┐
                        │ Payment Provider │
                        │ [EXTERNAL]       │
                        └──────────────────┘

Legend: ───> sync call   publish = async message   [KIND] = container type
Notes: outer dashed box = trust boundary; Payment Provider is third-party
```

Rules:
- Users/clients top or left, data stores bottom or right, external systems outside the boundary
- Kind tag on line 2 of every box: `[SPA]`, `[SERVICE]`, `[DB]`, `[QUEUE]`, `[EXTERNAL]`
- Sync vs async distinguished by line style, stated in legend
- Max 7 containers; above that, draw a context diagram (system as one box + externals) and one container diagram per subsystem

### 6.2 Layer Diagram

Question: which tier sits on which. SPEC-DG-03. One outer box, tiers separated by full-width rules, call direction top-down, each tier lists its members with `#` comments.

```
[LAYER DIAGRAM - REQUEST HANDLING STACK]

┌───────────────────────────────────────────────────────────────┐
│  Presentation                                                 │
│  ├─> HTTP routes            # parse request, pick handler     │
│  └─> Response formatter     # JSON / HTML envelope            │
├───────────────────────────────────────────────────────────────┤
│  Application                                                  │
│  ├─> Use cases              # one class per user action       │
│  └─> Validation             # schema + business rules         │
├───────────────────────────────────────────────────────────────┤
│  Domain                                                       │
│  ├─> Entities               # Order, Customer, Product        │
│  └─> Domain events          # OrderPlaced, PaymentFailed      │
├───────────────────────────────────────────────────────────────┤
│  Infrastructure                                               │
│  ├─> Repositories           # SQL adapters                    │
│  └─> Message bus client     # publish / subscribe             │
└───────────────────────────────────────────────────────────────┘

Legend: calls flow downward only; a tier never calls the tier above
```

Rules:
- Highest abstraction on top
- Cross-cutting concerns (logging, auth) as a narrow vertical box at the right edge or as a note, not as a layer
- Max 5 tiers

### 6.3 Deployment and Process Topology

Question: where does each part run. Nodes = machines, containers, processes. Edges = network or IPC.

```
[PROCESS TOPOLOGY - THREE COOPERATING PROCESSES ON ONE HOST]

┌─[ Host: workstation ]──────────────────────────────────────────────┐
│                                                                    │
│  ┌───────────────┐   stdio/IPC   ┌───────────────┐                 │
│  │ Frontend      │<─────────────>│ Coordinator   │                 │
│  │ [PROCESS 1]   │               │ [PROCESS 2]   │                 │
│  └───────────────┘               └───────┬───────┘                 │
│                                          │                         │
│                                          │ spawn + IPC             │
│                                          v                         │
│                                  ┌───────────────┐                 │
│                                  │ Worker        │                 │
│                                  │ [PROCESS 3]   │                 │
│                                  └───────────────┘                 │
│                                          │                         │
│                                          │ append only             │
│                                          v                         │
│                                  ┌───────────────┐                 │
│                                  │ events.jsonl  │                 │
│                                  │ [FILE]        │                 │
│                                  └───────────────┘                 │
└────────────────────────────────────────────────────────────────────┘
        │
        │ HTTPS
        v
┌───────────────┐
│ Model API     │
│ [EXTERNAL]    │
└───────────────┘

Legend: <───> bidirectional IPC   ───> one-way   [PROCESS n] = OS process
Notes: only Worker writes events.jsonl (single-writer rule)
```

Rules:
- Outer box = host, VM, or cluster; inner boxes = processes or containers
- Label each edge with transport (`stdio`, `HTTPS`, `Unix socket`, `IPC`)
- Ownership rules (who writes a file, who spawns whom) in notes, not in boxes

### 6.4 Data Flow Diagram

Question: where does the data go and how does it change. Processes as rounded `( )`, stores as `[ ]`, external entities as `{ }`.

```
[DATA FLOW - LOG INGESTION]

{Log Source}                                         {Analyst}
     │                                                   ^
     │ raw lines                                         │ report
     v                                                   │
  (Parse) ───────> (Enrich) ─────> (Aggregate)──────> (Render)
     │                │                 │
     │ rejected       │ lookups         │ hourly rollups
     v                v                 v
 [Dead Letter]   [GeoIP Table]    [Metrics Store]

Legend: ( ) = process   [ ] = data store   { } = external entity
        ───> data movement, label = what moves
```

Rules:
- Every edge labeled with the data that moves (noun), never with the operation
- No control flow (no `if`); DFD shows what, not when
- Level 0 (context) = one process; Level 1 = 3-7 processes
- 1 space horizontal margin between (process) and arrows ───>

### 6.5 Sequence Diagram

Question: who calls whom, in what order. Lifelines vertical, time flows down, one column per participant.

```
[SEQUENCE - LOGIN WITH TOKEN REFRESH]

 User          Frontend        Auth Service       Database
  │               │                 │                 │
  │  submit form  │                 │                 │
  │──────────────>│                 │                 │
  │               │  POST /login    │                 │
  │               │────────────────>│                 │
  │               │                 │  SELECT user    │
  │               │                 │────────────────>│
  │               │                 │  row            │
  │               │                 │<────────────────│
  │               │  200 + JWT      │                 │
  │               │<────────────────│                 │
  │  redirect     │                 │                 │
  │<──────────────│                 │                 │
  │               │                 │                 │
  │  ──── alt: token expired ──────────────────────   │
  │               │  POST /refresh  │                 │
  │               │────────────────>│                 │
  │               │  200 + JWT      │                 │
  │               │<────────────────│                 │
  │  ───────────────────────────────────────────────  │

Legend: ───> request   <─── response   alt: = conditional block
```

Rules:
- Max 5 participants; above that, split by use case
- Messages are short verbs or endpoint names; payload detail in notes
- Return arrows for every request unless the legend says "responses omitted"
- Blocks (`alt`, `loop`, `opt`) as a labeled dashed line spanning the lifelines

### 6.6 State Machine

Question: what states exist and what event moves between them. States as boxes, transitions as labeled arrows, initial state marked.

```
[STATE MACHINE - DOCUMENT REVIEW]

 (*)
  │  create
  v
┌─────────┐   submit    ┌──────────┐   approve   ┌───────────┐
│ Draft   │────────────>│ Review   │────────────>│ Published │
└─────────┘             └──────────┘             └───────────┘
  ^                        │    │                      │
  │       reject           │    │ request changes      │ archive
  └────────────────────────┘    v                      v
                          ┌──────────┐            ┌───────────┐
                          │ Changes  │            │ Archived  │
                          └──────────┘            └───────────┘
                                │  resubmit           (final)
                                └─────────> Review

Legend: (*) = initial   (final) = terminal   arrow label = event
```

Rules:
- One box per state, one label per transition; guards in square brackets `[valid]`
- Self-transitions as a small loop arrow with label, or listed in notes
- Max 7 states; nested states as a second diagram

### 6.7 Event Flow Tree

Question: what happens after one trigger. SPEC-CT-04 format: trigger on line 1, call chain as indented tree. Best when there is one root and no cycles.

```
[EVENT FLOW - USER CLICKS "Pause"]

User clicks [Pause]
├─> controlJob(jobId, "pause")
│   └─> fetch("/jobs/{id}/control?action=pause")
│       ├─> on success
│       │   └─> updateJob(jobId, { state: "paused" })
│       │       └─> renderJobRow(jobId)       # button becomes [Resume]
│       └─> on error
│           └─> showToast("Pause failed", "error")
└─> logAction("pause", jobId)
```

Rules:
- Tier 2 form: `├─>` `└─>` `│`; Tier 1 fallback: `+->` `|`
- `#` comment for side effects the reader cannot infer from the call name
- If the tree needs a back-reference, it is a graph: switch to Section 6.4 or 6.6

### 6.8 Pipeline

Question: what are the stages and what enters/leaves each. Left-to-right boxes, artifacts between stages, side-outputs below.

```
[BUILD PIPELINE - SOURCE TO SIGNED BINARY]

 src/*.ts        bundle.js        app.exe         app.exe (signed)
    │               │                │                  │
    v               v                v                  v
┌─────────┐     ┌─────────┐     ┌───────────┐     ┌────────────┐
│ Compile │────>│ Bundle  │────>│ Package   │────>│ Sign       │
│ [tsc]   │     │ [bun]   │     │ [compile] │     │ [signtool] │
└─────────┘     └─────────┘     └───────────┘     └────────────┘
    │               │                │                  │
    v               v                v                  v
 type errors     size report     checksum          signature log

Legend: top row = input artifact   bottom row = side output   [tool] = stage tool
```

Rules:
- Inputs above, side outputs below, main artifact flows along the arrow row
- Fan-in/fan-out as a vertical bar `│` joining rows, not diagonals
- Max 6 stages per row; snake or split beyond that

### 6.9 Dependency Graph

Question: what depends on what. Arrows point from dependent to dependency. Top-down, no cycles allowed (a cycle is a bug worth drawing separately).

```
[DEPENDENCY GRAPH - PACKAGE LEVEL]

             ┌──────────┐
             │   cli    │
             └────┬─────┘
                  │
       ┌──────────┴──────────┐
       │                     │
       v                     v
  ┌──────────┐          ┌──────────┐
  │  core    │          │  render  │
  └────┬─────┘          └────┬─────┘
       │                     │
       └──────────┬──────────┘
                  │
                  v
            ┌──────────┐
            │  shared  │
            └──────────┘

Legend: A ───> B means A imports B; shared has no dependencies
```

Rules:
- Leaves at the bottom; roots (entry points) at the top
- Fan-in joins with `┬` on a horizontal bar
- Vertical arrowed lines need min length 1 `│` before the `v` tip; never place `v` directly below a junction
- Above 8 nodes: group into named clusters and draw cluster-level edges

### 6.10 Entity Relationship

Question: which entities exist, which attributes matter, how do they relate. Cardinality on the connector ends.

```
[ENTITY RELATIONSHIP - ORDERS]

┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│ Customer     │1        *│ Order        │1        *│ OrderLine    │
│──────────────│──────────│──────────────│──────────│──────────────│
│ id      PK   │          │ id      PK   │          │ id      PK   │
│ email   UQ   │          │ customer FK  │          │ order    FK  │
│ name         │          │ placed_at    │          │ product  FK  │
└──────────────┘          │ status       │          │ qty          │
                          └──────────────┘          └──────────────┘
                                                           │*
                                                           │
                                                           │1
                                                    ┌──────────────┐
                                                    │ Product      │
                                                    │──────────────│
                                                    │ id      PK   │
                                                    │ sku     UQ   │
                                                    └──────────────┘

Legend: 1 ─── * = one-to-many   PK primary key   FK foreign key   UQ unique
```

Rules:
- Entity name row, separator, attributes; keys tagged in a fixed right column
- Only attributes that matter for the point being made (max 5 per entity)
- Cardinality digits sit directly beside the connector end, inside the box border line

## 7. UX Design Diagrams

UX mockups obey stricter rules than architecture diagrams because they are the source of truth for implementation (SPEC-DG-02, SPEC-DG-05):

- Show ALL buttons and interactive elements; a missing button is a missing requirement
- Label text is the exact text the user will see; no abbreviations, no placeholders
- One component per box; overlays (toast, modal, dropdown) are drawn as separate boxes below the main screen, never nested inside it
- Whitespace is part of the design: 2-space padding, blank line between control groups
- Notation for controls (use consistently across all mockups in one document):

```
[Button]              button, label = exact text
[x] / [ ]             checkbox checked / unchecked
(o) / ( )             radio selected / unselected
[ text_______ ]       text input with placeholder or value
[ Option      v]      dropdown, closed
[=====-----] 50%      progress bar
[x]  (top right)      close control
> Item                selected list row or active tab
  Item                unselected row
Tab1 | Tab2 | Tab3    tab strip, active tab marked with > or underline row
...                   truncated content
```

All mockups use Tier 2 (`┌─┐│└─┘`, rounded `╭╮╰╯` if the UI has rounded corners), for human, LLM, and image-generation consumers alike. Examples below use Tier 2 light.

### 7.1 Screen Wireframe (Desktop)

Question: what does the page look like, which controls exist, where. Header row, action row, content, footer. Main container first, overlays after.

```
[SCREEN - JOBS OVERVIEW, DESKTOP 1280px]

┌─────────────────────────────────────────────────────────────────────────────┐
│  Logo   Jobs │ Sites │ Settings                      jane.smith  [Sign out] │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Streaming Jobs (2)                                                         │
│                                                                             │
│  [Start Job]  [Refresh]                              Toasts appear here ->  │
│                                                                             │
│  ┌────┬─────────┬──────────┬─────────┬────────────────────────────────────┐ │
│  │ ID │ Router  │ Endpoint │ State   │ Actions                            │ │
│  ├────┼─────────┼──────────┼─────────┼────────────────────────────────────┤ │
│  │ 42 │ crawler │ update   │ running │ [Monitor] [Pause / Resume] [Cancel]│ │
│  │ 41 │ crawler │ update   │ done    │ [Monitor]                          │ │
│  └────┴─────────┴──────────┴─────────┴────────────────────────────────────┘ │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Console Output                                                [Clear] │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │  [ 1 / 20 ] Processing 'document_001.pdf'...                           │ │
│  │    OK.                                                                 │ │
│  │  [ 2 / 20 ] Processing 'document_002.pdf'...                           │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Toast (separate component, bottom right, auto-dismiss 5 s):
┌───────────────────────────────────────────────┐
│  Job Started │ ID: 42 │ Total: 20 items   [x] │
└───────────────────────────────────────────────┘

Legend: [Text] = button with exact label   "Toasts appear here ->" = anchor, not visible text
```

Rules:
- Width of the mockup = 78-100 chars regardless of real screen width; state the target breakpoint in the title
- Repeating rows: show 2, then `...` if more exist
- Every `[Button]` in the mockup appears in the spec's User Actions list and vice versa

### 7.2 Modal Dialog

Question: what does the dialog ask, what can the user do. Title row, body, footer with buttons. SPEC-DG-07: primary action LEFT, secondary RIGHT, both right-aligned.

```
[MODAL - CONFIRM CANCEL JOB]

┌──────────────────────────────────────────────────────────────────────┐
│  Cancel job 42?                                                 [x]  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  The job has processed 7 of 20 items. Cancelling keeps the           │
│  7 finished items and discards the rest.                             │
│                                                                      │
│  [ ] Also delete the 7 finished items                                │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                        [Cancel job]        [Keep]    │
└──────────────────────────────────────────────────────────────────────┘

Legend: [Cancel job] = primary (destructive, red)   [Keep] = secondary
```

Rules:
- Title states the decision as a question or imperative, not "Confirmation"
- Body max 3 lines; details go to a help link
- Destructive primary buttons noted in legend so the implementer styles them

### 7.3 Form

Question: which fields, in what order, which are required, what validates. Label left or above, control right, validation message under the control.

```
[FORM - CREATE SITE]

┌──────────────────────────────────────────────────────────────────────┐
│  New Site                                                            │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Site name *     [ Marketing intranet__________________ ]            │
│                                                                      │
│  URL *           [ https://________________________________ ]        │
│                  ! Must start with https://                          │
│                                                                      │
│  Crawl depth     [ 3          v]                                     │
│                                                                      │
│  Auth method     (o) API key     ( ) Managed identity                │
│                                                                      │
│  API key *       [ ****************************___________ ] [Show]  │
│                                                                      │
│  [x] Start first crawl immediately                                   │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                            [Create site]  [Cancel]   │
└──────────────────────────────────────────────────────────────────────┘

Legend: * = required   ! = inline validation message (red)   [Show] = toggles masking
```

Rules:
- Labels in one column, controls in one column; align control left edges
- Show the validation state that matters (one error shown is enough)
- Conditional fields (API key only if API key auth) drawn in the state that shows them; note the condition

### 7.4 Table and List View

Question: which columns, which row actions, which bulk actions, how are empty and loading states shown. Draw the populated state; draw empty state as a second small mockup.

```
[TABLE - SITES LIST]

  Sites (3)                                           [ Search_______ ] [+ New]

  [ ] │ Name                 │ Status   │ Last crawl        │ Actions
  ────┼──────────────────────┼──────────┼───────────────────┼─────────────────
  [ ] │ Marketing intranet   │ active   │ 2026-01-15 14:30  │ [Crawl] [Edit]
  [x] │ HR portal            │ paused   │ 2026-01-14 09:10  │ [Resume] [Edit]
  [ ] │ Legacy wiki          │ error    │ 2026-01-10 22:05  │ [Retry] [Edit]

  1 selected   [Delete selected]                            < 1 2 3 >

Empty state:
  ┌──────────────────────────────────────────────────────────────────────┐
  │                                                                      │
  │                        No sites yet.                                 │
  │                        [+ New] to add the first one.                 │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘

Legend: [ ]/[x] row selection   status values: active | paused | error
```

Rules:
- Column headers = exact display text; sort indicator `^`/`v` after the sorted header if sorting exists
- Actions column shows the button set per status (Resume for paused, Retry for error)
- Pagination or "Load more" is a control and must appear

### 7.5 Navigation and Menu

Question: which entries exist, which is active, what nests under what. Vertical sidebar or horizontal bar; dropdowns as a separate box.

```
[NAVIGATION - SIDEBAR AND USER MENU]

Sidebar (collapsible, 240px):            User menu (opens on click of name):
┌────────────────────────┐               ┌───────────────────────────┐
│  Logo                  │               │  jane.smith               │
│                        │               │  jane.smith@example.com   │
│  > Jobs                │               ├───────────────────────────┤
│    Sites               │               │  Profile                  │
│    Domains             │               │  Preferences              │
│    Settings            │               ├───────────────────────────┤
│      General           │               │  Sign out                 │
│      API keys          │               └───────────────────────────┘
│                        │
│  [<] Collapse          │
└────────────────────────┘

Legend: > = active entry   indented = child entry   [<] = collapse control
```

Rules:
- Max 2 nesting levels drawn; deeper trees go to Section 9.1
- Active state marked on exactly one entry
- Menus that open on hover vs click: state in legend

### 7.6 Toast, Banner, Inline Notification

Question: where does feedback appear, what does it say, how does it go away. One box per notification type; position and dismissal in legend.

```
[NOTIFICATIONS - THREE TYPES]

Toast (bottom right, stack upward, auto-dismiss 5 s, hover pauses):
┌─────────────────────────────────────────────────┐
│  i  Job Started │ ID: 42 │ Total: 20 items  [x] │
└─────────────────────────────────────────────────┘

Banner (top of content, persistent until dismissed):
┌───────────────────────────────────────────────────────────────────────┐
│  !  Your API key expires in 3 days.  [Renew key]                 [x]  │
└───────────────────────────────────────────────────────────────────────┘

Inline (under the failing control, no dismissal):
  API key *   [ ******************* ]
              ! Key rejected by provider (401)

Legend: i = info (blue)   ! = warning/error (amber/red)   [x] = dismiss
```

### 7.7 CLI and Terminal UI

Question: what does the terminal show during and after a command. Fixed 80 columns. Announce, track, report pattern. Prompt line included.

```
[TERMINAL - CRAWL COMMAND, 80 COLUMNS]

$ app crawl --site "Marketing intranet"
Crawling site 'Marketing intranet'...
  3 libraries found.
  [ 1 / 3 ] Processing library 'Documents'...
    342 files retrieved.
    12 added, 3 changed, 0 removed.
    OK.
  [ 2 / 3 ] Processing library 'Reports'...
    ERROR: Access denied -> (403) Forbidden
  [ 3 / 3 ] Processing library 'Archive'...
    88 files retrieved.
    0 added, 0 changed, 0 removed.
    OK.
PARTIAL FAIL: 2 libraries processed, 1 failed.
$ _

Interactive REPL frame (full-screen TUI):
┌──────────────────────────────────────────────────────────────────────────────┐
│  app 2.1.0   session: 2026-01-15_14-30   model: gpt-x        [Ctrl+C] quit   │
├──────────────────────────────────────────────────────────────────────────────┤
│  > read src/index.ts                                                         │
│  Reading src/index.ts (212 lines)...                                         │
│  OK.                                                                         │
│                                                                              │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  > _                                                                         │
└──────────────────────────────────────────────────────────────────────────────┘

Legend: $ = shell prompt   > = app prompt   _ = cursor   [Ctrl+C] = keybinding hint
```

Rules:
- Exactly 80 columns for the frame; content lines never exceed 78
- Indentation = nesting of the operation (2 spaces per level)
- Show one success path and one failure path

### 7.8 Mobile Screen

Question: same as 7.1 but for a narrow viewport. 40-44 chars wide, tall. Bottom tab bar, hamburger, FAB drawn explicitly.

```
[MOBILE - JOBS LIST, 390px]

┌──────────────────────────────────────────┐
│  9:41                           *  ││││  │
├──────────────────────────────────────────┤
│  [=]   Jobs                        [+]   │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  #42  crawler / update             │  │
│  │  running   7 / 20                  │  │
│  │  [====──────]                      │  │
│  │               [Pause]  [Cancel]    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  #41  crawler / update             │  │
│  │  done   20 / 20                    │  │
│  │  [==========]                      │  │
│  │                        [Monitor]   │  │
│  └────────────────────────────────────┘  │
│                                          │
│                                          │
├──────────────────────────────────────────┤
│   Jobs      Sites     Settings    More   │
│    *                                     │
└──────────────────────────────────────────┘

Legend: [=] hamburger   [+] new job   * under tab = active   status bar row = OS chrome
```

### 7.9 Screen Flow (User Journey)

Question: how does the user move between screens, which action triggers each transition. Screens as boxes with 1-2 word names, arrows labeled with the triggering action.

```
[SCREEN FLOW - FIRST CRAWL]

┌──────────┐  [+ New]   ┌───────────┐  [Create site]  ┌───────────┐
│ Sites    │───────────>│ New Site  │────────────────>│ Site      │
│ (empty)  │            │ (form)    │                 │ Detail    │
└──────────┘            └─────┬─────┘                 └─────┬─────┘
                              │                             │
                              │ [Cancel]                    │ [Crawl]
                              v                             v
                        ┌───────────┐                 ┌───────────┐
                        │ Sites     │                 │ Job       │
                        │ (list)    │<────────────────│ Monitor   │
                        └───────────┘   job done      └───────────┘

Legend: box = screen   arrow label = user action [Button] or system event
```

Rules:
- Arrow label = the button the user presses, in exact text, or a system event in lowercase
- Max 7 screens; one flow per goal
- Error and cancel paths included when they lead to a different screen

### 7.10 BEFORE / AFTER

Question: what changes. SPEC-DG-04: the two states are adjacent, same width, same structure, only the delta differs. A one-line caption states the change.

```
[HEADER ROW - AUTH BUTTONS ADDED]

BEFORE:
┌─────────────────────────────────────────────────────────────────────────┐
│  Sites (3)  [Reload]                                                    │
│  Back to Main Page │ Domains │ Sites │ Jobs                             │
└─────────────────────────────────────────────────────────────────────────┘

AFTER:
┌─────────────────────────────────────────────────────────────────────────┐
│  Sites (3)  [Reload] [OpenAI (API Key)] [SharePoint (Managed Identity)] │
│  Back to Main Page │ Domains │ Sites │ Jobs                             │
└─────────────────────────────────────────────────────────────────────────┘

Change: two auth status buttons added to the header row, right-aligned. Nothing else moves.
```

Rules:
- Same box width, same row order, so the eye finds the delta by scanning
- Applies to UI, data schemas, API payloads, architecture (Section 6 diagrams side by side)
- Never place BEFORE and AFTER in different sections of a document

## 8. Charts

Charts encode quantity. In monospace text every character is one unit, so precision is limited to the width you have. Rules that apply to all charts:

- **Value printed next to every bar or point.** The bar shows proportion; the number carries the fact
- **Scale stated once**: `1 char = 100 units` or a labeled axis
- **Sorted** by value unless the category order carries meaning (time, sequence)
- **Max 8 categories**; group the rest into `Other`
- **Fill characters**: `#` or `=` for ASCII-only pipelines; `█ ▓ ▒ ░` for Unicode (fixed single-cell width, safe for all consumers)
- **Structured data alongside** (llm-transcription rule): when the chart is a transcription or feeds a model, add the values as a JSON line after the legend
- **Never a pie chart.** Angles cannot be drawn in text; use a proportion bar (8.5)

### 8.1 Horizontal Bar Chart

Best default. Bars filled with Tier 3 blocks (fixed single-cell width). Labels stay horizontal and readable, bars grow to the right, values fit at the end.

```
[BAR CHART - REQUESTS PER ENDPOINT, LAST 24 H]

/api/search    ████████████████████████████████████████████  4,420  (44 %)
/api/items     ██████████████████████████                    2,610  (26 %)
/api/login     ██████████████                                1,380  (14 %)
/api/export    ████████                                        820  ( 8 %)
Other          ████████                                        790  ( 8 %)
                                                     Total  10,020

Scale: 1 █ = 100 requests
```

Multi-color horizontal bars (stacked segments, one bar per row, each segment a distinct shade):

```
[BAR CHART - STORAGE BY TYPE AND TIER, GB]

/docs    ████████████████████▓▓▓▓▓▓▒▒▒░░  120  (hot 80  warm 24  cold 16)
/images  ████████████▓▓▓▓▒▒░░              72  (hot 48  warm 16  cold 8)
/video   ████▓▓▓▓▓▓▓▓▒▒▒▒▒▒░░░░          140  (hot 16  warm 32  cold 92)
/logs    ░░░░░░░░░░░░░░░░░░░░              48  (cold 48)

Legend: █ hot (SSD)   ▓ warm (HDD)   ▒ cold (tape)   ░ archive (glacier)
```

Rules:
- Labels left-padded to equal width; bars start in the same column
- Values right-aligned in one column; percentages in a second column if useful
- Total or reference value on its own row when meaningful
- Multi-color: max 4 shades per bar, legend maps shade to category

### 8.2 Vertical Bar Chart and Histogram

Use only when the x-axis is ordinal (time buckets, size classes) and comparing heights matters more than reading labels. Height 8-12 rows.

```
[HISTOGRAM - RESPONSE TIME DISTRIBUTION, ms]

count
 40 │                 ██
 35 │                 ██
 30 │            ██   ██
 25 │            ██   ██   ██
 20 │       ██   ██   ██   ██
 15 │       ██   ██   ██   ██   ██
 10 │  ██   ██   ██   ██   ██   ██
  5 │  ██   ██   ██   ██   ██   ██   ██
  0 └──────────────────────────────────────
      <50  100  150  200  250  300  >300
                 bucket upper bound (ms)

Values: 8, 18, 30, 40, 26, 15, 5   n = 142   p50 = 180 ms
```

Rules:
- Bars 2 chars wide, 3 chars apart; y-axis labels right-aligned
- Values row under the chart because reading heights is imprecise
- Never rotate labels; if labels do not fit, use 8.1

Multi-color vertical bars (stacked segments per column, each segment a distinct shade):

```
[STACKED BAR - DEPLOYMENTS BY ENV AND RESULT, LAST 6 WEEKS]

count
 12 │                 ██
 10 │            ▓▓   ██   ██
  8 │       ▓▓   ▓▓   ██   ▓▓
  6 │  ██   ▓▓   ▒▒   ▓▓   ▓▓   ██
  4 │  ██   ▒▒   ▒▒   ▒▒   ▒▒   ▓▓
  2 │  ░░   ░░   ░░   ░░   ░░   ░░
  0 └──────────────────────────────────
     W1   W2   W3   W4   W5   W6

Legend: █ prod   ▓ staging   ▒ dev   ░ failed
Values: W1 2p 0s 1d 1f   W2 0p 2s 1d 1f   W3 1p 2s 2d 0f
        W4 2p 1s 1d 0f   W5 0p 2s 2d 1f   W6 2p 1s 0d 1f
```

Rules:
- Bars 2 chars wide, 3 chars apart; y-axis labels right-aligned
- Values row under the chart because reading heights is imprecise
- Never rotate labels; if labels do not fit, use 8.1
- Multi-color: stack shades bottom-to-top, legend maps shade to category

Grouped vertical bars (3 bars per category, side-by-side comparison):

```
[GROUPED BAR - RESPONSE TIME BY PROVIDER, ms, p50/p90/p99]

  ms
 300 │      ██             ▓▓
 250 │      ██             ▓▓             ▒▒
 200 │      ██             ▓▓             ▒▒
 150 │  ██  ██         ▓▓  ▓▓             ▒▒
 100 │  ██  ██         ▓▓  ▓▓  ▓▓         ▒▒  ▒▒
  50 │  ██  ██  ██     ▓▓  ▓▓  ▓▓         ▒▒  ▒▒  ▒▒
   0 └──────────────────────────────────────────────────────
       OpenAI            Anthropic            Z.AI
       p50 p90 p99     p50 p90 p99       p50 p90 p99

Legend: █ OpenAI   ▓ Anthropic   ▒ Z.AI   (lower is better)
Values: OpenAI 40/120/280   Anthropic 60/150/260   Z.AI 30/90/220
```

Rules:
- Bars 2 chars wide, 2 chars gap within group, 4 chars between groups
- One shade per category (provider), 3 bars per category for sub-metrics
- Category label centered under each group; sub-labels under each bar
- Max 4 bars per group, max 5 groups; beyond that use a table (8.6)
- Multi-color: stack shades bottom-to-top, legend maps shade to category

### 8.3 Line Chart and Sparkline

Trend over time. Plot with `*` or `o`, connect only if the reader must see slope. For a quick inline trend use a one-row sparkline.

```
[LINE CHART - DAILY ACTIVE USERS, 14 DAYS]

users
1200 │                                          *
1100 │                                    *  *
1000 │                              *  *
 900 │                        *  *
 800 │        *  *  *   *  *
 700 │  *  *
 600 └────────────────────────────────────────────────
      01 02 03 04 05 06 07 08 09 10 11 12 13 14  (day)

Sparkline:  _..--''""^   (low -> high)   min 690  max 1,210  last 1,210
```

Rules:
- One series per chart in text; two series only with distinct markers (`*` and `o`) and a legend
- ASCII sparkline alphabet, low to high: `_ . - ' " ^` (6 levels); in Tier 2 documents prefer the block sparkline `▁▂▃▄▅▆▇█` (Section 8.10)
- Include min, max, last values with every sparkline

### 8.4 Timeline and Gantt

When does what happen, how long, what overlaps. One row per item, one column per time unit, `▄` for duration, `◆` for milestone (Tier 1 fallback: `=` and `|`).

```
[GANTT - RELEASE PLAN, WEEKS]

                    W1   W2   W3   W4   W5   W6   W7   W8
Spec review         ▄▄▄▄
Implementation           ▄▄▄▄▄▄▄▄▄▄▄▄▄
Test automation                    ▄▄▄▄▄▄▄▄▄
Docs                                    ▄▄▄▄▄▄▄▄▄
Beta                                              ▄▄▄▄◆
Release                                                   ◆

Legend: ▄▄▄▄ duration   ◆ milestone   1 column = 1 week (5 chars)
```

Timeline variant (events on a line):

```
[TIMELINE - INCIDENT 2026-01-15]

14:02        14:05          14:11             14:30            15:10
  │            │              │                 │                │
  v            v              v                 v                v
alert      on-call        root cause         hotfix          postmortem
fired      paged          found              deployed        scheduled
```

Rules:
- Time unit width fixed (5 chars per week here); label the unit once
- Dependencies as indentation order, not as arrows (arrows clutter)
- Milestones as `◆` at the end of the last bar or alone

### 8.5 Proportion Bar (Pie Replacement)

Parts of a whole in one row. Each segment a distinct fill char, legend maps char to category.

```
[PROPORTION - STORAGE BY FILE TYPE, 100 GB]

│██████████████████████▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒░░░░░░░░│
 0%                  40%                60%          80%      100%

Legend: █ PDF 40 GB (40 %)   ▓ Images 20 GB   ▒ Video 24 GB   ░ Other 16 GB
```

Rules:
- Bar length 50 or 100 chars so 1 char = 2 % or 1 %
- Order segments largest first unless categories are ordinal
- Max 5 segments; below 3 % becomes `Other`

### 8.6 Matrix and Heatmap

Two short enumerations against each other; cell holds a symbol or a number. Replaces a comparison table when DevSystem forbids Markdown tables.

```
[MATRIX - FEATURE SUPPORT BY PROVIDER]

                 Streaming  Tools  Vision  Caching  Reasoning
Provider A          Y         Y      Y       Y        Y
Provider B          Y         Y      Y       P        Y
Provider C          Y         Y      N       N        P
Provider D          P         N      N       N        N

Legend: Y = yes   P = partial   N = no
```

Heatmap variant with density fill:

```
[HEATMAP - ERRORS PER HOUR AND WEEKDAY]

        00 03 06 09 12 15 18 21
Mon      ░  ░  ░  ▒  █  █  ▒  ░
Tue      ░  ░  ░  ▒  █  ▓  ▒  ░
Wed      ░  ░  ░  ▒  █  █  ▒  ░
Thu      ░  ░  ░  ▒  ▓  ▓  █  ░
Fri      ░  ░  ░  ▒  █  █  ▒  ░
Sat      ░  ░  ░  ░  ░  ░  ░  ░
Sun      ░  ░  ░  ░  ░  ░  ░  ░

Scale: ░ 0-4   ▒ 5-9   ▓ 10-19   █ 20-49   ◆ 50+   (errors per hour)
```

Rules:
- Column headers of equal width; cells centered under them
- Symbol alphabet max 5 levels; state the scale
- Above 8x8 cells, split by row group

### 8.7 Funnel

Stages with shrinking counts. Centered bars, count and conversion per stage.

```
[FUNNEL - SIGNUP CONVERSION]

Visited        ████████████████████████████████████████████  10,000
Signed up             ████████████████████████████          5,200   52 %
Verified email            ██████████████████████              3,900   75 %
Created project               ██████████████                  2,100   54 %
Paid                              ██████                        640   30 %

Percent = conversion from previous stage
```

### 8.8 Quadrant

Two binary or scalar axes, items placed in four cells. Axis labels at the ends.

```
[QUADRANT - EFFORT VS IMPACT]

              high impact
                   ^
                   │
   Quick wins      │     Major projects
   # cache layer   │     # new billing
   # fix login     │     # data migration
                   │
 low effort <──────┼──────> high effort
                   │
   Fill-ins        │     Thankless tasks
   # rename fields │     # legacy port
                   │
                   v
              low impact
```

Rules:
- Max 3 items per cell; more means the quadrant is not the right encoding
- Cell titles in a fixed corner position; items as `#` list

### 8.9 Venn and Set Overlap

Two or three sets with shared members. Text cannot draw circles well; use overlapping brackets or a membership matrix.

```
[SET OVERLAP - USERS BY CHANNEL]

   Web only      Web + Mobile     Mobile only
  [ 3,200   [       850       ]     1,100   ]
  <─────── Web 4,050 ────────>
             <──────── Mobile 1,950 ────────>
```

For three sets use the matrix form (8.6) with `Y/N` per set; the visual Venn is not worth the alignment cost.

### 8.10 Block Sparkline (Eighth Blocks)

One row, one glyph per bucket, 8 levels. The [Textual Sparkline](https://textual.textualize.io/widgets/sparkline/) pattern: data is split into `width` buckets, each bucket summarized (max, mean, min, last), summary mapped to `▁▂▃▄▅▆▇█`. Tier 4, line-pure (blocks are fixed width, so a label on the same line is tolerated in human docs; keep labels on their own line for LLM consumers).

```
[SPARKLINE - LATENCY p95, 40 BUCKETS OF 90 s]

▁▁▂▂▃▃▄▅▆▇███▇▆▅▄▄▅▆▇███▇▆▄▃▂▂▁▁▁▂▃▄▄▃▂▁
min 120 ms   max 980 ms   last 140 ms   summary = max per bucket
```

Rules:
- State the summary function; `max` shows spikes, `mean` hides them
- Always print min, max, last under the line
- Three sparklines stacked = a compact multi-metric panel; align their start columns

### 8.11 Block Area Chart (Stacked Eighth Rows)

Several rows of eighth blocks give 8 x rows levels. Each row shows the slice of the value that falls in its band; lower rows are solid `█` under any taller column. This is the Dolphie dashboard style (Textual-based MySQL monitor).

```
[AREA CHART - CPU %, 40 SAMPLES, 3 ROWS = 24 LEVELS]

100 %                                   ▕
      ▁▃▅▆▇██▇▅▂     ▂▄▆▇▇▆▄▁           ▕
    ▃▆██████████▇▅▄▅▇████████▆▃▁        ▕
▂▃▅█████████████████████████████▇▆▅▄▃▂▁▁▕
0 %                                  now▕
```

Rules:
- Axis labels on separate lines above and below, never left of the block rows (keeps rows line-pure and start columns identical)
- Rows x 8 = resolution; 3-4 rows is enough for a dashboard panel
- Close every row with a right-edge tick `▕` (or a Tier 2 frame as in 8.15). Without it the rows end in trailing spaces, which editors strip and Section 3.1 forbids
- Not for image generation: the model reads block rows as texture, not as values. Give numbers in prose instead

### 8.12 Braille Line Plot and Scatter

2 x 4 dots per cell. Generated, not hand-drawn: use [plotille](https://github.com/tammoippen/plotille) (Python), [drawille](https://github.com/asciimoo/drawille), or a 40-line script that sets bits `0x2800 + dots` (bit layout in Section 2.4). Axis labels on separate lines.

```
[LINE PLOT - ADOPTION CURVE (solid) vs BASELINE (dotted), 44 x 5 CELLS = 88 x 20 DOTS]

100 %
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠤⠒⠒⠊⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⠊⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡀⠠⠀⠂⠈⠀⠁⠐⠀⠄⢀⠀⠀⠀⠀⠀⣀⠤⠒⠉⠀⠀⠠⠀⠂⠐⠀⠁⠈⠀⠂⠠⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀
⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠤⠤⠥⠒⠊⠍⠠⠀⠂⠐⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠂⠠⠀⠄⠐⠀⠁
0 %                                          week 12
Legend: continuous dots = adoption   every third dot = baseline

[SCATTER - LATENCY vs PAYLOAD SIZE, 40 x 5 CELLS, n = 90]

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠠⠠⡀⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⢀⠀⠀⠀⠀⡀⡀⡠⢈⠄⠊⠀⠀⡠⠀⠀⠈⠑⠀
⠀⠀⠀⠀⠀⠀⢀⠀⢀⠀⠀⠀⡐⢠⡀⡐⡐⢠⠈⠄⠃⡁⠠⠐⠐⠀⠂⠈⠃⠀⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠐⠀⠂⡐⡚⠠⠑⡃⠀⡀⠈⠆⠡⠂⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠠⠀⠁⠀⠉⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
0 KB                                                 2 MB
Legend: one dot = one request   x = payload size   y = latency (0-800 ms)
```

Braille histogram (bars 3 dots wide, 1 dot gap, 4 rows = 16 levels):

```
⠀⠀⠀⠀⠀⠀⠀⠀⣶⡆⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⣿⡇⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⣿⡇⣿⡇⣶⡆⣀⡀⠀⠀⠀⠀⠀⠀⣤⡄⣿⡇⣿⡇⣿⡇⣿⡇⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⣀⡀⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣶⡆⣤⡄⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣤⡄⠀⠀⠀⠀
⣶⡆⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣿⡇⣤⡄
values: 3 5 8 12 15 14 11 9 7 6 8 10 13 16 15 12 9 6 4 2
```

Rules:
- Braille is for human terminals and rich Markdown viewers. Not for LLM or image-generation consumers: models see noise, not a curve. Ship the numbers alongside
- Pad with `⠀` (U+2800), never with space; the line must be braille-only
- Two series: solid vs dotted (every 2nd or 3rd dot), or two separate plots. Color is the usual third channel in terminals and is lost in Markdown
- Generate, then paste. Hand-drawing braille is error-prone; a bit error moves a dot silently

### 8.13 Braille Picture Rendition

Any bitmap becomes braille at 2 x 4 pixels per cell: threshold to black/white, map each 2 x 4 block to one glyph. An 80 x 80 pixel image becomes 40 x 20 cells. Use for icons, logos, silhouettes, QR-like patterns in terminal UIs and README headers.

```
[PICTURE - PLAY BUTTON ICON, 24 x 8 CELLS = 48 x 32 PIXELS]

⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡾⠛⠉⠀⠀⠀⠀⠉⠛⢷⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⡟⠀⠀⣷⣦⣀⠀⠀⠀⠀⠀⢻⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠀⠀⠀⣿⣿⣿⣷⣦⣄⠀⠀⠀⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⠀⠀⠀⣿⣿⣿⡿⠟⠋⠀⠀⠀⣿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢹⣧⠀⠀⡿⠟⠉⠀⠀⠀⠀⠀⣼⡏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⢷⣤⣀⠀⠀⠀⠀⣀⣤⡾⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
```

Rules:
- Source image: high contrast, no gradients, subject fills the frame; resize so width in pixels = 2 x cells
- Threshold at the median grey value for balanced pictures; `inverse` for dark backgrounds
- Cells are about 2:1 tall; a square source image needs `cells_wide = 2 x cells_high` to look square (48 x 32 pixels = 24 x 8 cells)
- Alternative for coarser pictures: quadrant blocks `▖▗▘▝▞▚▜▛▙▟█` (2 x 2 per cell) or shades `░▒▓█` for greyscale (Section 2.4). Quadrants tolerate mixing with Tier 2 lines; braille does not

### 8.14 Big Digits and KPI Tiles

Numbers that must be read from across the room: dashboards, timers, counters. The [Textual Digits](https://textual.textualize.io/widgets/digits/) 3 x 3 font builds every digit from Tier 2 line pieces, so a digit row is Tier 2 line-pure and can sit inside a Tier 2 frame.

```
Font (light):  0     1     2     3     4     5     6     7     8     9     :   .
              ╭─╮   ╶╮    ╶─╮   ╶─╮   ╷ ╷   ╭─╴   ╭─╴   ╶─┐   ╭─╮   ╭─╮
              │ │    │    ┌─┘    ─┤   ╰─┤   ╰─╮   ├─╮     │   ├─┤   ╰─┤    :
              ╰─╯   ╶┴╴   ╰─╴   ╶─╯     ╵   ╶─╯   ╰─╯     ╵   ╰─╯   ╶─╯       •

Bold variant uses heavy pieces: ┏━┓ ┃ ┃ ┗━┛ ╺┓ ╺┻╸ ...
```

KPI tile (frame, label, big number, trend sparkline, delta):

```
[KPI TILE - REQUESTS PER SECOND]

┌──────────────────────────────┐
│  Requests / s                │
│                              │
│    ╶╮ ╶─╮╭─╮╭─╮              │
│     │ ┌─┘│ ││ │              │
│    ╶┴╴╰─╴╰─╯╰─╯              │
│                              │
│  ▁▂▃▅▆▇▇█▇▆▅▅▆▇█    +12 %    │
└──────────────────────────────┘

Timer row (Textual stopwatch style, three rows per digit line):

  ╭─╮╭─╮ ╭─╮╭─╮ ╶╮ ╭─╴ ╶╮ ╶─╮
  │ ││ │:│ ││ │: │ ├─╮  │ ┌─┘
  ╰─╯╰─╯ ╰─╯╰─╯ ╶┴╴╰─╯•╶┴╴╰─╴
  00 : 00 : 16 . 12
```

Rules:
- Each glyph is exactly 3 cells wide (pad with spaces); `:` and `.` are 1-3 cells per the font table
- One big number per tile; 3-6 tiles per dashboard row
- Small caption above, delta and sparkline below; the number is the largest element
- Plain-text fallback for LLM consumers: write the number plainly, `1200 req/s (+12 %)`; a 3-row Tier 1 digit font (`###`, `#  `, `###`) is readable but wastes space

### 8.15 Dashboard Layout (Panels)

A dashboard is a grid of panels; each panel is one of the chart types above with a title row. The Dolphie layout: a header strip, a row of 4-5 fixed-width info panels, a wide graph area split in 2-4 tiles, a full-width table at the bottom.

```
[DASHBOARD - SERVICE HEALTH, 100 COLUMNS]

┌[ Host ]───────────────┐┌[ Utilization ]────────┐┌[ Storage ]───────────┐┌[ Errors/s ]──────────┐
│ Version  2.1.0        ││ CPU      89 %         ││ Used     12.7 GB     ││ 4xx      21          │
│ Uptime   9 d 18 h     ││ Load     11.9 10.1    ││ Free     19.3 GB     ││ 5xx       0          │
│ Replicas 2            ││ Memory   40 %         ││ IOPS R/W 3.3K/21K    ││ Timeouts  3          │
└───────────────────────┘└───────────────────────┘└──────────────────────┘└──────────────────────┘
┌[ CPU % ]───────────────────────────────────────┐┌[ Memory GB ]─────────────────────────────────┐
│                                                ││                                              │
│       ▁▃▅▆▇██▇▅▂     ▂▄▆▇▇▆▄▁                  ││ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   │
│     ▃▆██████████▇▅▄▅▇████████▆▃▁               ││                                              │
│ ▂▃▅█████████████████████████████▇▆▅▄▃▂▁▁       ││ 0 ─────────────────────────────────── 32 GB  │
│ 15:34:05          15:34:36          15:35:08   ││ 15:34:05          15:34:36         15:35:08  │
└────────────────────────────────────────────────┘└──────────────────────────────────────────────┘
┌[ Processlist (4) ]─────────────────────────────────────────────────────────────────────────────┐
│ ID    User      Command   State         Age       Query                                        │
│ 1381  msandbox  Query     System lock   00:00:00  SELECT quantity FROM stock WHERE id = 78489  │
│ 1377  msandbox  Query     statistics    00:00:00  SELECT price, name FROM item WHERE id = 44   │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Rules:
- Panel title inside the top border: `┌─[ Title ]──┐`; saves one row per panel
- All panels in a row have equal height; widths may differ but the row must sum to the same total
- Block rows inside Tier 2 frames are safe (blocks are fixed width); braille inside frames is not (Section 2.4). For a braille panel, draw the frame rows above and below only, or accept Western-font-only rendering
- Tables at the bottom, graphs in the middle, scalars on top: eye goes to numbers first
- Image generation: describe the grid ("2 x 2 panels, header strip, footer table") in prose; the model will not reproduce block glyphs

### 8.16 Infographic Elements

Small visual encodings that make a text infographic scan like a designed one. Each element is one to three lines; combine 3-5 of them under one title.

```
[INFOGRAPHIC ELEMENTS - CATALOG]

Stat callout (number first, unit and label second):
      4,420           98.6 %          17 ms
   requests/day     uptime, 30 d    p50 latency

Chevron process (steps as arrows):
   [ Collect ]─>[ Clean ]─>[ Train ]─>[ Evaluate ]─>[ Ship ]

Numbered steps with one-line detail:
   (1) Collect ──── pull 30 days of logs
   (2) Clean ────── drop bots, dedupe
   (3) Train ────── 3 models, 5-fold CV

Harvey balls (0 / 25 / 50 / 75 / 100 %):
   ASCII:    ( )  (.)  (o)  (O)  (*)
   Unicode:  ○  ◔  ◑  ◕  ●        <- own line only (ambiguous width)

Star rating:
   ASCII:    ****.   (4 of 5)
   Unicode:  ★★★★☆                <- own line only

Stacked bar (parts of several wholes):
   Q1  ██████████▓▓▓▓▒▒▒▒░░░░   100 = 40 █ / 20 ▓ / 15 ▒ / 25 ░
   Q2  ████████████▓▓▓▓▓▒▒▒░░
   Q3  ██████████████▓▓▓▓▒▒░░

Waffle chart (10 x 10 = 1 % per cell):
   ██████████   Legend: █ paid 62 %
   ██████████           ▓ trial 23 %
   ██████████           ░ free 15 %
   ██████████
   ██████████
   ██████████
   ██▓▓▓▓▓▓▓▓
   ▓▓▓▓▓▓▓▓▓▓
   ▓▓▓▓▓░░░░░
   ░░░░░░░░░░  (draw 62 / 23 / 15 cells exactly; count before publishing)

Dot plot (one mark per item, compare groups):
   Team A  . . . . . . . .            n = 8
   Team B  . . . . . . . . . . . .    n = 12
   Team C  . . .                      n = 3

Bullet chart (value bar, target tick, qualitative bands):
   Sales   [████████████████████│█████      ]  target │  bands ░ low, ▒ ok, █ good
            ░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒██████████

Slope chart (two time points, one line per item):
   2025          2026
   42  ──────────>  61   Search
   38  ──────────>  35   Items
   12  ──────────>  27   Export

Waterfall (running total, + and - steps):
   Start   │██████████                       │ 100
   + Sales │          ██████                 │ +60
   - Costs │               ████              │ -40
   + Grant │                   ██            │ +20
   End     │██████████████                   │ 140

Box plot (min, Q1, median, Q3, max):
   Latency  │─────[████│███████]─────────────│
            0    45   80      140          400 ms

Tally / count marks:
   Mon  ││││ ││││ ││     12
   Tue  ││││ │││         8

Comparison bars (two values, mirrored around a center axis):
   Mobile  ████████████████████│████████████  Desktop
                 2,010         │     1,240
```

Rules:
- One idea per element; an infographic is 3-5 elements under one title, not a page of them
- Numbers always printed; the shape is redundancy, not the source of truth
- Unicode symbol rows (Harvey balls, stars, ● ○ ■ □) stay on their own line: East-Asian ambiguous width breaks any frame they sit in
- For image generation: name the element ("a waffle chart with 62 filled cells of 100") and give the numbers; do not expect the model to count `█`

## 9. Other Diagram Types

### 9.1 Tree and Hierarchy

Containment or parent-child without cycles: file systems, org charts, menus, taxonomies. Tier 2 form: `├──` `└──` `│`; Tier 1 fallback: `+--` and `|`.

```
[FILE TREE - PROJECT LAYOUT]

project/
├── src/
│   ├── index.ts            # entry point
│   ├── core/
│   │   ├── executor.ts
│   │   └── events.ts
│   └── tools/
│       ├── read_file.ts
│       └── run_command.ts
├── test/
│   └── executor.test.ts
├── package.json
└── README.md
```

Org chart / horizontal hierarchy:

```
[ORG - PRODUCT TEAM]

                  ┌───────────┐
                  │ Lead      │
                  └─────┬─────┘
          ┌─────────────┴─────────────┐
          │             │             │
          v             v             v
    ┌───────────┐ ┌───────────┐ ┌───────────┐
    │ Backend   │ │ Frontend  │ │ QA        │
    │ 3 eng     │ │ 2 eng     │ │ 1 eng     │
    └───────────┘ └───────────┘ └───────────┘
```

Rules:
- Last child uses `└──` so the branch visibly ends; the Tier 1 fallback has no distinct glyph (`+--` for every child)
- `#` comment for purpose, right-aligned in one column
- Depth max 4; deeper trees are split at a subtree root

### 9.2 Mind Map

One central topic, radiating branches, no cross-links. Text form is a two-sided tree: left branches and right branches around a center box.

```
[MIND MAP - RELEASE READINESS]

  Tests pass ───┐                            ┌─── Release notes
  Lint clean ───┼── Quality          Docs ───┼─── Changelog
                │                            │
                │     ┌─────────────┐        │
                ├─────│   Release   │────────┤
                │     └─────────────┘        │
                │                            │
Version bump ───┼── Packaging     Publish ───┼─── Signed binary
  Checksums  ───┘                            └─── Upload to release page
```

Rules:
- Max 4 branches per side, 3 leaves per branch
- Beyond that, it is an outline: use a nested list

### 9.3 Decision Tree and Flowchart

Branching logic with one start. Diamond decisions approximated by `< >` or `/ \`; keep the main path vertical, branches to the right.

```
[FLOWCHART - RETRY POLICY]

        ┌───────────┐
        │ Call API  │
        └─────┬─────┘
              │
              v
        / Succeeded? \──── Yes ────>  ┌─────────┐
        \            /                │ Return  │
         ─────┬──────                 └─────────┘
              │ No
              v
        / Attempts < 3? \── No ────>  ┌─────────┐
        \               /             │ Fail    │
         ──────┬────────              └─────────┘
               │ Yes
               v
        ┌──────────────┐
        │ Wait 2^n s   │
        └──────┬───────┘
               │
               └────────────> back to "Call API"

Legend: / \ = decision   Yes/No = branch   2^n = exponential backoff
```

Compact form for LLM consumers (indent instead of draw):

```
Call API
├── Succeeded?  Yes -> Return
└── No
    ├── Attempts < 3?  No -> Fail
    └── Yes -> Wait 2^n s -> back to Call API
```

Rules:
- Main (happy) path vertical; exceptions branch right
- Loops as a labeled text arrow ("back to X"), not a drawn line crossing the diagram
- Max 6 decisions; more = split by phase

### 9.4 Swimlane

Who does which step. One lane per actor, steps left to right, handoffs as arrows crossing lane borders.

```
[SWIMLANE - PULL REQUEST FLOW]

Author    │ ┌───────────┐                              ┌───────────┐
          │ │ Open PR   │────────┐            ┌───────>│ Fix       │
          │ └───────────┘        │            │        └─────┬─────┘
──────────┼──────────────────────│────────────│──────────────│────────
CI        │                      v            │              v
          │                ┌───────────┐      │        ┌───────────┐
          │                │ Run tests │──────┴───────>│ Run tests │
          │                └─────┬─────┘   fail        └─────┬─────┘
──────────┼──────────────────────│───────────────────────────│────────
Reviewer  │                      │ pass                      │ pass
          │                      v                           v
          │                ┌───────────┐               ┌───────────┐
          │                │ Review    │──────────────>│ Merge     │
          │                └───────────┘   approve     └───────────┘
```

Rules:
- Lanes horizontal, actors in a fixed left column, lane separators full width
- Max 4 lanes, 8 steps
- Every arrow that crosses a lane is a handoff and gets a label

### 9.5 Network Topology

Nodes and links with addresses or protocols. Similar to 6.3 but network-centric: zones as boxes, links labeled with protocol/port.

```
[NETWORK - DMZ AND INTERNAL ZONE]

  Internet
     │
     │ 443
     v
┌─[ DMZ ]─────────────────────────┐
│  ┌────────────┐                 │
│  │ Reverse    │                 │
│  │ Proxy      │                 │
│  └─────┬──────┘                 │
└────────│────────────────────────┘
         │ 8080
         v
┌─[ Internal ]────────────────────┐
│  ┌────────────┐   5432   ┌────┐ │
│  │ App Server │─────────>│ DB │ │
│  └────────────┘          └────┘ │
└─────────────────────────────────┘

Legend: number on link = TCP port   zone box = firewall segment
```

### 9.6 Memory and Byte Layout

Field positions in a record, packet, or struct. Offsets on the left, field width proportional or annotated.

```
[BYTE LAYOUT - MESSAGE HEADER, 12 BYTES]

offset  0        1        2        3
       ┌────────┬────────┬────────┼────────┐
  0    │ version│ flags  │      length     │
       ├────────┴────────┴────────┼────────┤
  4    │               message id          │
       ├────────┼────────┼────────┼────────┤
  8    │               timestamp           │
       └────────┼────────┼────────┼────────┘

Legend: one cell = 1 byte   multi-byte fields big-endian
```

### 9.7 Kanban Board

Columns as states, cards as boxes. Snapshot of work in progress.

```
[KANBAN - SPRINT 14]

  To Do (3)          In Progress (2)     Review (1)          Done (4)
┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ #51 Rate limit│  │ #48 Retry     │  │ #47 Auth fix  │  │ #40 Logging   │
├───────────────┤  │ logic         │  └───────────────┘  ├───────────────┤
│ #52 Metrics   │  ├───────────────┤                     │ #42 Config    │
├───────────────┤  │ #50 Docs      │                     ├───────────────┤
│ #53 Export    │  └───────────────┘                     │ #44 CLI help  │
└───────────────┘                                        ├───────────────┤
                                                         │ #45 Selftest  │
                                                         └───────────────┘
```

### 9.8 Comparison as List (Table Replacement)

DevSystem forbids Markdown tables. For 2-4 options across criteria, use a list with indented properties; for many-by-many use the matrix (8.6).

```
Option A: Unicode box-drawing
- Readability: high in monospace docs
- Portability: fails in proportional fonts and ASCII pipelines
- LLM value: none

Option B: Pure ASCII
- Readability: medium ("engineering sketch")
- Portability: universal
- LLM value: stable alignment, no ambiguous widths
```

## 10. ASCII Art as Image-Generation Prompt

ASCII art is a strong structural input for image models but a weak instruction. The model reads the grid as "boxes, arrows, labels, relative position" and reads the prose as "what to draw and how". Both are required.

### 10.1 What Image Models Do With ASCII

Observed behavior (ChatGPT image generation / gpt-image class models, field reports and vendor docs; see Sources):

- Preserve: box count (up to about 6), left-right and top-bottom order, arrow direction, short labels (1-3 words), nesting one level deep
- Compress or drop: anything past 6-8 modules, labels longer than 4 words, second-level nesting, fine line styles (dashed vs solid), exact proportions in charts
- Invent when underspecified: icons, extra connectors, decorative components, "corrected" label text
- Render text unreliably: label spelling degrades with density; every label must be repeated in the prose prompt so the model has a second source

Consequence: the ASCII fixes topology; the prose fixes semantics, style, and negative constraints.

### 10.2 Prompt Structure

Send one message with five blocks in this order. Keep the whole prompt under about 60 lines.

```
1. Intent        why the image exists, who views it, what they must understand at a glance
2. Deliverable   diagram kind + style + aspect ratio (e.g. "flat 2D architecture diagram, 16:9")
3. Structure     the ASCII block (title, art, legend)
4. Element list  every box and edge in prose, with exact label text, one line each
5. Constraints   flow direction, grouping, color roles, what NOT to do
```

Template:

```
Create a [flat 2D | isometric | hand-drawn whiteboard] [architecture | UI | flow] diagram for
[audience]. The viewer must understand [one-sentence message] at a glance.

Layout: [left-to-right | top-to-bottom] flow. [N] main boxes, grouped as shown.
Aspect ratio [16:9 | 4:3 | 1:1]. Sharp, readable text. Clean sans-serif labels.

Structure (keep this topology exactly):

[ASCII BLOCK]

Elements:
- Box "Web Frontend" (client tier, top-left)
- Box "Shop API" (service tier, center), receives from Web Frontend
- Box "Shop DB" (data tier, right), receives from Shop API
- Box "Payment Provider" (external, outside the boundary, bottom), dashed border
- Arrow Web Frontend -> Shop API labeled "HTTPS"

Style: [color role per tier, e.g. "clients blue, services green, data stores grey,
external white with dashed border"].
Boundary "company network" as a light background band around the three internal boxes.

Do not add components, icons, or arrows that are not listed. Do not abbreviate or change label text.
Do not reverse any arrow. No decorative background, no 3D effects, no logos.
```

### 10.3 Preparing the ASCII for the Model

- **Compress first.** 3-6 boxes. If the source diagram has more, draw a context diagram (system + externals) and one detail diagram per subsystem, and generate one image each
- **Tier 2 light.** Same glyphs as the document version; the model reads box-drawing lines as box edges. No heavy, double, or dashed variants: the model does not distinguish line styles, state them in prose instead
- **Width 70-100.** Wider grids are read as one blurred row
- **One flow direction.** State it in prose as well ("left-to-right")
- **Labels 1-3 words, Title Case**, identical in the art and the element list
- **Kind tags** on line 2 of each box (`[SERVICE]`, `[DB]`, `[EXTERNAL]`) translate directly into color roles in the prose
- **Legend line** kept; the model uses it to distinguish line styles
- **No data values in the art** for charts; give the values in prose and ask for a chart of that data instead (the model draws bars from numbers better than from `#` counts)
- **No Tier 4 glyphs** (braille, block eighths, digit fonts). The model does not decode dot patterns; describe the chart type, axes, and values in prose. Use Tier 4 for the human-facing document version only
- **Depth cues in prose**, not in the art: "modal dialog centered over a dimmed page", "three stacked worker instances". The Section 3.6 techniques are for text readers; the image model needs the words

### 10.4 Style Choice

- **Flat 2D / C4 style**: technical accuracy, label clarity, documentation use. Default for architecture and UX
- **Hand-drawn whiteboard / knowledge card**: explainers, onboarding, slides. Tolerates fewer boxes (max 5), more prose per box
- **Isometric / subtle 3D**: deployment and infrastructure visuals where "boxes on a plane" reads naturally. Costs label legibility
- **Wireframe / mockup style** for UX: ask for "greyscale low-fidelity wireframe" so the model does not invent visual design; exact button text in the element list

### 10.5 Iteration Protocol

1. Generate once from the full prompt
2. Check against the element list: every box present, every label spelled correctly, every arrow in the stated direction, nothing extra
3. Fix one thing per follow-up message ("Move 'Payment Provider' below the boundary; keep everything else identical")
4. Never regenerate from scratch after a good topology; edit
5. Record the final prompt next to the ASCII in the source document so the image can be regenerated

### 10.6 Test Before Scaling

EDIRD rule (edird-phase-planning.md "Visual verification"): before drawing a set of diagrams for image generation, run one through the model and inspect the result. Adjust the prompt template, then draw the rest. One test image costs minutes; a set of wrong diagrams costs a session.

## 11. Verification Checklist

Run on every diagram before it leaves the draft. Adapted from transcribe.md F2b and the alignment rules of the three ASCII skills in Sources.

Grid:
- [ ] No tab characters
- [ ] Every line of every box has the same character count
- [ ] Every vertical connector stays in one column
- [ ] Every arrowhead touches its target box edge
- [ ] Box interiors in one row have equal width
- [ ] No trailing whitespace
- [ ] Width within the limit for the consumer (70 / 100 / 120 / 180)
- [ ] One character tier only; no `-` next to `─`; no `─` inside prose words or dates (conversion artifact)
- [ ] Min 1 space between text and every `│`; no `│text│`
- [ ] Frames do not touch: 1-space gutter for nested boxes, gap between adjacent boxes (Section 3.1)
- [ ] Line-pure: braille lines contain only braille (`⠀` for padding); Unicode symbol rows (`● ○ ★`) have no frame characters on the same line
- [ ] Block rows end in a visible glyph (`▕` or frame), not trailing spaces
- [ ] Depth technique consistent (Section 3.6): front box complete, back box interrupted; no double-drawn borders unless the legend says "overlap"

Semantics:
- [ ] Title line names the diagram type and what it shows
- [ ] Every node labeled; kind tags where the consumer is an LLM or image model
- [ ] Legend explains every symbol, line style, and state marker used
- [ ] Labels 1-3 words; sentences moved to notes
- [ ] 3-7 primary elements (max 6 for image generation)
- [ ] One dominant flow direction
- [ ] Encoding matches the question (Section 5); cycles are not drawn as trees

UX mockups additionally:
- [ ] Every interactive element drawn; every drawn control appears in the User Actions list
- [ ] Label text matches implementation 1:1
- [ ] Overlays (toast, modal, dropdown) as separate boxes
- [ ] Modal footer: primary left, secondary right, both right-aligned
- [ ] BEFORE and AFTER adjacent, same width

Charts additionally:
- [ ] Every bar or point has its value printed
- [ ] Scale stated
- [ ] No pie chart
- [ ] Values not duplicated in surrounding prose

Image-generation prompts additionally:
- [ ] Prose element list matches the art 1:1
- [ ] Negative constraints present (no invented components, no label changes, no reversed arrows)
- [ ] Style, aspect ratio, and flow direction stated
- [ ] One test image generated and checked before scaling

## 12. Next Steps

1. Decide LANAV2DGRM-PR-0004 (character tier for this session): recommendation from Section 2.6 is Tier 2 light for all diagrams including image generation; Tier 4 only for a human-facing companion document
2. Select diagram types for the target architecture from Section 5 (candidates: 6.1 component, 6.3 process topology, 6.5 sequence, 6.6 state machine, 6.2 layer)
3. Draw one diagram, run the Section 10.2 prompt through ChatGPT, adjust the template (Section 10.6)
4. Draw the remaining diagrams; run Section 11 on each
5. Consider promoting Sections 2-5 and 11 into a DevSystem skill rule file once validated

## 13. Sources

**DevSystem (local):**
- `LANAV2DGRM-IN01-SC-DEVSYS-CORECONV`: `.devin/rules/core-conventions.md` - Unicode box-drawing default for documents; `→` spacing; never `▼` [VERIFIED]
- `LANAV2DGRM-IN01-SC-DEVSYS-SPECRULES`: `.devin/skills/write-documents/SPEC_RULES.md` - SPEC-DG-01..07, SPEC-CT-04/07: UI mockup rules, layer diagrams, BEFORE/AFTER, UX text fidelity, modal button order, event flows [VERIFIED]
- `LANAV2DGRM-IN01-SC-DEVSYS-INFORULES`: `.devin/skills/write-documents/INFO_RULES.md` and `INFO_GUIDES.md` - INFO-FT-03 diagram characters; "diagram when 3+ components interact" [VERIFIED]
- `LANAV2DGRM-IN01-SC-DEVSYS-TRANSCRIBE`: `.devin/workflows/transcribe.md` Figure Transcription Protocol F0-F3 - pure ASCII for LLM consumption, MAXIMIZE SEMANTICS, 80-120 width, 2:1 aspect, self-verify [VERIFIED]
- `LANAV2DGRM-IN01-SC-DEVSYS-TRANSPROMPT`: `.devin/skills/llm-transcription/prompts/transcription.md` v14 and `prompts/judge.md` - label every node, ASCII + JSON pairing, anti-duplication, penalties [VERIFIED]
- `LANAV2DGRM-IN01-SC-DEVSYS-EDIRD`: `.devin/rules/edird-phase-planning.md` - visual [PROVE] before full implementation [VERIFIED]

**External:**
- `LANAV2DGRM-IN01-SC-OPENAI-IMAGEGEN`: https://learn.chatgpt.com/docs/image-generation - prompt guidance: purpose, subject, composition, style, constraints; infographics need concise labels and explicit hierarchy; iterate one element at a time [VERIFIED]
- `LANAV2DGRM-IN01-SC-LIHUANYU-GPTIMAGE2`: https://www.lihuanyu.com/en/posts/2026/gpt-image-2-technical-diagram-prompts/ - tested gpt-image-2 prompts for architecture diagrams; readability degrades beyond 6 modules; "compress first, then draw"; preserve names and arrow direction; do not invent components [VERIFIED]
- `LANAV2DGRM-IN01-SC-BRADSJM-DIAGRAMPROMPT`: https://gist.github.com/bradsjm/f7e97e2abc9ffe51814b814643458e29 - prompt specification for architecture images: intent first, style selection (flat 2D vs isometric vs infographic), one dominant flow direction, tier placement top-to-bottom, bands for boundaries [VERIFIED]
- `LANAV2DGRM-IN01-SC-WEBREACTIVA-ASCIIFLOW`: https://github.com/webreactiva/skills/blob/main/skills/engineering/ascii-flow/SKILL.md - three character tiers, East-Asian ambiguous width of Unicode arrows, never mix tiers, spaces not tabs, boxes before connectors, compute centers, pick the encoding before drawing [VERIFIED]
- `LANAV2DGRM-IN01-SC-XFRI-ASCIIDIAGRAMS`: https://github.com/X-FRI/skills/blob/main/skills/ascii-art-diagrams/SKILL.md - stability over decoration, ASCII default with Unicode as opt-in, single-word branch labels, width verification with tooling, split instead of widen [VERIFIED]
- `LANAV2DGRM-IN01-SC-JASONSIE-ASCIIAGENT`: https://github.com/jasonsie/zkfy/blob/main/agents/ascii-diagram-agent.md - box width = label + 4, 3-5 char gaps, 1 blank line between rows, 70-char target, validation checklist [VERIFIED]
- `LANAV2DGRM-IN01-SC-PLAYBOOKS-UNICODEBOX`: https://playbooks.com/skills/andredezzy/maccing/unicode-box-drawing - right-padding rule, identical line length per box, breathing-room lines, light lines for compatibility, 70-char limit [VERIFIED]
- `LANAV2DGRM-IN01-SC-IETF-DIAGRAMS`: https://authors.ietf.org/diagrams - ASCII art width under 72 columns for plaintext rendering; asciiflow and Monodraw as tools [VERIFIED]
- `LANAV2DGRM-IN01-SC-MERMAID2IMG-PROMPTING`: https://mermaid2img.com/blog/mermaid-prompt-engineering-for-llms - declare diagram type and constraints before content; negative constraints; iterative refinement one change at a time [VERIFIED]
- `LANAV2DGRM-IN01-SC-PLANTUML-ASCIIART`: https://plantuml.com/ascii-art - PlantUML text output dialect: rounded corners `` ,-. `-' ``, fragments with `!` border and `~~~` separators, dashed returns `- - -`, stick-figure actors; Unicode variant available [VERIFIED]
- `LANAV2DGRM-IN01-SC-ASCIIDIAGRAMS-CORPUS`: https://asciidiagrams.github.io/ - corpus of ASCII diagrams from Chromium, Linux, LLVM, TensorFlow source; visual encoding taxonomy (Connection::Graph/Tree, Geometry::Nested, Sequential::Aligned, Multiples, Annotation, Legend, Math Notation); nested box and multiples patterns [VERIFIED]
- `LANAV2DGRM-IN01-SC-TEXTUAL-SPARKLINE`: https://textual.textualize.io/widgets/sparkline/ and https://github.com/Textualize/textual/blob/main/src/textual/renderables/sparkline.py - bucket data to `width`, apply summary function (max default), map to `▁▂▃▄▅▆▇█`; multi-row rendering via `height` [VERIFIED]
- `LANAV2DGRM-IN01-SC-TEXTUAL-DIGITS`: https://textual.textualize.io/widgets/digits/ and https://raw.githubusercontent.com/Textualize/textual/main/src/textual/renderables/digits.py - 3 x 3 cell digit font from box-drawing pieces (light and bold variants); `.` rendered as `•`; glyphs ljust to 3 cells [VERIFIED]
- `LANAV2DGRM-IN01-SC-TEXTUAL-DOLPHIE`: https://textual.textualize.io/ "Built with Textual" Dolphie - dashboard layout: info panel row, block-row metric graphs in framed tiles, footer table [VERIFIED: screenshot and page text]
- `LANAV2DGRM-IN01-SC-PLOTILLE`: https://github.com/tammoippen/plotille - braille canvas 2 x 4 dots per cell, `width * 2` x `height * 4` dot grid, line/scatter/histogram/heatmap, `braille_image()` maps pixels 1:1 to dots (80 x 80 px = 40 x 20 cells) [VERIFIED]
- `LANAV2DGRM-IN01-SC-DRAWILLE`: https://github.com/asciimoo/drawille/blob/master/drawille.py - braille bit layout `pixel_map = ((0x01,0x08),(0x02,0x10),(0x04,0x20),(0x40,0x80))`, offset `0x2800` [VERIFIED]
- `LANAV2DGRM-IN01-SC-LOCAL-BRAILLEGEN`: `__braille_render.ps1` (session folder) - PowerShell generator used for the braille examples in 8.12 and 8.13; implements the drawille bit layout [TESTED]

## 14. Document History

**[2026-09-10 19:15]**
- Changed: all rule text synced to Tier 2 default (6 intro, 6.7, 6.8, 7 intro, 8.1, 8.3, 8.4, 8.14, 9.1, 10.3, 12); Tier 1 named as fallback only
- Added: 3.1 "Text never touches a frame" and "Frames never touch" rules; 3.1 isometric diagonal exception; Section 11 checks for both
- Fixed: conversion artifacts `─` inside prose words and dates (7.1, 7.4, 7.6, 7.7); leftover ASCII `|` `=` `-` and Tier 3 `►◄` inside Tier 2 diagrams (2.6, 4.6, 4.7, 4.10, 6.6, 6.8, 8.9, 8.16, 9.3); `│[signtool]│` padding (6.8); form column alignment (7.3); isometric Tier 2 corners (3.6 E)

**[2026-09-10 17:20]**
- Added: 2.4 Tier 4 line-pure glyph sets (braille, block eighths, digit fonts) with line-purity rule; 2.5 ASCII dialects (PlantUML rounded, fragments, actors)
- Added: 3.6 Depth: boxes on top of boxes (occlusion, offset stack, shadow, dimmed modal, isometric, overlap)
- Added: 5.1 Visual encoding taxonomy from the ASCII Diagrams corpus with multiples and annotation patterns
- Added: 8.10 block sparkline, 8.11 block area chart, 8.12 braille line/scatter/histogram, 8.13 braille picture, 8.14 big digits and KPI tiles, 8.15 dashboard layout, 8.16 infographic elements (13 encodings)
- Added: Section 10 notes on Tier 4 and depth for image generation; Section 11 line-purity, trailing-glyph, depth checks
- Changed: decision rule (2.6) includes Tier 4 branch; Summary extended; Sources extended with 8 entries
- Fixed: waffle chart cell counts; area chart trailing spaces replaced by right-edge tick; dashboard panel widths equalized to 98

**[2026-09-10 16:45]**
- Initial guide created: audiences, character tiers, universal constraints, 10 anti-patterns, type selector, 10 architecture types, 10 UX types, 9 chart types, 8 other types, image-generation prompt protocol, verification checklist
