# SOCAS Writing Rules

Field rules of Signs of Confusion and Sloppiness (SOCAS) for writing and publications. Run together with `SOCAS_RULES.md` (general rules, application rules, reporting rules, priority model and rule format). Origin: `_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md [SOCAS-IN01]` (Karsten Held, 2026). Discarded, merged and deferred candidates: `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

**Content types**: articles, reports, ebooks, whitepapers, INFO documents, news, blog posts, slide decks, websites, offers, proposals, newsletters, marketing and sales text, user documentation, review outputs (`_CRITIQUE`, `_FACT-CHECK`), tracking files (NOTES, PROBLEMS, PROGRESS, FAILS), and non-code normative documents (policies, standard operating procedures (SOPs), process descriptions, standards, rule files, guides, templates, workflows, `SKILL.md` files). Code specifications and technical READMEs use `SOCAS_CODING_RULES.md`; prompts and other one-time orders for agents use `SOCAS_COMMUNICATION_RULES.md`.

## Rule Index

Writing (WR)
- SOCAS-WR-01: Cited Source Missing or Changed
- SOCAS-WR-02: Specific Claim Without Source
- SOCAS-WR-03: Missing Date, Author, Version or Scope
- SOCAS-WR-04: Responsible Party and Interest Unclear
- SOCAS-WR-05: Undisclosed Commercial Interest
- SOCAS-WR-06: Pressure Tactics in Commercial Text
- SOCAS-WR-07: Unsubstantiated Commercial Claim
- SOCAS-WR-08: Outdated Content
- SOCAS-WR-09: Empty Structure
- SOCAS-WR-10: Vague Word Where a Measure Belongs
- SOCAS-WR-11: Requirement Quality in Normative Documents

## Table of Contents

- [Rank Order](#rank-order)
- [Sources and Provenance](#sources-and-provenance)
- [Commercial Intent and Persuasion](#commercial-intent-and-persuasion)
- [Currency, Structure and Precision](#currency-structure-and-precision)

## Rank Order

Run after the general rules (SOCAS-AP-11). Within this file:
- P1: SOCAS-WR-06, WR-01, WR-05, WR-07, WR-09, WR-10, WR-11, WR-02, WR-03
- P2: SOCAS-WR-04, WR-08

Content of any field that cites external sources also runs SOCAS-WR-01 (SOCAS-AP-03). Direct commercial messages run SOCAS-WR-05 to WR-07 with the communication file.

## Sources and Provenance

### SOCAS-WR-01: Cited Source Missing or Changed

- A cited source does not exist, or exists but says something different (other figure, date, scope or wording)
- A reference without enough data to find it (no author, year or venue) is searched by title; not found = `ERROR: not found`. A present digital object identifier (DOI) proves nothing: 64% of fabricated references with a DOI had a valid DOI pointing to an unrelated article
- **Applies to**: content that cites sources (links, named studies, "according to")
- **Test**: Does the opened source exist and say what the content claims at the cited location?
- **Priority**: P1 | Cost: medium, web within SOCAS-AP-09 budget | Value: high, evidence A ([LLM references: 18% to 55% fabricated](https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/); [64% of fabricated DOIs pointed to unrelated articles](https://pmc.ncbi.nlm.nih.gov/articles/PMC12658395/))
- **Web**: yes, max 5 sources
- **Overlap**: none

### SOCAS-WR-02: Specific Claim Without Source

- A sentence with a number, named party, date or money value gives no source for it
- **Applies to**: content that states facts with numbers, named parties, dates or money values
- **Test**: Does each specific factual claim name where it comes from?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([check-worthy sentences](https://ceur-ws.org/Vol-3677/paper4.pdf) contain more numbers and named entities)
- **Web**: no
- **Overlap**: none

### SOCAS-WR-03: Missing Date, Author, Version or Scope

- No date, no named author or owner, no version, no stated scope or coverage limits
- **Applies to**: documents shared beyond the author (stage working version or final version); not drafts. In a repository, version control records date and author; only version and scope are tested
- **Test**: Can the reader tell when, by whom and for what scope the content was written?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([AACODS checklist](https://fac.flinders.edu.au/dspace/api/core/bitstreams/e94a96eb-0334-4300-8880-c836d4d9a676/content) (Authority, Accuracy, Coverage, Objectivity, Date, Significance): no discernible date is "a strong concern")
- **Web**: no
- **Overlap**: none (APAPL-PR-01 governs date format, not presence)

### SOCAS-WR-04: Responsible Party and Interest Unclear

- Organizational or customer-facing content with no named responsible person or organization, only generic contacts (info@), or no way to tell the publisher's interest
- **Applies to**: organizational or customer-facing content (websites, offers, newsletters, customer policies); not articles by a named author, memos or internal specifications
- **Test**: Can the reader find who is responsible for this content and what their interest is?
- **Priority**: P2 | Cost: medium, 1 web lookup of the publisher | Value: medium, evidence B ([checking the source in other tabs beats close reading](https://journals.sagepub.com/doi/10.1177/016146811912101102)); the [Stanford credibility comments](https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf) show only that readers look at sponsor identity and company motive, not that the sign is valid
- **Web**: optional, 1 lookup
- **Overlap**: REF - contact format fixed by APAPL-PR-03

## Commercial Intent and Persuasion

### SOCAS-WR-05: Undisclosed Commercial Interest

- Selling while presenting as information, education or opinion; sponsor or funder not named; independence claim contradicted by a commercial relationship; call to action only after long emotional build-up; hidden or recurring costs revealed late; guilt-inducing decline options; author condemns competitors for tactics it uses itself; advertising formatted as editorial content; comparisons or rankings ordered by paid placement
- **Applies to**: content with a call to action, a vendor or sponsor as author, or product recommendations
- **Test**: Does content that presents itself as information, education or opinion lose its purpose when the final call to action is removed, or does it hide a commercial interest of the author? Openly commercial content (offer, product page, sales email) passes the first part
- **Priority**: P1 | Cost: medium, 1 web lookup when no sponsor is named | Value: high, evidence A ([Cochrane review](https://www.cochrane.org/evidence/MR000033_industry-sponsorship-and-research-outcome): sponsored studies reached favorable conclusions more often, relative risk (RR) 1.34)
- **Web**: optional, 1 lookup of author or publisher
- **Overlap**: none

### SOCAS-WR-06: Pressure Tactics in Commercial Text

- Artificial scarcity or deadline on non-scarce goods; countdown timers; unverifiable social proof ("thousands of customers"); testimonials without disclosed payment or connection; unsolicited "free" gift creating obligation; small ask (quiz, trial) escalating to a large ask; cancel harder than sign-up; fear appeal only the product solves; in-group vs out-group framing; purchase framed as moral duty or identity act ("join the movement")
- Concrete commercial form of SOCAS-GN-07 (SOCAS-AP-05: this rule takes precedence)
- **Applies to**: commercial or persuasive content (offers, sales text, marketing, fundraising)
- **Test**: Does the text push the reader with pressure, fear, invented scarcity or unverifiable social proof instead of evidence?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A-B ([US Federal Trade Commission (FTC) dark-pattern report](https://search.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf): dark patterns doubled sign-ups for a dubious service)
- **Web**: optional (whether the scarcity is real)
- **Overlap**: none

### SOCAS-WR-07: Unsubstantiated Commercial Claim

- Quality, environmental or performance claim without a named certificate, test report or standard the reader can open
- **Applies to**: content with quality, environmental or performance claims about a product or service
- **Test**: Does each marketing claim name evidence the reader can check?
- **Priority**: P1 | Cost: medium, 1 web lookup of the named scheme | Value: high, evidence B ([European Commission](https://environment.ec.europa.eu/topics/circular-economy-topics/green-claims_en): 53% of green claims vague, misleading or unfounded; 40% without supporting evidence)
- **Web**: optional, 1 lookup
- **Overlap**: none

## Currency, Structure and Precision

### SOCAS-WR-08: Outdated Content

- Outdated facts next to current ones; latest cited source much older than the content date; named product versions behind the current version; references to abandoned tools or sources
- **Applies to**: content that names products, versions, prices, laws or sources with a date
- **Test**: Is any fact, version or source outdated relative to the content date?
- **Priority**: P2 | Cost: medium, 1 date or version lookup | Value: medium, evidence C ([reference rot](https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/): 38% of 2013 webpages gone by 2023)
- **Web**: optional, 1 lookup
- **Overlap**: none

### SOCAS-WR-09: Empty Structure

- Headings label topics instead of stating findings; main point buried at the end or missing; summaries describe what a section covers, not what it found; no stated purpose
- **Applies to**: documents that report or argue (articles, reports, INFO documents, slide decks, proposals); not reference-type documents (API reference, rule index, glossary), where topic headings are the correct form
- **Test**: Can the reader get the main point from the headings and the first paragraph alone?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([assertion-evidence slides](https://www.ijee.ie/articles/Vol29-6/23_ijee2791ns.pdf): better comprehension and delayed recall, 110 students)
- **Web**: no
- **Overlap**: REF - fix by MECT-HS-01, APAPL-ST-01

### SOCAS-WR-10: Vague Word Where a Measure Belongs

- Unverifiable adjectives where the claim needs a number, unit, scope or condition: flexible, easy, sufficient, robust, fast, user-friendly, appropriate, "-ly" adverbs; vague claim terms: natural, sustainable, eco
- **Applies to**: claims about quality, performance, effort or requirements
- **Test**: Does a claim that needs a measure carry only a vague qualifier?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C ([NASA](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) and [IBM](https://www.ibm.com/docs/en/erqa?topic=assistant-guidelines-good-requirements) requirement lists; [EU study](https://op.europa.eu/en/publication-detail/-/publication/f7c4cb8b-f877-11ee-a251-01aa75ed71a1/language-en): 54 of 150 environmental claims unclear)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-07; SOCAS adds the term list

### SOCAS-WR-11: Requirement Quality in Normative Documents

- Required and optional not distinguishable; escape clauses ("where possible", "as appropriate", "etc.", "and/or", "but not limited to"); one statement holding several obligations; no actor; edge case undefined; no escalation or exception path in a process description; steps in an order that cannot run (a step needs the result of a later step)
- **Applies to**: normative documents: policies, SOPs, process descriptions, standards, rule files, guides, templates, workflows, `SKILL.md` files
- **Test**: Can the reader tell what is required, what is optional, who must act and what happens in the edge case, and can the steps run in the stated order?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C (Internet Engineering Task Force key words [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html), IBM, NASA, [Easy Approach to Requirements Syntax (EARS) case study](https://doi.org/10.1109/re.2009.9))
- **Web**: no
- **Overlap**: REF - obligation words fixed by MECT-VO-04, missing actor fixed by MECT-VO-01

