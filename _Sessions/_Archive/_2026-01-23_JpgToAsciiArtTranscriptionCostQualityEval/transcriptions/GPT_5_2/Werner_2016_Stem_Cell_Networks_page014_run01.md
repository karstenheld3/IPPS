# Eric Werner, Stem cell networks

11

**Figure 7: Network Nl_k G1  Multi-linear stem cell network starting from 2^k identical cells:**

```ascii
[NETWORK Nl_k G1 - Multi-linear stem cell network from one founder producing 2^k identical B cells, then C]

Legend: (o) = state node, [RED BAR] = linear A-chain segment, [BLUE BAR] = terminal C segment
        green arc = alpha_i (top), blue arc = alpha_i (bottom), red loop = alpha_k (self-loop at Ak=B)
        red dotted bar = omitted intermediate repeats, rightward bar indicates progression

 (o)A0         (o)A1         (o)A2                (o)Ak-1            (o)Ak = B     [BLUE BAR] -> C(o)
   \            \             \                     \                 ^   \              ^
    \alpha1      \alpha2       \alpha?               \alpha_k         |alpha_k(loop)     | c
     v            v             v                     v               |      \           |
  [RED BAR]    [RED BAR]     [RED BAR]      ...    [RED BAR]          |       v          |
     ^            ^             ^                     ^               |     (o)          |
    /alpha1      /alpha2       /alpha?               /alpha_k         |                   |
   /            /             /                     /                 +-------------------+
 (o)           (o)           (o)                   (o)
 (bottom arcs show alpha_i in blue returning around each red bar segment; final blue arc labeled c goes from B to C)
```

<transcription_notes>
- Mode: Structural
- Dimensions: 120x17 characters
- ASCII captures: Sequence of states A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak=B; top/bottom alpha_i arcs; dotted omitted region; B->C transition labeled c; self-loop at B labeled alpha_k.
- ASCII misses: Exact curvature of arrows; precise colors and thickness of bars; spacing/typography (subscripts, italics).
- Colors:
  - Red bars/dots/loop: linear stem cell chain and self-loop at Ak
  - Green arcs: top alpha_i transitions
  - Blue arcs/bar: bottom alpha_i transitions and final C segment
- Layout: Horizontal chain left-to-right; repeated modules; final node Ak=B connects to terminal C to the right; self-loop drawn above Ak=B.
- Details: Nodes shown as small circles; labels include A0, A1, A2, Ak-1, Ak=B, C, alpha1, alpha2, alpha_k, c; dotted red segment indicates omitted intermediate steps.
- Data: No numeric axes; symbolic labels only.
- Reconstruction hint: Think of repeated two-arc modules around each red segment (top green alpha_i, bottom blue alpha_i), then a final branching to a blue terminal segment C.
</transcription_notes>

Fig. 7: **Network Nl\_kG\_1  Multi-linear stem cell network starting from 2^k identical cells:**  
This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n, k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7

Cells(n,k) = { 2^n                           if n <= k  
              2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2)   for n > k

## 3.2  Stem cells that generate identical cells

**Figure 8: Network NG1l_k Linear stem cell producing 2^k identical cells each loop:**

```ascii
[NETWORK NG1l_k - Linear stem cell producing 2^k identical cells each loop]

Legend: (o)=state node, [RED BAR]=linear A-chain segment, [BLUE BAR]=terminal Ak=B segment
        red loop = alpha_L (self-loop at AL), green top arcs = alpha_i, blue bottom arcs = alpha_i

        alpha_L(loop)
           ^
           |
        (o)AL
          \
           \ alpha0 (blue bottom arc shown under first segment)
            v
          [RED BAR] -> A0(o)    [RED BAR] -> A1(o)    [RED BAR] -> A2(o)   ...   [RED BAR] -> Ak-1(o)   [BLUE BAR] -> Ak = B(o)
             ^  \alpha1(g)         ^  \alpha2(g)         ^  \alpha?(g)               ^  \alpha_k(g)             ^
             |                     |                     |                           |                          |
           alpha0(b)             alpha1(b)             alpha2(b)                    alpha_k(b)                 (bottom blue arc)
 (each segment has a green top arc alpha_i from left node to right node, and a blue bottom arc alpha_i returning around)
```

<transcription_notes>
- Mode: Structural
- Dimensions: 132x16 characters
- ASCII captures: Leftmost AL node with self-loop labeled alpha_L; progression through A0, A1, A2, ... Ak-1 to Ak=B; repeated red-bar modules; final Ak=B shown with a blue bar; green/blue arc labeling (alpha0, alpha1, alpha2, alpha_k).
- ASCII misses: Exact placement of small circles, precise arrowheads, and dotted red segment styling; exact color saturation.
- Colors:
  - Red bars/dots: linear chain segments and omitted intermediate region
  - Green arcs: upper alpha_i transitions
  - Blue arcs/bar: lower alpha_i transitions and final segment at Ak=B
- Layout: Horizontal chain; AL placed at far left with a red self-loop above it; intermediate modules repeat; final node Ak=B at far right.
- Details: Labels visible: AL, A0, A1, A2, Ak-1, Ak = B, alpha_L, alpha0, alpha1, alpha2, alpha_k.
- Data: No plotted values; symbolic parameters only.
- Reconstruction hint: Same repeating module as Fig. 7 but starting from AL with a self-loop, ending at Ak=B (blue segment), with a dotted omission region in the middle.
</transcription_notes>

Fig. 8: **Network NG1l\_k Linear stem cell producing 2^k identical cells each loop:** This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n×2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n, k) = 2^n otherwise.

<!-- Tokens: in=2465 out=1647 -->