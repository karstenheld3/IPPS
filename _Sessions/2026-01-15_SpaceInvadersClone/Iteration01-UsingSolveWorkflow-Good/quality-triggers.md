# Quality Triggers

Rules for detecting and enforcing quality requirements from user requests.

## Trigger Word Detection

### COMPLEXITY-HIGH Triggers

These words in user requests MUST set complexity to HIGH:

- **Accuracy**: "100%", "exact", "perfect", "precise", "accurate"
- **Replication**: "replica", "clone", "identical", "faithful", "authentic"
- **Production**: "production", "enterprise", "mission-critical"
- **Compliance**: "compliant", "certified", "auditable", "specification"

### Mandatory Research Triggers

These words REQUIRE research phase with cited sources:

- "replica", "clone", "port", "recreation", "remake"
- "original", "authentic", "accurate", "faithful"
- "specification", "standard", "protocol", "compatible"

## Enforcement Rules

### When Triggers Detected

```
IF request contains COMPLEXITY-HIGH trigger:
  THEN complexity = COMPLEXITY-HIGH (no override without user approval)
  THEN SPEC, IMPL, TEST documents REQUIRED
  THEN gate output REQUIRED before each transition

IF request contains RESEARCH trigger:
  THEN INFO document REQUIRED before implementation
  THEN sources MUST be cited (not training data)
  THEN accuracy criteria MUST be measurable
```

### Trigger Detection Output

At start of any workflow, output:

```markdown
## Trigger Analysis

**Request**: "[user request summary]"
**Triggers detected**: [list or "none"]
**Complexity assigned**: [LOW/MEDIUM/HIGH]
**Required documents**: [list]
**Research required**: YES/NO
```

## Anti-Bypass Rules

### Training Data is Not Research

When accuracy/fidelity is requested:
- Training data = assumptions, not facts
- Must verify against authoritative sources
- If no sources available, state `[ASSUMED]` explicitly

### Self-Completion Bias Prevention

Agent MUST NOT:
- Mark phases complete without explicit evidence
- Skip document creation to save time
- Assume requirements without verification

### Quality Over Speed

```
WHEN uncertain between:
  - Fast delivery with assumptions → REJECT
  - Slower delivery with verification → ACCEPT
```

## Integration

Add to workflow entry points (`/build`, `/solve`, `/next`):

1. Parse request for trigger words
2. Output trigger analysis
3. Set complexity/requirements accordingly
4. Enforce throughout workflow
