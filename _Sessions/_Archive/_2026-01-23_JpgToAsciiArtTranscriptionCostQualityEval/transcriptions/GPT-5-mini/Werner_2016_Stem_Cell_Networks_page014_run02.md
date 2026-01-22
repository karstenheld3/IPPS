# [Page Title]

Eric Werner, Stem cell networks                                                                                      11

[Image — two figures with captions and explanatory text]

Fig. 7: Network N1kG1 Multi-linear stem cell network starting from 2^k identical cells:
This network generates k identical divisions to produce 2^k identical daughter stem cells of type
Ak = B from one founder cell A1.  The B stem cells are controlled by a linear stem cell sub-
network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while
retaining a constant 2^k of linear stem cells of type B.  Starting from one founder cell, the total
number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) =
2^k × (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where
k is the number of identical daughter cell divisions nodes in the network in Fig. 7

Cells(n,k) = { 2^n                                   if n <= k
               2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2)   for n > k }

**Figure 1: Network N1kG1 Multi-linear stem cell network (corresponds to Fig. 7 image)**

```ascii
[DIAGRAM TITLE - Network N1kG1 Multi-linear stem cell network]
Legend: (green arc) = α_i  (blue arc) = α_i (lower)  (red loop) = α_k  (c) = c (to C)
(width: ~90 chars)

   (A0)      (A1)      (A2)      ...      (Ak-1)       (Ak = B)        (C)
    o---------]===]---------]===]------ [===]  ------ [===]  ----------  []
    | red bar  red bar     red bar         red bar         blue bar        |
    |                                                                      |
   / \                                                                    |
  /   \                                                                   |
 /     \                                                                  |
α1      α1   α2      α2            α(k-1)    αk           αk             c v
^       ^    ^       ^             ^         ^            ^              v
\       /    \       /             \         \            /              []
 (green)   (green) (green)       (green)   (red loop)  (blue loop)
 below arcs:
  o       o     o               o            o
  |-------|-----|---------------|------------|
   α1      α2    α3  ...        α(k-1)      αk
 (blue arcs pointing back to previous nodes)

Semantics:
- Nodes: A0, A1, A2, ..., Ak-1, Ak (= B), C
- Top green arcs represent forward identical-division signals α1..αk
- Bottom blue arcs represent cyclic/feedback α1..αk
- At Ak a red self-loop α_k indicates additional self-renewal
- From Ak (=B) a blue arrow labeled "c" goes to terminal cell type C
```

<transcription_notes>
- Mode: Structural
- Dimensions: approx 90x18 characters (width x height in characters)
- ASCII captures: Linear chain of nodes (A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak = B -> C);
  green forward arcs α1..αk above nodes; blue feedback arcs α1..αk below nodes; red loop at Ak;
  label mapping of nodes and arrow semantics.
- ASCII misses: Precise graphical styling (colored bars, rounded arrow curvature), exact spacing,
  small circular node glyphs, dashed intermediate red segment between A2 and Ak-1, and exact
  visual proportions.
- Colors:
  - red bars / red loop - indicate stem-cell dividing segments / self-loop (α_k)
  - green arcs - labeled α1..αk represent forward identical-division arcs
  - blue arcs - labeled α1..αk (lower) represent feedback/renewal arcs; blue arrow 'c' to C
- Layout: Left-to-right sequence of stem cell nodes; repeated identical-division motifs; final node
  Ak marked as B then a terminal node C to the right.
- Details: The original used colored curved arrows (green above, blue below) and red rectangular
  bars for cell-level segments; a red looping arrow at Ak; a distinct blue arrow from Ak to C
  labeled "c".
- Data: Node labels (A0, A1, A2, ..., Ak-1, Ak = B, C) and arrow labels α1, α2, ..., αk, c.
- Reconstruction hint: Imagine a horizontal chain of red segments (stem stages) with pairs of
  curved green (above) and blue (below) arrows between successive segments; the final stage Ak
  has an extra red self-loop and a blue arrow to terminal cell C.
</transcription_notes>

3.2  Stem cells that generate identical cells

[Second figure and caption follow]

Fig. 8: Network NG1L Linear stem cell producing 2^k identical cells each loop: This linear
stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop.
The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division,
that ultimately produces n × 2^k terminal cells of type B.  Starting from one founder cell, the
total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) =
2^k × (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

**Figure 2: Network NG1L Linear stem cell producing 2^k identical cells each loop (corresponds to Fig. 8 image)**

```ascii
[DIAGRAM TITLE - Network NG1L Linear stem cell producing 2^k identical cells each loop]
Legend: (red loop AL)= α_L  (green arcs)= α1, α2, ...  (blue arcs lower)= α0, α1, ...
(width: ~100 chars)

  (AL)   (A0)      (A1)      (A2)      ...      (Ak-1)      (Ak = B)
   o------]===]-------]===]-------]===]-------]===]--------]===]
   | red bar for AL  red bar   red bar   red bar         red bar
   |  (red loop α_L)
   \/
   (red loop)
   α_L (self)
    ^
    |
    o   o        o        o            o           o
   / \ / \      / \      / \          / \         / \
  α0 α1  α1 α2  α2 ...   α(k-1)  αk (green arcs above successive nodes)
  (lower blue arcs labeled α0, α1, α2 ... point back)
   -----------------------------------------------------
   | lower blue loops: α0 -> A0, α1 -> A1, ... αk -> Ak |
   -----------------------------------------------------

Semantics:
- Nodes: AL, A0, A1, A2, ..., Ak-1, Ak (= B)
- AL has a red self-loop labeled α_L
- Each Ai has green forward arcs α1, α2,... and blue lower loops α0, α1,...
- This network indicates that at each loop 2^k identical daughter cells of Ak=B are produced
```

<transcription_notes>
- Mode: Structural
- Dimensions: approx 100x14 characters
- ASCII captures: Left-to-right linear chain of nodes starting with AL then A0..Ak; red self-loop at AL
  labeled α_L; repeated green arcs above and blue loops below for each Ai; final node Ak labeled B.
- ASCII misses: Exact colored rectangular bars, curved arc shapes, small open circles used in original,
  and precise visual spacing/dashed segments between A2 and Ak-1 in the original.
- Colors:
  - red (AL bar and loop) - denotes the AL stem cell and its self-loop α_L
  - green arcs - labeled α1, α2, ... above nodes representing forward identical-division arcs
  - blue arcs - lower arcs labeled α0, α1,... representing feedback/renewal loops
- Layout: Horizontal sequence with AL at left containing a red loop; subsequent identical-division modules
  A0..Ak linked; final Ak marked as B (stem output).
- Details: Original figure used color-coded arcs and bars, small circle glyphs marking connection points,
  and consistent iconography across nodes to show loop semantics.
- Data: Node and arrow labels preserved (AL, A0, A1, A2, ..., Ak = B; α_L, α0, α1, α2, ...).
- Reconstruction hint: Visualize a repeated module of a red rectangular segment (cell module) with green
  arcs above and blue arcs below linking successive modules; the AL module at the far left has an extra red
  looping arrow α_L indicating an initial self-loop.
</transcription_notes>

Fig. 8: Network NG1L Linear stem cell producing 2^k identical cells each loop: This linear stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

<!-- Tokens: in=2465 out=3835 -->