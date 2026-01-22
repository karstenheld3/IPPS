# Cancer network editing and simulation

One of the difficult steps in the protocol is the cancer network editing process in *Step 3* of the Cancer Cell Suicide Protocol. The efficacy of the insertion of the cell death signal depends on the architecture of the cancer network. These can be complex and difficult to analyze. Here the Cancer-CAD software can be of great value. Consider some simple examples:

**Figure 2: A fast growing tumor. Cancer cells in *Red*. *Yellow* cells are dying. The tumor grows too fast. There is not enough cancer cell death to prevent tumor expansion.**

```ascii
        @@@@@@@
      @@@#####@@@
     @@###%%%###@@
    @@##%%%%%%%##@@
    @##%%%%%%%%%##@
    @##%%%%%%%%%##@
    @@##%%%%%%%##@@
     @@###%%%###@@
      @@@#####@@@
        @@@@@@@

[3D tumor visualization]        [Network diagram with colored segments and connections]
                                 ----[][][][][][][]----
                                /                      \
                               |  Blue and red curves   |
                                \                      /
                                 ----[][][][][][][]----
                                                    /\
                                                   /  \
                                                  Green spike
```

<transcription_notes>
- Mode: Shading
- Dimensions: 80x10 characters
- ASCII captures: 3D spherical tumor structure
- ASCII misses: Specific cell colors (red cancer cells, yellow dying cells), network diagram details
- Colors: Red (cancer cells), Yellow (dying cells)
- Layout: Left panel shows 3D tumor, right panel shows network diagram with multicolored segments and curved connections
- Details: Network has blue and red curved lines connecting to a horizontal bar with colored segments, green spike on right
- Data: Fast growth rate indicated
- Reconstruction hint: Tumor composed of red spheres with yellow spheres interspersed
</transcription_notes>

**Figure 3: A slow growing tumor. Between 1 and 4 cells are cancerous (Red) at any given time. Most cancer cells are dying (*Yellow*). The *Blue* cells are terminal, non-proliferating cells. This network edit produces a slow growing tumor generating a passive mass of *Blue* terminal cells. The tumor continues to expand, but only produces the same number terminal cells as pre-existing cancer cells. The cancer cells do not proliferate.**

```ascii
    @@@@@@
   @#####@@
  @###%###@
  @#%%%%%#@
  @###%###@
   @#####@
    @@@@@@

[Small tumor cluster]           [Network diagram with colored segments and connections]
                                ----[][][][][][][]----
                               /                      \
                              |  Blue and red curves   |
                               \                      /
                                ----[][][][][][][]----
                                                   /\
                                                  /  \
                                                 Green spike
```

<transcription_notes>
- Mode: Shading
- Dimensions: 80x7 characters
- ASCII captures: Smaller tumor structure
- ASCII misses: Specific cell colors (red cancer, yellow dying, blue terminal cells), network diagram details
- Colors: Red (1-4 cancer cells), Yellow (dying cells), Blue (terminal non-proliferating cells)
- Layout: Left panel shows small tumor cluster, right panel shows network diagram
- Details: Network has blue and red curved connections, horizontal bar with colored segments, green spike on right
- Data: 1-4 cancer cells at any given time
- Reconstruction hint: Small cluster with mix of red, yellow, and blue spherical cells
</transcription_notes>

**Figure 4: Fast growing tumor. Equal numbers of cancer cells (Red), dying cells (*Yellow*) and terminal, non-proliferating cells (*Blue*). The cancer cells continue to divide. There is not enough cancer cell death to stop the cancer.**

```ascii
      @@@@@@@@@
    @@@#######@@@
   @@###%%%%%###@@
  @@##%%%%%%%%%##@@
 @@##%%%%%%%%%%%##@@
 @##%%%%%###%%%%%##@
 @##%%%%#####%%%%##@
 @@##%%%%%%%%%%%##@@
  @@##%%%%%%%%%##@@
   @@###%%%%%###@@
    @@@#######@@@
      @@@@@@@@@

[Large tumor visualization]     [Network diagram with colored segments and connections]
                                ----[][][][][][][]----
                               /                      \
                              |  Blue and red curves   |
                               \                      /
                                ----[][][][][][][]----
                                                   /\
                                                  /  \
                                                 Green spike
```

<transcription_notes>
- Mode: Shading
- Dimensions: 80x12 characters
- ASCII captures: Large tumor structure
- ASCII misses: Equal distribution of red/yellow/blue cells, network diagram details
- Colors: Red (cancer cells), Yellow (dying cells), Blue (terminal cells) in equal numbers
- Layout: Left panel shows large tumor, right panel shows network diagram
- Details: Network has blue and red curved connections, horizontal bar with multicolored segments, green spike on right
- Data: Equal numbers of each cell type, continued division
- Reconstruction hint: Large mixed tumor with equal proportions of red, yellow, and blue spherical cells
</transcription_notes>

---

Cite as: Werner, E. (2018) A Cancer Cell Suicide Protocol. Preprint. DOI: (Insert DOI at top of this document).