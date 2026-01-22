# Eric Werner, Stem cell networks

---

**Fig. 7: Network NIkG1 Multi-linear stem cell network starting from 2^k identical cells:**
This network generates k identical divisions to produce 2^k identical daughter stem cells of type Ak = B from one founder cell A1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n, k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7:

                    { 2^n                            if n <= k
    Cells(n, k) = {
                    2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2)   for n > k

---

## 3.2 Stem cells that generate identical cells

---

**Figure 7: Network NIkG1 Multi-linear stem cell network starting from 2^k identical cells**

```ascii
[NETWORK NIkG1 MULTI-LINEAR STEM CELL NETWORK - 2^k IDENTICAL CELLS]
      +-----+         +-----+         +-----+       ...       +-----+         +-----+     +-----+
      |  A0 | --α1--> |  A1 | --α2--> |  A2 | ====         ==== | Ak-1| --αk--> | Ak=B |--c-->|  C  |
      +-----+         +-----+         +-----+       ...       +-----+         +-----+     +-----+
        ^               |               |                                                    
       α0              α1              α2                                                   
        |               v               v               
      +-----+         +-----+         +-----+       ...       +-----+         +-----+
      |  A0 | <-------|  A1 | <-------|  A2 | <--- ... <----- | Ak-1| <-------| Ak=B |
      +-----+         +-----+         +-----+       ...       +-----+         +-----+
```

<transcription_notes>
- Mode: Structural
- Dimensions: 100x14 characters
- ASCII captures: Linear progression of nodes A0, A1, A2... Ak=B with transitions (arrows α1, α2... αk), parallel lines showing bidirectional transitions, and terminus from Ak=B to C.
- ASCII misses: Node colors, precise curvature of arcs, and labels' styles.
- Colors:
    - Green (α) - represents the stem cell division transitions.
    - Blue (c, Ak=B, C) - indicates terminal transitions to C.
    - Red (section Ak-1 to Ak) - highlights region with major division.
- Layout: Left to right linear sequence; parallel line structure illustrates division and retention.
- Details: Precise shapes, spatial spacing, and multiple identical divisions per node.
- Data: Labels A0, A1, ..., Ak=B, C, α0, α1, ..., αk, c.
- Reconstruction hint: Imagine each arc and color for functionally distinct transitions and duplications.
</transcription_notes>

---

**Figure 8: Network NG1L Linear stem cell producing 2^k identical cells each loop**

```ascii
[NETWORK NG1L LINEAR STEM CELL PRODUCING 2^k IDENTICAL CELLS EACH LOOP]

    +-----+     +-----+     +-----+    ...    +-----+     +-----+     +-----+
    |  AL |--αL>|  A0 |--α1>|  A1 |--α2>| A2 |====...====>| Ak-1|--αk>| Ak=B|
    +-----+     +-----+     +-----+    ...   +-----+     +-----+     +-----+
      ^           |           |                       |     |                  
     α0          α1          α2                     αk-1   αk                 
      |           v           v                       v     v                 
    +-----+     +-----+     +-----+    ...   +-----+     +-----+      
    |  AL |<-----|  A0 |<-----|  A1 |<-...--| Ak-1|<-----| Ak=B |
    +-----+     +-----+     +-----+    ...   +-----+     +-----+
```

<transcription_notes>
- Mode: Structural
- Dimensions: 100x12 characters
- ASCII captures: Sequential looped architecture, where AL initiates a loop producing two or more daughter stem cells per cycle, culminating in Ak=B. Shows bidirectional flow and labelling for all key transition arcs.
- ASCII misses: Node and arrow colors, arc shapes/curvature, actual number of identical cells produced visually.
- Colors: 
    - Green (α transitions) - division/duplication events.
    - Red (central repeated segment) - each loop's output.
    - Blue (Ak=B, output node) - final stem cell identity.
- Layout: Loop from AL init node, linear sequence to Ak=B, with repeated feedback/loop.
- Details: Node shapes, spatial density of repeated structure.
- Data: Labels AL, A0, A1, ..., Ak=B, α0, α1, ..., αL, c.
- Reconstruction hint: Imagine AL at the start of a loop, producing multiple identical outputs with linear progression and loop closure.
</transcription_notes>

---

**Fig. 8: Network NG1L Linear stem cell producing 2^k identical cells each loop:** This linear stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n×2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n, k) = 2^k + 2^k × (n − k + 1) = 2^k × (n − k + 2) if n > k and Cells(n, k) = 2^n otherwise.