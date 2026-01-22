# Eric Werner, Stem cell networks

## Figure 7: Network N1,G1 Multi-linear stem cell network starting from 2^k identical cells

```ascii
    a1    a2          ak
A0 ----> A1 ----> ... ---> Ak-1 ---> Ak === B
 |        |               |         |  \
 a1       a2              ak        c   C
 v        v               v
```

<transcription_notes>
- Mode: Structural
- Type: Cell division network diagram
- Key Elements:
  - Cells labeled A0 through Ak
  - Stem cell network with multiple linear paths
  - Color-coded connections (red, blue, green)
- Connections show cell divisions and transformations
- Blue path indicates terminal cell type C
- Green arrows show cell division progression
</transcription_notes>

**Text Description:**
This network generates k identical 2^k divisions to produce 2^k identical daughter cells.

The network starts from one founder cell A1. The B stem cells are controlled by a linear stem cell sub-network that after n rounds of division, jointly produce 2^k × n terminal cells of type C while retaining a constant 2^k of linear stem cells of type B.

**Cell Count Function:**
```
Cells(n,k) = { 
  2^n      if n <= k
  2^k + 2^k × (n-k+1) = 2^k × (n-k+2)   for n > k
}
```

## Figure 8: Network NG1I, Linear stem cell producing 2^k identical cells each loop

```ascii
    aL    a0    a1    a2          ak
AL ----> A0 ----> A1 ----> ... ---> Ak === B
                                    |  \
                                    k   C
```

<transcription_notes>
- Mode: Structural
- Similar to Figure 7 but with additional initial cell AL
- Shows linear stem cell network generating identical daughter cells
- Blue path indicates terminal cell type B
- Green arrows represent cell division process
</transcription_notes>

**Text Description:**
This linear stem cell network generates 2^k identical daughter cells of type Ak = B at each stem cell loop. The Ak stem cell is controlled by a linear stem cell sub-network that after n rounds of division ultimately produces n × 2^k terminal cells of type B.

**Cell Count Function:**
```
Cells(n,k) = { 
  2^k      otherwise
  2^k + 2^k × (n-k+1) = 2^k × (n-k+2)   for n > k
}
```

<!-- Tokens: in=2244 out=635 -->