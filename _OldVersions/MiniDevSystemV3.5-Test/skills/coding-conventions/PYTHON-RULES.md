# Python Coding Rules

## Definitions

```
MAX_LINE_CHARS = 220
TAB = "  " (2 spaces)
UNKNOWN = '[UNKNOWN]'
```

## Formatting Rules (FT)

### PYTHON-FT-01: Indentation
Indent with TAB (2 spaces).

### PYTHON-FT-02: Single Line Statements
Statements ≤ MAX_LINE_CHARS stay on one line. Ignore limit in Markdown.

BAD: `client.func(\n  arg1=x,\n  arg2=y\n)` GOOD: `client.func(arg1=x, arg2=y)`
BAD: `if not x:\n  raise ...` GOOD: `if not x: raise ...`

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

BAD: `# ====` or `# SECTION NAME` blocks. GOOD: `# --- START: Name ---` / `# --- END: Name ---`

## Import Rules (IM)

### PYTHON-IM-01: Import Location
All imports at top of file.

### PYTHON-IM-02: Core Imports
All core imports on single line: `import asyncio, datetime, json, random`

### PYTHON-IM-03: No Local Imports
No imports inside functions. Move to top with other imports from same module.

### PYTHON-IM-04: Import Grouping
Order: standard library, third-party, internal modules.

### PYTHON-IM-05: Multi-Name Imports
Import all needed names from a module in single line.

## Code Generation Rules (CG)

### PYTHON-CG-01: No Symbol Renaming
Do not rename existing symbols unless explicitly asked.

### PYTHON-CG-02: Re-use Patterns
Analyze codebase first. Re-use existing patterns, naming, formatting, logging style.

### PYTHON-CG-03: Check Existing Helpers
Before creating new helpers, verify no alternatives exist in codebase.

### PYTHON-CG-04: Principle of Least Surprise
Simple idiomatic Python over clever code. Readability over micro-optimization.

### PYTHON-CG-05: Explicit Loops
Avoid `lambda`, `map`, `filter`, `reduce` for control flow; use `for` loops. Exception: string/list joins.

### PYTHON-CG-06: Standard Library First
Prefer stdlib; add dependencies only when helper would be unreasonably complex.

### PYTHON-CG-07: No Emojis
No emojis in code/logging. Exception: UI may use ✅ ❌ ⚠️ ★ ☆ ⯪

### PYTHON-CG-08: Timezone-Aware Datetime
Use `datetime.datetime.now(datetime.timezone.utc)` not deprecated `utcnow()`.

### PYTHON-CG-09: Singular/Plural
Handle correctly: `0 files`, `1 file`, `2 files`. Avoid `file(s)`.

## Naming Rules (NM)

### PYTHON-NM-01: Clear Names
Use clear, fully written names.

### PYTHON-NM-02: Follow Patterns
Follow existing naming patterns in the codebase.

### PYTHON-NM-03: No Abbreviations
BAD: `body_attrs`, `content`, `dynamic_count` GOOD: `body_attributes`, `html_content`, `use_dynamic_count_for_updating`

### PYTHON-NM-04: Corresponding Pairs
Use same word stem for opposites.

Verbs: `send/receive`, `pack/unpack`, `accept/reject`, `enable/disable`, `visible/hidden`, `show/hide`, `do/undo`, `open/close`, `check/uncheck`, `validate/invalidate`, `include/exclude`, `existant/nonExistant`, `empty/filled`, `expand/shrink`

Entities: `Input/Output`, `Addition/Removal`, `Activation/Deactivation`, `Source/Target`, `Current/Target`, `Origin/Destination`, `Departure/Arrival`, `Prefix/Suffix`

### PYTHON-NM-05: Avoid Misleading Concepts
`visible/invisible` implies object still occupies space. Use `visible/hidden` if hidden means "not there at all".

### PYTHON-NM-06: Specific Over Generic
Avoid `nextTo`. Use `leftTo/rightTo` (direction), `northTo/southTo` (axis), `nearTo` (distance), `closeTo` (relationship).

### PYTHON-NM-07: Origin/Destination Not Source/Target
"Planes with the target Bagdad" = bad news. "Planes with the destination Bagdad" = travel plans.

### PYTHON-NM-08: Don't Rename Established APIs
Keep working names even if they became misnomers. People predict behavior by association field, not literal name. `login()` stays even without credentials. Like "horsepower" - association field matters.

## Comment Rules (CM)

### PYTHON-CM-01: Comment Intent
Comment intent, edge cases, non-obvious behavior. Never restate obvious code.

### PYTHON-CM-02: No Docstrings for Small Functions
Single-purpose functions with clear names get one comment line above, not docstrings.

```python
# Generate HTTP error response in requested format ('json' | 'html')
def generate_error_response(error_message: str, format: str, status_code: int = 400):
  if format == 'json': return JSONResponse({"error": error_message}, status_code=status_code)
  else: return HTMLResponse(generate_error_div(error_message), status_code=status_code)
```

```python
# Set config for Crawler management. app_config: Config dataclass with openai_client, persistent_storage_path, etc.
def set_config(app_config):
  global config
  config = app_config
```

### PYTHON-CM-03: Docstrings for Complex Functions
Use docstrings for FastAPI endpoints and complex functions (5+ args, multiple responsibilities, complex return types). Include example outputs.

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

### PYTHON-CM-04: ASCII Quotes
Use ASCII "double quotes" or 'single quotes' in documentation/UI output. No typographic quotes.

### PYTHON-CM-05: Hierarchy Characters
Use `└──` for hierarchies and maps.