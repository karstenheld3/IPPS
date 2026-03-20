# Session Notes

**Doc ID**: 2026-03-19_MinimalIPPS-NOTES

## Initial Request

````text
@[/session-new] MinimalIPPS

The goal of this session is to create a set of prompts that can reduce the complexity of IPPS to be usable by less expensive LLMs.

The overall idea is this:
1) Read the entire DevSystem rules, workflows and skills.(currently ca. 1MB text)

2) Create a _01_FILE_CALL_TREE.md file that explores which files are loaded first and when and which files trigger the agent to load which other files. For example all rules must be loaded first. Workflows are loaded only at invocation time. For Skills, all SKILL.md files are loaded and on skill invocation they trigger the loading of additional files following the progressive disclosure principle. All files (skills and workflows) might trigger the loading of other files, even the execution or other workflows. This document has to document the 1) startup sequence, 2) for each workflow: the call tree for each workflow (even if recursive), 3) for eask slkill: the skill call tree. 4) File refernce list by loaded file (which other files trigger the loading of a single file; this is a common pattern to refresh context)

3) Create a _02_FILE_COMPLEXITY_MAP.md file with 1) Exhaustive list of concepts that the agent must remember, 2) List of all files with a) length in tokens, b) number of introduced concepts or principles, c) number of introduced rules, d) number of introduced steps, e) branching count - how much conditional behavior is specified in the file

4) Analyze the most complex 20 files and create a _03_FILE_COMPRESSION_STRATEGY.md with focus on reducing the size of the a) largest, b) most complex and c) most often loaded files. The strategy goal is to sacrifice less important instructions, concepts and rules across the entire system and keep in full the primary function of the system. In this document we create 3 lists: 1) Primary (concepts, features, rules, functions, etc.) -> Leave mostly as is, 2) Secondary -> try to compress, 3) Drop -> remove entirely

5) From this strategy create up to 10 compression prompts to be used for different types of files: workflows, skill.md files, rules, templates, etc. Primary concept descriptions, rules, instructions should be compressed by sacrificing formatting etc. according to agent formatting rules and APAPALAN principle. Less important concepts, rules and features should be dropped entirely. For each of these prompts (up to 10) we create a LLM-Judge-Prompt that defines criteria according to our goal of the transformation of a file was successful.

6) Then using a script we run over all files and transform them using the intended prompt and the eval prompt with multiple candidates (same method as llm-transcription script) and a min target score

7) Finally we verify each file against its original version and craete a _04_FILE_COMPRESSION_REPORT.md that contains a 5 line summary for each file: 1) structural changes, 2) removed features, 3) simplified content, 4) sacrificed details, 5) possible impact

From 7) we can draw conclusions and modify _03_FILE_COMPRESSION_STRATEGY.md to re-iterate.

note but do nothing
````

## Session Info

- **Started**: 2026-03-19
- **Goal**: Create prompts to reduce IPPS complexity for less expensive LLMs
- **Operation Mode**: IMPL-ISOLATED
- **Output Location**: [SESSION_FOLDER]/

## Current Phase

**Phase**: DELIVER
**Workflow**: `/go` autonomous loop
**Assessment**: IMPLEMENT done (57/57 tests). REFINE done (2 fixes: cost tracking wired up, cache_last_used field added). Ready for DELIVER.

## Agent Instructions

- This is a document creation and analysis session - no codebase modifications
- All outputs go to session folder
- User explicitly requested "note but do nothing" - await confirmation before executing any steps

## Key Decisions

(pending review of options)

## Important Findings

### Anthropic Pricing Reference (2026-03-20)

Pricing data available in `.windsurf/skills/llm-evaluation/`:
- **Source doc**: `pricing-sources/2026-03-20_Anthropic-ModelPricing.md`
- **JSON data**: `model-pricing.json` (batch tier pricing)

Key rates for MIPPS pipeline (per 1M tokens, batch pricing):
- **Claude Opus 4.6** (Mother): $7.50 input, $0.75 cached, $37.50 output
- **GPT-5-mini** (Verification): $0.125 input, $1.00 output

Note: `model-pricing.json` uses batch tier (50% discount). Standard API rates are 2x.

## Topic Registry

- `MIPPS` - Minimal IPPS (this session)

## Bug List

(none yet)

## Significant Prompts Log

### Model Specialization Strategy (2026-03-19 23:15)

```text
No wait the idea is to load ALL files into the context  of a "Mother" model (Claude Opus 4,.6 thinking 1M) and then solve all problems with this context that is then a cached input prompt
Using this we can solve Steps 1 to 4. 

we can always verify results using cheaper "Verification" models with file-by-file read and comparing against the created files. This way we can find problems and fix them in the files and always ask the "Mother" model verification questions.

then in step 5 we use "Prompting" models like Claude Opus 4.5 Thinking 200k to generate the transformer and eval prompts

For the transformation itself we can use cheaper "Transformer" models like GPT-5.4 and such.


Then in steps 7 we can again use "Verification" models that are less expensive but nonetheless good.
```

**Derived document**: `_OPTION_A_PIPELINE_WITH_PROMPTS.md`

### File Exclusion Thresholds (2026-03-19 23:38)

```text
I want the complexity analysis to work out certain thresholds for when to not even touch files. For example some SKILL.md files will be rarely loaded and if they are not that large (100 lines limit), they can be ignored. Same for some workflows etc.
```

**Impact**: Add exclusion criteria to Step 3 (complexity map) and Step 4 (compression strategy):
- Files < 100 lines AND rarely loaded → skip compression
- Apply to: SKILL.md files, workflows, supporting docs
- Reduces compression scope and cost
