# Eric Werner, Stem cell networks                                                                                  11

[DIAGRAM 1 - top of page]

(A0)      (A1)      (A2)      ...     (Ak-1)    (Ak = B)    C
 o─[red]─o─[red]─o─[red]─o─[red]─o─[red]─o─[red]─o─[blue]─> (C)
  ^  α1   ^  α2    ^ αk            loop αk      c (arrow to C)
  v α1    v α2    v αk                        (blue lower loops)

Fig. 7: Network NIkG1 Multi-linear stem cell network starting from 2^k identical cells:
This network generates k identical divisions to produce 2^k identical daughter stem cells of type
Ak = B from one founder cell A1. The B stem cells are controlled by a linear stem cell sub-
network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while
retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total
number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n − k + 1) =
2^k × (n − k + 2) if n > k and Cells(n, k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where
k is the number of identical daughter cell divisions nodes in the network in Fig. 7

Cells(n,k) = {  2^n                                      if n <= k
                2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2)   for n > k  }

3.2    Stem cells that generate identical cells

[DIAGRAM 2 - lower of page]

(AL)     (A0)      (A1)      (A2)      ...     (Ak-1)    (Ak = B)
 o─(red)─o─[red]─o─[red]─o─[red]─o─[red]─o─[red]─o
 ^ αL    ^ α1    ^ α2   ^ αk (green upper loops)
 v α0    v α1    v α2   v αk (blue lower loops)

Fig. 8: Network NGI1k Linear stem cell producing 2^k identical cells each loop: This linear
stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop.
The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division,
that ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the
total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n − k + 1) =
2^k × (n − k + 2) if n > k and Cells(n, k) = 2^n otherwise.

**Figure 1: Fig. 7 (ASCII diagram + XML description)**

```ascii
[DIAGRAM TITLE - Multi-linear stem cell network starting from 2^k identical cells]
Legend: [R] = red stem-segment node, [B] = blue terminal segment (C)
        o = node/cell junction, --> = directed arrow
        green loop (αi) = upward arrow labeled αi
        blue loop (αi)  = downward arrow labeled αi
        red loop (αk)   = self-loop at Ak labeled αk
                                                                                
  o--[R]--o--[R]--o--[R]--o--...--o--[R]--o--[R=B]--[B]-->
  A0      A1      A2             Ak-1    Ak = B       C
   \^ α1   \^ α2   \^ α3          \^ αk   \^ αk
    \       \       \             \       \
     v α1    v α2    v α3          v αk    v c
   (lower loops)    (lower loops)              (arrow to C)
   
Inline labels:
 - Nodes: A0, A1, A2, ..., Ak-1, Ak = B, C
 - Upper green arcs: α1 above A0->A1, α2 above A1->A2, ..., αk above Ak-1->Ak
 - Lower blue arcs: α1 below A0->A1, α2 below A1->A2, ..., αk below Ak-1->Ak
 - At Ak there is a red self-loop labeled αk (self-renewal)
 - From Ak=B there is a blue arrow labeled c to terminal C

(ASCII captures the linear chain of labeled nodes, upper and lower loops,
 a self-loop at Ak, and an outgoing arrow to terminal C.)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~72x15 characters (ASCII art block)
- ASCII captures: linear sequence of nodes A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak = B -> C;
  upper green arcs labeled α1, α2, ..., αk; lower blue arcs labeled α1, α2, ..., αk;
  red self-loop at Ak labeled αk; arrow from Ak to C labeled c.
- ASCII misses: exact visual styling (colored bars: red segments for stem nodes, blue box for C),
  curved arc shapes, relative spacing/color; dashed red segment between A2 and Ak-1 in original,
  small open/closed circle glyphs at arrowheads.
- Colors:
  - red (stem) - represents proliferative stem cell segments (filled red bars in original)
  - green (upper arcs αi) - represent upward differentiation/activation arcs
  - blue (lower arcs αi and C) - represent lower loop/back-division or terminal differentiation
- Layout: nodes arranged left-to-right as A0 ... Ak = B then C at far right; loops above and below each link;
  self-loop at Ak.
- Details: original used colored curved arrows; some intermediate nodes represented by small empty circles.
- Data: labels α1, α2, ..., αk; ak index positions; equation references in caption preserved in main text.
- Reconstruction hint: imagine a horizontal chain of red rectangular stem segments linked by curved green arrows above
  and curved blue arrows below; the final stem Ak (colored red) has a red self-loop and also a blue outgoing arrow
  to a blue terminal block labeled C.
</transcription_notes>

**Figure 2: Fig. 8 (ASCII diagram + XML description)**

```ascii
[DIAGRAM TITLE - Linear stem cell producing 2^k identical cells each loop]
Legend: [R] = red stem-segment node, o = junction node, --> = directed arrow
        green loop (αi) = upward arrow labeled αi
        blue loop (αi)  = downward arrow labeled αi
        red loop (αL)   = self-loop at AL labeled αL

  o--[R]--o--[R]--o--[R]--o--...--o--[R]--o
  AL     A0     A1     A2           Ak-1  Ak = B
   \^ αL  \^ α1  \^ α2   \^ ...      \^ αk
    \      \      \                \
     v α0   v α1   v α2             v αk
  (lower blue loops)            (upper green loops)
  
Inline labels:
 - Nodes: AL, A0, A1, A2, ..., Ak-1, Ak = B
 - Upper green arcs: α1 above A0->A1, α2 above A1->A2, ..., αk above Ak-1->Ak
 - Lower blue arcs: α0 below AL->A0, α1 below A0->A1, α2 below A1->A2, ..., αk below Ak-1->Ak
 - AL has a red self-loop labeled αL

(ASCII captures the left-to-right linear chain with an initial AL node with self-loop,
 upper/lower loops at each link, and labeled nodes.)
```

<transcription_notes>
- Mode: Structural
- Dimensions: ~72x12 characters (ASCII art block)
- ASCII captures: chain AL -> A0 -> A1 -> A2 -> ... -> Ak-1 -> Ak = B; red self-loop at AL labeled αL;
  upper green loops α1, α2, ..., αk; lower blue loops α0, α1, α2, ..., αk; labeling of nodes.
- ASCII misses: color-coded rectangular bars, exact curved arcs shapes, dashed segments and precise graphic spacing;
  tiny open/closed circle glyphs at connectors.
- Colors:
  - red (stem segments including AL and intermediate red bars) - indicates stem cell segments
  - green (upper arcs) - indicate one class of daughter-division arcs
  - blue (lower arcs) - indicate another class of division/return arcs
- Layout: nodes laid left-to-right; AL at far left with self-loop; repeating motif across chain.
- Details: original had colored curved arrows and rectangular colored segments; ASCII approximates positions and labels.
- Data: labels α0, α1, α2, ..., αk and αL; nodes AL, A0, A1, ..., Ak = B retained.
- Reconstruction hint: visualize a horizontal series of red stem blocks connected by curved green arrows on top and blue arrows below,
  with a red self-loop at the leftmost AL and repeated identical loop structures producing 2^k daughter cells per loop.
</transcription_notes>

<!-- Tokens: in=2465 out=3427 -->