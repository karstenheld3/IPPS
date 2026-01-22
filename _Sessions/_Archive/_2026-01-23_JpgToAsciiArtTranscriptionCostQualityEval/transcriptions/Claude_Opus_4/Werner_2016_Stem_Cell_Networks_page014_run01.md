# Eric Werner, Stem cell networks (Page 11)

```ascii
[MULTI-LINEAR STEM CELL NETWORK - NETWORK NL₁G₁]

        α₁               α₂                         αₖ
    ↗       ↖       ↗       ↖                  ↗       ↖
   O         O     O         O                O         O
  A₀========A₁========A₂=====...===Aₖ₋₁========Aₖ==B====C
   O         O     O         O                O         O
    ↖       ↙       ↖       ↙                  ↖       ↙
        α₁               α₂                         αₖ     c

Legend: === solid red line    == solid blue line    ... dotted red line
        O = cell division node    αᵢ = division type
```

<transcription_notes>
- Mode: Structural
- Dimensions: 70x8 characters
- ASCII captures: Linear network topology, division nodes, cell progression
- ASCII misses: Color coding (red for A-type cells, blue for B-C cells)
- Colors:
  - Red - stem cells of type A₀ through Aₖ
  - Blue - terminal cells B and C
  - Red dotted - continuation indicator
- Layout: Linear chain with symmetric division loops at each node
- Details: Each αᵢ represents identical daughter cell division
- Data: 2ᵏ identical cells, n rounds of division
- Reconstruction hint: Shows controlled stem cell differentiation pathway
</transcription_notes>

**Fig. 7: Network NL₁G₁. Multi-linear stem cell network starting from 2ᵏ identical cells:**
This network generates k identical divisions to produce 2ᵏ identical daughter stem cells of type Aₖ = B from one founder cell A₁. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2ᵏ × n terminal cells of type C while retaining a constant 2ᵏ of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2) if n > k and Cells(n, k) = 2ⁿ otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n, k) = { 2ⁿ                                           if n <= k
              { 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2)   for n > k

## 3.2 Stem cells that generate identical cells

```ascii
[LINEAR STEM CELL NETWORK - NETWORK NG11]

        αL
    ↗       ↖
   O         O              α₁               α₂                         αₖ
  AL========A₀========A₁========A₂=====...===Aₖ₋₁========Aₖ==B
   O         O     O         O     O         O                O         O
    ↖       ↙       ↖       ↙       ↖       ↙                  ↖       ↙
        α₀               α₁               α₂                         αₖ

Legend: === solid red line    == solid blue line    ... dotted red line
        O = cell division node    αᵢ = division type
```

<transcription_notes>
- Mode: Structural
- Dimensions: 75x7 characters
- ASCII captures: Linear network with initial self-renewal loop, progression chain
- ASCII misses: Color coding (red for A-type cells, blue for B cells)
- Colors:
  - Red - stem cells AL through Aₖ
  - Blue - terminal cells of type B
  - Red dotted - continuation indicator
- Layout: Linear chain with asymmetric division at AL, identical divisions after
- Details: AL has self-renewal (αL loop), each subsequent node produces 2 identical daughters
- Data: Produces n×2ᵏ terminal B cells while maintaining stem cell population
- Reconstruction hint: Shows controlled amplification with stem cell maintenance
</transcription_notes>

**Fig. 8: Network NG11. Linear stem cell producing 2ᵏ identical cells each loop:** This linear stem cell network generates 2ᵏ identical daughter cells of type Aₖ = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n×2ᵏ terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2ᵏ + 2ᵏ × (n - k + 1) = 2ᵏ × (n - k + 2) if n > k and Cells(n, k) = 2ⁿ otherwise.

<!-- Tokens: in=2244 out=1297 -->