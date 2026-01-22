# Eric Werner, Stem cell networks

**Figure 7: Network N1,G1 Multi-linear stem cell network starting from 2^k identical cells**

This network generates k identical divisions to produce 2^k identical daughter cells of type:
A_k = B from one founder cell A1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n,k) = 2^k otherwise.

```ascii
[Network Diagram of Stem Cell Divisions]
   a1     a2     ...    ak    ak
A0 --> A1 --> A2 --> ... --> Ak-1 --> Ak = B
 |      |      |             |        |
 v      v      v             v        v
 O      O      O             O        O
(Blue)  
                             C
```

<transcription_notes>
- Mode: Structural
- Captures: Hierarchical cell division network
- Key elements:
  - Nodes represent cell types (A0, A1, etc.)
  - Green arrows show cell division progression
  - Blue and red color coding for different cell types
- Misses: Precise mathematical details of cell multiplication
- Layout: Linear progression with branching cell divisions
</transcription_notes>

**Figure 8: Network NG1I, Linear stem cell producing 2^k identical cells each loop**

This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_k stem cell is controlled by a linear sub-network that after n rounds of division ultimately produces n × 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k × (n - k + 1) = 2^k × (n - k + 2) if n > k and Cells(n,k) = 2^k otherwise.

```ascii
[Network Diagram of Linear Stem Cell Division]
   a1     a2     ...    ak    ak
AL --> A0 --> A1 --> A2 --> ... --> Ak-1 --> Ak = B
 |      |      |             |        |
 v      v      v             v        v
 O      O      O             O        O
(Blue)
                             C
```

<transcription_notes>
- Mode: Structural
- Very similar to Figure 7
- Captures: Linear progression of stem cell division
- Key differences:
  - Additional starting node AL
  - Same color-coding and division mechanism
- Misses: Precise mathematical transformation details
- Layout: Identical linear progression model
</transcription_notes>

<!-- Tokens: in=2244 out=740 -->