# DIATAXIS Rules

Output standards for documentation written `using DIATAXIS` (tutorial, how-to guide, reference, explanation).

**Writing quality:** Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: AP-PR-10 (never abbreviate keys and references), MW-VO-02 (address reader as "you"), MW-HS-03 (write for declared audience).

## Rule Index

Structure (ST)
- DIATAXIS-ST-01: Each page has exactly one declared mode
- DIATAXIS-ST-02: Tutorials and how-to guides use numbered steps
- DIATAXIS-ST-03: How-to guide titles start with "How to"
- DIATAXIS-ST-04: Pages link to other modes instead of mixing them

Content (CT)
- DIATAXIS-CT-01: Tutorials use a safe exercise with a guaranteed result
- DIATAXIS-CT-02: How-to guides address a real user goal and state prerequisites
- DIATAXIS-CT-03: Reference pages contain no instructions and use a repeated item structure
- DIATAXIS-CT-04: Explanation pages contain no step-by-step instructions

Evidence (EV)
- DIATAXIS-EV-01: Interface labels and commands are quoted exactly
- DIATAXIS-EV-02: Each procedure states its expected result
- DIATAXIS-EV-03: Product version or date of validity is stated

## DIATAXIS-ST-01: One Mode per Page

**BAD:** A page titled "Sharing" that explains permission theory, lists all settings, and walks through steps.

**GOOD:** Four pages: tutorial "Share your first notebook", how-to "How to share with an external partner", reference "Sharing permission levels", explanation "Why permission levels instead of passwords".

## DIATAXIS-ST-02: Numbered Steps

**BAD:** "Open the notebook, then go to the share menu and enter the address and pick a permission."

**GOOD:**
```
1. Open the notebook.
2. Select Share in the top-right corner.
3. Enter the email address.
4. Select Can comment.
```

## DIATAXIS-ST-03: "How to" Titles

**BAD:** `External Sharing`

**GOOD:** `How to Share a Notebook with an External Partner`

## DIATAXIS-ST-04: Link Instead of Mix

**BAD:** A how-to guide contains three paragraphs on the security model.

**GOOD:** "To understand why links expire, see [Why shared links expire after 30 days]."

## DIATAXIS-CT-01: Safe Tutorial

**BAD:** "Tutorial: share your company's client notebook with a customer."

**GOOD:** "Tutorial: create a practice notebook and share it with your own second email address."

## DIATAXIS-CT-02: Real Goal and Prerequisites

**BAD:** A how-to guide starts with step 1 and fails for users without permission.

**GOOD:** "Before you start: you need the Owner or Editor role on the notebook."

## DIATAXIS-CT-03: Instruction-Free Reference

**BAD:** "Can edit: Use this when you trust the person. Click Share first, then..."

**GOOD:**
```
Can edit
- Allows: add, change, and delete pages
- Default for: members of your workspace
- Limit: 50 editors per notebook
```

## DIATAXIS-CT-04: Instruction-Free Explanation

**BAD:** An explanation page ends with "1. Go to Settings. 2. Select Security."

**GOOD:** The explanation discusses why expiring links reduce risk and links to the how-to guide for the steps.

## DIATAXIS-EV-01: Exact Labels

**BAD:** "Click the sharing button."

**GOOD:** "Select Share."

## DIATAXIS-EV-02: Expected Result

**BAD:** The procedure ends after the last click.

**GOOD:** "Your partner receives an email with the subject 'A notebook was shared with you' within one minute."

## DIATAXIS-EV-03: Version Stated

**BAD:** No indication which app version the screenshots and labels belong to.

**GOOD:** "Applies to: Notely web app, version 5.2 and later."
