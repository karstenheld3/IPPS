# Workflow Rules

## Target Audience

LLM-consumed files. Optimize for medium-reasoning models, low context windows, instruction following.

APAPALAN: As precise as possible, as little as necessary.

Design principles:
1. Maximum clarity - one interpretation per instruction
2. Numbered steps - LLMs follow sequences better than prose
3. MUST-NOT-FORGET technique for complex skills with verification
4. No `**bold**` in LLM-consumed files - adds tokens without improving comprehension
5. `#`/`##` headers as parsing boundaries
6. Compact format for lookups - one line per resource
7. Verbose only when justified - multi-step reasoning, troubleshooting, code with explanation
8. JSON intermediate output between steps to enforce explicit reasoning:
```
## Step 3: Determine context
Emit before proceeding:
{"context": "INFO|SPEC|IMPL|Code|TEST|Session|Workflow|Skill", "reason": "..."}
```

## Formatting

1. Frontmatter: only `description` field
2. Workflow refs as inline code (`/verify`), skill refs with `@skills:skill-name`
3. Steps: numbered, actionable verbs
4. No hardcoded paths - use `[WORKSPACE_FOLDER]`, `[SESSION_FOLDER]`
5. No `## Usage` sections unless showing parameters
6. No replication of rules defined elsewhere - reference the source

## Structure

Complex workflows: separate GLOBAL-RULES and CONTEXT-SPECIFIC sections. See `/verify` as canonical example.

## Token Optimization

Remove: `**Bold**` markup, filler prose, prose restating headings, unnecessary blank lines between list items.

Keep: `#`/`##` headers, parenthetical notes with critical context, all technical detail/URLs/parameters, concrete BAD/GOOD examples.

Test: "Remove this token. Does the LLM lose information?" No? Remove it.

MUST-NOT-FORGET technique for end-verification:
```
### MUST-NOT-FORGET (check after completion)
- [ ] Item 1
- [ ] Item 2

### Steps
1. Do thing
2. Do other thing
3. Walk MUST-NOT-FORGET list. All checked?
```

## Quality Checks

- Ambiguities: unclear instructions with multiple interpretations?
- Term conflicts: same concept named differently?
- Underspecified behavior: missing edge cases?
- Outdated references: broken links to renamed/removed items?

Cross-reference checklist:
- [ ] All `/workflow` refs exist in workflows folder
- [ ] All `@skills:` refs exist in skills folder
- [ ] All `[STATE]` refs defined in ID-REGISTRY.md
- [ ] All document refs use correct naming conventions