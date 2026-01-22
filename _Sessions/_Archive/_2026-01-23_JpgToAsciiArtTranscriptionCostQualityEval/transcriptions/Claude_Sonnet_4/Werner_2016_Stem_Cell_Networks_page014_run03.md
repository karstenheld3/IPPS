# Eric Werner, Stem cell networks                                                    11

**Figure 7: Network NL1 G1 Multi-linear stem cell network starting from 2^k identical cells:**

```ascii
[STEM CELL DIVISION NETWORK - LINEAR CASCADE WITH TERMINAL BRANCHING]

    α1        α2                αk      αk
  ----→    ----→             ----→   ↗---↖
 ○         ○         ○  ○     ○      ○     ○
A0 ===== A1 ===== A2 ::::: Ak-1 ===== Ak=B ===== C
○         ○         ○  ○     ○       ↘   f ↙
  ←----    ←----             ←----     ----→
   α1        α2                αk        c

Legend: [===] red stem cells, [:::] dotted connection, [===] blue terminal
        [○] cell nodes, [→] division pathways, [α] division parameters
```

<transcription_notes>
- Mode: Structural
- Dimensions: 65x8 characters
- ASCII captures: Linear progression A0→A1→A2→...→Ak-1→Ak=B→C, bidirectional arrows, cell nodes
- ASCII misses: Red/blue color coding of cell segments, exact arrow curvature
- Colors:
  - Red - stem cell segments A0 through Ak-1
  - Blue - terminal cell segment B to C
  - Dotted line - connection between Ak-1 and Ak
- Layout: Horizontal linear chain with feedback loops above and below
- Details: Greek letters α1, α2, αk labeling division rates, parameter 'c' and 'f'
- Reconstruction hint: Linear stem cell network with red stem cells transitioning to blue terminal cells
</transcription_notes>

This network generates k identical divisions to produce 2^k identical daughter stem cells of type Ak = B from one founder cell A1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n,k) = { 2^n                                    if n <= k
             { 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2)  for n > k

## 3.2 Stem cells that generate identical cells

**Figure 8: Network NG II, Linear stem cell producing 2^k identical cells each loop:**

```ascii
[LINEAR STEM CELL WITH SELF-RENEWAL LOOP - IDENTICAL CELL PRODUCTION]

  αL
 ↗--↖       α1        α2               αk
○    ○    ----→    ----→             ----→
AL ===== A0 ===== A1 ===== A2 ::::: Ak-1 ===== Ak=B
○    ○    ○       ○       ○    ○     ○         ○  f
 ↘--↙    ←----    ←----             ←----    ----→
  α0       α1        α2               αk

Legend: [===] red stem cells, [:::] dotted connection, [===] blue terminal
        [○] cell nodes, [→] division pathways, [α] parameters
        [AL] self-renewing stem cell with loop
```

<transcription_notes>
- Mode: Structural  
- Dimensions: 70x8 characters
- ASCII captures: Self-renewal loop at AL, linear progression to Ak=B, bidirectional arrows
- ASCII misses: Red/blue color distinction, exact loop curvature
- Colors:
  - Red - stem cell segments AL through Ak-1  
  - Blue - terminal segment Ak=B
- Layout: Self-renewing loop on left, then linear chain extending right
- Details: Parameters αL, α0, α1, α2, αk, and 'f', dotted connection before terminal
- Data: 2^k identical cells produced each loop, n×2^k terminal cells after n rounds
- Reconstruction hint: Linear stem cell network with prominent self-renewal loop producing identical outputs
</transcription_notes>

This linear stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n×2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

<!-- Tokens: in=2244 out=1299 -->