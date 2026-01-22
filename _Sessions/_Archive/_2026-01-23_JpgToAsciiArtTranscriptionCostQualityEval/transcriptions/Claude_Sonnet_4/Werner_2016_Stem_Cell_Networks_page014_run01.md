# Eric Werner, Stem cell networks

**Figure 7: Network NLkG1 Multi-linear stem cell network starting from 2k identical cells:**

```ascii
[STEM CELL NETWORK - LINEAR CHAIN WITH BRANCH TO TERMINAL CELLS]

    α1        α2              αk    αk
   ↗ ↘      ↗ ↘             ↗ ↘   ↗ ↘
  A0 ═══ A1 ═══ A2 ┅┅┅┅┅ Ak-1 ═══ Ak = B ███ C
  ↘     ↙↘     ↙            ↘       ↙↘   ↙
   α1        α2              αk      f c

[Legend: ═══ red stem cells, ┅┅┅ dashed connection, ███ blue terminal, 
         α arrows = division pathways, f,c = final transitions]
```

<transcription_notes>
- Mode: Structural
- Dimensions: 65x8 characters
- ASCII captures: Linear chain structure, division pathways, cell type transitions
- ASCII misses: Color coding (red/blue), exact arrow curvatures, precise cell shapes
- Colors:
  - Red - stem cells A0 through Ak
  - Blue - terminal cell type C
- Layout: Horizontal linear progression with curved feedback loops above and below
- Details: Self-renewal loops (α arrows), transition from stem to terminal cells
- Data: Formulas for cell counts after n divisions
- Reconstruction hint: Imagine red rectangular cells in chain with curved arrows looping back, blue final cell
</transcription_notes>

This network generates k identical divisions to produce 2k identical daughter stem cells of type Ak = B from one founder cell A1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2k × n terminal cells of type C while retaining a constant 2k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2k + 2k × (n - k + 1) = 2k × (n - k + 2) if n > k and Cells(n, k) = 2n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n, k) = {
    2n                                      if n <= k
    2k + 2k × (n - k + 1) = 2k × (n - k + 2)  for n > k
}

## 3.2 Stem cells that generate identical cells

**Figure 8: Network NG II, Linear stem cell producing 2k identical cells each loop:**

```ascii
[LINEAR STEM CELL NETWORK - SELF-RENEWING WITH TERMINAL OUTPUT]

   αL
  ↗ ↘
 AL ○ → A0 ═══ A1 ═══ A2 ┅┅┅┅┅ Ak-1 ███ Ak = B
    ↘   ↙↘     ↙↘     ↙           ↘     ↙
     α0   α1     α2               αk

[Legend: ○ self-renewing stem cell AL, ═══ linear chain, 
         ███ terminal cell B, α = division pathways]
```

<transcription_notes>
- Mode: Structural  
- Dimensions: 60x6 characters
- ASCII captures: Self-renewing stem cell, linear progression, terminal endpoint
- ASCII misses: Color coding, curved arrow paths, exact cell shapes
- Colors:
  - Red - stem cells AL through Ak-1
  - Blue - terminal cell type B (Ak)
- Layout: Self-renewing cell on left feeding into horizontal linear chain
- Details: AL has self-renewal loop, linear progression ends at terminal cell B
- Data: Produces n×2k terminal cells after n rounds
- Reconstruction hint: Imagine red cells in linear chain with blue terminal cell, curved feedback loops
</transcription_notes>

This linear stem cell network generates 2k identical daughter cells of type Ak = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2k + 2k × (n - k + 1) = 2k × (n - k + 2) if n > k and Cells(n, k) = 2n otherwise.

<!-- Tokens: in=2244 out=1162 -->