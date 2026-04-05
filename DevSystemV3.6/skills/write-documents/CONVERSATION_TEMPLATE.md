# Conversation: [Name or Description]

## MUST-NOT-FORGET

- DATETIME FORMAT: Use `YYYY-MM-DD HH:MM` everywhere (logs, todos, headings, attachments)
- CHRONOLOGICAL ORDER: History section = newest on top, oldest at bottom (reverse chronological)
- TRANSLATION FORMAT: All non-English text MUST be followed by English translation in quote block
  - Format: `**Person (HH:MM)**: Original text here.`
  - Next line: `> English translation here.`
  - Example:
    ```
    **Person (11:49)**: Non-English text here.
    > English translation here.
    ```
- NATIVE CHARACTERS: Non-English text must use native special characters (e.g., ä, ö, ü, ß for German). Never substitute with ASCII approximations (ae, oe, ue, ss)
- No markdown tables except when sent in emails
- SEND EMAILS VIA PLAYWRIGHT GMAIL UI - NEVER use CLI tools to send (body encoding fails)
- Email header format: `From: | To: | CC: | BCC: | Subject: | Reply-To: | Thread: | Message-ID:`
- History heading format: `### YYYY-MM-DD HH:MM - Summary`
- Log entry format: `- **YYYY-MM-DD HH:MM** - Main topic`
- Todo format: `- **YYYY-MM-DD HH:MM** - Item - Deadline: YYYY-MM-DD, Status: TODO:[ACTION]/DONE`
- Todo actions: `TODO:REPLY`, `TODO:REVIEW`, `TODO:PAY`, `TODO:PLAN`, `TODO:SCHEDULE_CALL` (web), `TODO:SCHEDULE_TRIP`, `TODO:SCHEDULE_MEETING` (in person)
- Attachment folder format: `Attachments/YYYY-MM-DD_HH-MM_[Topic]/`
- All URLs as Markdown clickable links: `[Title](https://...)`
- CHECK DOWNLOADED IMAGES - After downloading, review each image. Delete signature icons, logos, spacers, and other email template garbage. Keep only real attachments.

## Ignore Files

Files matching these patterns should NOT be downloaded. If downloaded, delete them.

`line.png` | `space.png` | `*-logo*.png` | `i-facebook*.png` | `i-instagram*.png` | `i-link*.png` | `image-horizontal*.png` | `Outlook-*.png`

## Status

**Current**: [ACTIVE / AWAITING_RESPONSE / ON_HOLD / COMPLETED]

### Todos and Deliverables

- **2026-03-15 09:15** - Send proposal draft - Deadline: 2026-03-20, Status: TODO:REPLY
- **2026-03-17 14:30** - Review contract terms - Status: DONE

## Links and shared documents

- **2026-03-15 09:15** - Some websites to check
  - [Website Title](https://example.com)
- **2026-03-17 14:30** - Document title
  - [Document.pdf](Attachments/2026-03-17_14-30_Topic/Document.pdf)

## Conversation Context

### Persons Involved

**[Contact Name]** (contact@example.com)
- Role: [Role at Organization]
- Phone: [+XX XXX XXX XXXX]
- Timezone: [TZ]
- Notes: [Communication preferences]

**[Second Contact]** (second@example.com)
- Role: [Role]
- Notes: [Relevant notes]

**[Your Name]** (your@email.com)
- Role: Me

### Topics

- **Topic 1** - Brief description
- **Topic 2** - Brief description

## Log

- **2026-03-17 14:30** - Discussed Q2 timeline adjustments
  - Decision: Move milestone 2 to April 15
  - Action: Send updated document by Friday
  - Attachment: [Doc.pdf](Attachments/2026-03-17_14-30_Topic/Doc.pdf)
  - [Email](#2026-03-17-1430---q2-timeline-discussion)
- **2026-03-15 09:15** - Initial project kickoff
  - Decision: Use agile methodology
  - [Email](#2026-03-15-0915---project-kickoff)

## History

### 2026-03-17 14:30 - Q2 Timeline Discussion

From: contact@example.com | To: your@email.com | CC: second@example.com | BCC: -
Subject: Re: Q2 Timeline | Reply-To: - | Thread: Q2 Planning | Message-ID: abc123

Email body here.

---

### 2026-03-15 09:15 - Project Kickoff

From: your@email.com | To: contact@example.com | CC: - | BCC: -
Subject: Project Alpha - Kickoff | Reply-To: - | Thread: Project Alpha | Message-ID: def456

Email body here.

---

### 2026-03-14 WhatsApp - Topic Name

Platform: WhatsApp | Participants: [Your Name], [Contact Name]

**14:30 [You]**: Message text here.

**14:45 [Contact]**: Reply text here.
> English translation here.

**Key outcomes:**
- Outcome 1
- Outcome 2
