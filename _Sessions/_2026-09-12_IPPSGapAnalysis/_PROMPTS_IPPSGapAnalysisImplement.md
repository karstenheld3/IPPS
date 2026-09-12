---
intended_model: claude-opus-4-1-20250805
context_window_size: 200k
effort: high
prompt_system: IPPS
---

## Prompt 1 - Deep read remaining LLM best practices articles

<!-- Read 12 remaining high-value articles not yet covered in preflight analysis. -->

```
Read `__STRUT_IPPSGAP.md` step P3-S1, `_INFO_PREFLIGHT_ANALYSIS.md`, and the LLM best practices directory at `e:\Dev\Delphios\knowledge\AI-Stuff\LLMBestPractices_2026-09-12`. Treat earlier conversation as compacted. Step P3-S1.
Planning document: `__STRUT_IPPSGAP.md`, step P3-S1.

Read the following 12 articles from the LLM best practices knowledge base completely. For each article, extract: key claims, concrete recommendations, and any IPPS-relevant patterns. Do not skim - read the full article content.

Articles to read:
- ai-agents/structured-output.md
- ai-agents/system-prompts.md
- ai-agents/role-framing.md
- ai-agents/rag.md
- ai-agents/mcp-servers.md
- prompt-engineering/reasoning-model-prompting.md
- prompt-engineering/prompt-caching-strategies.md
- knowledge-vaults/vault-frontmatter-schema.md
- knowledge-vaults/linking-and-tags.md
- knowledge-vaults/team-vaults.md
- knowledge-vaults/vault-evolution.md
- writing/glossary.md (if exists, for terminology cross-reference)

Write a summary of each article to `_INFO_IPPSGAP-IN03_ArticleSummaries.md` in the session folder. For each article: 3-5 bullet points of key takeaways relevant to IPPS.

Constraints:
- Read each article file completely before summarizing
- Do not rely on preflight analysis summaries for article content
- Do not modify any files in the LLM best practices directory
- Re-running this prompt must not corrupt state or waste cost

Verify: `_INFO_IPPSGAP-IN03_ArticleSummaries.md` exists with summaries for all articles read (11-12 depending on glossary existence).
```

---

## Prompt 2 - Write standalone mapping file

<!-- Previous step produced article summaries; now write the mapping file using the template. -->

```
Read `__STRUT_IPPSGAP.md` step P3-S2, `__TEMPLATE_GapAnalysisMapping.md`, `_INFO_PREFLIGHT_ANALYSIS.md`, and `_INFO_IPPSGAP-IN03_ArticleSummaries.md`. Treat earlier conversation as compacted. Step P3-S2.
Planning document: `__STRUT_IPPSGAP.md`, step P3-S2.

Write the standalone mapping file `_INFO_MAPPING_LLMBP_TO_IPPS.md` in the session folder. Use `__TEMPLATE_GapAnalysisMapping.md` as the structural template. Map every article read (41 from preflight plus 12 from step P3-S1 = 53 total) to IPPS concepts.

For each article: state the article path, identify the IPPS equivalent (concept, spec, skill, workflow, or rule), classify match level (strong, partial, or gap), and add a 1-2 sentence note explaining the match or gap.

Group mappings by category (18 categories). Include summary statistics per category. Fill in all template sections: Methodology, Source Material, Mapping by Category, Gap Analysis, Concept Deviations, Improvement Opportunities, Overlap Analysis, Coverage Matrix, Recommendations, Sources.

Constraints:
- Use the template structure exactly - fill in all sections
- Do not skip any category, even if only 1 article was read
- Every gap must cite the specific article and explain what IPPS lacks
- Every deviation must cite both the article and the specific IPPS spec
- Do not invent articles or claims not present in the source material
- Re-running this prompt must not corrupt state or waste cost

Verify: `_INFO_MAPPING_LLMBP_TO_IPPS.md` exists with all 18 categories mapped.

/verify
_INFO_MAPPING_LLMBP_TO_IPPS.md
```

---

## Prompt 3 - Verify and expand gap and deviation analysis

<!-- Mapping file created; now verify each gap and deviation against actual IPPS files. -->

```
Read `__STRUT_IPPSGAP.md` steps P3-S3 and P3-S4, `_INFO_MAPPING_LLMBP_TO_IPPS.md`, and the IPPS specs directory at `e:\Dev\IPPS\specs\`. Also read `e:\Dev\IPPS\.devin\workflows\` and `e:\Dev\IPPS\.devin\skills\` directory listings. Treat earlier conversation as compacted. Step P3-S3.
Planning document: `__STRUT_IPPSGAP.md`, steps P3-S3, P3-S4.

Verify and expand the gap analysis (10 gaps identified in preflight) and deviation analysis (9 deviations identified in preflight) in `_INFO_MAPPING_LLMBP_TO_IPPS.md`.

For each gap: read the actual IPPS spec, workflow, or skill file that might cover this topic. Search `e:\Dev\IPPS\.devin\workflows\` and `e:\Dev\IPPS\.devin\skills\` directories for any coverage. If IPPS has coverage: reclassify from gap to partial or strong. If IPPS truly lacks coverage: confirm the gap with specific evidence (which files were checked). Add any new gaps found during deeper reading.

For each deviation: read the specific IPPS spec section cited in the deviation. Read the specific best practice article cited in the deviation. Verify the deviation is real (not a false positive from superficial reading). Assess whether the deviation is an intentional improvement or an unintentional gap. Add any new deviations found during deeper reading.

Update `_INFO_MAPPING_LLMBP_TO_IPPS.md` sections 4 (Gap Analysis) and 5 (Concept Deviations) with verified and expanded findings.

Constraints:
- Read actual IPPS files to verify each gap - do not rely on memory or preflight summary
- Each gap must cite which IPPS files were checked and found lacking
- Each deviation must cite both the article path and the IPPS spec path
- Do not classify something as a gap without searching workflows and skills directories first
- Re-running this prompt must not corrupt state or waste cost

/fact-check
key claims in _INFO_MAPPING_LLMBP_TO_IPPS.md sections 4 and 5
```

---

## Prompt 4 - Verify and expand improvement and overlap analysis

<!-- Gaps and deviations verified; now verify improvements and overlaps. -->

```
Read `__STRUT_IPPSGAP.md` steps P3-S5 and P3-S6, `_INFO_MAPPING_LLMBP_TO_IPPS.md`, and the IPPS specs directory at `e:\Dev\IPPS\specs\`. Treat earlier conversation as compacted. Step P3-S5.
Planning document: `__STRUT_IPPSGAP.md`, steps P3-S5, P3-S6.

Verify and expand the improvement analysis (10 improvements identified in preflight) and overlap analysis in `_INFO_MAPPING_LLMBP_TO_IPPS.md`.

For each improvement: read the specific best practice article cited as the source. Read the specific IPPS spec, skill, or workflow that would be affected. Verify the improvement is actionable (can be implemented as a spec change, new skill, or workflow update). Assess priority: HIGH (safety or correctness), MEDIUM (efficiency), LOW (nice-to-have). Add any new improvements found during deeper reading.

For each overlap: read both the best practice article and the IPPS concept. Verify the overlap is genuine (both address the same topic with similar approaches). Classify overlap level: High (near-identical), Medium (same topic, different details), Low (tangential). Add any new overlaps found during deeper reading.

Update `_INFO_MAPPING_LLMBP_TO_IPPS.md` sections 6 (Improvement Opportunities), 7 (Overlap Analysis), 8 (Coverage Matrix), and 9 (Recommendations) with verified and expanded findings.

Constraints:
- Read actual files to verify each improvement and overlap
- Each improvement must cite the specific article and specific IPPS file affected
- Each overlap must cite both sides with specific section references
- Do not invent improvements not supported by the source material
- Re-running this prompt must not corrupt state or waste cost

/fact-check
key claims in _INFO_MAPPING_LLMBP_TO_IPPS.md sections 6, 7, 8, and 9
```

---

## Prompt 5 - Write full gap analysis report with verification

<!-- All analysis complete; now write the full report with final verification. -->

```
Read `__STRUT_IPPSGAP.md` step P3-S7, `_INFO_MAPPING_LLMBP_TO_IPPS.md`, `_INFO_PREFLIGHT_ANALYSIS.md`, and `_INFO_IPPSGAP-IN03_ArticleSummaries.md`. Treat earlier conversation as compacted. Step P3-S7.
Planning document: `__STRUT_IPPSGAP.md`, step P3-S7.

Write the full gap analysis report `_INFO_GAP_ANALYSIS_REPORT.md` in the session folder. This report is the comprehensive deliverable that supersedes the preflight analysis.

Report structure (10 sections):
1. Executive summary - key findings, coverage percentage, top 3 recommendations
2. Methodology - how the analysis was conducted, articles read, IPPS specs cross-referenced
3. Complete mapping - reference to `_INFO_MAPPING_LLMBP_TO_IPPS.md` (do not repeat full mapping)
4. Gap analysis - expanded from preflight, each gap with evidence and impact
5. Concept deviations - expanded from preflight, each deviation with assessment and verdict
6. Improvement opportunities - expanded from preflight, each improvement with priority and rationale
7. Overlap analysis - what IPPS already does well, aligned with best practices
8. Coverage matrix - category-by-category coverage percentages
9. Recommendations - prioritized, actionable, with affected IPPS files
10. What IPPS does better than best practices - areas where IPPS exceeds the source

Constraints:
- Reference the mapping file for detailed mappings - do not duplicate the full mapping in the report
- Every claim must trace to a source (article path or IPPS file path)
- Do not introduce findings not present in the mapping file
- The report must be self-contained: a reader can understand the analysis without reading the mapping file
- Re-running this prompt must not corrupt state or waste cost

Verify: `_INFO_GAP_ANALYSIS_REPORT.md` exists with all 10 sections.

/verify
_INFO_GAP_ANALYSIS_REPORT.md

/fact-check
key claims in _INFO_GAP_ANALYSIS_REPORT.md sections 1, 4, 5, 6, and 10
```
