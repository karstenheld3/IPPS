# Python Coding Rules

## Definitions

```
MAX_LINE_CHARS = 220
TAB = "  " (2 spaces)
UNKNOWN = '[UNKNOWN]'
```

## Rule Index

Formatting (FT): FT-01 Indent 2 spaces | FT-02 Single line ≤220 chars | FT-03 Signature on one line | FT-04 One empty line between functions/classes | FT-05 Topic markers (127 chars)

Imports (IM): IM-01 Top of file | IM-02 Core imports single line | IM-03 No local imports | IM-04 Group: stdlib, third-party, internal | IM-05 Single-line multi-name

Code Generation (CG): CG-01 No symbol renaming | CG-02 Re-use patterns | CG-03 Check existing helpers | CG-04 Least Surprise | CG-05 Explicit loops | CG-06 Stdlib first | CG-07 No emojis | CG-08 Timezone-aware datetime | CG-09 Singular/plural

Naming (NM): NM-01 Clear names | NM-02 Follow patterns | NM-03 No abbreviations | NM-04 Corresponding pairs | NM-05 No misleading concepts | NM-06 Specific over generic | NM-07 Origin/destination not source/target | NM-08 Don't rename established APIs

Comments (CM): CM-01 Comment intent | CM-02 No docstrings for small functions | CM-03 Docstrings for complex functions | CM-04 ASCII quotes | CM-05 Tree characters for hierarchies

## Formatting Rules (FT)

### PYTHON-FT-01: Indentation
Indent with TAB (2 spaces).

### PYTHON-FT-02: Single Line Statements
If statement ≤ MAX_LINE_CHARS, keep on single line. Ignore limit in Markdown.

```python
# GOOD
content_page = client.vector_stores.files.content(vector_store_id=vector_store_id, file_id=file_id)
if not vector_store_id: raise ValueError(f"Expected a non-empty value for 'vector_store_id' but received {vector_store_id!r}")
```

### PYTHON-FT-03: Function Signatures
Full signature on single line; body starts next line.

### PYTHON-FT-04: Empty Lines
One empty line between imports, functions, class definitions.

### PYTHON-FT-05: Function Grouping
Group functions with 127-char start/end markers. One blank line after each function.

```python
# ----------------------------------------- START: Topic A --------------------------------------------------------------------

def function01():
  ...

def function02():
  ...

# ----------------------------------------- END: Topic A ----------------------------------------------------------------------
```

## Import Rules (IM)

### PYTHON-IM-01: All imports at top of file.

### PYTHON-IM-02: Core Imports
All core imports on single line (even if exceeds MAX_LINE_CHARS).
```python
import asyncio, datetime, json, random
```

### PYTHON-IM-03: No local imports inside functions.

### PYTHON-IM-04: Group: standard library, third-party, internal modules.

### PYTHON-IM-05: Import all needed names from a module in single line.

## Code Generation Rules (CG)

### PYTHON-CG-01: Do not rename existing symbols unless explicitly asked.

### PYTHON-CG-02: Analyze existing codebase first. Re-use implementation patterns, naming, formatting, design philosophy, logging style.

### PYTHON-CG-03: Check for existing helpers before creating new ones.

### PYTHON-CG-04: Prefer simple, idiomatic Python. Optimize readability over micro-optimizations.

### PYTHON-CG-05: Avoid `lambda`, `map`, `filter`, `reduce` for control flow; use explicit `for` loops. Exception: string/list joins.

### PYTHON-CG-06: Prefer standard library; add dependencies only if helper would be unreasonably complex.

### PYTHON-CG-07: No emojis in code/logging. Exception: UI may use ✅❌⚠️★☆⯪

### PYTHON-CG-08: Use `datetime.datetime.now(datetime.timezone.utc)` not deprecated `utcnow()`.

### PYTHON-CG-09: Handle singular/plural correctly: `0 files`, `1 file`, `2 files`. Never `file(s)`.

## Naming Rules (NM)

### PYTHON-NM-01: Use clear, fully written names.

### PYTHON-NM-02: Follow existing naming patterns in codebase.

### PYTHON-NM-03: No Abbreviations
`body_attrs` -> `body_attributes`, `content` -> `html_content`

### PYTHON-NM-04: Corresponding Pairs
Use same word stem for opposites.
- Verbs: send/receive, pack/unpack, accept/reject, enable/disable, visible/hidden, show/hide, do/undo, open/close, check/uncheck, validate/invalidate, include/exclude, existant/nonExistant, empty/filled, expand/shrink
- Entities: Input/Output, Addition/Removal, Activation/Deactivation, Source/Target, Current/Target, Origin/Destination, Departure/Arrival, Prefix/Suffix

### PYTHON-NM-05: `visible/invisible` implies object occupies space. Use `visible/hidden` if hidden means "not there at all".

### PYTHON-NM-06: Avoid generic `nextTo`. Use specific: `leftTo`, `rightTo`, `northTo`, `nearTo`, `closeTo`.

### PYTHON-NM-07: Use origin/destination not source/target for travel/routing contexts.

### PYTHON-NM-08: Don't rename established APIs even if misnomers. Association field > literal name.

## Comment Rules (CM)

### PYTHON-CM-01: Comment intent, edge cases, non-obvious behavior. Never restate obvious code.

### PYTHON-CM-02: No Docstrings for Small Functions
Single comment above if intent/types need clarification.

```python
# Generate HTTP error response in requested format ('json' | 'html')
def generate_error_response(error_message: str, format: str, status_code: int = 400):
  if format == 'json': return JSONResponse({"error": error_message}, status_code=status_code)
  else: return HTMLResponse(generate_error_div(error_message), status_code=status_code)
```

### PYTHON-CM-03: Docstrings for Complex Functions
Use docstrings for FastAPI endpoints and complex functions (>5 args, multiple responsibilities, complex return types). Include example outputs.

```python
def generate_simple_page(title: str, html_content: str, body_attributes: str = "") -> str:
  """
  Generate simple HTML page with title and html content.
  
  Example output:
    <!DOCTYPE html><html><head>[GENERATE_HTML_HEAD_OUTPUT]</head>
    <body [BODY_ATTRIBUTES_IF_ANY]>
      [HTML_CONTENT]
    </body>
    </html>
  """
```

### PYTHON-CM-04: Use ASCII "double quotes" or 'single quotes' in documentation/UI output.

### PYTHON-CM-05: Use "└──" for hierarchy indenting.