```markdown
# Eric Werner, Stem cell networks

Fig. 7: Network N\_{k}G\_{1} Multi-linear stem cell network starting from 2^k identical cells:
This network generates k identical divisions to produce 2^k identical daughter stem cells of type A\_{k} = B from one founder cell A\_{1}. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k * n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k * (n - k + 1) = 2^k * (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

```ascii
[NETWORK N_k G_1 - Multi-linear stem cell network]
   A0  --α1->  A1  --α2->  A2  --α3-> ... --α(k-1)->  A(k-1)  --αk->  A_k = B
    |         |         |          |                    |        |      
   C <--α1-- C <--α2-- C <-- ... -- C <--α(k-1)-- C <--αk--  C
```

<transcription_notes>
- Mode: Structural
- Dimensions: 80x10 characters
- ASCII captures: Sequence of cells and directional links
- ASCII misses: Visual representation of arrows and colors
- Colors:
  - Green - connections within initial cells
  - Red - external connections from initial
  - Blue - connections within terminal cells
- Layout: Linear progression with loops back to C at each stage
- Details: Arrows represent divisions and connections
- Data: n, k values described in text
- Reconstruction hint: Picture side loops as connections wrapping around
</transcription_notes>

The below is function describing the ideal rate of growth after n synchronous divisions where k is the number of identical daughter cell divisions nodes in the network in Fig. 7

```
Cells(n,k) = { 
  2^n                if n <= k
  2^k + 2^k * (n-k+1) = 2^k * (n-k+2)  for n > k
}
```

3.2 Stem cells that generate identical cells

```ascii
[NETWORK N_G_11 - Linear stem cell producing 2^k identical cells each loop]
   A0 --α0->  A1 --α1->  A2 --α2-> ... --α(k-1)->  A(k-1) --αk->  A_k = B
    |        |        |          |                  |        |      
   C <-α0-- C <-α1-- C <- ... -- C <-α(k-1)-- C <-αk--  C
```

Fig. 8: Network NG\_{1}I Linear stem cell producing 2^k identical cells each loop: This linear stem cell network generates 2^k identical daughter cells of type A\_{k} = B at each stem cell loop. The A\_{L} stem cell is controlled by a linear stem cell sub-network that after n rounds of division, that ultimately produces n*2^k terminal cells of type B. Starting from one founder cell, the total number of cells after n rounds of synchronous division is: Cells(n,k) = 2^k + 2^k * (n - k + 1) = 2^k * (n - k + 2) if n > k and Cells(n,k) = 2^n otherwise.

<transcription_notes>
- Mode: Structural
- Dimensions: 80x10 characters
- ASCII captures: Sequence of cells and directional links
- ASCII misses: Visual representation of arrows and colors
- Colors:
  - Green - connections within initial cells
  - Red - external connections from initial
  - Blue - connections within terminal cells
- Layout: Linear progression with loops back to C at each stage
- Details: Arrows represent divisions and connections
- Data: n, k values described in text
- Reconstruction hint: Picture side loops as connections wrapping around
</transcription_notes>
```