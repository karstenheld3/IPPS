# ASCII Art Width Test

**Goal**: Identify Unicode characters with incorrect monospace width on GitHub

## Test Method

Each character sits between two `|` bars. If the bars stay aligned vertically, the character has correct width. Look for bars that shift right (char too wide) or left (char too narrow).

## Arrows

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference (letters)
|←|→|↑|↓|↔|↕|↖|↗|↘|↙|  <-- basic arrows
|⇐|⇒|⇑|⇓|⇔|⇕|x|x|x|x|  <-- double arrows
|➔|➜|➤|➡|x|x|x|x|x|x|  <-- AVOID (fancy)
```

## Circles and Shapes

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|○|●|◎|◉|⊙|x|x|x|x|x|  <-- circles OK
|◯|⬤|⦿|⦾|x|x|x|x|x|x|  <-- circles AVOID
|□|■|▢|▣|x|x|x|x|x|x|  <-- squares
|◇|◆|x|x|x|x|x|x|x|x|  <-- diamonds
|☆|★|x|x|x|x|x|x|x|x|  <-- stars
```

## Triangles

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|◀|▶|▲|▼|◄|►|△|▽|◁|▷|  <-- triangles
|◐|◑|◒|◓|x|x|x|x|x|x|  <-- half-circles
```

## Box Drawing

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|┌|─|┬|─|┐|│|├|┼|┤|x|  <-- single
|╔|═|╦|═|╗|║|╠|╬|╣|x|  <-- double
|╭|─|┬|─|╮|│|x|x|x|x|  <-- rounded
|┏|━|┳|━|┓|┃|┣|╋|┫|x|  <-- heavy
|└|─|┴|─|┘|x|x|x|x|x|  <-- corners
```

## Lines

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|─|━|│|┃|═|║|x|x|x|x|  <-- solid lines
|┆|┇|┊|┋|x|x|x|x|x|x|  <-- dashed lines
```

## Shading

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|░|▒|▓|█|x|x|x|x|x|x|  <-- shading
|▀|▄|▌|▐|x|x|x|x|x|x|  <-- halves
|▖|▗|▘|▙|▚|▛|▜|▝|▞|▟|  <-- quadrants
```

## Brackets

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|(|)|{|}|[|]|<|>|x|x|  <-- ASCII OK
|⟨|⟩|〈|〉|⦃|⦄|x|x|x|x|  <-- AVOID
```

## Math and Logic

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|+|-|x|:|=|<|>|x|x|x|  <-- basic
|∈|⊂|⊃|∩|∪|x|x|x|x|x|  <-- set
|∧|∨|¬|⊕|⊗|x|x|x|x|x|  <-- logic
```

## Special

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|•|◦|·|x|x|x|x|x|x|x|  <-- bullets OK
|✓|✗|☐|☑|☒|x|x|x|x|x|  <-- checks
|❖|✦|✧|‣|⁃|x|x|x|x|x|  <-- AVOID
```

## Diagonals

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|/|\|X|x|x|x|x|x|x|x|  <-- ASCII OK
|╱|╲|╳|x|x|x|x|x|x|x|  <-- AVOID
```

## Punctuation

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|·|x|x|x|x|x|x|x|x|x|  <-- dot OK
|…|⋯|⋮|x|x|x|x|x|x|x|  <-- ellipsis AVOID
```

## Arcs and Corners

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|⌒|⌓|◜|◝|◞|◟|x|x|x|x|  <-- AVOID
```

## Detailed Analysis: Problematic Characters

Characters from misaligned lines, tested individually:

### Fancy Arrows (from line 15)
```
|a|  ref
|➔|  fancy arrow 1
|➜|  fancy arrow 2
|➤|  fancy arrow 3
|➡|  fancy arrow 4
```

### Large Circles (from line 23)
```
|a|  ref
|◯|  large circle 1
|⬤|  large circle 2
|⦿|  large circle 3
|⦾|  large circle 4
```

### Angle Brackets (from line 70)
```
|a|  ref
|⟨|  math angle left
|⟩|  math angle right
|〈|  CJK angle left
|〉|  CJK angle right
|⦃|  curly bracket left
|⦄|  curly bracket right
```

### Decorative (from line 88)
```
|a|  ref
|❖|  diamond 4
|✦|  star 4 pointed
|✧|  star outline
|‣|  triangular bullet
|⁃|  hyphen bullet
```

### Unicode Diagonals (from line 96)
```
|a|  ref
|╱|  box diagonal right
|╲|  box diagonal left
|╳|  box diagonal cross
```

### Ellipsis (from line 104)
```
|a|  ref
|…|  horizontal ellipsis
|⋯|  midline ellipsis
|⋮|  vertical ellipsis
```

### Arcs and Corners (from line 111)
```
|a|  ref
|⌒|  arc
|⌓|  segment
|◜|  upper left arc
|◝|  upper right arc
|◞|  lower right arc
|◟|  lower left arc
```

### Half Circles (from line 34)
```
|a|  ref
|◐|  left half black
|◑|  right half black
|◒|  lower half black
|◓|  upper half black
```

## How to Read Results

1. View on GitHub (not IDE)
2. Each `|` should align vertically with the reference row
3. If a `|` shifts right: preceding char is TOO WIDE
4. If a `|` shifts left: preceding char is TOO NARROW
5. Mark broken chars for AVOID list

## JetBrains Mono: Confirmed Misaligned Characters

Tested 2026-01-21. Characters that break monospace alignment:

**TOO WIDE (bar shifts right):**
```
➔ ➜ ➤ ➡     fancy arrows
◯ ⬤ ⦿ ⦾     large circles
〈 〉          CJK angle brackets
⦃ ⦄          curly brackets
❖ ✦          decorative diamonds/stars
⌒ ⌓          arc symbols
◜ ◝ ◞ ◟     corner arcs
```

**TOO NARROW (bar shifts left):**
```
…            horizontal ellipsis
✧ ‣ ⁃       star outline, bullets
```

**OK (properly aligned):**
```
⟨ ⟩          math angle brackets
╱ ╲ ╳        box diagonals
⋯ ⋮          midline/vertical ellipsis
◐ ◑ ◒ ◓     half circles
```

**AVOID list for transcribe.md:**
```
➔ ➜ ➤ ➡ ◯ ⬤ ⦿ ⦾ 〈 〉 ⦃ ⦄ ❖ ✦ ✧ ‣ ⁃ ⌒ ⌓ ◜ ◝ ◞ ◟ …
```
