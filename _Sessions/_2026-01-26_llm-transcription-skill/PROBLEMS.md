# Session Problems

**Doc ID**: 2026-01-26_LLMTranscriptionSkill-PROBLEMS

## Open

(None)

## Resolved

**LLMTR-PR-004: Implement ensemble+judge+refinement pipeline**
- **History**: Added 2026-01-27 00:09 | Resolved 2026-01-27 01:05
- **Solution**: Rewrote `transcribe-image-to-markdown-advanced.py` per SPEC LLMTR-SP01
- **Verification**: Tested with 2 images, scores 4.50-5.00 with gpt-4o, 4.15-4.75 with gpt-5-mini
- **Key fix**: gpt-5 models require `max_completion_tokens` instead of `max_tokens`

**LLMTR-PR-001: Create llm-transcription skill structure**
- **History**: Added 2026-01-26 23:56 | Resolved 2026-01-27 00:00
- **Solution**: Created SKILL.md, SETUP.md in DevSystemV3.2/skills/llm-transcription/
- **Verification**: Files synced to .windsurf/skills/llm-transcription/

**LLMTR-PR-002: Implement transcribe-image-to-markdown.py**
- **History**: Added 2026-01-26 23:56 | Resolved 2026-01-27 00:00
- **Solution**: Implemented with OpenAI/Anthropic vision API support, batch processing, custom prompts
- **Verification**: --help works, CLI interface complete
- **Prompts**: Two optimized prompts in `_input/`:
  - `llm-image-to-markdown-transcription-v1b.md` - Transcription prompt (text accuracy, structure, graphics with ASCII art)
  - `llm-image-to-markdown-judge-v1d.md` - Judge prompt (scoring: text 0.25, structure 0.35, graphics 0.40)

**LLMTR-PR-003: Implement transcribe-audio-to-markdown.py**
- **History**: Added 2026-01-26 23:56 | Resolved 2026-01-27 00:00
- **Solution**: Implemented with Whisper API, optional LLM formatting, batch processing
- **Verification**: --help works, CLI interface complete

## Deferred

(None yet)

## Problems Changes

**[2026-01-27 01:05]**
- Resolved: LLMTR-PR-004 (advanced pipeline implemented and tested)

**[2026-01-27 00:00]**
- Resolved: LLMTR-PR-001, LLMTR-PR-002, LLMTR-PR-003 (all implemented)

**[2026-01-26 23:56]**
- Added: LLMTR-PR-001 (skill structure)
- Added: LLMTR-PR-002 (image transcription)
- Added: LLMTR-PR-003 (audio transcription)
