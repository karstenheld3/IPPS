# IMINTO Guide

Read BEFORE writing a news item, incident report, release note, status update, or executive brief with `using IMINTO`.

## 1. Decide Whether the Inverted Pyramid Fits

Use it when readers may stop after the first sentence or paragraph and still need the most important facts: who, what, when, where, why, how. Typical outputs: incident briefs, release notes, status updates, news summaries, announcement emails, executive briefs.

Tell the user that a different technique fits better, and keep `IMINTO` until the user decides (`DRSYNART-DD-08`), when:
- The point only makes sense after a chain of reasoning (cutting from the bottom would remove the justification): use `MINTO`
- The reader reads for pleasure and the story needs a scene before the facts: use `KABOB`
- The reader needs step-by-step instructions: use `DIATAXIS` (how-to mode)

## 2. Plan Before Writing

1. List every fact you have. Mark each fact with its importance to the reader, not to the author
2. Pick the 3-5 facts a reader must know if they read only one sentence; these form the lede
3. Decide what the nut graf must answer: why this matters to the reader and what the rest of the text covers
4. Order the remaining facts strictly by decreasing importance; background and history go last
5. Mark facts that are still unconfirmed; they must be labeled in the text

## 3. Execute Each Section

1. Headline: state the news itself (actor, action, result), not a topic
2. Lede: 1-2 sentences, 25-40 words, active voice, the most important facts first
3. Nut graf: within the next 1-2 paragraphs, state the impact on the reader and what follows
4. Body: one fact cluster per paragraph, each less important than the one before. Apply the cut test: deleting the last paragraph must not remove anything the reader needs to act
5. Closing: least important context (history, related links). No summary paragraph

## 4. When the User Also Passes a Persona

- This section applies only when the user passes `as <persona>`. Without it, apply no persona and do not pick one from the list below (`DRSYNART-DD-08`)
- Fitting personas, offered only when the user asks for persona help: `TECHNICAL-WRITER` (incident and release notes), `CXO-ADVISOR` (executive briefs), `ANALYST` (findings briefs), `INVESTIGATIVE-JOURNALIST` (news follow-ups)
- Persona Narrative values above 3 must not delay the lede; a scene, if any, appears after the nut graf
- Persona traits such as One-Line Verification Step fit at the end of an action paragraph, never inside the lede
- Persona warmth may acknowledge impact on readers ("if your payments failed between...") but must not replace the facts

## 5. Use the Template and the Example

- Skeleton: [TEMPLATES/IMINTO_TEMPLATE.md](TEMPLATES/IMINTO_TEMPLATE.md)
- Complete GOOD example with `TECHNICAL-WRITER`: [EXAMPLES/IMINTO_EXAMPLE_01-IncidentAndReleaseBrief.md](EXAMPLES/IMINTO_EXAMPLE_01-IncidentAndReleaseBrief.md)

## 6. Strategic Review Questions

Used by `/critique` after writing:
- Was the reader really an early stopper, or did they need the reasoning chain that the inverted pyramid cuts?
- Were facts ranked by importance to the reader or by the order in which the author learned them?
- Would a reader who stops after the lede make a correct decision?
