# Eric Werner, Stem cell networks

11

Fig. 7: Network NIkG1 Multi-linear stem cell network starting from 2^k identical cells: This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7

Cells(n,k) = {  2^n                                    if n <= k
                2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2)   for n > k

3.2  Stem cells that generate identical cells

Fig. 8: Network NG1Ik Linear stem cell producing 2^k identical cells each loop: This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n×2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

**Figure 7: NI_kG1 Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[NI_kG1 - Multi-linear stem cell network starting from 2^k identical cells]
Legend: (alphaX) top control arrow; (loop alphaX) self-renewal loop; [::::] repeating/dotted

Top controls:        (alpha1)           (alpha2)                 ...                 (alphak)     (c)
Chain:         [A0] -------> [A1] -------> [A2] ---- [::::::: repeated :::::::] ----> [A(k-1)] -----> [Ak = B] -----> [C]
Self-renew:     (loop a0)     (loop a1)     (loop a2)                                   (loop ak)      (loop ak)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~120x6 characters
- ASCII captures: Linear chain of nodes A0 → A1 → A2 → ... → A(k-1) → Ak=B → C; top control arrows labeled alpha1..alphak and c; self-renewal loops under nodes; a repeated/dotted segment between A2 and A(k-1).
- ASCII misses: Exact curved arrow shapes; precise placement of labels; Greek letters (alpha) are spelled out; dashed/dotted red styling approximated with "[:::::::]".
- Colors:
  - Green: top control arrows labeled α1, α2, …, αk.
  - Red: long dotted segment between A2 and A(k−1).
  - Blue: bottom/self-renewal loops and arrow to C (label c).
- Layout: Nodes in a left-to-right line with loops above/below; final arrow from B to C on right.
- Details: Exact typography (subscripts/superscripts); loop curvature and thickness.
- Data: Node labels A0, A1, A2, …, A(k−1), Ak = B, C; labels α0/α1/α2/…/αk and c; repetition indicator.
- Reconstruction hint: Imagine colored curved arrows above (green) and below (blue) a horizontal series of labeled circles/boxes with a red dotted stretch in the middle leading to B, then a blue arrow to C.
</transcription_notes>

**Figure 8: NG1Ik Linear stem cell producing 2^k identical cells each loop**

```ascii
[NG1Ik - Linear stem cell producing 2^k identical cells each loop]
Legend: (alphaX) top control arrow; (loop alphaX) self-renewal loop; [::::] repeating/dotted

Top controls:   (alphaL)       (alpha1)         (alpha2)                 ...                 (alphak)
Chain:       [AL] -------> [A0] -------> [A1] -------> [A2] ---- [::::::: repeated :::::::] ----> [A(k-1)] -----> [Ak = B]
Self-renew:                 (loop a0)       (loop a1)       (loop a2)                              (loop ak)        (loop ak)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~120x6 characters
- ASCII captures: Leftmost AL feeding into a linear chain A0 → A1 → A2 → … → A(k−1) → Ak=B; top control arrows αL, α1, α2, … αk; self-renewal loops under nodes; repeated/dotted section in the middle.
- ASCII misses: Exact curved arrow geometry and colors; precise spacing of labels; Greek letters shown as "alpha".
- Colors:
  - Green: top control arrows αL, α1, α2, …, αk.
  - Red: dotted segment between A2 and A(k−1).
  - Blue: self-renewal loops including on B.
- Layout: Horizontal left-to-right progression starting at AL and ending at B.
- Details: No depiction of arrow thickness or exact node shapes; no gradients.
- Data: Node labels AL, A0, A1, A2, A(k−1), Ak = B; control labels αL, α1, α2, …, αk.
- Reconstruction hint: Visualize a colored, curved-arrow pathway across a row of labeled nodes with a red dotted stretch and loops under each node, culminating in B.
</transcription_notes>

<!-- Tokens: in=1299 out=7848 -->