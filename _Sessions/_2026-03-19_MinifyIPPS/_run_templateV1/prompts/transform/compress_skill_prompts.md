Compress this LLM prompt file while preserving ALL instruction content that affects model output.

Primary (keep as-is): All DO/DON'T rules, all CRITICAL/FORBIDDEN constraints, all output format specifications, all tag definitions (<transcription_image>, <transcription_json>, etc.), all scoring scales with numeric thresholds, all evaluation criteria with point allocations, format check rules (instant fail conditions), all required output JSON schemas.

Secondary (compress):
- Verbose explanations of WHY a rule exists (the model needs the WHAT, not the WHY).
- Multiple examples showing the same pattern: Keep 1 complete example per pattern.
- Descriptive headers for sections that are self-explanatory.
- Anti-duplication rule explanation: Reduce to the rule statement, drop the worked scenario.
- Scoring justification prose: Keep the numeric scale and criteria keywords, drop explanatory sentences.
- "What to Compare" sections that restate what's obvious from the evaluation criteria.

Drop:
- Section dividers (---) that are purely visual.
- Introductory sentences before rule lists ("The following rules apply:").

Formatting rules:
- Preserve ALL tag names and formats exactly (<transcription_image>, ```ascii, etc.).
- Preserve ALL numeric scoring thresholds exactly.
- Preserve ALL output format JSON structures exactly.
- Preserve ALL DO/DON'T lists verbatim.
- Preserve ALL CRITICAL/FORBIDDEN constraints verbatim.
- Preserve evaluation weights exactly (e.g., text=0.25, structure=0.35, graphics=0.40).
- Keep complete examples that show the required output format.
- Do NOT rephrase instructions - preserve exact wording of behavioral directives.
- Do NOT add content not in the original.