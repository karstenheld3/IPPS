# Eric Werner, Stem cell networks

---
**Fig. 7: Network NIkG1 Multi-linear stem cell network starting from 2^k identical cells:**
This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k * n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k * (n - k + 1) = 2^k * (n - k + 2) if n > k and Cells(n, k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n, k) = {  2^n                                      if n <= k
                2^k + 2^k * (n - k + 1) = 2^k * (n - k + 2)   for n > k

---

**Figure 7: Network NIkG1 Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[STEM CELL NETWORK NIkG1 STRUCTURE]

           (α1)          (α2)                       (αk)
   A0 ----> A1 ----> A2 ---- ... ----> Ak-1 ----> Ak = B ----> C
    ^       |       |                   |         |   
    |       v       v                   v         v
   (loop α0) (loop α1) (loop α2)    (loop αk-1) (loop αk)

Legend:
A0, A1, ..., Ak = Sequence of stem cell nodes
B = Set of identical daughter stem cells
C = Terminal cell type
αi = Division or transition step (with loops on each node)
Red dashed line = Repeating sequence for general k
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x13 characters
- ASCII captures: Node sequence (A0 to Ak = B to C), labeled arrows (α1 to αk), loopbacks on each node, dashed region for generic extension.
- ASCII misses: Precise color usage (red for dashed repeat extension, blue for some arrows and nodes), graphical node shapes, visual node/arrow styling (roundedness, thickness).
- Colors:
  - Red = repeated section (dashed line for extension)
  - Blue = transition and loop arrows
  - Green/black = other arrows and nodes
- Layout: Left-to-right chain with loopbacks at each step, dashed midsection, linear progression.
- Details: Importance of identical divisions indicated by multiple loops and node labels.
- Data: Ak = B indicates 2^k identical daughter cells produced; C is the terminal cell.
- Reconstruction hint: Imagine colored arrows (red, blue, green) and colored dashed lines for extension across central region.
</transcription_notes>

---

## 3.2 Stem cells that generate identical cells

---

**Figure 8: Network NG1I1 Linear stem cell producing 2^k identical cells each loop:**
This linear stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n * 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k * (n - k + 1) = 2^k * (n - k + 2) if n > k and Cells(n, k) = 2^n otherwise.

```ascii
[LINEAR STEM CELL NG1I1 - LOOPED PRODUCTION OF 2^k CELLS EACH CYCLE]

           (α1)          (α2)                      (αk)
   AL -->  A0 ----> A1 ----> A2 ---- ... ----> Ak-1 ----> Ak = B
    ^       |       |                   |         |   
    |       v       v                   v         v
   (loop α0) (loop α1) (loop α2)    (loop αk-1) (loop αk)

Legend:
AL = Founder stem cell for each loop
A0, ..., Ak = Linear chain of stem cell states
B = 2^k identical daughter (terminal) cells generated at Ak
αi = Division step (directed arrow with loop upon node)
Red dashed line = General k extension
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x12 characters
- ASCII captures: Node chain (AL to A0 ... Ak = B), inline loops for division/renewal, generalized loop/repeat shown, direction and labels.
- ASCII misses: Node and line color (original uses red for repeat, blue/green for different arrows), visual line thickness.
- Colors:
  - Red = repeated extension, loops
  - Blue = division arrows
  - Green = large loop arrow from terminal back to founder
- Layout: Left-to-right, loops return to founder, with division at each node.
- Details: Stepwise transitions (αi), terminal node B at right, process repeats via loop from B/AL.
- Data: Looped production of 2^k identical cells each cycle.
- Reconstruction hint: Original diagram features color-coded arrows and lines to indicate recurring steps and loops.
</transcription_notes>

---

[Continue with remaining text]