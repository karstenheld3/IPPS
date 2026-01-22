# Eric Werner, Stem cell networks

Page 11 contains two figures discussing stem cell networks with mathematical descriptions.

**Figure 7: Network N1,G1 Multi-linear stem cell network starting from 2^k identical cells**

```ascii
       α1        α2             αk
   A0 ◯→     A1 ◯→     ...   Ak-1 ◯→ Ak = B
   ○ ←α1     ○ ←α2             ○ ←αk    ○ ←c
```

**Figure 8: Network NG1I, Linear stem cell producing 2^k identical cells each loop**

```ascii
       αL        α0        α1             αk
   AL ◯→     A0 ◯→     A1 ◯→     ...   Ak-1 ◯→ Ak = B
   ○ ←α0     ○ ←α1     ○ ←α2             ○ ←αk
```

## Text Transcription

### Figure 7 Description
This network generates k identical divisions to produce 2^k identical daughter cells:
- One founder cell A0 = B
- Linear stem cell sub-network
- After n rounds of division, jointly produce 2^k × n terminal cells of type C
- Maintaining a constant 2^k of linear stem cells of type B

### Cell Count Function
```
Cells(n,k) = {
  2^n     if n <= k
  2^k + 2^k × (n-k+1) = 2^k × (n-k+2)  for n > k
}
```

### Figure 8 Description
- Linear stem cell network generating 2^k identical daughter cells each loop
- Stem cell controlled by a linear stem cell sub-network
- After n rounds, produces n × 2^k terminal cells of type B

The transcription preserves the mathematical notation, cell network diagrams, and explanatory text exactly as shown in the original document.

<transcription_notes>
- Mode: Structural network diagram
- Captures: Cell division progression, mathematical growth model
- Misses: Precise spatial relationships and cell type nuances
- Symbols: 
  - ◯ represents cell
  - → shows division/progression
  - ← shows control/feedback
- Key visualization: Exponential cell generation patterns
</transcription_notes>

<!-- Tokens: in=2244 out=579 -->