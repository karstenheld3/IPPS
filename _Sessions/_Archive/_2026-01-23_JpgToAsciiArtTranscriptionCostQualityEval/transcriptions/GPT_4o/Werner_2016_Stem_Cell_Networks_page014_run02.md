```markdown
# Eric Werner, Stem cell networks

Fig. 7: Network NₖG₁ Multi-linear stem cell network starting from 2ᵏ identical cells: 
This network generates k identical divisions to produce 2ᵏ identical daughter stem cells of type 
Aₖ = B from one founder cell A₁. The B stem cells are controlled by a linear stem cell sub- 
network that after n rounds of division, jointly produce 2ᵏ x n terminal cells of type C while 
retaining a constant 2ᵏ of linear stem cells of type B. Starting from one founder cell, the total 
number of cells after n rounds of synchronous division is: Cells(n, k) = 2ᵏ + 2ᵏ x (n - k + 1) = 
2ᵏ x (n - k + 2) if n > k and Cells(n, k) = 2ⁿ otherwise. 

The below is function describing the ideal rate of growth after n synchronous divisions where 
k is the number of identical daughter cell divisions nodes in the network in Fig. 7

           { 2ⁿ                         if n <= k
Cells(n, k)=                          
           { 2ᵏ + 2ᵏ x (n - k + 1) = 2ᵏ x (n - k + 2)    for n > k

3.2  Stem cells that generate identical cells

                             αₗ
    Aₗ -------------------> A₀ -------------------> A₁ -------------------> A₂ - - - - - - - -> Aₖ₋₁ ---> Aₖ = B
    |                       |                      |                                               |
    v α₀                α₁ v                  α₂ v                                               | αₖ
                         C                                                                            

Fig. 8: Network NG₁Iₗ Linear stem cell producing 2ᵏ identical cells each loop: This linear 
stem cell network generates 2ᵏ identical daughter cells of type Aₖ = B at each stem cell loop. 
The Aₗ stem cell is controlled by a linear stem cell sub-network that after n rounds of division, 
that ultimately produces n x 2ᵏ terminal cells of type B. Starting from one founder cell, the total 
number of cells after n rounds of synchronous division is: Cells(n, k) = 2ᵏ + 2ᵏ x (n - k + 1) =
2ᵏ x (n - k + 2) if n > k and Cells(n, k) = 2ⁿ otherwise.

**Figure 7: Network NₖG₁ Multi-linear stem cell network**

```ascii
  A₀ --> A₁ --> A₂ - - - -> Aₖ₋₁ --> Aₖ = B
   |        |         |                       |
α₁ v    α₂ v      αₖ v                    | αₖ
   C
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x8 characters
- ASCII captures: Cell types, flow of division, connections 
- ASCII misses: Detailed cell graphic specifics, color
- Colors:
  - Red (α connections)
  - Blue (stem nodes, B)
  - Green (arrows from A to C)
- Layout: Sequential flow, cell and connections labeled
- Reconstruction hint: Imagine a flowchart with arrows connecting cell types
</transcription_notes>

**Figure 8: Network NG₁Iₗ Linear stem cell**

```ascii
   Aₗ --> A₀ --> A₁ --> A₂ - - - -> Aₖ₋₁ --> Aₖ = B
    |        |        |                              |
 αₗ v    α₀ v   α₁ v                          | αₖ 
                    C
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x6 characters
- ASCII captures: Sequential division, loop connections
- ASCII misses: Specific details of cell divisions, color
- Colors:
  - Red (α connections)
  - Blue (stem nodes, B)
  - Green (connections)
- Layout: Linear progression with labeled nodes and connections
- Reconstruction hint: Visualize a simplified linear network of stem cells
</transcription_notes>
```
