# Workflow Document Rules

Apply `APAPALAN_RULES.md` to all workflow content. Key rules: AP-PR-07 (be specific), AP-BR-02 (sacrifice grammar for brevity), AP-ST-01 (goal first), AP-NM-01 (one name per concept).

## Rule Index

Header (HD)
- WF-HD-01: Frontmatter with description field required
- WF-HD-02: Include Goal and Why after title
- WF-HD-03: Brief description - no AGEN verb references
- WF-HD-04: Scope boundary - clarify what workflow does NOT do (optional)

Structure (ST)
- WF-ST-01: Use GLOBAL-RULES + CONTEXT-SPECIFIC pattern
- WF-ST-02: Steps must be numbered and actionable
- WF-ST-03: Include MUST-NOT-FORGET section
- WF-ST-04: Include Verification section
- WF-ST-05: Include Output format with expected structure
- WF-ST-06: Use Quality Gate for final checklist

References (RF)
- WF-RF-01: Workflow references use inline code: `/verify`
- WF-RF-02: Skill references use @skills: format: `@skills:skill-name`
- WF-RF-03: No hardcoded paths - use placeholders
- WF-RF-04: Cross-references use relative paths from `[AGENT_FOLDER]`

Content (CT)
- WF-CT-01: Avoid AGEN verbs in prose descriptions
- WF-CT-02: Write out acronyms on first usage
- WF-CT-03: Avoid Markdown tables - use lists
- WF-CT-04: Avoid emojis - use text equivalents
- WF-CT-05: Product names spelled correctly
- WF-CT-06: APAPALAN requires examples - precision over brevity
- WF-CT-07: No Document History section in rule files

Branching (BR)
- WF-BR-01: Context branching by document type or mode
- WF-BR-02: Include "No Context Match" fallback
- WF-BR-03: Gate checks use checkbox format
- WF-BR-04: Use Trigger section for invocation patterns

## Frontmatter Format

```yaml
---
description: Verify work against specs and rules
auto_execution_mode: 1
---
```

Only `description` field. No `name:`, `type:`, or extras.

## Header Block

```markdown
# Verify Workflow

Verify work against specs, rules, and quality standards.

Goal: Validated work with all issues identified and labeled

Why: Prevents shipping bugs, spec violations, and rule breaks
```

## MUST-NOT-FORGET Section

Simple list, no subheadings or explanations.

```markdown
## MUST-NOT-FORGET

- Prerequisites ensure required documents (SPEC, IMPL, TEST) exist
- GLOBAL-RULES apply BEFORE any code change
- Run `/verify` after implementation complete
```

## Mandatory Re-read Section

Branch by mode, list documents.

```markdown
## Mandatory Re-read

SESSION-MODE: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

PROJECT-MODE: README.md, !NOTES.md, FAILS.md
```

## GLOBAL-RULES Section

```markdown
## GLOBAL-RULES

Apply to ALL contexts before any context-specific steps.

1. Trace scope - identify all affected artifacts
2. Assess impact - what depends on changes
3. Define verification - checkpoints to catch regressions
```

## CONTEXT-SPECIFIC Section

Use H1 for section, H2 for contexts. Include fallback.

```markdown
# CONTEXT-SPECIFIC

## IMPL exists

1. Read IMPL plan
2. Execute steps in order
3. Run tests after each step

## No Context Match

1. Ask user for clarification
```

## Steps Format

Numbered, actionable, concise. No prose preambles.

```markdown
## Steps

1. Detect context (INFO, SPEC, IMPL, Code, TEST)
2. Read GLOBAL-RULES section
3. Read relevant CONTEXT-SPECIFIC section
4. Execute steps
5. Run `/verify`
```

## Gate Checks

```markdown
## Gate Check: IMPLEMENT→REFINE

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed

Pass: Run `/refine` | Fail: Continue implementing
```

## Stuck Detection

```markdown
## Stuck Detection

If 3 consecutive attempts fail:
1. Document in PROBLEMS.md
2. Ask user for guidance
3. Either get guidance or defer and continue
```

## Verification Section

```markdown
## Verification

Run `/verify` to check:
1. All steps completed
2. Output matches expected format
3. MNF items addressed
```

## Workflow References

Format: `/verify`, `/implement`. Never prose ("the verify workflow").

## Skill References

Format: `@skills:skill-name`. Never prose ("the coding conventions skill").

## Path Placeholders

Never hardcode paths. Standard placeholders:
- `[WORKSPACE_FOLDER]`, `[PROJECT_FOLDER]`, `[SESSION_FOLDER]`, `[AGENT_FOLDER]`, `[DEVSYSTEM_FOLDER]`

## Acronyms

Write out on first usage: `MUST-NOT-FORGET (MNF)`, `Verify-Critique-Reconcile-Implement-Verify (VCRIV)`.

## Scope Boundary

One line: `Scope: Logic flaws only. Use `/verify` for conventions.`

## Output Format

Show expected structure inline: `Executed: [item] | Result: OK/FAIL | Remaining: [N]`

## Trigger

```markdown
## Trigger

- `/fail [description]` - User reports failure
- `/fail` - Agent detects issue
```

## Quality Gate

```markdown
## Quality Gate

- [ ] Rules re-read
- [ ] Findings documented
- [ ] Severity classified
```