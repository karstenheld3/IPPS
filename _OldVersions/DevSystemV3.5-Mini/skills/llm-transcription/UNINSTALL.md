# LLM Transcription Skill Uninstall

## Components

- Skill folder: `.windsurf/skills/llm-transcription/` (~50KB)
- Temp output: `../.tools/_transcription_output/` (variable size)
- Shared venv: `../.tools/llm-venv/` (~200MB, shared with llm-evaluation, llm-computer-use)

WARNING: Shared venv removal breaks llm-evaluation and llm-computer-use skills.
API keys file is NOT removed - `[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt` shared across projects.

## Removal Options

- Option 1 (Minimal) - Skill folder only
- Option 2 (Recommended) - Skill folder + temp output
- Option 3 (Full) - Skill folder + temp output + shared venv

## Removal Commands

```powershell
# 1. Skill folder
Remove-Item ".windsurf\skills\llm-transcription" -Recurse -Force

# 2. Temp output
Remove-Item "..\.tools\_transcription_output" -Recurse -Force

# 3. Shared venv (breaks other LLM skills)
Remove-Item "..\.tools\llm-venv" -Recurse -Force
```