# SOCAS Communication Rules

Field rules of Signs of Confusion and Sloppiness (SOCAS) for communication: chat, email, orders, requests and the written trace of calls. Run together with `SOCAS_RULES.md` (general rules, application rules, reporting rules, priority model and rule format). Origin: `_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md [SOCAS-IN01]` (Karsten Held, 2026). Discarded, merged and deferred candidates: `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

**Content types**: chat, email, short memos, status messages, requests, orders, meeting notes, conversation entries, the written trace of calls (summary, confirmation, call notes), and prompts (`_PROMPTS_*`) and other one-time orders written for agents. Reusable procedures for agents (workflows, SOPs) use `SOCAS_WRITING_RULES.md`. Spoken tone and read-back cannot be checked from text [ASSUMED].

APAPALAN communication rules prescribe the form of a message (APAPL-CM-02 and CM-03 own questions, dates and times; APAPL-CM-01 is the fix cited by SOCAS-CM-01). SOCAS-CM rules detect what those rules do not: the content is wrong, empty of substance or hostile even when the form is right. Evidence comes mostly from healthcare handoffs and lab experiments; no study of business email quality scoring was found.

## Rule Index

Communication (CM)
- SOCAS-CM-01: Who Does What by When Unclear
- SOCAS-CM-02: Lookups Needed to Act
- SOCAS-CM-03: Unbacked Basis for Action
- SOCAS-CM-04: Underspecified or Conflicting Order
- SOCAS-CM-06: Tone Depends on Unstated Intent
- SOCAS-CM-07: Rude or Hostile Language
- SOCAS-CM-08: Pressure Without Reason or Inverted Priorities
- SOCAS-CM-10: Omitted or Replaced Information

## Table of Contents

- [Focus Questions](#focus-questions)
- [Rank Order](#rank-order)
- [Actionability](#actionability)
- [Tone and Pressure](#tone-and-pressure)
- [Completeness](#completeness)

## Focus Questions

Questions a reader asks of a message and the rules that answer them:
- Is it actionable? SOCAS-CM-01, SOCAS-CM-04
- Is it self-contained? SOCAS-CM-02
- Does it require much lookup or verification effort? SOCAS-CM-02 (lookups), SOCAS-CM-03 (verification)
- Does it contradict itself? SOCAS-GN-01 (message forms)
- Does it contain underspecified requests or actions? SOCAS-CM-04, SOCAS-CM-01
- Does it contain misleading or vague interpretations? SOCAS-GN-03 (ambiguous terms), SOCAS-GN-06 (assumption as fact), SOCAS-CM-06 (meaning depends on unstated tone)
- Does it contain manipulative or aggressive language? SOCAS-GN-08, SOCAS-CM-07, SOCAS-CM-08
- Is the tone appropriate? SOCAS-CM-06, SOCAS-CM-07; appropriateness that depends on relationship and culture has no rule (discarded until researched)
- Does it omit or replace relevant information? SOCAS-CM-10
- Does it invert priorities? SOCAS-CM-08

## Rank Order

Run after the general rules (SOCAS-AP-12). Within this file:
- P1: SOCAS-CM-01, CM-04, CM-06, CM-07, CM-08, CM-02
- P2: SOCAS-CM-03, CM-10

## Actionability

### SOCAS-CM-01: Who Does What by When Unclear

- The reader must guess the actor, the outcome or the time of a request or decision
- **Applies to**: messages with a request, decision or commitment, and documents that recommend actions or decisions (SOCAS-AP-03); not purely informational content
- **Test**: Can the reader say who must do what by when?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A-B ([plans stating when, where and how](https://kops.uni-konstanz.de/entities/publication/2e749bfb-8533-437c-8203-7e788c910c5f): d = 0.65 over 94 tests)
- **Web**: no
- **Overlap**: REF - fix by APAPL-CM-01, APAPL-CM-02, APAPL-ST-02

### SOCAS-CM-02: Lookups Needed to Act

- "See attachment", "as discussed", "per the thread", a bare link, or a reference to a previous message carries the information the reader needs
- **Applies to**: messages with a request or decision
- **Test**: Must the reader open another source to understand or act? Count the lookups
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([integrated vs separated sources](https://doi.org/10.1016/j.learninstruc.2006.10.001): d = 0.85 over 50 studies; transfer from instruction to messages by analogy)
- **Web**: no
- **Overlap**: REF - fix by APAPL-ST-03, APAPL-ST-04

### SOCAS-CM-03: Unbacked Basis for Action

- The reader must trust a claim before acting: figures, names, claimed approvals ("legal approved this"), claimed earlier decisions
- **Applies to**: messages that ask the reader to act
- **Test**: Does acting on the message require trusting a claim the message does not back?
- **Priority**: P2 | Cost: medium, judgment of what needs backing | Value: medium, evidence C
- **Web**: no (verification itself: `/fact-check`)
- **Overlap**: none

### SOCAS-CM-04: Underspecified or Conflicting Order

- The request leaves open a choice between valid but inconsistent results (which file, which version, which format, when done); two requirements in one order conflict. Core case: orders written for agents
- **Applies to**: one-time orders and work requests, especially prompts written for agents; reusable procedures (workflows, SOPs) use SOCAS-WR-12
- **Test**: Does the order leave valid but inconsistent results open, or do two of its requirements conflict?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([unstated requirements dropped agent accuracy 22.6% on average, up to 93.1%](https://aclanthology.org/2026.findings-acl.441/); Association for Computational Linguistics (ACL) Findings 2026)
- **Web**: no
- **Overlap**: REF - fix by APAPL-ST-04

## Tone and Pressure

### SOCAS-CM-06: Tone Depends on Unstated Intent

- Irony, sarcasm, humor or understatement in a text-only channel, with the intended tone not stated in words
- **Applies to**: all messages in text-only channels
- **Test**: Does the meaning depend on a tone the words do not state?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([email senders predicted 78% tone accuracy, readers reached 56%](https://doi.org/10.1037/0022-3514.89.6.925); 5 experiments)
- **Web**: no
- **Overlap**: none (MECT-WC-10 covers idioms, not irony)

### SOCAS-CM-07: Rude or Hostile Language

- Insult, threat, contempt, profanity, identity attack. Judge the sentence, not the person. Expect false positives on quoted speech and negations
- **Applies to**: all messages
- **Test**: Does a quoted phrase insult, threaten or show contempt?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([mild rudeness lowered performance of 24 randomized medical teams](https://pubmed.ncbi.nlm.nih.gov/26260718/) via less information sharing)
- **Web**: no
- **Overlap**: none

### SOCAS-CM-08: Pressure Without Reason or Inverted Priorities

- Deadline, escalation threat or urgency with no stated reason; deadline or small item emphasized while the larger consequence is absent or last; the main ask comes after background or secondary items. Concrete message form of SOCAS-GN-08
- **Applies to**: messages with a deadline, escalation or urgency word, or with a request
- **Test**: Is pressure applied without a stated reason, or does the order of the message hide the main ask or the larger consequence?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([spurious urgency: 31.3% vs 13.3% chose the worse task](https://academic.oup.com/jcr/article-abstract/45/3/673/4847790), 5 experiments; [reminding people of the payoffs at the moment of choice reduced the effect](https://hub.jhu.edu/2018/05/31/meeting-deadlines-time-management-behaviors/))
- **Web**: no (truth of the deadline: owner or web)
- **Overlap**: REF - ask-first order fixed by APAPL-ST-01

## Completeness

### SOCAS-CM-10: Omitted or Replaced Information

- What the reader needs to decide or act is missing (what, who, by when, impact, risks, what is unknown); a question answered with a different, easier answer
- **Applies to**: messages that ask for a decision, answer a question or hand over work
- **Test**: Is anything the reader needs to decide missing, or is the question answered with a different one?
- **Priority**: P2 | Cost: medium, element list per message type | Value: medium, evidence C ([I-PASS handoff elements](https://www.nejm.org/doi/full/10.1056/NEJMsa1405556) (Illness severity, Patient summary, Action list, Situation awareness, Synthesis by receiver); [US Centers for Disease Control and Prevention (CDC) Clear Communication Index](https://www.cdc.gov/ccindex/tool/description-examples-parta.html) item on what is not known)
- **Web**: no
- **Overlap**: none

