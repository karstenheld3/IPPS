# Eric Werner, Stem cell networks                                                11

**Figure 7: Network NI.G₁ Multi-linear stem cell network starting from 2ᵏ identical cells:**

```ascii
[MULTI-LINEAR STEM CELL NETWORK - DIVISION PATTERN]

        αₖ
    O------>O
    |       |
    |   αₖ  |
A₀===========A₁  αₖ
O             O------>O
|             |       |
|    α₁       |   α₂  |           αₖ         αₖ
|             |       |           O------>O------>O
|             |       |           |       |       |
=============A₁===========A₂ ■■■■■■■■■ Aₖ₋₁===========Aₖ = B========C
              O           O           O               O
              |           |           |               |
              |    α₂     |           |      αₖ       |      c
              |___________|           |_______________|

Legend: === Red (Type A/B cells)  === Blue (Type C cells)  ■■■ Dotted continuation
        O = Cell division node  --> = Division arrow
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x12 characters
- ASCII captures: Network topology, cell types, division patterns
- ASCII misses: Exact color shading (red vs blue bars)
- Colors:
  - Red - Type A and B stem cells
  - Blue - Type C terminal cells
- Layout: Linear progression with self-loops and division branches
- Details: Shows 2ᵏ starting cells progressing through k rounds of division
- Data: Mathematical formula preserved in caption
- Reconstruction hint: Self-loops indicate cell self-renewal, straight progression shows differentiation
</transcription_notes>

This network generates k identical divisions to produce 2ᵏ identical daughter stem cells of type Aₖ = B from one founder cell A₁. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2ᵏ × n terminal cells of type C while retaining a constant 2ᵏ of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2) if n > k and Cells(n,k) = 2ⁿ otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n,k) = {
    2ⁿ                                              if n <= k
    2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2)      for n > k

### 3.2 Stem cells that generate identical cells

**Figure 8: Network NG11. Linear stem cell producing 2ᵏ identical cells each loop:**

```ascii
[LINEAR STEM CELL NETWORK - 2ᵏ IDENTICAL CELLS PER LOOP]

    αₗ
O------>O
|       |
|       |                                               αₖ
Aₗ===========A₀     α₁        A₁     α₂        A₂ ■■■■■■■■■ Aₖ₋₁========Aₖ = B
O             O------------->O------------->O                O
|             |              |              |                |
|      α₀     |       α₁     |       α₂     |         αₖ     |
|_____________|______________|______________|________________|

Legend: === Red (Type A/B cells)  ■■■ Dotted continuation
        O = Cell division node  --> = Division arrow
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x8 characters
- ASCII captures: Linear progression with feedback loops, cell divisions
- ASCII misses: Blue coloring for type B cells
- Colors:
  - Red - Type Aₖ cells
  - Blue - Type B terminal cells (shown as "= B" in ASCII)
- Layout: Linear chain with self-loops at each stage
- Details: Each loop produces 2ᵏ identical daughter cells
- Data: Mathematical formulas preserved exactly
- Reconstruction hint: Self-loops show stem cell maintenance while producing daughters
</transcription_notes>

This linear stem cell network generates 2ᵏ identical daughter cells of type Aₖ = B at each stem cell loop. The Aₗ stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2ᵏ terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2) if n > k and Cells(n,k) = 2ⁿ otherwise.

<!-- Tokens: in=2244 out=1310 -->