# TASKS Guide

Read BEFORE writing TASKS documents or sizing STRUT steps. Follow `TASKS_TEMPLATE.md` for mandatory sections. Model data comes from @skills:llm-tools `MODEL_INVENTORY.md`.

## 1. Classify the Planning Document

Decide who executes each task or step. Classification determines which sizing rules apply:

1. Executed by a human or by an agent in open-ended conversation: estimate HWH (Human Work Hours, Section 2), no model sizing
2. Executed as one prompt of a prompts file: estimate HWH (Section 2) and size to the executing model (Section 3)
3. STRUT step executed as one prompt: same as 2. STRUT steps not executed as prompts keep the minute-based scope calibration in @skills:edird-phase-planning

If the executing model is unknown, size for the model named in the session NOTES.md model switching section; if none is named, size for an outcome-level row (`D7-D9`, Items 6, 3 files per prompt in `MODEL_INVENTORY.md`).

## 2. Estimate HWH

HWH = hours a skilled human expert needs for the task without AI, including reading, editing, and verifying. HWH measures task size and does not depend on the model. Target precision: factor 2.

1. Pick a size bucket instead of a free number:
   - 0.25 HWH - one file, one clear edit, known location
   - 0.5 HWH - one file with analysis, or 2-3 small edits
   - 1 HWH - one feature slice across 2-3 files including verification
   - 2 HWH - multi-file change with design decisions
   - Near 4 HWH or more - split the task before estimating further
2. Write the estimate as `Est: [N] HWH` on every task (`TASKS_TEMPLATE.md`)
3. Write the sum of all `Est` values as `Estimated total` in Task Overview

The planning agent may estimate HWH itself. Model and human estimates are both imperfect; buckets keep the error at the bucket boundary.

Common mistake: estimating agent time instead of human time. HWH stays the same when a faster model executes the task.

## 3. Size Tasks and Steps to the Executing Model

Applies to classification 2 and 3 (Section 1).

1. Look up the executing model's row in `MODEL_INVENTORY.md`: Depth, Items, and Notes. Shift Depth by the chosen effort to the effective rung and read its explicitness level and max_files (`MODEL_INVENTORY.md` Section 2)
2. Check each task or step: `Est <= 1 HWH`, numbered instructions after explicitness expansion <= Items, changed files <= max_files
3. If a check fails, split the task into tasks that each pass all three checks. Split along files first, then along instruction groups
4. Write task instructions at the explicitness level of the effective rung; a shallower rung needs more, smaller items, not longer prose

## 4. Estimate AWH

AWH (Agent Work Hours) = wall-clock time the agent runs, excluding user wait. Use AWH for scheduling and STRUT phase budgets, never for task size.

1. Before measured data exists: `AWH = 0.2 * HWH` for well-specified, self-contained tasks
2. After 3 sessions with the same model and effort: `AWH = prompt_count * observed minutes per prompt`, taken from STRUT Time Log net working time
3. Tasks in large, familiar codebases with heavy review: do not convert. Review and correction dominate the time; estimate from previous sessions instead

## 5. Hand Over to /write-prompts

1. `/write-prompts` takes task HWH from the `Est` values (`PROMPTS_GUIDES.md` Section 1g)
2. Name the intended model and effort in the TASKS Model hint when known, so Section 3 sizing and prompt partitioning use the same row

## 6. Review Checklist

- [ ] Every task classified by executor (Section 1)
- [ ] Every task has `Est: [N] HWH` from the bucket list; `Estimated total` equals the sum
- [ ] No task near 4 HWH or more remains unsplit
- [ ] Prompt-executed tasks pass `Est <= 1 HWH`, expanded items <= Items, files <= max_files for the executing model
- [ ] AWH used only for scheduling, not for task size
