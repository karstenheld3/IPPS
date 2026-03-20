# Step 7: Verify Compressed File (FR-07)

Compare a compressed file against its original and produce a 5-line verification report.

## Original File

**Path**: {file_path}
```
{original_content}
```

## Compressed File

```
{compressed_content}
```

## Report Format

Produce exactly 5 lines for this file:

1. **Structural changes**: What sections were merged, reordered, or flattened
2. **Removed features**: What was dropped entirely
3. **Simplified content**: What was reduced but kept in shorter form
4. **Sacrificed details**: What examples, edge cases, or formatting was removed
5. **Possible impact**: What agent behavior may change as a result

## Cross-Reference Check

Also check: Does the compressed file reference any other files? If so, verify those references still exist (they may have been renamed or removed during compression). List any broken references found.

Report broken references as:
- BROKEN_REF: [reference] in [file_path] -> target not found
