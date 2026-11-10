<!-- DIATAXIS Technique Template (DD-44 Export Form).
Documentation framework across four distinct modes (Tutorial, How-To, Reference, Explanation).
Companion files: DIATAXIS_GUIDES.md, DIATAXIS_RULES.md.
Exports: 1) Section Inventory, 2) Output Body Fragment. -->

## Section Inventory

Ordered list of sections/modes for drafting and documentation output:

1. **Tutorial Mode** (learning + action): Safe hands-on practice exercise guiding a beginner to a guaranteed visible result.
2. **How-To Guide Mode** (working + action): Goal-oriented operational steps solving a real problem for an active user, with error handling.
3. **Reference Mode** (working + information): Strict, comprehensive technical description of objects, configurations, and settings in interface order.
4. **Explanation Mode** (learning + information): Discursive exploration of architectural reasons, background concepts, design trade-offs, and alternatives.

## Output Body Fragment

<!-- MODE BLOCK: TUTORIAL (action + learning). Safe practice exercise with guaranteed result. -->

# Tutorial: [What the learner will create]

Applies to: [Product name], version [N.N] and later

In this tutorial you will [outcome in one sentence]. It takes about [N] minutes.

Before you start: [Prerequisite]

1. [Action]
2. [Action]

   You should now see [visible result].

3. [Action]

What you learned: [one sentence]. Next: [link to how-to guide].

<!-- MODE BLOCK: HOW-TO GUIDE (action + working). Real user goal. -->

# How to [user goal]

Applies to: [Product name], version [N.N] and later

Before you start:
- [Role or permission required]
- [Other prerequisite]

1. [Action]
2. [Action]
3. [Action]

Result: [What the user sees when the goal is reached.]

<!-- Conditional: insert when a common failure exists at a specific step. Per DIATAXIS-EV-02 -->
If [failure symptom], [fix in one sentence].

Background: [link to explanation page]. Exact settings: [link to reference page].

<!-- MODE BLOCK: REFERENCE (knowledge + working). No instructions, repeated item structure. -->

# [Object or setting group name]

Applies to: [Product name], version [N.N] and later

## [Item name exactly as shown in the interface]

- Allows: [What it permits or does]
- Default: [Default value or audience]
- Limit: [Maximum, minimum, or constraint]

<!-- Repeat the item block for every item, in interface order. -->

<!-- MODE BLOCK: EXPLANATION (knowledge + learning). Reasons, trade-offs, alternatives. No steps. -->

# Why [concept works the way it does]

[Paragraph: the problem the design solves.]

[Paragraph: how the concept works, at the level of the audience.]

[Paragraph: trade-offs and alternatives that were not chosen.]

To do this in practice, see [link to how-to guide].
