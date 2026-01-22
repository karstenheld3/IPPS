```markdown
# Eric Werner, Stem cell networks

**Fig. 7: Network NIkGI Multi-linear stem cell network starting from 2^k identical cells:**
This network generates k identical divisions to produce 2^k identical daughter stem cells of type A_k = B from one founder cell A_1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k (n - k + 1) = 2^k (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

```ascii
[NETWORK DIAGRAM - MULTI-LINEAR STEM CELL NETWORK]
   A_0 --α₀--> A_1 --α₁--> A_2 ---- ... ----> A_k-1 --α𝗄--> A_k = B --c--> C 
  |     α₀     α₁     α₂                α𝗄          α𝗄       α𝗄
  |                                                        | 
  --------------------------------------------------------- 
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x7 characters
- ASCII captures: Node relationships, linear progression, labels for cell types and transformations
- ASCII misses: Curved arrow depiction; exact position nuances
- Colors:
  - Red - Pathways between nodes
  - Blue - Main linear progression
  - Green - Alternative paths
- Layout: Left to right progression with branching paths
- Details: Linear network with constant stem cell production
- Data: Specific node labels, transformation labels (α, c)
- Reconstruction hint: Imagine curved arrows for better flow understanding
</transcription_notes>

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7:

Cells(n,k) = { 2^n if n <= k 
             { 2^k + 2^k x (n - k + 1) = 2^k x (n - k + 2) for n > k

## 3.2 Stem cells that generate identical cells

**Fig. 8: Network NGIIL Linear stem cell producing 2^k identical cells each loop:**
This linear stem cell network generates 2^k identical daughter cells of type A_k = B at each stem cell loop. The A_L stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n x 2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k (n - k + 1) = 2^k x (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

```ascii
[LINEAR NETWORK DIAGRAM - STEM CELL PRODUCTION]
   A_L --α_𝐋--> A_0 --α₀--> A_1 --α₁--> A_2 ---- ... ----> A_k-1 --α𝗄--> A_k = B 
  |         α_𝐋   α₀   α₁   α₂               α𝗄       α𝗄       α𝗄
  ----------------------------------------------------------
```

<transcription_notes>
- Mode: Structural
- Dimensions: 78x7 characters
- ASCII captures: Node sequence, linear and loop structure, transformation labels
- ASCII misses: Curved arrows, precise loop start depiction
- Colors:
  - Red - Pathways and loops
  - Green - Initial connections
  - Blue - Main linear network
- Layout: Sequential nodes with linear and looping structure
- Details: Linear production, emphasis on identical cell generation
- Data: Node labels, transformation indicators
- Reconstruction hint: Visualize starting node with full loop integration
</transcription_notes>
```