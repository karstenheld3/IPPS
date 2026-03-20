# Step 4: Compression Strategy (FR-04)

You are creating a compression strategy for a DevSystem. All files, the call tree, and the complexity map are provided in the context above.

## Task

Create a compression strategy document (`_03_FILE_COMPRESSION_STRATEGY.md`) with these sections:

### 1. Exclusion List
Files that should NOT be compressed. Criteria:
- Files with fewer than {exclusion_max_lines} lines AND {exclusion_max_references} or fewer references
- These files are too small or rarely loaded to justify compression cost

### 2. Primary (Keep Mostly As-Is)
Files and concepts that are core to the system's primary function. These should retain full detail:
- Core rule definitions
- Critical workflow logic
- Essential skill functionality
- Anything that, if simplified, would break agent behavior

### 3. Secondary (Compress)
Files and concepts that can be reduced while preserving function:
- Verbose examples (BAD/GOOD pairs can be shortened)
- Redundant explanations across files
- Detailed formatting rules (compress to key points)
- Supporting documentation

### 4. Drop (Remove Entirely)
Content that can be safely removed:
- Redundant repetitions of rules already stated elsewhere
- Historical context not needed for execution
- Overly detailed edge case descriptions
- Examples that don't add unique information

## Output Format

Write the complete `_03_FILE_COMPRESSION_STRATEGY.md` document. List specific file paths in each category. For Secondary and Drop items, explain what specifically to compress or remove.

## Quality Criteria

- Every non-excluded file must appear in exactly one category (Primary, Secondary, or Drop)
- Excluded files must meet both criteria (lines AND references)
- Primary items must be justified (why they cannot be compressed)
- Drop items must be justified (why removal is safe)
