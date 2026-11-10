---
name: llm-tools
description: Single source of truth for all skill-based LLM activities - shared LLM call scripts (single, batch, worker-limit probe), canonical model data (model-registry.json, model-pricing.json, model-parameter-mapping.json, MODEL_INVENTORY.md), and three functions - evaluation (LLM-as-judge pipelines, cost analysis), transcription (image/audio to markdown), computer-use (desktop automation via LLM vision). Apply when calling LLM APIs from scripts, looking up model capabilities, context windows, effort levels, prices, depth rungs, or Items for PROMPTS/TASKS planning, evaluating LLM output quality, transcribing images or audio, or automating the desktop with an LLM.
---

# LLM Tools Skill

One skill for every LLM activity that runs from scripts or needs model data. Root holds the shared parts; function subfolders hold the specialized pipelines.

## Routing

Read this file, then jump to exactly one target:

- **Call an LLM from a script** (single file, batch folder, find max workers) → root scripts below, parameters in `evaluation/LLM_EVALUATION_SCRIPTS.md`
- **Look up model data** (context window, max output, effort levels, method, price, depth rung, Items, scope guard) → `MODEL_INVENTORY.md` (human/planning view), `model-registry.json` + `model-pricing.json` + `model-parameter-mapping.json` (script view)
- **Size PROMPTS or TASKS to a model** (`intended_model`, `effort`, `context_window_size`, prompt count, checkpoints) → `MODEL_INVENTORY.md` Sections 1-2, then `@skills:write-documents` `PROMPTS_GUIDES.md` Section 1g / `TASKS_GUIDES.md` Section 2
- **Evaluate LLM output** (questions, answers, LLM-as-judge scoring, run comparison, cost analysis) → `evaluation/EVALUATION.md`
- **Transcribe images or audio to markdown** (ensemble + judge + refinement) → `transcription/TRANSCRIPTION.md`
- **Automate the desktop with LLM vision** (click, type, navigate) → `computer-use/COMPUTER_USE.md`
- **Install or remove** → `SETUP.md`, `UNINSTALL.md`
- **Verify the skill works** → `llm-tools-selftest.py --skip-api-calls`, `test-call-llm.py --keys-file [API_KEYS_FILE]`

## Do NOT Apply When

- Making a single ad-hoc LLM call from the chat (use the agent directly)
- Browser automation (use `@skills:ms-playwright-mcp`)
- Switching the IDE model (use `@skills:devin-auto-model-switcher`)

## Folder Layout

```
llm-tools/
├── SKILL.md                         this file (routing)
├── SETUP.md, UNINSTALL.md           shared venv [SKILL_TOOLS_FOLDER]/llm-venv/, keys file
├── MODEL_INVENTORY.md               planning view of all models (generated from the 3 JSONs)
├── model-registry.json              model IDs, prefix routing, context/output limits, methods, efforts, depth ladder
├── model-pricing.json               USD per 1M tokens (standard tier, long-context tier)
├── model-parameter-mapping.json     effort level → API parameter mapping
├── call-llm.py                      single call, auto-detects image/text input
├── call-llm-batch.py                batch folder processing, parallel workers, resume
├── find-workers-limit.py            probe max concurrent workers per provider
├── test-call-llm.py                 API matrix test (models x efforts), needs real keys
├── llm-tools-selftest.py            structural self-test of all scripts and JSONs
├── evaluation/                      pipeline: generate-questions → generate-answers → evaluate-answers, compare runs, analyze costs
├── transcription/                   transcribe-image-to-markdown.py, transcribe-audio-to-markdown.py, prompts/
└── computer-use/                    cli.py, core.py (Anthropic computer-use tool loop)
```

## Shared Rules

- All scripts resolve the three model JSONs from the `llm-tools/` root. Scripts in subfolders use `Path(__file__).resolve().parent.parent`. Never copy the JSONs into a subfolder
- Model data changes follow `SOPS.md` SOP 5 (edit here, regenerate `MODEL_INVENTORY.md` via session `!ModelRegistryUpdate`, sync to `[AGENT_FOLDER]`)
- Python: `[SKILL_TOOLS_FOLDER]/llm-venv/Scripts/python.exe`. Keys: `[API_KEYS_FILE]` (`OPENAI_API_KEY=`, `ANTHROPIC_API_KEY=`, one per line) passed via `--keys-file`
- Effort levels everywhere: `none | minimal | low | medium | high | xhigh | max` mapped by `model-parameter-mapping.json`; the registry lists which levels each model supports

## Agent-Created Folders

- `_markdown/` - role: markdown; parent: content folder (batch input folder of the script); creator: `transcribe-image-to-markdown.py` and `transcribe-audio-to-markdown.py` batch default output; content: one markdown file per input file

## Quick Commands

```powershell
$venv = "[SKILL_TOOLS_FOLDER]\llm-venv\Scripts\python.exe"
$skill = "[AGENT_FOLDER]\skills\llm-tools"

& $venv "$skill\call-llm.py" --model gpt-5-mini --input-file page.jpg --prompt-file prompt.md --keys-file [API_KEYS_FILE]
& $venv "$skill\call-llm-batch.py" --model gpt-5-mini --input-folder images\ --output-folder out\ --prompt-file prompt.md --workers 8 --keys-file [API_KEYS_FILE]
& $venv "$skill\transcription\transcribe-image-to-markdown.py" --input-folder images\ --output-folder out\ --model gpt-5-mini --keys-file [API_KEYS_FILE]
& $venv "$skill\computer-use\cli.py" -k [API_KEYS_FILE] "Click the Start button"
& $venv "$skill\llm-tools-selftest.py" --skip-api-calls
```
