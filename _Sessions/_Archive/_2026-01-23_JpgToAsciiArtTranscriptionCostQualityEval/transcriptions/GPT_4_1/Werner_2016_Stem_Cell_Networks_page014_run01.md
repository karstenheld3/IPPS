# Eric Werner, Stem cell networks

---
Page 11

**Fig. 7: Network NkG1 Multi-linear stem cell network starting from 2^k identical cells:**  
This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n, k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7:

Cells(n, k) = {  2^n                         if n <= k  
        2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2)    for n > k  
}

---

## 3.2 Stem cells that generate identical cells

**Fig. 8: Network NG1L Linear stem cell producing 2^k identical cells each loop:**  
This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n, k) = 2^n otherwise.

---

**Figure 7: Network NkG1 Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[NETWORK NkG1 MULTI-LINEAR STEM CELL NETWORK STARTING FROM 2^k IDENTICAL CELLS]

     α1        α2           αk         c
A0 ----> A1 ----> A2 --- ... ---> Ak=B ----> C
^         ^         ^           ^
|         |         |           |
|         |         |           |
α0        α1        α2          αk         

(Red vertical bars between A2 and Ak-1 = multiple nodes/steps)

Legend:
A0, A1, ..., Ak-1, Ak = B : Stem cell nodes (circles)
--->    : progression arrows (green/blue)
c             : terminal cell output arrow (blue)
α labels      : feedback or loop arrows (green)
red segment   : represents repeated division process
```

<transcription_notes>
- Mode: Structural
- Dimensions: approx. 87x11 characters
- ASCII captures: Sequential A nodes from A0 to Ak, arrows indicating linear progression, feedback/loop arrows, red repeated region, output to "C".
- ASCII misses: Colors (actual green/blue/red arrows), node shapes (all shown as circles in figure), node border colors, arrowhead styles.
- Colors:
  - Green: α (alpha) feedback/loop arrows
  - Blue: linear progression arrows and terminal output
  - Red: region marking repeats between A2 and Ak-1
- Layout: Linear chain with repeated interior, feedback/loop arrows return to previous nodes.
- Details: Feedback/loop arcs are slightly curved above/below nodes; all node labels visible.
- Data: n, k, explicit "A0", "A1", ..., "Ak = B", "C", with α0...αk.
- Reconstruction hint: Imagine colored arrows; vertical bar region to indicate mid-network expansion.
</transcription_notes>

---

**Figure 8: Network NG1L Linear stem cell producing 2^k identical cells each loop**

```ascii
[NETWORK NG1L LINEAR STEM CELL PRODUCING 2^k IDENTICAL CELLS EACH LOOP]

     α_L         α1      α2           αk
AL ----> A0 ----> A1 ----> A2 ---...---> Ak-1 ----> Ak=B
^          ^         ^            ^
|          |         |            |
α0         α1        α2           αk

(Red vertical bars between A2 and Ak-1 = multiple nodes/steps)

Legend:
AL, A0, A1, ..., Ak-1, Ak = B : Stem/stem loop nodes (circles)
--->  : arrows of division/progression (green/blue)
α labels : feedback/loop arrows (green)
red segment: repeated nodes/steps
```

<transcription_notes>
- Mode: Structural
- Dimensions: approx. 95x10 characters
- ASCII captures: Sequential chain from AL to Ak = B, emphasis on loops/feedback at each node, interior repeat region.
- ASCII misses: Colors (distinction between green, blue, red), specific circular node style, layer separation.
- Colors:
  - Green: α feedback/loop arrows
  - Blue: progression arrows
  - Red: region indicating repetitions (multi-step)
- Layout: Linear chain with feedback/loop arrows at each transition; repeated region marked.
- Details: Title and legend present; feedback/loop arcs above nodes.
- Data: AL, A0, A1, ..., Ak-1, Ak = B, α labels.
- Reconstruction hint: Colored/arced arrows show stem cell loops and identical output at Ak = B.
</transcription_notes>
