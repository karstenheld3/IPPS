# SPEC: IPPS Prompt File Format

**Doc ID**: IPPSPRMTFMT-SP01
**Feature**: ipps-prompt-file-format
**Goal**: Define the syntax, semantics, and execution model for IPPS prompt queue files
**Timeline**: Created 2026-08-31

**Depends on:**
- `PROMPTS_RULES.md [WRTPRMPT]` for content quality rules (PRMT-* rule IDs)
- `PROMPTS_GUIDES.md [WRTPRMPT]` for authoring guidance

**Does not depend on:**
- `_SPEC_LANA_MVP-2_ACP.md [LANAACPB-SP01]` (Lana implements this format but does not define it)

## MUST-NOT-FORGET

- Format rules are parser-level: violations make the file unparseable
- Content rules are quality-level: violations produce valid but low-quality prompts
- The spec defines WHAT the format is; PROMPTS_RULES.md defines HOW to write good content within it
- Fence length is per-prompt, not per-file

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Design Decisions](#5-design-decisions)
6. [Key Mechanisms](#6-key-mechanisms)
7. [Examples](#7-examples)
8. [Technical Constraints](#8-technical-constraints)
9. [Document History](#9-document-history)

## 1. Scenario

**Problem:** Autonomous agents executing multi-step tasks need a way to receive an ordered sequence of prompts as input. Without a standard format, each tool invents its own syntax, prompts get concatenated into single mega-instructions (degrading quality), and there is no separation between human-readable commentary and model-intended content.

**Solution:**
- A plain-text Markdown-compatible file format using fenced code blocks as prompt delimiters
- `---` separators between prompts with optional human-readable commentary
- Per-prompt fence length selection (3-9 backticks) to handle nested code blocks
- All prompts execute as turns of one session, preserving conversational context

**What we don't want:**
- JSON/YAML/TOML structured formats (not human-writable, no Markdown rendering)
- YAML frontmatter before the first prompt (`---` conflicts with separator token)
- Global fence length (forces unnecessary depth when only one prompt contains code blocks)
- Implicit prompt boundaries (whitespace-based splitting is ambiguous and error-prone)
- Concatenating all prompts into a single model submission (defeats the purpose of prompt files - see FR-12, DD-10)

## 2. Context

The IPPS Prompt File Format is a DevSystem standard for encoding ordered prompt sequences. It is designed for headless agent execution where a human authors prompts in advance, and an agent processes them sequentially in a single session.

**Implementations:**
- **Lana** (`lana --prompt-file <path>`) - Reference implementation. Parser documented in `Lana-V1/docs/PROMPT_FILE_FORMAT.md [LANAACPB-DOC01]`
- **DevSystem write-prompts workflow** (`/write-prompts`) - Authoring workflow producing files conforming to this format

**Related DevSystem artifacts:**
- `PROMPTS_RULES.md` - Content quality rules (PRMT-FT, PRMT-ST, PRMT-SQ, PRMT-CT, PRMT-EX, PRMT-NM)
- `PROMPTS_GUIDES.md` - Authoring guidance (decomposition, density, state flow, precision)
- `PROMPTS_TEMPLATE.md` - File skeleton for authoring

## 3. Domain Objects

### Prompt Queue File

A **Prompt Queue File** is a Markdown-compatible text file containing one or more Prompt Blocks separated by Separators. Recommended name pattern: `_PROMPTS_[Topic].md` (DevSystem convention) or `PROMPTS*.md` (general convention).

- **Encoding**: UTF-8
- **First fenced line**: Must be an Opening Fence (Commentary allowed before it)
- **Minimum content**: One Prompt Block

### Prompt Block

A **Prompt Block** is the unit of execution. It consists of an Opening Fence, prompt text, and a Closing Fence.

- **Content**: Text intended for the model (objective, context, constraints, verification, examples)
- **Scope**: One reasoning mode per block (research, implementation, testing, etc.)
- **Fence length**: Chosen independently per block (3-9 backticks)

### Fence

A **Fence** is a line of N consecutive backticks (3 <= N <= 9) that delimits a Prompt Block.

- **Opening Fence**: May carry an optional Info String (ignored by parser)
- **Closing Fence**: First subsequent line with >= N backticks
- **Nesting rule**: Outer fence must be longer than the deepest inner fence within the prompt

### Separator

A **Separator** is a single `---` line between two consecutive Prompt Blocks. It marks the boundary between the Closing Fence of one prompt and the Opening Fence of the next.

### Commentary

**Commentary** is human-readable text placed between prompts or before the first prompt. Commentary is never sent to the model. It documents expected state, purpose of the next prompt, or context for human reviewers.

Commentary consists of two elements:
- **Headings** (`## Prompt N - [title]`) - plain Markdown, provide structure for human scanning
- **Commentary notes** (explanations, expected state, session split markers) - MUST be wrapped in HTML comments (`<!-- ... -->`)

Wrapping commentary notes in HTML comments creates a clear visual distinction between meta-content and prompt content in raw text, and prevents markdown renderers from displaying commentary as prose. In final output files, Commentary is limited to a heading plus one HTML comment of max 1 sentence. Templates may use longer HTML comments for authoring instructions.

### Execution Frontmatter

**Execution Frontmatter** is an optional YAML block at the very top of a Prompt Queue File (before any Commentary or Opening Fence). It provides execution hints to the execution engine: intended model, context window size, reasoning settings, and prompt system. The execution engine MAY use these hints or override them with its own configuration. Frontmatter is delimited by `---` lines, which is unambiguous because Separators only appear between Prompt Blocks (after a Closing Fence).

### Info String

An **Info String** is optional text following the backticks on an Opening Fence line (e.g., `` ```text ``). The parser ignores it. It exists for Markdown renderer compatibility.

## 4. Functional Requirements

### Format Rules (Parser-Level)

These rules define what makes a file syntactically valid. A parser MUST reject files that violate these rules.

**IPPSPRMTFMT-FR-01: Leading Fence**
- The first Opening Fence must appear before any non-Commentary content
- Commentary (headings, notes) is allowed before the first Prompt Block
- Optional Execution Frontmatter (per FR-11) may appear before Commentary
- No other frontmatter or YAML header blocks before the first fence

**IPPSPRMTFMT-FR-02: Fence Length Range**
- Opening Fence backtick count N: 3 <= N <= 9
- Closing Fence: first subsequent line with >= N backticks
- Each Prompt Block chooses its fence length independently

**IPPSPRMTFMT-FR-03: Fence Nesting**
- The outer fence of a Prompt Block must be longer than the deepest inner fence within that block
- Inner fences are code blocks embedded in the prompt text (examples, templates)

**IPPSPRMTFMT-FR-04: Separator Required**
- Every pair of consecutive Prompt Blocks requires exactly one `---` Separator line between them
- The Separator appears after the Closing Fence of the preceding block and before the Opening Fence (or Commentary) of the next block

**IPPSPRMTFMT-FR-05: Commentary Placement**
- Commentary is allowed between a Separator and the next Opening Fence
- Commentary is also allowed before the first Prompt Block (per FR-01)
- Commentary is never sent to the model
- Commentary headings (`## Prompt N - [title]`) are plain Markdown
- Commentary notes (explanations, expected state, context) MUST be wrapped in HTML comments (`<!-- ... -->`)
- Commentary density in final output files: heading + max 1 sentence in one HTML comment per prompt. Templates may use longer HTML comments for authoring instructions.

**IPPSPRMTFMT-FR-06: Minimum One Prompt**
- The file must contain at least one Prompt Block
- Empty files or files containing only Commentary are invalid

**IPPSPRMTFMT-FR-07: Prompt Order**
- Prompt Blocks execute in file order (top to bottom)
- No mechanism for conditional branching or reordering

### Execution Rules

**IPPSPRMTFMT-FR-08: Sequential Turn Execution**
- Each Prompt Block executes as a separate turn, submitted individually to the model
- The execution engine submits one prompt, waits for the model response, then submits the next prompt
- All Prompt Blocks execute within one session: later prompts see all earlier conversation context (model responses included)
- Prompts are NEVER concatenated into a single submission (see FR-12)

**IPPSPRMTFMT-FR-12: No Concatenation**
- Concatenating multiple Prompt Blocks into a single model submission is a format violation
- Each Prompt Block is a discrete turn that receives the model's full context engineering, input rendering, and compute budget
- Concatenation limits execution depth to what the model can produce in one response, defeating the purpose of prompt files
- An agent that writes a prompt file and then executes all prompts in a single run is NOT executing the prompt file - it is circumventing the format

**IPPSPRMTFMT-FR-09: Failure Handling**
- A failed turn (provider error, cancellation) abandons remaining prompts
- Completed turns persist and the session is resumable
- The exit code is non-zero on failure

### Content Quality Rules

Content quality is governed by `PROMPTS_RULES.md` (PRMT-* rules). This spec does not replicate those rules. Key categories:

- **PRMT-FT-***: Format rules (overlap with FR-01 through FR-06 above)
- **PRMT-ST-***: Structure rules (objective, constraints, verification, reasoning mode, density)
- **PRMT-SQ-***: Sequence rules (no contradictions, explicit dependencies, commentary)
- **PRMT-CT-***: Content rules (specificity, negative constraints, observable verification, precision)
- **PRMT-EX-***: Execution rules (one prompt per turn, no self-execution)
- **PRMT-NM-***: Naming rules (filename pattern, topic naming)

### Naming Convention

**IPPSPRMTFMT-FR-11: Optional Execution Frontmatter**
- Execution Frontmatter is an optional YAML block at the very top of the file (before any Commentary or Opening Fence)
- Format: `---` on first line, YAML key-value pairs, `---` closing line
- Supported keys:
  - `intended_model`: Model identifier (e.g., `claude-sonnet-4-5`, `gpt-4o`)
  - `context_window_size`: Context window size (e.g., `200k`, `128k`, `1M`)
  - `reasoning_settings`: Reasoning effort (`medium` | `high` | `extra-high`)
  - `prompt_system`: Prompt system identifier (e.g., `IPPS`)
- The execution engine MAY honor these hints or override with its own configuration
- If present, frontmatter MUST be the first content in the file (no blank lines or content before the opening `---`)
- Only one frontmatter block allowed (at file start only)
- Frontmatter is never sent to the model

**IPPSPRMTFMT-FR-10: DevSystem Filename**
- DevSystem convention: `_PROMPTS_[Topic].md` where Topic is CamelCase
- General convention: `PROMPTS*.md` (e.g., `PROMPTS.md`, `PROMPTS_setup.md`)
- Per PRMT-NM-01, PRMT-NM-02

## 5. Design Decisions

**IPPSPRMTFMT-DD-01:** Markdown fenced code blocks as delimiters. Rationale: Human-readable in any text editor and Markdown renderer. No special tooling required to author or review. Syntax is already familiar to developers.

**IPPSPRMTFMT-DD-02:** Per-prompt fence length (not per-file). Rationale: Most prompts contain no inner code blocks and use 3 backticks. Only prompts with embedded code examples need longer fences. Per-file minimum would force unnecessary depth everywhere.

**IPPSPRMTFMT-DD-03:** Commentary allowed before first fence. Optional Execution Frontmatter allowed at file start (per FR-11). Rationale: A heading before the first prompt improves human readability. The parser skips non-fence lines until it finds the first Opening Fence. Execution Frontmatter (YAML `---` blocks) is allowed only at the very top of the file and is unambiguous because Separators only appear between Prompt Blocks (after a Closing Fence).

**IPPSPRMTFMT-DD-04:** `---` separator (not blank lines). Rationale: Blank lines are ambiguous (could appear within prompts). `---` is an explicit, unambiguous boundary that also renders as a horizontal rule in Markdown.

**IPPSPRMTFMT-DD-05:** Commentary never sent to model, wrapped in HTML comments. Rationale: Clean separation between human-readable documentation and model-intended instructions. HTML comments create a visual boundary in raw text that prevents accidental injection of meta-commentary into the model's context. Headings remain as plain Markdown for structural scannability.

**IPPSPRMTFMT-DD-06:** Single session execution. Rationale: Later prompts can reference earlier results without explicit state serialization. Matches the natural workflow where steps build on prior work. Trade-off: a failed middle prompt blocks all subsequent prompts (mitigated by resume capability per FR-09).

**IPPSPRMTFMT-DD-10:** One prompt per turn, never concatenated. Rationale: Prompt files exist to work around the context, compute, and output limits of a single model run. Each turn receives the agent's full context engineering and input rendering mechanisms. Concatenating prompts into one submission collapses the sequence into a single run, limiting execution depth to whatever the model can produce in one response. This defeats the entire purpose of decomposing work into a prompt queue. An agent that writes a prompt file and then executes all prompts at once has not used the prompt file format - it has bypassed it.

**IPPSPRMTFMT-DD-07:** Maximum 9 backticks. Rationale: Practical upper bound. A prompt needing > 9 levels of fence nesting is a design smell indicating the prompt should be split. Keeps the format simple for parser implementations.

**IPPSPRMTFMT-DD-08:** Heading consistency. Rationale: Markdown headings before each prompt improve human readability - scan structure, locate prompts, understand flow. Using headings is recommended (SHOULD) but not required. However, if headings are used for any prompt's Commentary, all prompts MUST have headings for consistency. Mixed files (some prompts with headings, some without) are invalid. Enforced by PRMT-FT-07.

**IPPSPRMTFMT-DD-09:** Optional Execution Frontmatter. Rationale: Execution hints (intended model, context window, reasoning settings) help the execution engine select appropriate configuration. Frontmatter is OPTIONAL - the execution engine decides whether to honor it or use its own configuration. This enables portability: the same prompt file can run on different engines with different models. Frontmatter is unambiguous with Separators because it only appears at the file start (before any fence), while Separators only appear between Prompt Blocks (after a Closing Fence).

## 6. Key Mechanisms

### Fence Length Selection

The author examines each prompt for inner fenced code blocks and selects the minimum sufficient outer fence:

- No inner fences → 3 backticks
- Contains `` ``` `` blocks → 4+ backtick outer fence
- Contains `` ```` `` blocks (e.g., markdown examples containing `` ``` ``) → 5+ backtick outer fence
- Rule: outer fence length > deepest inner fence length

### State Flow Between Prompts

All prompts share one session. State flows implicitly through conversation history. Best practice (per PRMT-SQ-02, PRMT-SQ-03):

- Dependent prompts name the prior output explicitly ("Using the analysis from step 1...")
- Commentary documents expected state for human reviewers
- No restatement of facts already in conversation history
- No contradiction of constraints from earlier prompts

### Prompt Structure (Content Quality)

Each Prompt Block follows a 4-part structure (per `PROMPTS_GUIDES.md` section 3):

1. **Objective** - Desired outcome (1-3 sentences)
2. **Context** - Facts the agent cannot infer (selective, not exhaustive)
3. **Constraints** - What NOT to do (negative form)
4. **Verification** - Machine-checkable success criteria

Not every prompt needs all four parts. Complexity determines which parts to include.

### Error Rejection

A conforming parser rejects the file with a diagnostic message when:

- No Opening Fence found before non-Commentary content (violates FR-01)
- A fence is never closed (violates FR-02)
- Separator missing between consecutive Prompt Blocks (violates FR-04)
- Opening Fence exceeds 9 backticks (violates FR-02)
- File contains zero Prompt Blocks (violates FR-06)

## 7. Examples

### Minimal Valid File (Single Prompt)

``````text
```
List all Python files in the project and count their lines.
```
``````

### File with Optional Execution Frontmatter

``````text
---
intended_model: claude-sonnet-4-5
context_window_size: 200k
reasoning_settings: high
prompt_system: IPPS
---

## Prompt 1 - Analyze codebase

```
List all Python files in the project and count their lines.
```
``````

### Multi-Prompt with Commentary (Headings per PRMT-FT-07, HTML comments per FR-05)

``````text
## Prompt 1 - Create calc module

```
Create `calc.py` with an `add(a, b)` function.

Verify: File exists and `python -c "from calc import add; assert add(2, 3) == 5"` succeeds.
```

---

## Step 2 - extend with multiply

<!-- Previous step created calc.py with add(). Now add multiplication. -->

```
Add a `multiply(a, b)` function to `calc.py`.

Constraints:
- Do not modify the existing add() function
- No external dependencies

Verify: `python -c "from calc import multiply; assert multiply(2, 3) == 6"` succeeds.
```
``````

### Mixed Fence Lengths (Nested Code Blocks, Headings per PRMT-FT-07, HTML comments per FR-05)

```````text
## Prompt 1 - Security analysis

```
Analyze the authentication module in src/auth/ for security vulnerabilities.

Constraints:
- Do not modify any code in this step
- Limit analysis to src/auth/ directory only

Verify: Output a numbered list of findings with severity (HIGH/MEDIUM/LOW) and file location.
```

---

## Step 2 - fix highest-severity finding

<!-- Previous step produced a numbered findings list. Fix the highest-severity item. -->

````
Using the analysis from the previous step, fix the highest-severity vulnerability identified.

Example fix pattern:
```typescript
try {
  const token = jwt.verify(input, secret, { algorithms: ['HS256'] })
} catch (err) {
  return res.status(401).json({ error: 'Invalid token' })
}
```

Constraints:
- Fix only the single highest-severity issue
- Do not change the public API of any exported function

Verify: Run `pnpm test:auth`. All tests pass.
````
```````

## 8. Technical Constraints

- Files must be UTF-8 encoded
- Line endings: LF or CRLF (parser must handle both)
- The format is Markdown-compatible: a prompt queue file renders meaningfully in any Markdown viewer (fenced blocks as code, `---` as horizontal rules, commentary as prose)
- No binary content: prompt text is plain text only
- Maximum file size is limited by the agent's context window, not by the format

## 9. Document History

**[2026-09-05 16:56]**
- Changed: FR-05 commentary notes MUST be wrapped in HTML comments (`<!-- ... -->`), headings remain plain Markdown
- Changed: DD-05 updated - HTML comments create visual boundary, prevent meta-commentary injection
- Changed: Commentary domain object updated with two-element structure (headings + HTML comment notes)
- Changed: All multi-prompt examples updated to use HTML comments for commentary notes

**[2026-09-05 16:45]**
- Added: FR-12 No Concatenation (each prompt is a separate turn, never concatenated into one submission)
- Added: DD-10 One prompt per turn rationale (why separate turns matter: context engineering, compute budget, execution depth)
- Changed: FR-08 renamed from "Single Session" to "Sequential Turn Execution", explicit one-prompt-per-turn language
- Changed: "What we don't want" section: added concatenation as anti-pattern

**[2026-09-05 16:18]**
- Added: FR-11 Optional Execution Frontmatter (intended_model, context_window_size, reasoning_settings, prompt_system)
- Added: DD-09 Execution Frontmatter design decision
- Added: Execution Frontmatter domain object
- Changed: FR-01 allows optional Execution Frontmatter before Commentary
- Changed: DD-03 updated - frontmatter now allowed at file start, unambiguous with Separators
- Added: Example file with optional frontmatter

**[2026-09-05 14:50]**
- Added: DD-08 heading consistency - headings recommended (SHOULD); if used, all prompts MUST have headings
- Added: PRMT-FT-07 rule reference in PROMPTS_RULES.md
- Changed: Examples updated to use headings consistently (Multi-Prompt, Mixed Fence Lengths)
- Changed: DD-03 rationale updated - headings before first prompt recommended for readability

**[2026-09-01 18:00]**
- Changed: FR-01 allows Commentary before first Prompt Block (was: first non-empty line must be fence)
- Changed: FR-05 allows Commentary before first Prompt Block; added density rule (heading + 1 sentence in final files, no limit in templates)
- Changed: DD-03 rationale updated for Commentary-before-first-fence allowance
- Changed: Domain Object "Commentary" and "Prompt Queue File" definitions updated

**[2026-08-31 22:20]**
- Fixed: Term consistency - capitalized "Prompt Block" and "Commentary" as domain objects throughout (MW-WC-05)

**[2026-08-31 22:15]**
- Initial specification created
- Source: Lana implementation doc `PROMPT_FILE_FORMAT.md [LANAACPB-DOC01]`, DevSystem `PROMPTS_RULES.md`, `PROMPTS_GUIDES.md`
