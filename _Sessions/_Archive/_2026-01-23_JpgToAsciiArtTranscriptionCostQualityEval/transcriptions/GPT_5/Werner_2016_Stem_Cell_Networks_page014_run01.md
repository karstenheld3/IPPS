# Eric Werner, Stem cell networks

11

Fig. 7: Network NI_k G_1, Multi-linear stem cell network starting from 2^k identical cells:
This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n,k) = {
    2^n                             if n <= k
    2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2)   for n > k
}

## 3.2  Stem cells that generate identical cells

Fig. 8: Network NG_1 I_k, Linear stem cell producing 2^k identical cells each loop: This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

**Figure 7: Network NI_k G_1 — Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[NI_k G_1 - Multi-linear stem cell network starting from 2^k identical cells]

Legend:
- [green αx] = identical-division edges (above, left-to-right)
- [blue αx]  = self/loop or linear-control edges (below/right)
- [red ====] = omitted repeated identical nodes
- B = linear stem cell; C = terminal cells

               [green α1]   [green α2]                 [green αk]
 A0    A1       A2           ...            A(k-1)       A_k = B    -> C
[o]----->[o]----->[o]---[========== red =========]----->[o]----->(terminal)
 |α0 (blue loop)|α1 (blue loop)|α2 (blue loop)                 |
  \___________/   \__________/  \__________/                  [blue c] to C

Nodes shown left-to-right:
 A0   A1   A2   ...   A(k-1)   A_k(=B)

Lower blue semi-loops under each A_i indicate persistent stemness at that stage.
Rightmost blue arrow from B to C indicates production of terminal cells C.
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~110x17 characters
- ASCII captures: A linear chain of A-nodes (A0...A_k), green above-edge labels α1..αk, blue loops under A-nodes, an omitted middle segment marked by a red hashed band, and a final arrow from B to C.
- ASCII misses: Exact curvature, colors (green/blue/red), and precise glyph styling of α labels.
- Colors:
  - green - identical division edges above
  - blue - self/linear-control loops and B→C edge
  - red - elided repeated segment between A2 and A(k−1)
- Layout: Nodes placed left-to-right culminating in A_k = B, then an arrow to C; loops beneath each A_i; top arcs imply progression α1→αk.
- Details: The original shows smooth curved arrows; here represented as straight arrows and textual loops.
- Data: Labels A0, A1, A2, A(k−1), A_k = B, C; α0..αk; an elided red region; final production of C.
- Reconstruction hint: Imagine curved green arrows above connecting successive A_i, small blue semicircular loops under each A_i, and a thick red dotted bar indicating omitted nodes.
</transcription_notes>

**Figure 8: Network NG_1 I_k — Linear stem cell producing 2^k identical cells each loop**

```ascii
[NG_1 I_k - Linear stem cell producing 2^k identical cells each loop]

Legend:
- [green αx] = identical-division edges above
- [blue αx]  = sustaining/loop edges below
- [red ====] = omitted repeated identical nodes
- B = linear stem cell generating identical cells each loop

A_L  --(green αL)-->  A0 --(green α1)--> A1 --(green α2)--> A2 --[==== red ====]--> A(k-1) --(green αk)--> A_k = B
[o]                  [o]                 [o]                [o]                     [o]
 |αL (blue loop)      |α0 (blue loop)     |α1 (blue loop)    |α2 (blue loop)         |αk (blue loop)

Right side behavior:
B (A_k) --[blue linear control each round]--> produces 2^k identical daughter cells
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~118x14 characters
- ASCII captures: Leftmost A_L feeding into chain A0→A1→A2→...→A(k−1)→A_k=B with green-labeled transitions; blue loops beneath nodes; omitted middle segment in red; emphasis that B is the stage producing identical cells each loop.
- ASCII misses: Exact loop geometry and color fidelity; no explicit rendering of produced daughter cells as icons.
- Colors:
  - green - identical-division progression edges
  - blue - sustaining self/loop edges
  - red - elided repeated nodes in the middle of the chain
- Layout: Linear left-to-right path starting from A_L then A0 up to A_k (=B), with per-node lower loops.
- Details: Original uses curved arrows and color; ASCII simplifies to straight arrows and text labels.
- Data: Node labels A_L, A0, A1, A2, A(k−1), A_k = B; αL, α0..αk; description that B yields 2^k identical daughters per loop.
- Reconstruction hint: Visualize curved green arrows above connecting nodes and blue curved loops beneath each node, with B as the rightmost node.
</transcription_notes>

<!-- Tokens: in=1299 out=4917 -->