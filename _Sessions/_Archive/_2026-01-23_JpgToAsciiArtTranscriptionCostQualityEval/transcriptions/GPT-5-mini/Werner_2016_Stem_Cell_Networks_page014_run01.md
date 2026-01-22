# Eric Werner, Stem cell networks

Eric Werner, Stem cell networks                                                                  11

Fig. 7: Network N1kG1 Multi-linear stem cell network starting from 2^k identical cells:
This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell subnetwork that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7

Cells(n,k) = {
  2^n                                if n <= k
  2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2)   for n > k
}

**Figure 1: Illustration of Fig. 7 (diagram transcription)**

```ascii
[DIAGRAM TITLE - Network N1kG1 Multi-linear stem cell network starting from 2^k identical cells]
[Legend: (o) = division node, [RED] = stem cell state bar, [BLUE] = terminal cell bar
         αi = upward green control arrow, αi (below) = downward blue loop arrow, c = terminal arrow]

                     α1         α2                     αk-1        αk
                  o----->      o----->    ...    o----->      o----->   o-----> o
                 (A0) [===] (A1) [===] (A2)      (Ak-1)[===] (Ak=B)[===] [C]
                   ^   α1      ^   α2               ^   αk-1     ^   αk      ^
                   |---------- |---------- ... -----|----------- |--------- |
                   |  (blue   |  (blue   )          |  (blue     |  (blue   )
                   |   loop)  |   loop)             |   loop)    |   loop)
                   |         |                     |            |        c
                   |         |                     |            |        ->
                   o         o                     o            o

Notes on ASCII:
- Each [===] denotes a horizontal rectangular stem-cell state (red in original).
- A0, A1, A2, ..., Ak-1, Ak = B label the stem states under the red bars.
- The final small blue bar at far right denotes terminal cell type C.
- Green upward arcs labeled α1, α2, ..., αk indicate forward control edges between stem nodes.
- Blue downward arcs (loops) labeled α1, α2, ..., αk indicate self-renewal/looping at each node.
- The terminal arrow from Ak=B to C labeled 'c' indicates differentiation to C.
```

<transcription_notes>
- Mode: Structural
- Dimensions: approx. 96x21 characters (width x height of ASCII block)
- ASCII captures:
  - Left-to-right sequence of stem states A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak = B -> C
  - Upward/forward control arrows (α1, α2, ..., αk)
  - Downward/looping self-renewal arcs at each node (α1, α2, ..., αk)
  - Final differentiation arrow labeled c from Ak = B to C
  - Visual distinction of stem-state bars ([===]) and terminal cell at far right
- ASCII misses:
  - Exact visual styling: colors (green arcs, blue arcs, red bars, blue terminal bar)
  - Small circular glyphs and precise curved arrow shapes
  - Spacing and dotted connector motif between A2 and Ak-1 used in original to indicate continuation
- Colors:
  - green (αi upward arcs) - control edges producing next stem state
  - blue (downward arcs and terminal bar) - self-renewal/terminal differentiation loop/terminal cell
  - red (horizontal bars) - stem cell state blocks
- Layout:
  - Nodes are laid out left-to-right in sequence A0, A1, A2, ..., Ak-1, Ak = B, then terminal C
  - Each stem node has a forward control arrow to the next node and a loop/back arc signifying self-renewal
- Details:
  - The original used small open circles at arrowheads and small filled/empty circles at loop bases
  - The Ak node shows both a self-loop (αk) and a forward differentiation to C (c)
- Data:
  - Labels include α1, α2, ..., αk, c, A0, A1, A2, ..., Ak-1, Ak = B, C
- Reconstruction hint:
  - Imagine red rectangular blocks as stem cell states with green curved arrows above connecting them,
    blue curved arrows below forming loops, and a final blue block for terminal C at the rightmost end.
</transcription_notes>

3.2 Stem cells that generate identical cells

Figure below (second diagram in page)

```ascii
[DIAGRAM TITLE - Network NG1Lk Linear stem cell producing 2^k identical cells each loop]
[Legend: (o) = division node, [RED] = stem cell state bar, [BLUE] = terminal cell bar
         αL = left loop control, α0..αk = loop/forward labels]

    αL
   (red loop)
     o
    (AL) [===]  (founder AL with loop)
      |
      v
    α0  α1       α2                αk-1  αk
 o-----> o-----> o-----> ... -----> o-----> o-----> o
(A_L)  (A0)   (A1)   (A2)   ...  (Ak-1) (Ak=B)  [C]
  ^      ^      ^       ^              ^       ^
  |      |      |       |              |       |
  |      |      |       |              |       |
  |      |      |       |              |       |
  |------|------|-------|--------------|-------|
  (blue loops α0,α1,α2,...,αk)

Notes on ASCII:
- Leftmost AL (A_L) has an additional self-loop αL (red loop in original).
- Sequence proceeds A_L -> A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak = B -> C.
- Each A_i has both an upward green forward control (αi) and a blue loop (self-renewal) beneath.
- The final Ak = B differentiates to terminal C via a blue terminal bar/arrow.
```

<transcription_notes>
- Mode: Structural
- Dimensions: approx. 96x20 characters
- ASCII captures:
  - The presence of an initial looped stem cell A_L with loop labeled αL
  - The chain A_L -> A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak = B -> C
  - Forward labels α0, α1, α2, ..., αk above/between nodes and blue loops beneath each node
  - The final differentiation to C from Ak = B
- ASCII misses:
  - Color encoding (red loop αL, green forward arcs, blue loops and blue terminal)
  - Small circular glyphs and exact curved geometry of arrows
  - The dashed/dotted segment representing omitted intermediate nodes in the original
- Colors:
  - red (αL loop and stem bars) - initial AL stem loop emphasis
  - green (α1, α2, ..., αk forward arcs) - forward control transitions
  - blue (loops and terminal) - self-renewal loops and terminal differentiation arrow/bar
- Layout:
  - Horizontal left-to-right progression with loops rendered below each node and an initial leftmost loop above AL
- Details:
  - Original included small open circles on arrow tails/heads and colored bars indicating stem vs terminal states
- Data:
  - Labels: αL, α0, α1, α2, ..., αk; A_L (AL), A0, A1, A2, ..., Ak-1, Ak = B, C
- Reconstruction hint:
  - Visualize a linear chain of red stem-state blocks each with a green forward arc and a blue self-loop; the leftmost AL block has an additional red loop αL and the chain culminates at Ak = B which differentiates to C.
</transcription_notes>

Fig. 8: Network NG1Lk Linear stem cell producing 2^k identical cells each loop: This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n,k) = 2^n otherwise.

<!-- Tokens: in=2465 out=4243 -->