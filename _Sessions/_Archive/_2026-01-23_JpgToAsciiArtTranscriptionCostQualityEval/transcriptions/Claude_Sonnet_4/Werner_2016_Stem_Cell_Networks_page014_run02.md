# Eric Werner, Stem cell networks

**Figure 7: Network NL1G1 Multi-linear stem cell network starting from 2^k identical cells:**

```ascii
[STEM CELL NETWORK - LINEAR CHAIN WITH DIVISIONS AND LOOPS]

     α1        α2              αk      αk
    ↗  ↘      ↗  ↘            ↗      ↗  ↘
   ○    ○    ○    ○           ○      ○    ○
  A0 ═══ A1 ═══ A2 ┅┅┅┅ Ak-1 ═══ Ak=B ███ C
   ○    ○    ○    ○           ○      ○    ○
    ↘  ↗      ↘  ↗            ↘      ↘  ↗
     α1        α2              αk      c

Legend:
═══ Red stem cell connections
███ Blue terminal cell connection  
┅┅┅ Dotted connection (continuation)
○   Cell division nodes
α   Division parameters
```

<transcription_notes>
- Mode: Structural
- Dimensions: 60x8 characters
- ASCII captures: Linear chain structure, division loops, cell connections, parameter labels
- ASCII misses: Red/blue color coding of connections, exact arrow curvature
- Colors:
  - Red - stem cell network connections (A0 through Ak)
  - Blue - terminal cell connection (B to C)
- Layout: Horizontal linear progression with symmetric loops above/below
- Details: Self-loops at each node, bidirectional connections, parameter annotations
- Data: Subscripts k, division parameters α1, α2, αk, cell types A0-Ak, B, C
- Reconstruction hint: Each stem cell has symmetric division loops with α parameters
</transcription_notes>

This network generates k identical divisions to produce 2^k identical daughter stem cells of type Ak = B from one founder cell A1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7.

Cells(n,k) = { 2^n                                    if n <= k
             { 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2)  for n > k

## 3.2 Stem cells that generate identical cells

**Figure 8: Network NG II, Linear stem cell producing 2^k identical cells each loop:**

```ascii
[LINEAR STEM CELL NETWORK - SELF-RENEWING WITH CASCADING DIVISIONS]

      αL       α1        α2              αk
     ↗  ↘     ↗  ↘      ↗  ↘            ↗  ↘
    ○    ○   ○    ○    ○    ○           ○    ○
   AL ═══ A0 ═══ A1 ═══ A2 ┅┅┅┅ Ak-1 ███ Ak=B
    ○    ○   ○    ○    ○    ○           ○    ○
     ↘  ↗     ↘  ↗      ↘  ↗            ↘  ↗
      α0       α1        α2              αk

Legend:
═══ Red stem cell connections
███ Blue terminal connection
┅┅┅ Dotted connection (continuation)  
○   Cell division nodes
α   Division parameters
```

<transcription_notes>
- Mode: Structural
- Dimensions: 65x8 characters
- ASCII captures: Linear chain with self-renewing loop, cascading divisions, parameter structure
- ASCII misses: Red/blue color distinction, exact loop positioning
- Colors:
  - Red - stem cell network connections (AL through Ak-1)
  - Blue - terminal connection (Ak-1 to Ak=B)
- Layout: Linear progression with initial self-loop, symmetric division patterns
- Details: AL has self-loop, each node has division loops, terminal connection to B
- Data: Cell types AL, A0-Ak, B; parameters αL, α0-αk; 2^k identical cells per loop
- Reconstruction hint: AL self-renews while driving linear cascade producing 2^k cells at each loop
</transcription_notes>

This linear stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop. The AL stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

<!-- Tokens: in=2244 out=1356 -->