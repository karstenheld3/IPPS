# Compare Image Transcription Semantic Capture

Evaluate how well two transcriptions capture the **same underlying visual content** from the same original figure.

## Transcription A

Contains ASCII art and `<transcription_notes>` metadata:

{transcription_a}

## Transcription B

Contains ASCII art and `<transcription_notes>` metadata:

{transcription_b}

## What to Compare

Each transcription contains:
- **ASCII art** (` ```ascii ... ``` `) - structural representation using text characters
- **`<transcription_notes>`** metadata including: Mode (Structural/Shading), Dimensions, What ASCII captures vs misses, Colors and their meanings, Layout description, Reconstruction hints

## Evaluation Criteria

1. **Structural Elements (35 points)** - Same components (boxes, nodes, connections)? Same hierarchy/flow? Same labels/annotations?
2. **Visual Information Preserved (25 points)** - Same colors documented? Same visual details noted as missing? Same reconstruction hints?
3. **Relationships and Layout (25 points)** - Same spatial arrangement? Same directional flow? Same groupings/regions?
4. **Completeness (15 points)** - Similar detail level? Neither omits significant elements the other includes?

## Scoring Guide

- **90-100**: Identical semantic content, only superficial wording differs
- **70-89**: Same core understanding, minor interpretive differences
- **50-69**: Similar overall, but one captures details the other misses
- **30-49**: Different interpretations of the same visual
- **0-29**: Fundamentally different understanding of the source image

## Output

JSON only, example format:

{{"score": 85, "differences": ["color description differs", "layout interpretation varies"]}}