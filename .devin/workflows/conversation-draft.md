---
description: Draft emails, WhatsApp messages, or other text AS the user
---

# Draft Conversation Workflow

Draft outbound text AS the user - matching their voice while maintaining precision.

**Goal**: Draft ready for user review that sounds like them and contains zero precision gaps

**Why**: Three rule layers must compose correctly. Missing any layer produces either generic text (missing humanizing) or imprecise text (missing APAPALAN Communication rules).

Scope: Drafts only. Use `/conversation-start` to create, `/conversation-update` to append.

## Required Skills

- @skills:write-documents for `CONVERSATION_HUMANIZING_RULES.md`, `CONVERSATION_RULES.md`, `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`

## MUST-NOT-FORGET

- Read `CONVERSATION_HUMANIZING_RULES.md` Anti-Pattern Index before finalizing
- Read `APAPALAN_RULES.md` Communication (CM) section
- AP-CM-01, AP-CM-02, AP-CM-03 apply to every draft in every language
- Full natural grammar: "I", "the", "a" preserved (CV-HM-07)
- Never invent greetings/closings - use user's habitual forms (CV-HM-06)
- Structural sections (Log, Todos, Status) = zero humanizing (CV-HM-01)
- If `CONVERSATION_[COUNTERPARTY].md` exists: ALWAYS write draft there, never chat only. Chat output is a SUMMARY, not the draft. (GLOB-FL-0036)
- If no conversation file exists: output draft in chat. Inform user about `/conversation-start` for future tracking.

## Rule Layers (Priority Order)

Three layers compose every draft. Higher priority wins on conflict:

```
Layer 1 - Minimal Explicit Consistent Terminology (MECT) + APAPALAN Communication (precision, clarity)
├─ MECT baseline: explicit terminology, deliberate redundancy for concept matching
├─ AP-CM-01: Accountable commitments
├─ AP-CM-02: Labeled questions/requests
└─ AP-CM-03: Time precision

Layer 2 - CONVERSATION_RULES.md (format)
└─ CV-EM-*, CV-WA-*, CV-DT-*, CV-TR-*

Layer 3 - CONVERSATION_HUMANIZING_RULES.md (voice)
└─ CV-HM-01 through CV-HM-07
```

**Conflict resolution**: Precision (Layer 1) always wins. Humanizing (Layer 3) never weakens precision or clarity.

**AP-BR-02 exception**: "Sacrifice grammar for brevity" applies to agent documents, NEVER to user-voice drafts. Keep full natural grammar (CV-HM-07).

## Trigger

- `/conversation-draft` - User wants a draft email or message
- `/conversation-draft [counterparty]` - With explicit target
- Implicit: User asks to "draft", "write", "reply" in conversation context

# EXECUTION

## Step 1: Detect Conversation File

Locate `CONVERSATION_[COUNTERPARTY].md`:

1. **Counterparty specified** (trigger or chat context): Search session/project folders for `CONVERSATION_[COUNTERPARTY].md`
2. **Not specified**: Infer from chat context (recipient name, email address, open files). Search for matching `CONVERSATION_*.md`
3. **Multiple candidates**: Choose most likely match from context, state choice to user
4. **Not found**: Note absence. Skip Steps 2 and 4 (file-write). Draft will be output in chat only.

## Step 2: Read Context

Skip if no conversation file found in Step 1.

1. Read target `CONVERSATION_[COUNTERPARTY].md`:
   - Humanizing Settings, Translation Settings
   - Last 3-5 History entries (voice calibration)
   - Status and open Todos (content)
2. Read `APAPALAN_RULES.md` Communication (CM) section
3. Read `CONVERSATION_HUMANIZING_RULES.md` Anti-Pattern Index

## Step 3: Extract Writing Profile

Use Humanizing Settings if populated. Otherwise extract from History:
- Greeting/closing forms (per context)
- Sentence length pattern (burstiness)
- Discourse markers and frequency
- Register (formal/informal, varies by recipient?)
- Spelling variants

## Step 4: Compose Draft

1. **Layer 1** - Write content per MECT + APAPALAN CM rules
2. **Layer 2** - Apply format per `CONVERSATION_RULES.md` (headers, datetime, translation)
3. **Layer 3** - Apply voice per `CONVERSATION_HUMANIZING_RULES.md` (CV-HM-01 through CV-HM-07)

## Step 5: Write Draft

**If conversation file exists** (found in Step 1):

1. Add draft to **History** section at the top (newest first) with heading: `### YYYY-MM-DD HH:MM - [Topic] **STATUS: DRAFT - NOT SENT**`
2. Add **Log** entry linking to the History section
3. Update **Todos** if the draft resolves or creates action items
4. Add any new attachments to **Links**
5. When user confirms sent, remove `**STATUS: DRAFT - NOT SENT**` from heading

**If no conversation file**: Output full draft in chat. Add note: `No CONVERSATION_[COUNTERPARTY].md found. Run /conversation-start to enable tracking.`

## Step 6: Verify

Scan draft against Anti-Pattern Index in `CONVERSATION_HUMANIZING_RULES.md`. Fix all violations.

## Quality Gate

- [ ] AP-CM-01, AP-CM-02, AP-CM-03 satisfied
- [ ] Anti-Pattern Index: zero violations
- [ ] If conversation file exists: draft written to History section with `**STATUS: DRAFT - NOT SENT**` (GLOB-FL-0036)
- [ ] If no conversation file: draft output in chat with `/conversation-start` note

## Output

`Draft ready: [type] to [counterparty] - [subject/topic]`
