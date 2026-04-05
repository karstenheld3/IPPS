---
description: Create or extend a CONVERSATION.md file from chat context
---

# Start Conversation Workflow

Create a new CONVERSATION.md or extend an existing one by extracting conversation partner data and communication history from the current chat.

**Goal**: Populated CONVERSATION.md with contacts, context, log entries, and full history

**Why**: Manual creation of conversation files is tedious and error-prone. This workflow extracts all data from the chat context and structures it according to `CONVERSATION_TEMPLATE.md`.

Scope: Creates conversation files only. Use `/transcribe` for PDF attachments, Playwright Gmail UI for sending emails.

## Required Skills

- @skills:write-documents for `CONVERSATION_TEMPLATE.md` and `CONVERSATION_RULES.md`

## MUST-NOT-FORGET

- Read `CONVERSATION_RULES.md` before creating any conversation file
- Read `CONVERSATION_TEMPLATE.md` before creating any conversation file
- Native characters mandatory for non-English text (e.g., ä, ö, ü, ß for German)
- Non-English/German text MUST have English translation in quote block
- DATETIME FORMAT: `YYYY-MM-DD HH:MM` everywhere
- NEVER use gogcli to send emails - Playwright Gmail UI only
- History section: newest on top (reverse chronological)
- All URLs as clickable Markdown links

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md in session folder

**PROJECT-MODE**: NOTES.md, PROBLEMS.md in project folder

## Trigger

- `/start-conversation` - User wants to track a new or ongoing conversation
- `/start-conversation [person/company]` - With explicit conversation partner

# EXECUTION

## Step 1: Detect Mode

Determine where the conversation file will live.

**PROJECT-MODE** (persistent conversation tracking):
- Active session is `_!EmailConversations` or similar dedicated conversation project
- Or user explicitly requests project-level tracking
- Output path: `[PROJECT_FOLDER]/[SubfolderName]/CONVERSATION.md`
- Subfolder naming: `FirstnameLastname-Description/` (e.g., `JoaoEstevao-FaroLandlordAppartment/`)

**SESSION-MODE** (conversation as part of broader work):
- Active session is any other session (e.g., `_!EmigrationGermanyToPortugal`)
- Conversations live in **topic subfolders** within the session (e.g., `Faro-Wohnung/`)
- Output path: `[SESSION_FOLDER]/[TopicSubfolder]/CONVERSATION.md` or `[TOPIC_OR_PERSON]_CONVERSATION.md`
- If subfolder already exists, place file there. If not, ask user for subfolder name.

**Filename rules** (both modes):
- Single conversation in folder: use `CONVERSATION.md`
- Multiple conversations in folder: each file named `[TOPIC_OR_PERSON]_CONVERSATION.md`
- Prefix: short uppercase identifier for partner/provider (e.g., `FAGAR`, `MEO`, `GASCAN`)
- When adding a second conversation to a folder that has `CONVERSATION.md`, rename the existing file first (see Step 3)

**No Context Match**: Ask user to specify mode and target folder.

## Step 2: Scan Chat for Conversation Partner

Extract from previous messages in the current chat:

- **Person/Company name**
- **Email address(es)**
- **Phone number(s)**
- **Role/relationship** (e.g., landlord, provider, coach)
- **Address** (if mentioned)
- **Website** (if mentioned)
- **Reference numbers** (contract IDs, user numbers, NIF, etc.)
- **Language** used in communication

Present extracted data to user for confirmation before proceeding.

## Step 3: Check for Existing Conversation Files

List all `*CONVERSATION.md` files in the target folder.

**Case A - Same partner already tracked:**
- A file for the same conversation partner exists (matching TOPIC prefix or generic `CONVERSATION.md` for the same partner)
- Do NOT create a new file. Extend it: add new data to Contacts, Context, Log, and History
- Confirm with user before modifying

**Case B - Folder has one `CONVERSATION.md` (different partner):**
- The existing `CONVERSATION.md` tracks a different partner
- Rename existing file to `[EXISTING_TOPIC_OR_PERSON]_CONVERSATION.md` first
- Then create new file as `[NEW_TOPIC_OR_PERSON]_CONVERSATION.md`
- Confirm rename with user before executing

**Case C - Folder already has prefixed files (different partner):**
- One or more `[TOPIC_OR_PERSON]_CONVERSATION.md` files exist, none match new partner
- Create new file as `[NEW_TOPIC_OR_PERSON]_CONVERSATION.md`

**Case D - Empty folder or folder does not exist:**
- PROJECT-MODE: create subfolder if needed
- Create `CONVERSATION.md` (single conversation, no prefix needed)

Proceed to Step 4 for file creation.

## Step 4: Create Conversation File

1. Read `CONVERSATION_TEMPLATE.md` from @skills:write-documents
2. Read `CONVERSATION_RULES.md` from @skills:write-documents
3. Fill template sections:

**Contacts** (quick reference at top):
```
- **[Name]** - [email] | [phone or -]
- **Karsten Held** - karstenheld3@gmail.com | +351 924 378 589
```

**MUST-NOT-FORGET**:
- Copy from template
- Adapt translation rule to conversation language (e.g., "All Portuguese text" instead of generic)

**Ignore Files**:
- Start with default patterns from template
- Adjust per conversation partner if known

**Status**:
- Set to `ACTIVE`
- Add any reference numbers, contract IDs

**Todos and Deliverables**:
- Extract any pending actions from chat

**Links and shared documents**:
- Extract any URLs or documents mentioned

**Conversation Context / Persons Involved**:
- Full contact details for each person
- Role, timezone, communication preferences

**Topics**:
- Extract discussion topics from chat

**Log**:
- One entry per communication event (email, WhatsApp, form submission, call)
- Reverse chronological (newest first)
- Include Decision/Action/Attachment sub-items

**History**:
- Full text of each communication
- Reverse chronological (newest first)
- Email header format: `From: | To: | CC: | BCC: - | Subject: | Reply-To: - | Thread: | Message-ID:`
- Non-English/German text followed by English translation in quote block
- Entries separated by `---`

## Step 5: Populate from Chat Context

Scan the entire current chat for:

1. **Emails** (quoted text, forwarded messages, Gmail content)
   - Extract full headers and body
   - Add to History with proper formatting
   - Create Log entry for each email

2. **WhatsApp messages** (if present)
   - Format: `**HH:MM Person**: message`
   - Add translation quote blocks for non-English/German
   - End section with `**Key outcomes:**`

3. **Form submissions** (if present)
   - Document submitted data
   - Note which platform/URL

4. **Attachments mentioned**
   - Create `Attachments/YYYY-MM-DD_HH-MM_[Topic]/` structure entries
   - Link in Log and History

5. **Decisions and actions**
   - Extract to Log sub-items (Decision:, Action:, Attachment:)
   - Create Todo entries for pending items

# FINALIZATION

## Verification

After creating/updating the file:

1. All contacts have email addresses
2. Log entries link to History sections via anchors
3. History in reverse chronological order
4. All non-English/German text has English translation
5. Native special characters used (no ASCII substitutes)
6. All dates in `YYYY-MM-DD HH:MM` format
7. All URLs are clickable Markdown links
8. Ignore Files section populated

## Quality Gate

- [ ] `CONVERSATION_RULES.md` read before creating file
- [ ] `CONVERSATION_TEMPLATE.md` read before creating file
- [ ] All contacts have email addresses
- [ ] Native special characters used (no ASCII substitutes)
- [ ] Non-English/German text has English translation in quote block
- [ ] All dates in `YYYY-MM-DD HH:MM` format
- [ ] History in reverse chronological order
- [ ] Log entries link to History sections via anchors

## Output

**New (single in folder)**: `Created: [FOLDER]/CONVERSATION.md`

**New (multiple in folder)**: `Renamed: CONVERSATION.md -> [EXISTING_TOPIC_OR_PERSON]_CONVERSATION.md | Created: [NEW_TOPIC_OR_PERSON]_CONVERSATION.md`

**Extended**: `Updated: [FOLDER]/[TOPIC_OR_PERSON]_CONVERSATION.md - added [data]`
