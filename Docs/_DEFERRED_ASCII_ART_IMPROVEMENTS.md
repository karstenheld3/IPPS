# Deferred ASCII Art Improvements

Candidates logged by `/improve` run 2026-09-12. Not applied without proof.

## Deferred Candidates

**AA-DF-01: Add depth/overlay techniques to GUIDES**
- Source: `/improve` scan 2026-09-12
- Candidate: GUIDES lacks depth/overlay guidance. INFO doc has 5 techniques (occlusion, offset stack, shadow, modal, isometric). CHECKS AA-QI-06 asks about depth but GUIDES has no corresponding section.
- Pragmatic filter: Real risk = low (depth techniques rarely needed, most diagrams are flat). Proportionate = no (adds complexity for edge case). Simpler alternative = yes (one-liner in existing section 3: "for overlapping boxes, state depth technique in legend").
- Assessment: DEFER - low frequency use, can be a one-liner if needed

**AA-DF-02: Add sequence diagram example**
- Source: `/improve` scan 2026-09-12
- Candidate: GUIDES section 1 lists "sequence diagram" but no example file covers it. Architecture examples cover component/layer/topology; state machine examples cover state/flowchart/decision tree.
- Pragmatic filter: Already addressed = partially (flowchart example covers ordering). Real risk = medium (sequence diagrams have distinct notation: lifelines, activation bars, message arrows). Proportionate = yes (one new example file). Proven = no (no evidence agents produce wrong sequence diagrams yet).
- Assessment: DEFER - no evidence of need yet, add when agents produce sequence diagrams

**AA-DF-03: Add state machine notation rule to RULES**
- Source: `/improve` scan 2026-09-12
- Candidate: `(*)` for initial state and `(final)` for terminal state used in EXAMPLES but not codified in RULES. Agents may invent inconsistent notation.
- Pragmatic filter: Already addressed = partially (example shows notation). Real risk = low (notation is intuitive). Simpler alternative = yes (add to existing AA-LB-02 as "state machines use (*) for initial, (final) for terminal").
- Assessment: DEFER - can be folded into existing label rule if needed

**AA-DF-04: Add decision diamond notation to GUIDES**
- Source: `/improve` scan 2026-09-12
- Candidate: Flowchart example uses `/ \` for decision diamonds but notation is unexplained in GUIDES.
- Pragmatic filter: Already addressed = partially (example shows it). Real risk = low (self-evident from example). Simpler alternative = yes (one line in GUIDES section 3: "decisions use / \\ diamond shape with Yes/No labels").
- Assessment: DEFER - example is self-documenting, add only if agents ask
