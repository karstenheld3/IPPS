# INFO: Agent Skills

**Goal**: Document the Agent Skills open format for extending AI agent capabilities.

## Summary

Agent Skills is an open format by Anthropic for packaging specialized knowledge and workflows into reusable SKILL.md files that AI agents can discover, load, and execute.

**Key Points:** [TESTED]
- SKILL.md file with YAML frontmatter (name, description) + markdown instructions
- Progressive disclosure: metadata at startup (~100 tokens), full instructions on activation (<5000 tokens), resources on demand
- Directory structure: `SKILL.md` (required), `scripts/`, `references/`, `assets/` (optional)
- Token budget: Keep SKILL.md body under 500 lines
- Name: 1-64 chars, lowercase alphanumeric + hyphens, must match parent directory
- Description: 1-1024 chars, describe what + when to use
- Use forward slashes in paths (Unix-style), avoid Windows backslashes
- Provide default approaches, avoid too many options
- Include utility scripts that solve problems (not punt to Claude)
- Validation tool: `skills-ref validate ./my-skill`

## Table of Contents

1. [What Are Agent Skills](#1-what-are-agent-skills)
2. [How Skills Work](#2-how-skills-work)
3. [SKILL.md Specification](#3-skillmd-specification)
4. [Directory Structure](#4-directory-structure)
5. [Skill Architecture Patterns](#5-skill-architecture-patterns)
6. [Best Practices](#6-best-practices)
7. [Integration](#7-integration)
8. [Windsurf Integration](#8-windsurf-integration)
9. [Next Steps](#9-next-steps)
10. [Sources](#10-sources)

## 1. What Are Agent Skills

Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows.

**What Skills Enable:**
- **Domain expertise**: Package specialized knowledge (legal review, data analysis pipelines)
- **New capabilities**: Enable presentations, MCP server building, dataset analysis
- **Repeatable workflows**: Turn multi-step tasks into consistent, auditable workflows
- **Interoperability**: Reuse skills across different skills-compatible agent products

## 2. How Skills Work

**Three-Phase Lifecycle:**

1. **Discovery**: At startup, agents load only `name` and `description` of each skill (~100 tokens)
2. **Activation**: When task matches skill's description, agent reads full SKILL.md (<5000 tokens recommended)
3. **Execution**: Agent follows instructions, loading referenced files or executing scripts as needed

## 3. SKILL.md Specification

### Frontmatter (Required)

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

**Extended Example:**
```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

### Frontmatter Fields

**Required:**
- `name` (1-64 chars): Lowercase alphanumeric + hyphens only. Must match parent directory name. No uppercase, no leading/trailing hyphens, no consecutive hyphens.
- `description` (1-1024 chars): What the skill does AND when to use it. Include keywords for agent task matching.

**Optional:**
- `license`: License name or reference to LICENSE.txt
- `compatibility` (1-500 chars): Environment requirements (e.g., "Requires git, docker, jq")
- `metadata`: Key-value pairs for custom properties
- `allowed-tools`: Space-delimited list of pre-approved tools (experimental)

### Body Content

The markdown body after frontmatter contains:
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases
- References to additional files

## 4. Directory Structure

**Minimal:**
```
skill-name/
└── SKILL.md           # Required
```

**Full Structure:**
```
skill-name/
├── SKILL.md           # Required: instructions + metadata
├── scripts/           # Optional: executable code
│   ├── analyze.py
│   └── validate.py
├── references/        # Optional: documentation
│   ├── REFERENCE.md
│   └── FORMS.md
└── assets/            # Optional: templates, resources
    ├── template.docx
    └── schema.json
```

**Directory Purposes:**
- `scripts/`: Self-contained executable code with helpful error messages
- `references/`: Technical reference docs, form templates, domain-specific guides
- `assets/`: Document templates, images/diagrams, data files, lookup tables

## 5. Skill Architecture Patterns

Skills follow two structural architectures: **Simple** and **Composite**. The choice depends on how many distinct functions the skill covers and whether they share infrastructure.

### 5.1 Simple Skill

SKILL.md contains all instructions. Flat layout. Single domain or tool. Most skills are simple.

```
my-skill/
├── SKILL.md           # All instructions
├── SETUP.md           # Optional
└── REFERENCE.md       # Optional
```

Use when: one tool, one workflow, one domain. Use Intent Lookup in SKILL.md to cover multiple use cases within that domain.

### 5.2 Composite Skill

SKILL.md is a routing entry point that dispatches to function subfolders. Shared resources (scripts, configs, data) live at the skill root. Each function subfolder has its own guide document.

```
composite-skill/
├── SKILL.md                     # Router: routing table, shared rules, quick commands
├── SETUP.md, UNINSTALL.md       # Shared setup
├── shared-script.py              # Shared scripts at root
├── shared-config.json            # Shared data at root
├── function-a/
│   └── FUNCTION_A.md            # Function guide (no frontmatter)
├── function-b/
│   └── FUNCTION_B.md            # Function guide
└── function-c/
    └── FUNCTION_C.md            # Function guide
```

Use when:
- 3+ distinct functions share scripts, configs, or data files
- Each function is independent (own workflow) but needs common resources
- Inlining all functions in one SKILL.md would exceed 500 lines
- Users must discover which function applies before loading details

Do NOT use when:
- Functions are sequential steps of one workflow (keep as one SKILL.md)
- Functions share no infrastructure (split into separate skills)
- Fewer than 3 functions (use Intent Lookup in a flat SKILL.md instead)

### 5.3 Composite Skill Rules

- **Routing table**: SKILL.md contains one line per function: `- **[Goal]** → [subfolder]/[DOCUMENT].md`
- **No frontmatter on function documents**: Function guides are not separate skills. They have no YAML frontmatter
- **Uppercase function document names**: `EVALUATION.md`, `TRANSCRIPTION.md`, `COMPUTER_USE.md` (not `skill.md` or `guide.md`)
- **Shared resources at root**: Scripts, configs, and data files shared across functions live at the skill root. Function subfolders contain only function-specific files
- **Config resolution**: Subfolder scripts resolve shared configs via `Path(__file__).resolve().parent.parent`
- **Minimum three functions**: Composite structure requires 3+ distinct functions sharing infrastructure

### 5.4 Examples

- **llm-tools** - routes to `evaluation/`, `transcription/`, `computer-use/`; shared model JSONs and call scripts at root
- **hosting** - routes to `netlify/`, `vercel/`, `azure-app-service/`, `sharepoint-app-catalog/`, `zola/`; shared deploy patterns at root
- **research-methods** - routes to `default/`, `legal/`, `market-intel/`, `profiles/`, `software/`; shared research tools at root

## 6. Best Practices

### Core Principles

**Be Concise:**
- Context window is shared with system prompt, conversation, other skills
- Only add context Claude doesn't already have
- SKILL.md body under 500 lines recommended

**Degrees of Freedom:**
- High freedom (text instructions): Multiple valid approaches, context-dependent
- Medium freedom (pseudocode): Preferred pattern with acceptable variation
- Low freedom (specific scripts): Fragile operations, consistency critical

### Skill Structure

**Progressive Disclosure:**
```
pdf/
├── SKILL.md           # Main instructions (loaded when triggered)
├── FORMS.md           # Form-filling guide (loaded as needed)
├── reference.md       # API reference (loaded as needed)
└── scripts/
    ├── analyze_form.py
    └── fill_form.py
```

**Domain-Specific Organization:**
```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Common Patterns

**Template Pattern:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Analysis Title]
## Executive summary
[One-paragraph overview]
## Key findings
- Finding 1 with data
```

**Examples Pattern:**
Provide input/output pairs for quality-dependent outputs (commit messages, code review).

**Workflow Pattern:**
Break complex operations into checkable steps:
```markdown
## PDF form workflow
Task Progress:
- [ ] Step 1: Analyze form (run analyze_form.py)
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill form
- [ ] Step 5: Verify output
```

### Anti-Patterns

- **Avoid Windows paths**: Use `scripts/helper.py`, not `scripts\helper.py`
- **Avoid too many options**: Provide a default approach with escape hatch
- **Avoid punting errors**: Scripts should handle errors explicitly, not fail silently
- **Avoid magic numbers**: Document why values are chosen (timeout, retries)
- **Avoid deeply nested references**: Keep file references one level deep

### Executable Code

**Solve, Don't Punt:**
```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
```

**Utility Scripts Benefits:**
- More reliable than generated code
- Save tokens (no code in context)
- Ensure consistency across uses

**Visual Analysis:**
Convert PDFs to images for Claude to analyze layouts visually.

**Plan-Validate-Execute:**
Create intermediate output (e.g., changes.json), validate with script, then execute.

### Checklist

**Core Quality:**
- Description includes what + when to use
- SKILL.md body under 500 lines
- Additional details in separate files
- No time-sensitive information
- Consistent terminology
- Concrete examples
- File references one level deep
- Clear workflow steps

**Code and Scripts:**
- Scripts solve problems (no punting)
- Explicit error handling
- No magic numbers
- Required packages documented
- Forward slashes in paths
- Validation steps for critical operations

**Testing:**
- Test with Haiku, Sonnet, and Opus
- Real usage scenarios
- At least three evaluations

## 7. Integration

### How Agents Integrate Skills

1. Discover skills in configured directories (find SKILL.md files)
2. Load metadata (name, description) at startup
3. Match user tasks to relevant skills
4. Activate by loading full instructions
5. Execute scripts and access resources as needed

### Injecting Skills Into Context

```xml
<available_skills>
  <skill>
    <name>pdf-processing</name>
    <description>Extracts text and tables from PDF files...</description>
    <location>/path/to/skills/pdf-processing/SKILL.md</location>
  </skill>
</available_skills>
```

### Security Considerations

- **Sandboxing**: Run scripts in isolated environments
- **Allowlisting**: Only execute scripts from trusted skills
- **Confirmation**: Ask users before dangerous operations
- **Logging**: Record all script executions

### Validation Tool

```bash
skills-ref validate ./my-skill
skills-ref to-prompt ./skill1 ./skill2  # Generate prompt XML
```

## 8. Windsurf Integration

Windsurf implements the Agent Skills specification with full support for progressive disclosure. [TESTED]

### Skill Locations

- **Workspace skills**: `.devin/skills/<skill-name>/SKILL.md` - Current project only
- **Global skills**: `~/.codeium/windsurf/skills/<skill-name>/SKILL.md` - All workspaces

### Creating Skills in Windsurf

**Via UI (easiest):**
1. Open Cascade panel
2. Click three dots (top right) > Customizations menu
3. Click "Skills" section
4. Click "+ Workspace" or "+ Global"
5. Name the skill (lowercase letters, numbers, hyphens only)

**Manual Creation:**
```
.devin/skills/deploy-to-production/
├── SKILL.md
├── deployment-checklist.md
├── rollback-procedure.md
└── config-template.yaml
```

### Invoking Skills

- **Automatic**: Cascade matches task to skill description and invokes automatically
- **Manual**: Type `@skill-name` in Cascade input to explicitly activate

### Skills vs Rules vs Workflows

- **Skills**: Complex multi-step tasks with supporting files (folder + SKILL.md + resources). Invoked via progressive disclosure or @-mention.
- **Rules**: Behavioral guidelines, coding preferences (single .md file). Trigger-based: always-on, glob patterns, or manual.
- **Workflows**: Reusable automation scripts (single .md file). Invoked via `/workflow-name` slash command.

**When to use Skills:**
- Multi-step workflows needing reference files
- Deployment procedures with scripts/templates
- Code review processes with checklists
- Testing procedures with config files

### Example Use Cases

**Deployment Workflow:**
```
.devin/skills/deploy-staging/
├── SKILL.md
├── pre-deploy-checks.sh
├── environment-template.env
└── rollback-steps.md
```

**Code Review Guidelines:**
```
.devin/skills/code-review/
├── SKILL.md
├── style-guide.md
├── security-checklist.md
└── review-template.md
```

## 9. Next Steps

- Evaluate if Agent Skills format could replace or complement current Windsurf workflows/rules
- Review example skills at https://github.com/anthropics/skills for implementation patterns
- Consider creating a skill for common workspace tasks (PDF processing, code review)

## 10. Sources

**Primary Sources:** [TESTED]
- https://agentskills.io/home - Open format overview, what skills enable (domain expertise, capabilities, workflows, interoperability)
- https://agentskills.io/what-are-skills - Three-phase lifecycle (discovery, activation, execution), SKILL.md structure
- https://agentskills.io/specification - Frontmatter fields (name, description, license, compatibility, metadata, allowed-tools), directory structure
- https://agentskills.io/integrate-skills - Agent integration steps, XML injection format, security considerations
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices - Authoring best practices, patterns, anti-patterns, checklist

**Windsurf Documentation:** [TESTED]
- https://docs.devin.com/windsurf/cascade/skills - Windsurf Skills implementation, creation via UI/manual, invocation, scopes, use cases

**Reference Repositories:**
- https://github.com/agentskills/agentskills - Main repository, specification source
- https://github.com/anthropics/skills - Example skills by Anthropic
- https://github.com/agentskills/agentskills/tree/main/skills-ref - Validation tool (`skills-ref validate`)
