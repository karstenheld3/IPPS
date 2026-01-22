# Eric Werner, Stem cell networks 11

Fig. 7: Network NI_kG_1 Multi-linear stem cell network starting from 2^k identical cells: This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n,k) = { 
  2^n                             if n <= k
  2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2)   for n > k
}

3.2  Stem cells that generate identical cells

Fig. 8: Network NG1I_k Linear stem cell producing 2^k identical cells each loop: This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

**Figure 7: Network NI_kG_1 Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[NI_kG_1 — Multi-linear stem cell network from 2^k identical cells]
Legend: [A*] = stem cell stage, [B] = linear stem cell, [C] = terminal cell
        a# = alpha# edges (α# in original), c = edge to C
        Top forward arcs = a1..ak ; Bottom return arcs = a1..ak

                 a1            a2                         ak
[A0] ----- - - -> -> [A1] --- - - -> -> [A2] -- ... -- [Ak-1] --a k--> [Ak = B] --c--> [C]
  ^  <-- a1 --       ^  <-- a2 --                                     ^  <-- ak --
  |                                                                    
  |____________________________________________________________________________________
(back-return arcs shown below; red dotted path shown as "- - -"; curved geometry omitted)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~110x14 characters
- ASCII captures: Linear series of nodes A0…Ak-1 leading to Ak = B, with forward (alpha) edges,
  backward return edges, and the terminal edge from B to C (label c). Includes legend and labels.
- ASCII misses: Exact curved shapes of the arcs, dashed styling, and precise spacing of labels.
- Colors:
  - Red: dotted horizontal sequence from A0…Ak (represented by "- - -").
  - Green: forward α arcs above the nodes (represented as "a#" forward arrows).
  - Blue: return α arcs below the nodes (represented as "a#" backward arrows).
- Layout: A0 far left; A1, A2, …, Ak-1 to the right along a horizontal chain; Ak = B to the right of
  Ak-1; C at the far right with an arrow from B.
- Details: Original labels use Greek alpha (α1, α2, …, αk). In ASCII, these are written as "a1", …, "ak".
- Data: Node labels A0, A1, A2, Ak-1, Ak = B, and C are preserved; edge "c" from B to C is indicated.
- Reconstruction hint: Imagine green curved arrows above for α1..αk and blue curved arrows below returning
  from each stage to the previous; the red dotted horizontal path runs through the A-series to B.
</transcription_notes>

**Figure 8: Network NG1I_k Linear stem cell producing 2^k identical cells each loop**

```ascii
[NG1I_k — Linear stem cell producing 2^k identical cells each loop]
Legend: [AL] = controlling linear stem cell with loop (αL); [Ak = B] = terminal stem type
        a# = alpha# edges (α# in original)

         +-------+
         |  αL   |
         v       |
       [AL] -----+----> [A0] --a1--> [A1] --a2--> [A2] -- ... -- [Ak-1] --ak--> [Ak = B]
                                   ^<--a1--      ^<--a2--                         ^<--ak--
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~110x10 characters
- ASCII captures: Presence of the AL node with a self-loop (αL), the linear chain A0…Ak-1 to Ak = B,
  forward and backward α edges, and the concept of repeating loops producing 2^k identical cells.
- ASCII misses: Exact curvature of loops, color coding, and dotted styling.
- Colors:
  - Red: dotted path along A-series (represented by "...").
  - Green: forward α arcs (represented by "a#").
  - Blue: return α arcs (represented by backward "a#" arrows).
- Layout: AL with a loop at far left feeding into A0; successive A-stages lead to Ak = B on the right.
- Details: Greek α labels (αL, α1…αk) are rendered as "aL", "a1…ak" in ASCII due to ASCII-only rule.
- Data: Node labels AL, A0, A1, A2, Ak-1, Ak = B are preserved.
- Reconstruction hint: Visualize colored curved arrows: green above for forward α edges and blue below for
  return edges; AL has a prominent self-loop (αL) initiating each production loop.
</transcription_notes>

<!-- Tokens: in=1299 out=7375 -->