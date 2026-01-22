# Cancer network editing and simulation

One of the difficult steps in the protocol is the cancer network editing process in *Step 3* of the Cancer Cell Suicide Protocol. The efficacy of the insertion of the cell death signal depends on the architecture of the cancer network. These can be complex and difficult to analyze. Here the Cancer-CAD software can be of great value. Consider some simple examples:

**Figure 2: A fast growing tumor. Cancer cells in *Red*. *Yellow* cells are dying. The tumor grows too fast. There is not enough cancer cell death to prevent tumor expansion.**

```ascii
    @@@@@@@@
   @@######@@
  @##YYYY##@@@
 @###YYYY####@
 @##YYYYYY###@
 @###YYYY####@
  @########@@
   @@@@@@@@
```

<transcription_notes>
- Mode: Shading
- Dimensions: 15x8 characters
- ASCII captures: Spherical tumor structure with dying cells in center
- ASCII misses: Complex network diagram on right side, color gradients
- Colors: Red (cancer cells), Yellow (dying cells), black background
- Layout: Left side shows 3D tumor sphere, right side shows network diagram with colored bars and curved lines
- Details: Network shows horizontal bar with colored segments, curved lines (blue and red) connecting different points
- Data: Network diagram shows signal pathways
- Reconstruction hint: Tumor has mixed red and yellow spherical cells forming a cluster
</transcription_notes>

**Figure 3: A slow growing tumor. Between 1 and 4 cells are cancerous (Red) at any given time. Most cancer cells are dying (*Yellow*). The *Blue* cells are terminal, non-proliferating cells. This network edit produces a slow growing tumor generating a passive mass of *Blue* terminal cells. The tumor continues to expand, but only produces the same number terminal cells as pre-existing cancer cells. The cancer cells do not proliferate.**

```ascii
     BBBB
    B    B
   B  RR  B
  B  YYYY  B
   B  RR  B
    B    B
     BBBB
```

<transcription_notes>
- Mode: Structural
- Dimensions: 12x7 characters
- ASCII captures: Small tumor with different cell types
- ASCII misses: Complex network diagram, exact cell shapes and arrangements
- Colors: Red (cancer cells), Yellow (dying cells), Blue (terminal cells), black background
- Layout: Left shows tumor cluster, right shows network diagram with horizontal bar and curved connecting lines
- Details: Network has cyan, yellow, and other colored segments in horizontal bar, with blue and red curved lines above
- Data: 1-4 cancer cells at any time as stated in caption
- Reconstruction hint: Small cluster with blue cells surrounding red/yellow core
</transcription_notes>

**Figure 4: Fast growing tumor. Equal numbers of cancer cells (Red), dying cells (*Yellow*) and terminal, non-proliferating cells (*Blue*). The cancer cells continue to divide. There is not enough cancer cell death to stop the cancer.**

```ascii
    @@@@@@@@@@@
   @###BBB###@@
  @##RRBBRR###@
 @###YYBBYY####@
 @##RRBBBBRR###@
 @###YYBBYY####@
 @##RRBBBBRR###@
  @###BBB#####@
   @@@@@@@@@@@
```

<transcription_notes>
- Mode: Shading
- Dimensions: 15x9 characters
- ASCII captures: Large mixed tumor structure
- ASCII misses: Exact 3D rendering, network diagram details
- Colors: Red (cancer cells), Yellow (dying cells), Blue (terminal non-proliferating cells), black background
- Layout: Left shows large tumor mass, right shows network diagram with colored bar and curved lines
- Details: Network shows horizontal bar with multiple colored segments, blue and red curved lines connecting different points
- Data: Equal numbers of each cell type as stated
- Reconstruction hint: Large spherical tumor with mixed red, yellow, and blue cells throughout
</transcription_notes>

Cite as: Werner, E. (2018) A Cancer Cell Suicide Protocol. Preprint. DOI: (Insert DOI at top of this document).