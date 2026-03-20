# Failure Log

## MIPPS-FL-0001 [MEDIUM] IMPL File Structure showed only modified files, not actual directory

- **When**: 2026-03-20 17:57
- **Where**: `_IMPL_IPPS_MINIFICATION_MOTHER_MODEL_V2.md [MIPPS-IP03]` Section 1, lines 42-53
- **What**: File Structure tree listed 4 lib/ files and 3 test files. Actual `_run_templateV2/` has 33 files: 16 in lib/ (13 .py + 3 .json), 8 in tests/, 6 in prompts/step/, plus root-level files. Reader gets wrong mental model of codebase scope.
- **Evidence**: Screenshot of actual `lib/` directory shows 15 entries vs document's 3. Missing: `llm_client.py`, `mother_analyzer.py`, `run_manager.py`, `pipeline_state.py`, `file_bundle_builder.py`, `compression_prompt_builder.py`, `compression_refiner.py`, 3 JSON configs, entire `prompts/` directory.
- **Severity**: MEDIUM - Implementation steps reference correct target files, but incomplete tree hides codebase complexity and dependencies.
- **Workflow re-read findings**: IMPL_TEMPLATE.md File Structure section shows full project tree with annotations. Intent: complete structure context, not just modified files.
- **Root cause**: Only listed files from Target files header + new test files. Did not verify against actual directory listing. Assumed "show what changes" = "show only what changes".
- **Suggested fix**: Always run `find` or directory listing before writing File Structure. Show complete tree, annotate modified/new files with `[MODIFY]`/`[NEW]`/`[EXTEND]`.
