# Eric Werner, Stem cell networks                                                11

**Figure 7: Network NI₁G₁ Multi-linear stem cell network starting from 2ᵏ identical cells:**

```ascii
[MULTI-LINEAR STEM CELL NETWORK - 2^k FOUNDER CELLS]

        α₁              α₂                      αₖ
    ○-------○       ○-------○               ○-------○
    |       |       |       |               |       |
A₀ ═════ A₁ ═════ A₂ ░░░░░░░ Aₖ₋₁ ═════ Aₖ = B ═════ C
    |       |       |       |               |       |
    ○-------○       ○-------○               ○-------○
        α₁              α₂                      αₖ      c

Legend: ═══ = red cells (type A/B)  ░░░ = dashed continuation  ═══ = blue cells (type C)
        ○---○ = self-renewal loops   αᵢ = division parameters
```

<transcription_notes>
- Mode: Structural
- Dimensions: 75x8 characters
- ASCII captures: Network topology, cell progression from A₀ to C, self-renewal loops
- ASCII misses: Color coding (red for A/B cells, blue for C cells), precise loop curvature
- Colors:
  - Red - stem cells of type A and B
  - Blue - terminal cells of type C
- Layout: Linear chain with self-renewal loops above each node
- Details: Each αᵢ represents a division parameter; dotted section indicates continuation
- Data: Network generates 2ᵏ × n terminal C cells while maintaining 2ᵏ linear B stem cells
- Reconstruction hint: Imagine curved loops returning to same node, with red/blue cell coloring
</transcription_notes>

This network generates k identical divisions to produce 2ᵏ identical daughter stem cells of type Aₖ = B from one founder cell A₁. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2ᵏ × n terminal cells of type C while retaining a constant 2ᵏ of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2) if n > k and Cells(n,k) = 2ⁿ otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n,k) = { 2ⁿ                                    if n <= k
             { 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2)  for n > k

## 3.2 Stem cells that generate identical cells

**Figure 8: Network NGI1, Linear stem cell producing 2ᵏ identical cells each loop:**

```ascii
[LINEAR STEM CELL WITH 2^k IDENTICAL DAUGHTER PRODUCTION]

    αL
    ○-------○
    |       |
AL ═════ A₀ ═════ A₁ ═════ A₂ ░░░░░░░ Aₖ₋₁ ═════ Aₖ = B
    |       |       |       |               |       |
    ○-------○       ○-------○               ○-------○
        α₀              α₁      α₂              αₖ

Legend: ═══ = red cells (type A)  ░░░ = dashed continuation  ═══ = blue cells (type B)
        ○---○ = self-renewal loops   αᵢ = division parameters
```

<transcription_notes>
- Mode: Structural
- Dimensions: 70x7 characters
- ASCII captures: Linear stem cell network structure, self-renewal at AL, division chain
- ASCII misses: Color coding (red for AL/A cells, blue for B cells), precise loop shapes
- Colors:
  - Red - stem cells AL and A₀ through Aₖ₋₁
  - Blue - terminal cells of type B
- Layout: Linear progression with self-renewal loop only at AL, division loops at other nodes
- Details: AL has special self-renewal (αL), each Aᵢ produces 2ᵏ identical daughters
- Data: Produces n × 2ᵏ terminal B cells while maintaining one AL stem cell
- Reconstruction hint: First loop is self-renewal, others are division producing 2ᵏ cells
</transcription_notes>

This linear stem cell network generates 2ᵏ identical daughter cells of type Aₖ = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2ᵏ terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2) if n > k and Cells(n,k) = 2ⁿ otherwise.

<!-- Tokens: in=2244 out=1379 -->