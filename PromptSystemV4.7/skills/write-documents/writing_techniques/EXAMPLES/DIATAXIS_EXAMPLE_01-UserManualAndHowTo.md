# DIATAXIS Example 01: UserManualAndHowTo

Help-center section for one feature, written `using DIATAXIS as UX-MANUAL-WRITER`. The product, version, and all details are fictional.

## Context

A note-taking app launches notebook sharing. The help center needs content for first-time users, for users with a concrete sharing task, for users looking up permission levels, and for users who ask why shared links expire. Each need becomes one page in one mode.

## Document

```markdown
# Tutorial: Share Your First Notebook

Applies to: Notely web app, version 5.2 and later

In this tutorial you will create a practice notebook and share it with your own second email address. It takes about 5 minutes.

Before you start: have a second email address you can open, such as a personal one.

1. Select New notebook and name it "Practice".
2. Select Share in the top-right corner.
3. Enter your second email address.
4. Select Can view, then select Send.

   You should now see your second address under "People with access".

5. Open your second email inbox and select Open notebook in the message from Notely.

What you learned: how to invite someone and choose what they can do. Next: How to Share a Notebook with an External Partner.

# How to Share a Notebook with an External Partner

Applies to: Notely web app, version 5.2 and later

Before you start:
- You need the Owner or Editor role on the notebook.
- Your workspace admin must allow external sharing (if the Share button is grey, external sharing is turned off).

1. Open the notebook.
2. Select Share.
3. Enter your partner's email address.
4. Select Can comment.
5. Select Send.

Result: your partner receives an email with the subject "A notebook was shared with you" within one minute. Quick check: their address appears under "People with access" with the label External.

Background: Why Shared Links Expire After 30 Days. Exact settings: Sharing Permission Levels.

# Sharing Permission Levels

Applies to: Notely web app, version 5.2 and later

## Can view

- Allows: read pages and download attachments
- Default: people outside your workspace
- Limit: unlimited viewers per notebook

## Can comment

- Allows: read pages and add comments
- Default: none
- Limit: unlimited commenters per notebook

## Can edit

- Allows: add, change, and delete pages
- Default: members of your workspace
- Limit: 50 editors per notebook

# Why Shared Links Expire After 30 Days

Shared notebooks often contain information that is only needed for one project. Links that never expire keep that access open long after the project ends, and nobody remembers who still has it.

Notely therefore ends access for external people 30 days after the last visit. People inside your workspace keep access, because your admin already manages their accounts.

The alternative, links protected by passwords, was not chosen: passwords get forwarded by email and cannot be withdrawn from one person without changing them for everyone.

To give an external partner access again, see How to Share a Notebook with an External Partner.
```

## Key Decisions

- Four pages, one mode each: the tutorial uses a practice notebook and the user's own second address, so nothing real can be exposed (DIATAXIS-ST-01, DIATAXIS-CT-01)
- How-to title starts with "How to", lists role and admin prerequisites before step 1, and ends with the expected result (DIATAXIS-ST-03, DIATAXIS-CT-02, DIATAXIS-EV-02)
- Reference page repeats the same three fields for every level and contains no instructions (DIATAXIS-CT-03)
- Explanation page discusses the reason and the rejected alternative and links to the how-to guide instead of listing steps (DIATAXIS-CT-04, DIATAXIS-ST-04)
- Interface labels quoted exactly (Share, Can comment, People with access) and version stated on every page (DIATAXIS-EV-01, DIATAXIS-EV-03)
- Persona `UX-MANUAL-WRITER` (Technicality 1, Humor 0): no jargon, direct "you"; traits used once each in different pages: Pre-Emptive Reader Objection in the how-to prerequisites (grey Share button) and One-Line Verification Step after the how-to result; the reference page has no traits
