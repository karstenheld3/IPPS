# Session Problems

**Doc ID**: 2026-01-26_LLMTranscriptionSkill-PROBLEMS

## Open

**LLMTR-PR-005: Create high-performance transcribe-pdf-to-markdown.py**
- **History**: Added 2026-01-28 09:44
- **Type**: Feature
- **Priority**: High
- **Description**: Create a highly performance-optimized PDF-to-markdown script

**Requirements:**
- Default model: `gpt-5-mini`
- Auto-analyze PDF page count and calculate optimal strategy
- Target 80% CPU usage with max computer workers
- Target TPM/RPM limits with max OpenAI concurrent workers
- Use OpenAI async API with built-in retry strategy
- Support PDFs from ~30KB (1 page) to ~200MB (500 pages)
- Store limits and defaults in `transcribe-pdf-to-markdown.json`

**Performance optimization strategy:**
- Calculate workers based on: page count, file size, available CPU cores
- Dynamic TPM calculation based on model limits
- RPM (Requests Per Minute) limit awareness
- Concurrent processing with ThreadPoolExecutor + asyncio

**Calibration script** (`transcribe-pdf-to-markdown-calibration.py`):
- Runs on test PDFs to discover optimal settings
- Measures TPM/RPM actual limits (vs. documented)
- Measures CPU usage at different worker counts
- Builds quality vs. speed lookup table based on PDF properties
- Outputs calibration data to `transcribe-pdf-to-markdown-calibration.json`

**Before implementation:**
- [ ] Create calibration script first
- [ ] Run calibration on test PDFs (1, 10, 50, 100, 500 pages)
- [ ] Benchmark different worker configurations
- [ ] Document actual TPM/RPM limits for gpt-5-mini
- [ ] Build lookup table: PDF properties -> optimal settings

**Config file structure** (`transcribe-pdf-to-markdown.json`):
```json
{
  "default_model": "gpt-5-mini",
  "max_cpu_usage_percent": 80,
  "tpm_limit": 2000000,
  "rpm_limit": 500,
  "min_workers": 2,
  "max_workers": 32,
  "retry_attempts": 3,
  "retry_delay_seconds": 1,
  "quality_defaults": {
    "initial_candidates": 3,
    "min_score": 3.5,
    "enable_refinement": true
  }
}
```

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

**[2026-01-28 09:44]**
- Added: LLMTR-PR-005 (high-performance PDF transcription script)

**[2026-01-27 01:05]**
- Resolved: LLMTR-PR-004 (advanced pipeline implemented and tested)

**[2026-01-27 00:00]**
- Resolved: LLMTR-PR-001, LLMTR-PR-002, LLMTR-PR-003 (all implemented)

**[2026-01-26 23:56]**
- Added: LLMTR-PR-001 (skill structure)
- Added: LLMTR-PR-002 (image transcription)
- Added: LLMTR-PR-003 (audio transcription)
