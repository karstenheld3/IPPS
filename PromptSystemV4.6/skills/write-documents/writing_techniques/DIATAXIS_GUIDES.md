# DIATAXIS Guide

Read BEFORE writing technical documentation, a user manual, a help center, or onboarding content with `using DIATAXIS`. Diataxis (Daniele Procida) sorts documentation into 4 modes by user need.

## 1. Decide Which Mode Each Page Needs

Diataxis places every page on two axes: action vs. knowledge, and learning (acquisition) vs. working (use). Decide the mode per page before writing:

- Tutorial (action + learning): a newcomer learns by doing a guaranteed, safe exercise. Example: "Create your first shared notebook"
- How-to guide (action + working): a user with a real goal follows steps to reach it. Example: "How to share a notebook with an external partner"
- Reference (knowledge + working): a user looks up exact facts. Example: "Sharing permission levels"
- Explanation (knowledge + learning): a user wants to understand why something works the way it does. Example: "Why shared notebooks use permission levels instead of passwords"

When the content is a one-off announcement (`IMINTO`) or a skill-building chapter with a principle (`STA`), tell the user that a different technique fits better, and keep `DIATAXIS` until the user decides (`DRSYNART-DD-08`).

## 2. Plan the Documentation Set

1. List the user needs for the product or feature: what newcomers must learn, what tasks users perform, what facts they look up, what concepts confuse them
2. Assign each need to exactly one mode; one need becomes one page
3. Plan cross-links: tutorials link to how-to guides for next steps, how-to guides link to reference for exact values, any page links to explanation for background
4. Record the product version and the exact interface labels you will quote

## 3. Execute Each Mode

1. Tutorial: state what the learner will build, list prerequisites, give numbered steps that always work, show the visible result after key steps, end with what they learned and where to go next
2. How-to guide: title "How to [goal]", state prerequisites and permissions, numbered steps with one action each, state the expected result, handle the most common failure in one line
3. Reference: consistent structure for every item (name, description, values, defaults, limits); no instructions and no opinions
4. Explanation: discuss reasons, history, trade-offs, and alternatives in prose; no step-by-step instructions

## 4. When the User Also Passes a Persona

- This section applies only when the user passes `as <persona>`. Without it, apply no persona and do not pick one from the list below (`DRSYNART-DD-08`)
- Fitting personas, offered only when the user asks for persona help: `UX-MANUAL-WRITER` (end-user help, Technicality 1), `TECHNICAL-WRITER` (practitioner and developer docs, Technicality 3), `PRINCIPAL-ARCHITECT` (explanation pages on design decisions)
- Persona Technicality must match the mode audience: end-user tutorials need Technicality 0-1, developer reference may use 4-6
- Persona traits fit specific modes: One-Line Verification Step at the end of tutorials and how-to guides; The Catch for prerequisites in how-to guides; no traits in reference pages
- Persona style must not add explanations to reference pages or opinions to how-to steps

## 5. Use the Template and the Example

- Skeleton (all 4 modes): [TEMPLATES/DIATAXIS_TEMPLATE.md](TEMPLATES/DIATAXIS_TEMPLATE.md)
- Complete GOOD example with `UX-MANUAL-WRITER`: [EXAMPLES/DIATAXIS_EXAMPLE_01-UserManualAndHowTo.md](EXAMPLES/DIATAXIS_EXAMPLE_01-UserManualAndHowTo.md)

## 6. Strategic Review Questions

Used by `/critique` after writing:
- Does every page serve exactly one user need, or did convenience merge two modes into one page?
- Are there user needs without any page (for example, many how-to guides but no explanation of the core concept)?
- Would a first-time user and an experienced user each find their page within two clicks?
