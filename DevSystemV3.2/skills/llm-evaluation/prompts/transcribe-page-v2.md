Transcribe the provided image(s) to complete markdown. **Nothing may be omitted.**

## Core Rules

1. **100% content preservation** - Every heading, paragraph, list, footnote, caption
2. **Tables** - Convert to markdown tables
3. **Special characters** - Use Unicode (α β γ, ¹ ² ³) not ASCII alternatives
4. **Math formulas** - Use LaTeX syntax (`$E = mc^2$`)

## Figure Protocol

Every figure MUST have BOTH ASCII art AND XML description.

### ASCII Art

**Mode A (Structural)** - For flowcharts, diagrams, UI:
- Use: `+ - | / \ _ [ ] ( ) { } < > -> <- v ^`
- Width: 80-120 characters
- Include inline labels and legends

**Mode B (Shading)** - For photographs, gradients:
- Density ramp: `@#%&8BWM*oahkbd=+-:.`

Format:
```
**Figure [N]: [Caption]**

```ascii
[ASCII art here]
```
```

### XML Description

After ASCII, add:
```
<transcription_notes>
- Mode: Structural | Shading
- Dimensions: [width]x[height] characters
- ASCII captures: What the ASCII shows
- ASCII misses: What cannot be shown
- Colors: List colors and what they represent
- Layout: Spatial arrangement
- Details: Fine details, textures, icons
- Data: Specific values or measurements
- Reconstruction hint: Key detail for imagination
</transcription_notes>
```

## Page Boundaries

If page has header/footer, include:
```
<transcription_page_footer> Page 5 | Company Name </transcription_page_footer>

---

<transcription_page_header> Document Title | Section </transcription_page_header>
```

## Output

Return the complete markdown transcription. Do not summarize or abbreviate.
