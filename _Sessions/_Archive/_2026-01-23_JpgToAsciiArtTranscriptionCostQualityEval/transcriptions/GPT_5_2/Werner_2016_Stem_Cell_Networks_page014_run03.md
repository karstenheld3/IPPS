# Eric Werner, Stem cell networks

11

**Figure 7: Network Nl_kG_1  Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[DIAGRAM - MULTI-LINEAR STEM CELL NETWORK: A0 -> A1 -> ... -> Ak=B -> C]
Legend: [red bar] = division/transition stage A_i
        [blue bar] = terminal/output stage C
        (o) = node/vertex
        green arc label = alpha_i (top)
        blue arc label  = alpha_i (bottom)
        red arc label   = alpha_k (self/feedback at Ak=B)
        blue arc label  = c (transition from Ak=B to C)
        "........" = omitted repeated stages

   (o)        [red]        (o)        [red]        (o)      ........      (o)      [red]      (o)=[Ak=B]   [blue]    C
    A0  ----->==========--> A1  ----->==========--> A2  ---- ........ ---- Ak-1 --->==========-->  Ak=B   --->========--> C
     ^   alpha1 (blue)      ^   alpha2 (blue)      ^                     ^   alpha_k (blue)      \__ c (blue) __/
     \________________/     \________________/     \________________/     \________________/
      alpha1 (green)         alpha2 (green)         alpha2 (green)         alpha_k (green)

                                                           (red feedback at Ak=B)
                                                          alpha_k
                                                          (o)
                                                           \ 
                                                            )  (loop back to Ak=B)
                                                           /
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~118x18 characters
- ASCII captures: Sequential stages A0, A1, A2, ..., Ak-1 leading to Ak=B; colored/typed arcs approximated with labeled arcs; terminal C output from Ak=B with label c; omitted middle stages indicated by dots.
- ASCII misses: Exact curvature/placement of arcs, precise colors (green/blue/red), thickness of bars, spacing and typographic math formatting.
- Colors:
  - Green arcs: alpha_1, alpha_2, ..., alpha_k (top arcs)
  - Blue arcs: alpha_1, alpha_2, ..., alpha_k (bottom arcs) and c to C
  - Red: bars for A-stages and red feedback loop labeled alpha_k at Ak=B
  - Blue bar: C segment
- Layout: Left-to-right linear chain A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak=B, then to C on far right; feedback loop located above/right of Ak=B.
- Details: Nodes shown as small circles adjacent to labels; repeated red vertical ticks between A2 and Ak-1 in the original are represented as "........".
- Data: Labels include A0, A1, A2, Ak-1, Ak=B, C; alpha_1, alpha_2, alpha_k; c.
- Reconstruction hint: Think of a linear cascade of A-states with paired top/bottom arcs labeled alpha_i and a final state Ak=B that both loops (alpha_k) and outputs to terminal C (c).
</transcription_notes>

Fig. 7: **Network Nl_kG_1  Multi-linear stem cell network starting from 2^k identical cells:**  
This network generates k identical divisions to produce 2^k identical daughter stem cells of type  
A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-  
network that after n rounds of division, jointly produce 2^k x n terminal cells of type C while  
retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total  
number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k x (n - k + 1) =  
2^k x (n - k + 2) if n > k and Cells(n, k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where  
k is the number of identical daughter cell divisions nodes in the network in Fig. 7

Cells(n, k) = { 2^n                                     if n <= k  
               2^k + 2^k x (n - k + 1) = 2^k x (n - k + 2)  for n > k

## 3.2  Stem cells that generate identical cells

**Figure 8: Network NG1l_k  Linear stem cell producing 2^k identical cells each loop**

```ascii
[DIAGRAM - LINEAR STEM CELL LOOP PRODUCING 2^k IDENTICAL CELLS EACH LOOP]
Legend: [red bar] = division/transition stage A_i
        (o) = node/vertex
        green arc label = alpha_i (top)
        blue arc label  = alpha_i (bottom)
        red arc label   = alpha_L (loop at A_L)
        "........" = omitted repeated stages

      (red loop at far left)
        alpha_L
          __
         /  \
        v    \
      (o)     \
       A_L      \
                 \
 (o)      [red]      (o)      [red]      (o)      [red]      (o)    ........    (o)    [blue]     (o)=[Ak=B]
  A_L --->==========--> A0 --->==========--> A1 --->==========--> A2 ---........--- Ak-1 --->======--> Ak=B
     \__ alpha0 (blue)__/   \__ alpha1 (blue)__/   \__ alpha2 (blue)__/              \__ alpha_k (blue)__/
      alpha0 (green)         alpha1 (green)         alpha2 (green)                   alpha_k (green)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~120x18 characters
- ASCII captures: Leftmost stem cell A_L with a red self-loop labeled alpha_L; linear sequence A_L -> A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak=B; paired top/bottom arcs labeled alpha_0, alpha_1, alpha_2, ..., alpha_k.
- ASCII misses: Exact arc curvature, the precise rendering of the dashed red repetition marks in the middle, and the original color intensity and bar proportions.
- Colors:
  - Red: bars for A_L to Ak-1 stages; red loop labeled alpha_L
  - Green: top arcs labeled alpha_1, alpha_2, ..., alpha_k (and alpha_0 shown on first segment)
  - Blue: bottom arcs labeled alpha_0, alpha_1, alpha_2, ..., alpha_k
  - Blue bar: final segment near Ak=B (rendered as [blue] in ASCII)
- Layout: Horizontal chain across the page; special loop above leftmost A_L; ellipsis/dots indicate repeated intermediate stages; Ak=B at far right.
- Details: Nodes drawn as circles adjacent to labels; arrows implied by left-to-right connectors and arc annotations.
- Data: Labels include A_L, A0, A1, A2, Ak-1, Ak=B; alpha_L, alpha_0, alpha_1, alpha_2, alpha_k.
- Reconstruction hint: Imagine a linear “conveyor” of A-states with a leftmost looping controller A_L and repeated identical division motifs along the chain.
</transcription_notes>

Fig. 8: **Network NG1l_k  Linear stem cell producing 2^k identical cells each loop:** This linear  
stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop.  
The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division,  
that ultimately produces n x 2^k terminal cells of type B. Starting from one founder cell, the total  
number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k x (n - k + 1) =  
2^k x (n - k + 2) if n > k and Cells(n, k) = 2^n otherwise.

<!-- Tokens: in=2465 out=1774 -->