---
intended_model: claude-opus-4-1-20250805
context_window_size: 200k
effort: high
prompt_system: IPPS
---

## Prompt 1 - Verify report and mapping file

<!-- P3 complete; now run verification on both deliverables. -->

```
Read `__STRUT_IPPSGAP.md` steps P4-S1 and P4-S2, `_INFO_GAP_ANALYSIS_REPORT.md`, and `_INFO_MAPPING_LLMBP_TO_IPPS.md`. Treat earlier conversation as compacted. Step P4-S1.
Planning document: `__STRUT_IPPSGAP.md`, steps P4-S1, P4-S2.

Run verification on both deliverables against the `/research` workflow requirements and IPPS document standards.

For the report `_INFO_GAP_ANALYSIS_REPORT.md`: verify document structure (header block, sections, sources), verify all claims trace to sources, verify no markdown tables (use lists per core-conventions), verify no emojis, verify APAPALAN compliance (specific, concise).

For the mapping `_INFO_MAPPING_LLMBP_TO_IPPS.md`: verify all 18 categories are present, verify every article has a mapping entry, verify match levels are consistent (strong, partial, gap), verify gaps cite evidence and deviations cite both sides.

Document any issues found in `_INFO_IPPSGAP-IN04_VerifyResults.md` in the session folder.

Constraints:
- Read both files completely before verifying
- Do not modify the files being verified - only document issues
- Re-running this prompt must not corrupt state or waste cost

/verify
_INFO_GAP_ANALYSIS_REPORT.md and _INFO_MAPPING_LLMBP_TO_IPPS.md
```

---

## Prompt 2 - Critique and reconcile

<!-- Verification done; now critique logic and reconcile findings. -->

```
Read `__STRUT_IPPSGAP.md` steps P4-S3 and P4-S4, `_INFO_GAP_ANALYSIS_REPORT.md`, `_INFO_MAPPING_LLMBP_TO_IPPS.md`, and `_INFO_IPPSGAP-IN04_VerifyResults.md`. Treat earlier conversation as compacted. Step P4-S3.
Planning document: `__STRUT_IPPSGAP.md`, steps P4-S3, P4-S4.

Critique the gap analysis report for flawed assumptions, logic errors, and hidden risks. Apply SOCAS rules: check for inconsistencies (SOCAS-01), ambiguities (SOCAS-02), new solutions for already solved problems (SOCAS-03), overlapping concerns (SOCAS-03), underspecified behavior (SOCAS-06), unverified assumptions (SOCAS-10), and over-engineering (SOCAS-11).

Focus areas: Are any gaps actually false positives (IPPS covers the topic but analysis missed it)? Are any deviations actually alignments (different surface, same underlying principle)? Are any improvements too vague to be actionable? Are overlaps genuine or superficial? Does the report make claims about articles without citing specific passages?

Reconcile critique findings with the report content. For each critique finding: determine if it is valid (read the cited source to confirm). If valid: document the fix needed. If invalid: document why the critique finding is a false positive.

Document critique and reconciliation results in `_INFO_IPPSGAP-IN05_CritiqueResults.md`.

Constraints:
- Read actual source files to validate critique findings
- Do not modify the report or mapping file in this step
- Re-running this prompt must not corrupt state or waste cost

/critique
_INFO_GAP_ANALYSIS_REPORT.md
```

---

## Prompt 3 - Fix issues found

<!-- Issues documented; now fix them in both files. -->

```
Read `__STRUT_IPPSGAP.md` step P4-S5, `_INFO_IPPSGAP-IN04_VerifyResults.md`, `_INFO_IPPSGAP-IN05_CritiqueResults.md`, `_INFO_GAP_ANALYSIS_REPORT.md`, and `_INFO_MAPPING_LLMBP_TO_IPPS.md`. Treat earlier conversation as compacted. Step P4-S5.
Planning document: `__STRUT_IPPSGAP.md`, step P4-S5.

Fix all issues documented in `_INFO_IPPSGAP-IN04_VerifyResults.md` and `_INFO_IPPSGAP-IN05_CritiqueResults.md`. Apply fixes to both `_INFO_GAP_ANALYSIS_REPORT.md` and `_INFO_MAPPING_LLMBP_TO_IPPS.md`.

Fix priority: CRITICAL issues first (false positive gaps, hallucinated claims, missing sources), then HIGH (structural problems, missing sections), then MEDIUM (clarity, precision), then LOW (formatting, wording). After fixing, verify the fixes resolved the issues.

Constraints:
- Do not introduce new content - only fix documented issues
- Do not remove findings without evidence they are wrong
- Each fix must reference the issue it resolves
- Re-running this prompt must not corrupt state or waste cost

Verify: All issues in verify and critique results are resolved.

/verify
_INFO_GAP_ANALYSIS_REPORT.md
```

---

## Prompt 4 - Deliver results and update tracking

<!-- All fixes applied; now present results and update session tracking. -->

```
Read `__STRUT_IPPSGAP.md` phase P5, `_INFO_GAP_ANALYSIS_REPORT.md`, `_INFO_MAPPING_LLMBP_TO_IPPS.md`, `NOTES.md`, `PROGRESS.md`, and `PROBLEMS.md`. Treat earlier conversation as compacted. Step P5-S1.
Planning document: `__STRUT_IPPSGAP.md`, phase P5.

Present the gap analysis results to the user. Provide: executive summary of key findings (3-5 sentences), top 5 gaps with priority, top 5 improvements with priority, top 3 deviations with verdict, overall coverage assessment, pointer to `_INFO_MAPPING_LLMBP_TO_IPPS.md` for full mapping, pointer to `_INFO_GAP_ANALYSIS_REPORT.md` for full report.

Update session tracking files: PROGRESS.md (mark P3, P4, P5 as done, update phase plan), PROBLEMS.md (mark IPPSGAP-PR-0001 through PR-0004 as resolved), NOTES.md (update current phase to DELIVER, add key findings to Important Findings section).

Constraints:
- Do not modify the report or mapping file in this step
- Update tracking files only with factual status information
- Re-running this prompt must not corrupt state or waste cost

After presenting results, ask the user if the deliverables meet their expectations or if changes are needed. Do not proceed until the user confirms satisfaction or requests modifications.

Verify: PROGRESS.md shows P3-P5 done. PROBLEMS.md shows all 4 problems resolved. User has confirmed satisfaction or requested changes.
```
