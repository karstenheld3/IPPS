---
auto_execution_mode: 1
description: Prime context with workspace files
---

# Prime Context Workflow

## Step 1: Read Agent Rules

```
find_by_name Pattern="*.md" SearchDirectory="[AGENT_FOLDER]/rules" Type="file"
```

## Step 2: Read Priority Documentation (! prefix)

```
find_by_name Pattern="!*.md" SearchDirectory="[WORKSPACE_FOLDER]" Type="file"
```
Summarize key points internally.

## Step 3: Read Standard Documentation

```
find_by_name Pattern="*.md" SearchDirectory="[WORKSPACE_FOLDER]" Type="file" Excludes=["_*", "!*"]
```

## Exclusions

- Skip files starting with `_`
- Skip ALL folders starting with `_`

## Step 4: Detect Workspace Scenario

1. Project Structure: SINGLE-PROJECT or MONOREPO?
2. Version Strategy: SINGLE-VERSION or MULTI-VERSION?
3. Work Mode: SESSION-MODE or PROJECT-MODE?

## Final Output

Single row: "Read [a] .md files ([b] priority), [c] code files ([d] .py, [e] ...). Mode: [scenario]"