# Conversation Document Rules

Rules for writing and maintaining CONVERSATION.md files with GOOD/BAD examples.

## Rule Index

Datetime (DT)
- CV-DT-01: Use `YYYY-MM-DD HH:MM` format everywhere
- CV-DT-02: History and Log in reverse chronological order (newest first)
- CV-DT-03: Attachment folders use `YYYY-MM-DD_HH-MM_[Topic]/` format

Translation (TR)
- CV-TR-01: Non-English text MUST have English translation
- CV-TR-02: Translation uses quote block on next line

Email (EM)
- CV-EM-01: Email header format with all fields on one line
- CV-EM-02: Send via Playwright Gmail UI, never CLI tools
- CV-EM-03: Email signature included only on first occurrence per sender
- CV-EM-04: Draft emails marked with `**STATUS: DRAFT - NOT SENT**`

WhatsApp (WA)
- CV-WA-01: Message format `**HH:MM Person**: message`
- CV-WA-02: Section heading includes time range and platform
- CV-WA-03: End WhatsApp sections with `**Key outcomes:**` summary

Structure (ST)
- CV-ST-01: Required sections in order: MNF, Ignore Files, Status, Links, Context, Log, History
- CV-ST-02: Persons Involved in Context section (not separate Contacts)
- CV-ST-03: Log entries link to History sections via anchor
- CV-ST-04: History entries separated by `---`

Attachments (AT)
- CV-AT-01: Check downloaded images - delete email garbage (signatures, logos, spacers)
- CV-AT-02: Ignore files pattern maintained per conversation

Todos (TD)
- CV-TD-01: Todo format with timestamp, item, deadline, status
- CV-TD-02: Status actions: `TODO:REPLY`, `TODO:REVIEW`, `TODO:PAY`, `TODO:PLAN`, `TODO:SCHEDULE_CALL`, `TODO:SCHEDULE_TRIP`, `TODO:SCHEDULE_MEETING`

Links (LN)
- CV-LN-01: All URLs as clickable Markdown links
- CV-LN-02: Links section groups by date with description

## Table of Contents

- [Datetime Format](#datetime-format)
- [Reverse Chronological Order](#reverse-chronological-order)
- [Translation Format](#translation-format)
- [Email Header Format](#email-header-format)
- [Email Sending](#email-sending)
- [Draft Emails](#draft-emails)
- [WhatsApp Message Format](#whatsapp-message-format)
- [WhatsApp Section Heading](#whatsapp-section-heading)
- [WhatsApp Key Outcomes](#whatsapp-key-outcomes)
- [Log Entry Format](#log-entry-format)
- [Log Anchors](#log-anchors)
- [History Heading Format](#history-heading-format)
- [Todo Format](#todo-format)
- [Attachment Folder Format](#attachment-folder-format)
- [Image Cleanup](#image-cleanup)
- [URL Format](#url-format)

## Datetime Format

Use `YYYY-MM-DD HH:MM` in all timestamps: headings, log entries, todos, attachment folders.

**BAD:**
```
### March 17, 2026 2:30 PM - Timeline Discussion
- Mar 17 - Discussed timeline
- 17.03.2026 14:30 - Send proposal
```

**GOOD:**
```
### 2026-03-17 14:30 - Timeline Discussion
- **2026-03-17 14:30** - Discussed timeline
- **2026-03-17 14:30** - Send proposal - Deadline: 2026-03-20, Status: TODO:REPLY
```

## Reverse Chronological Order

History and Log: newest entry on top, oldest at bottom.

**BAD:**
```
## History

### 2026-03-15 09:15 - First Email
...
### 2026-03-17 14:30 - Second Email
```

**GOOD:**
```
## History

### 2026-03-17 14:30 - Second Email
...
### 2026-03-15 09:15 - First Email
```

## Translation Format

Non-English text: original first, English translation in quote block on next line.

**BAD:**
```
Person said: "Aqui vai a última fatura." (Here is the last invoice.)
```

**BAD:**
```
Person: Here is the last invoice.
(Original: Aqui vai a última fatura.)
```

**GOOD:**
```
**Person (11:49)**: Aqui vai a última fatura.
> Here is the last invoice.
```

## Email Header Format

All fields on one pipe-separated line. Use `-` for empty fields, never omit fields.

**BAD:**
```
From: john@example.com
To: me@example.com
Subject: Meeting
```

**BAD:**
```
From: john@example.com | To: me@example.com | Subject: Meeting
```

**GOOD:**
```
From: john@example.com | To: me@example.com | CC: - | BCC: -
Subject: Re: Meeting | Reply-To: - | Thread: Project Alpha | Message-ID: abc123
```

## Email Sending

Always use Playwright Gmail UI. CLI send tools have body encoding failures.

**BAD:** `cli-tool send --to "contact@example.com" --subject "Re: Meeting" --body "..."`

**GOOD:** Open Gmail in Playwright, compose and send via UI.

## Draft Emails

Mark unsent drafts clearly at top of entry.

**BAD:**
```
### 2026-03-18 13:52 - Electricity Inquiry

From: me@example.com | To: admin@company.com ...

Draft email body...
```

**GOOD:**
```
### 2026-03-18 13:52 - DRAFT Electricity Inquiry

**STATUS: DRAFT - NOT SENT**

From: me@example.com | To: admin@company.com ...

Draft email body...
```

## WhatsApp Message Format

Timestamp before person name, person in bold.

**BAD:**
```
Alice: Hi Bob, message here.
Bob replied: Ok no problem.
```

**GOOD:**
```
**13:44 Sender**: Message text here.

**15:11 Recipient**: Obrigado, irei mandar limpar de imediato o apartamento
> Thanks, I will have the apartment cleaned immediately
```

## WhatsApp Section Heading

Include date, platform, and topic. Add time range in body.

**BAD:**
```
### 2026-03-17 - WhatsApp Messages
```

**GOOD:**
```
### 2026-03-17 WhatsApp - Payment Confirmation

Platform: WhatsApp | Participants: [Your Name], [Contact Name]
```

## WhatsApp Key Outcomes

End WhatsApp sections with structured summary of decisions and next steps.

**BAD:**
```
**19:56 Sender**: No problem, tomorrow is fine.

---
```

**GOOD:**
```
**19:56 Sender**: No problem, tomorrow is fine.

**Key outcomes:**
- Contact confirmed: free to choose any provider
- Reference code pending confirmation tomorrow
- Key detail documented

---
```

## Log Entry Format

Bold timestamp, main topic on same line. Sub-items indented with Decision/Action/Attachment.

**BAD:**
```
- Discussed timeline on March 17. Decided to move milestone. Need to send chart.
```

**GOOD:**
```
- **2026-03-17 14:30** - Discussed Q2 timeline adjustments
  - Decision: Move milestone 2 to April 15
  - Action: Send updated Gantt chart by Friday
  - Attachment: [Q2_Timeline.pdf](Attachments/2026-03-17_14-30_Q2Timeline/Q2_Timeline.pdf)
  - [Email](#2026-03-17-1430---q2-timeline-discussion)
```

## Log Anchors

Every log entry links to its History section via Markdown anchor.

**BAD:**
```
- **2026-03-17 14:30** - Discussed timeline
```

**GOOD:**
```
- **2026-03-17 14:30** - Discussed timeline
  - [Email](#2026-03-17-1430---q2-timeline-discussion)
```

For WhatsApp:
```
  - [WhatsApp](#2026-03-17-whatsapp---payment-confirmation)
```

## History Heading Format

Email: `### YYYY-MM-DD HH:MM - Summary`
WhatsApp: `### YYYY-MM-DD WhatsApp - Topic`

**BAD:**
```
### Email from John about timeline
### WhatsApp chat 17 March
```

**GOOD:**
```
### 2026-03-17 14:30 - Q2 Timeline Discussion
### 2026-03-17 WhatsApp - Payment Confirmation
```

## Todo Format

Timestamp, item, optional deadline, status with action type.

**BAD:**
```
- [ ] Reply to John
- [ ] Pay invoice (due March 20)
```

**GOOD:**
```
- **2026-03-15 09:15** - Reply to John with proposal - Deadline: 2026-03-20, Status: TODO:REPLY
- **2026-03-17 11:03** - Pay deposit to landlord - Status: DONE
```

## Attachment Folder Format

`Attachments/YYYY-MM-DD_HH-MM_[Topic]/`

**BAD:**
```
Attachments/contract.pdf
Attachments/March2026/contract.pdf
```

**GOOD:**
```
Attachments/2026-03-16_16-50_RentalContract/CT_Arrendamento.pdf
```

## Image Cleanup

After downloading email attachments, review each image. Delete email template garbage.

Delete: signature icons, company logos, social media icons, spacer images, horizontal lines.
Keep: real attachments (documents, photos, screenshots).

Maintain per-conversation Ignore Files pattern list for recurring garbage.

## URL Format

All URLs as clickable Markdown links with descriptive title.

**BAD:**
```
Check https://www.company.com for details.
See provider.com/services/energy/
```

**GOOD:**
```
Check [Company Name](https://www.company.com) for details.
See [Provider Energy](https://provider.com/services/energy/)
```
