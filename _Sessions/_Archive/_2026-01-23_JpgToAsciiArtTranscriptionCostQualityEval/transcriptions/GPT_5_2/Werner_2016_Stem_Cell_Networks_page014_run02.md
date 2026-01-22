# Eric Werner, Stem cell networks

11

**Figure 7: Network Nl_kG_1  Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[DIAGRAM - Multi-linear stem cell network starting from 2^k identical cells]
Legend: (o) = state node   [====] = division/transition bar   curved arrows labeled by rates

(o) A0   [==== red ====]   A1   [==== red ====]   A2   [.. red dotted ..]   A_{k-1} [==== red ====] A_k = B [==== blue ====] C
  ^ \        alpha1           ^ \     alpha2          ...                      ^ \        alpha_k        ^ \         c
  |  \------------------------|  \-------------------                          |  \----------------------|  \---------------->
  |                            |                                             (green forward arcs)
 (blue reverse arcs under each red segment: alpha1 under A0->A1, alpha2 under A1->A2, ..., alpha_k under A_{k-1}->A_k=B)

Special loops:
- At A_k = B: a red self-loop labeled alpha_k (curved loop above B)
- From A_k = B to C: a blue arc labeled c (curved arc under/near the blue segment)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~118x13 characters
- ASCII captures: Sequence of states A0 -> A1 -> A2 -> ... -> A_{k-1} -> A_k=B -> C; forward (green) and reverse (blue) rate-labeled arcs; dotted red gap indicating repetition; special self-loop at B labeled alpha_k; transition to C labeled c.
- ASCII misses: Exact curvature/placement of arrows; exact color saturation and line thickness; small open-circle styling and precise arrowheads.
- Colors:
  - Red - linear stem cell segment / A-states progression bars and the self-loop at B
  - Green - forward arcs labeled alpha_1, alpha_2, ..., alpha_k
  - Blue - reverse arcs labeled alpha_1, alpha_2, ..., alpha_k and arc labeled c toward C; blue bar from B to C
- Layout: Left-to-right chain of labeled nodes and bars; green arcs above segments; blue arcs below segments; dotted red segment between A2 and A_{k-1}; B near right with a red loop above; final blue bar to C at far right.
- Details: Open circles at ends of arcs near each segment; labels alpha_i placed near corresponding arcs.
- Data: Node labels A0, A1, A2, A_{k-1}, A_k = B, C; arc labels alpha_1, alpha_2, alpha_k, c.
- Reconstruction hint: Visual shows repeated identical division stages (indicated by dotted red segment) culminating in B then producing C.
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

Cells(n, k) = { 2^n                               if n <= k  
              2^k + 2^k x (n - k + 1) = 2^k x (n - k + 2)   for n > k

## 3.2  Stem cells that generate identical cells

**Figure 8: Network NG1l_k Linear stem cell producing 2^k identical cells each loop**

```ascii
[DIAGRAM - Linear stem cell producing 2^k identical cells each loop]
Legend: (o) = state node   [====] = transition bar   curved arrows labeled by rates

(red loop) alpha_L
   .-----(curved)-----.
   |                  v
(o) A_L [==== red ====] A0 [==== red ====] A1 [==== red ====] A2 [.. red dotted ..] A_{k-1} [==== blue ====] A_k = B
           ^ \ alpha0        ^ \ alpha1        ^ \ alpha2          ...               ^ \ alpha_k
           |  \--------------|  \--------------|  \--------------                    |  \--------------->
        (blue reverse arcs under each segment: alpha0, alpha1, alpha2, ..., alpha_k)
        (green forward arcs above A0->A1 labeled alpha1, above A1->A2 labeled alpha2, ..., above A_{k-1}->A_k labeled alpha_k)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~118x14 characters
- ASCII captures: Left-to-right chain beginning with A_L then A0, A1, A2, ... to A_{k-1} and ending at A_k=B; red self-loop at A_L labeled alpha_L; forward green arcs (alpha_1, alpha_2, ..., alpha_k) and reverse blue arcs (alpha_0, alpha_1, alpha_2, ..., alpha_k); dotted red repetition segment; final segment shown in blue approaching A_k=B.
- ASCII misses: Exact positioning of open circles and arrowheads; the precise color boundaries where red bars switch to blue near the end; exact arc curvature.
- Colors:
  - Red - main linear stem cell bars (A_L through intermediate A-states)
  - Green - forward arcs labeled alpha_1, alpha_2, ..., alpha_k
  - Blue - reverse arcs labeled alpha_0, alpha_1, alpha_2, ..., alpha_k and the final bar into A_k=B
- Layout: A_L at far left with a red loop above; sequence of bars and labels across center; green arcs above, blue arcs below; dotted red gap between A2 and A_{k-1}; end state A_k=B at far right.
- Details: Rate labels placed near arcs; open-circle nodes at arc endpoints.
- Data: Node labels A_L, A0, A1, A2, A_{k-1}, A_k = B; arc labels alpha_L, alpha_0, alpha_1, alpha_2, alpha_k.
- Reconstruction hint: Emphasize that each loop through the linear chain yields 2^k identical cells of type A_k=B, with A_L regulating via the linear subnetwork.
</transcription_notes>

Fig. 8: **Network NG1l_k Linear stem cell producing 2^k identical cells each loop:** This linear  
stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop.  
The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division,  
that ultimately produces n x 2^k terminal cells of type B. Starting from one founder cell, the total  
number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k x (n - k + 1) =  
2^k x (n - k + 2) if n > k and Cells(n, k) = 2^n otherwise.

<!-- Tokens: in=2465 out=1694 -->