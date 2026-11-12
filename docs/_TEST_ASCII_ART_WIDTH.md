# ASCII Art Width Test

**Goal**: Identify Unicode characters with incorrect monospace width on GitHub

## Test Method

Each character sits between two `|` bars. If the bars stay aligned vertically, the character has correct width. Look for bars that shift right (char too wide) or left (char too narrow).

## Arrows

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference (letters)
|←|→|↑|↓|↔|↕|↖|↗|↘|↙|  <-- basic arrows
|a|b|c|d|e|f|g|h|i|j|
|⇐|⇒|⇑|⇓|⇔|⇕|x|x|x|x|  <-- double arrows
|a|b|c|d|e|f|g|h|i|j|
|➔|➜|➤|➡|x|x|x|x|x|x|  <-- fancy arrows
```

## Circles and Shapes

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|○|●|◎|◉|⊙|x|x|x|x|x|  <-- circles

|a|b|c|d|e|f|g|h|i|j|
|◯|⬤|⦿|⦾|x|x|x|x|x|x|  <-- circles 2

|a|b|c|d|e|f|g|h|i|j|
|□|■|▢|▣|x|x|x|x|x|x|  <-- squares

|a|b|c|d|e|f|g|h|i|j|
|◇|◆|x|x|x|x|x|x|x|x|  <-- diamonds

|a|b|c|d|e|f|g|h|i|j|
|☆|★|x|x|x|x|x|x|x|x|  <-- stars
```

## Triangles

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|◀|▶|▲|▼|◄|►|△|▽|◁|▷|  <-- triangles

|a|b|c|d|e|f|g|h|i|j|
|◐|◑|◒|◓|x|x|x|x|x|x|  <-- half-circles, AVOID
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
|⟨|⟩|〈|〉|⦃|⦄|x|x|x|x|  <-- unicode brackes
```

## Math and Logic

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|+|-|x|:|=|<|>|x|x|x|  <-- basic

|a|b|c|d|e|f|g|h|i|j|
|∈|⊂|⊃|∩|∪|x|x|x|x|x|  <-- set

|a|b|c|d|e|f|g|h|i|j|
|∧|∨|¬|⊕|⊗|x|x|x|x|x|  <-- logic
```

## Special

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|•|◦|·|x|x|x|x|x|x|x|  <-- bullets

|a|b|c|d|e|f|g|h|i|j|
|✓|✗|☐|☑|☒|x|x|x|x|x|  <-- checks

|a|b|c|d|e|f|g|h|i|j|
|❖|✦|✧|‣|⁃|x|x|x|x|x|  <-- special
```

## Diagonals

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|/|\|X|x|x|x|x|x|x|x|  <-- ASCII
|╱|╲|╳|x|x|x|x|x|x|x|  <-- diagonals unicode
```

## Punctuation

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|·|x|x|x|x|x|x|x|x|x|  <-- dot
|…|⋯|⋮|x|x|x|x|x|x|x|  <-- ellipsis
```

## Arcs and Corners

```
|a|b|c|d|e|f|g|h|i|j|  <-- reference
|⌒|⌓|◜|◝|◞|◟|x|x|x|x|  <-- arcs
```

## JetBrains Mono Test Results (2026-01-21)

### OK (properly aligned) - Verification Grid
```
|a|b|c|d|e|f|g|h|i|j|  ref
|←|→|↑|↓|↔|↕|↖|↗|↘|↙|  arrows
|┌|─|┬|┐|│|├|┼|┤|└|┘|  box single
|╔|═|╦|╗|║|╠|╬|╣|╚|╝|  box double
|╭|╮|╰|╯|x|x|x|x|x|x|  box rounded
|┏|━|┳|┓|┃|┣|╋|┫|┗|┛|  box heavy
|─|━|│|┃|═|║|┆|┇|┊|┋|  lines
|░|▒|▓|█|▀|▄|▌|▐|x|x|  shading
|▖|▗|▘|▙|▚|▛|▜|▝|▞|▟|  quadrants
|+|-|x|:|=|<|>|x|x|x|  math basic
|/|\|X|╱|╲|╳|x|x|x|x|  diagonals
|·|⋯|⋮|x|x|x|x|x|x|x|  dots/ellipsis
```

### BROKEN - TOO WIDE
```
fancy arrows:   ➔ ➜ ➤ ➡
double arrows:  ⇐ ⇒ ⇑ ⇓ ⇔ ⇕
triangles:      ◀ ▶ ▲ ▼ ◄ ► △ ▽ ◁ ▷
circles:        ○ ● ◎ ◉ ⊙ ◯ ⬤ ⦿ ⦾
squares:        □ ■ ▢ ▣
diamonds:       ◇ ◆
stars:          ☆ ★
half-circles:   ◐ ◑ ◒ ◓
brackets:       ( ) { } [ ] < > ⟨ ⟩ 〈 〉 ⦃ ⦄
math set/logic: ∈ ⊂ ⊃ ∩ ∪ ∧ ∨ ¬ ⊕ ⊗
bullets:        • ◦
checks:         ✓ ✗ ☐ ☑ ☒
decorative:     ❖ ✦ ✧ ‣ ⁃
arcs:           ⌒ ⌓ ◜ ◝ ◞ ◟
```

### BROKEN - TOO NARROW
```
…                                      horizontal ellipsis
```

### AVOID List (for transcribe.md)
```
➔ ➜ ➤ ➡ ⇐ ⇒ ⇑ ⇓ ⇔ ⇕ ◀ ▶ ▲ ▼ ◄ ► △ ▽ ◁ ▷
○ ● ◎ ◉ ⊙ ◯ ⬤ ⦿ ⦾ □ ■ ▢ ▣ ◇ ◆ ☆ ★ ◐ ◑ ◒ ◓
( ) { } [ ] < > ⟨ ⟩ 〈 〉 ⦃ ⦄
∈ ⊂ ⊃ ∩ ∪ ∧ ∨ ¬ ⊕ ⊗ • ◦ ✓ ✗ ☐ ☑ ☒ ❖ ✦ ✧ ‣ ⁃ ⌒ ⌓ ◜ ◝ ◞ ◟ …
```

## How to Read Results

1. View on GitHub (not IDE)
2. Each `|` should align vertically with the reference row
3. If a `|` shifts right: preceding char is TOO WIDE
4. If a `|` shifts left: preceding char is TOO NARROW
5. Mark broken chars for AVOID list

