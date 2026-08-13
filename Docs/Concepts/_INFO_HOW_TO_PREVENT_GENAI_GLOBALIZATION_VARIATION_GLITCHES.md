# INFO: How to Prevent GenAI Globalization Variation Glitches

**Doc ID**: LITRLPRVNT-IN01
**Goal**: Explain why GenAI corrupts literal values, what categories of corruption exist, and how to prevent them using the [LITERAL] marker system
**Timeline**: Created 2026-08-06

## Summary

- GenAI treats all text as semantic (predictable, improvable) but addresses, IBANs, tax IDs, and reference numbers are lexical (every character matters). This mismatch causes silent corruption. [VERIFIED]
- 8 corruption categories identified: Unicode normalization, punctuation drift, abbreviation/expansion, sub-premise loss, identifier transposition, script mixing, postal code reformatting, hallucinated gap-filling [VERIFIED]
- LLM tokenizers shred high-entropy strings (IBANs, UUIDs (Universally Unique Identifiers)) into 20+ subword tokens. Digit-swap error rate: ~24% per run on raw identifiers, drops to ~3% with aliases [VERIFIED]
- Sub-premise loss (floor/unit/door number dropped) is the #1 cause of undeliverable mail in Indian, Portuguese, Japanese, and UK addresses [VERIFIED]
- The `[LITERAL]` in-place marker system prevents corruption by signaling "copy character-for-character, do not reformat". Defined in `core-conventions.md`, enforced via AP-PR-13 and CV-LT-01 [VERIFIED]
- Validation APIs exist (Qiniso for identifiers, Shirabe for Japanese addresses, India Post PIN lookup) but are complementary - the marker system is the first line of defense [VERIFIED]

## Table of Contents

1. [Why GenAI Corrupts Literal Values](#1-why-genai-corrupts-literal-values)
2. [What Goes Wrong: 8 Corruption Categories](#2-what-goes-wrong-8-corruption-categories)
3. [Real-World Examples by Region](#3-real-world-examples-by-region)
4. [How to Prevent It: The LITERAL Marker System](#4-how-to-prevent-it-the-literal-marker-system)
5. [Next Steps](#5-next-steps)
6. [Sources](#6-sources)
7. [Document History](#7-document-history)

## 1. Why GenAI Corrupts Literal Values

### 1.1 The Semantic vs. Lexical Mismatch

Language models are trained to predict the next token from a learned distribution. Their core competence is interpolation over patterns seen before. This works for natural language but fails for literal values where the meaning IS the exact character sequence.

**Semantic values** (natural language): "The apartment is on the first floor, right side" - many valid phrasings, meaning preserved across variations.

**Lexical values** (identifiers): `Av. 5 de Outubro, 53, 1.o Dto.` - every character matters. "1.o Dto." cannot become "1-D" or "1.º Direito" without breaking mail delivery.

The model cannot distinguish these two categories unless explicitly told. Without a signal, it applies the same "improve and normalize" behavior to both.

### 1.2 How BPE Tokenization Destroys Identifier Fidelity

BPE (Byte-Pair Encoding) tokenizers shred high-entropy strings into many short subword tokens. According to a [published benchmark](https://tianpan.co/blog/2026-05-31-the-account-number-your-llm-could-not-actually-copy), one UUID requires ~24 tokens versus ~1.25 tokens per English word. The model must reproduce a 24-token sequence verbatim with no semantic anchor to verify against.

When two similar identifiers share a context window, the conditional probability of the correct continuation collapses. The same benchmark measured ~48 errors per 200-item aggregation task with raw UUIDs, dropping to ~6 errors when remapped to integer aliases.

**Critical asymmetry**: The model corrupts the characters with the highest local entropy (the random-looking middle). The corrupted identifier often still parses, still passes regex, still routes to a real record. No loud `not found` - a quiet wrong-customer.

### 1.3 Why "Looks Right" Is the Worst Failure Mode

Address validation firm [Melissa.com](https://blog.melissa.com/en-au/global-intelligence/ai-address-validation) confirms: "Formatting an address correctly and confirming that address exists are two different problems. A model trained on text patterns has learned what addresses tend to look like, not which specific combinations are real, current, and deliverable."

The model fills gaps with plausible-but-wrong values. It invents house numbers, "corrects" postal codes to nearby valid ones, and never signals uncertainty. This is not hallucination in the traditional sense - it is pattern completion applied where pattern completion is harmful.

## 2. What Goes Wrong: 8 Corruption Categories

### 2.1 Unicode Normalization

The model substitutes visually similar but technically different characters.

```
ORIGINAL: 1.o Dto.     (ASCII letter o)
CORRUPTED: 1.º Dto.    (Unicode U+00BA masculine ordinal indicator)

ORIGINAL: Av.           (ASCII period)
CORRUPTED: Av.ª         (Unicode U+00AA feminine ordinal indicator appended)

ORIGINAL: "straight"    (U+0022)
CORRUPTED: "curly"      (U+201C / U+201D)
```

Documented in Claude Code issues [#26141](https://github.com/anthropics/claude-code/issues/26141) and [#38765](https://github.com/anthropics/claude-code/issues/38765): the Edit tool silently downgrades Unicode to ASCII or vice versa, creating mixed encoding in the same file.

CJK (Chinese-Japanese-Korean)-specific: half-width katakana `ﾄｳｷｮｳ` → full-width `トウキョウ`. Both represent "Tokyo" but database lookups may fail on mismatch.

### 2.2 Punctuation Drift

The model changes separators while preserving what it considers "the same information".

```
IBAN:    DE64120300001207676238   → DE 64 1203 0000 1207 6762 38 (spaces)
Address: 53, 1.o Dto.            → 53 - 1.o Dto. (comma → dash)
Phone:   +351-966-080-541        → +351 966 080 541 (dashes → spaces)
Slash:   2/1 (Indian plot)       → 2-1 or 2 by 1
```

The ACL paper ["Do Not Change Me"](https://aclanthology.org/2025.mtsummit-1.19.pdf) tested 36,000 sentences across 9 entity types (IBANs, emails, URLs, phone numbers, ISBNs, IPs) and found that even state-of-the-art NMT (Neural Machine Translation) models fail to transfer these entities without modification.

### 2.3 Abbreviation and Expansion

The model "helpfully" shortens or expands abbreviations.

```
Dto.      → D          (abbreviation lost context: "D" is not deliverable)
Dto.      → Direito    (expansion changes the literal form)
Apt.      → Apartment  (expansion)
S/O       → Son of     (Indian address relational marker expanded)
Esq.      → E          (Portuguese "left side" abbreviated to single letter)
MG Road   → Mahatma Gandhi Road  (expanded, may not match records)
```

### 2.4 Sub-Premise Loss

Floor, unit, door, wing, and building information is dropped or merged. This is the #1 cause of undeliverable addresses globally.

```
ORIGINAL: Flat 453, Tagore Road Hostel, Tagore Road, 118923
LOST:     Tagore Road, 118923  (flat + building name gone)

ORIGINAL: Av. 5 de Outubro, 53, 1.o Dto.
LOST:     Av. 5 de Outubro 53-D  (floor "1.o" gone, "Dto." → "D")

ORIGINAL: 港区六本木6-10-1 六本木ヒルズ森タワー 5階
LOST:     港区六本木6-10-1  (building name + floor stripped)

ORIGINAL: Flat 4B, Wing C, 3rd Floor, Prestige Residency
LOST:     Prestige Residency, 4B  (wing + floor gone)
```

[Google Maps Platform India documentation](https://developers.google.com/maps/architecture/india-address-feedback) confirms: Indian addresses with "Flat No.", "Door No.", building wings are vital for last-mile delivery but often unstructured and systematically lost by automated systems.

### 2.5 Identifier Transposition

The model swaps digits in similar identifiers sharing a prefix. The corrupted ID still parses and routes to a different real record.

```
ORIGINAL: acct_7H9j3     → acct_7H9j2  (one digit, wrong customer gets refund)
ORIGINAL: NIF 123456789   → NIF 123459789  (valid NIF, wrong person)
ORIGINAL: Case 2026/300.10.002/1073  → 2026/300.10.002/1037  (transposed last digits)
```

Per the [Tian Pan analysis](https://tianpan.co/blog/2026-05-31-the-account-number-your-llm-could-not-actually-copy): "The trace looks clean: a search call returned the right record, a summarize call produced the right summary, a refund call ran without error. Every step succeeded. The wrong customer got the money."

### 2.6 Script and Romanization Mixing

The model switches between writing systems or transliterates without being asked.

```
ORIGINAL: 東京都港区六本木6丁目10番1号
MIXED:    Minato-ku, Roppongi 6-10-1, Tokyo  (kanji → romaji)

ORIGINAL: मकान नं. 21, गांधी नगर, भोपाल
MIXED:    Makan No. 21, Gandhi Nagar, Bhopal  (Devanagari → Latin)

ORIGINAL: شارع الملك فهد
MIXED:    King Fahd Road  (Arabic → English, loses right-to-left layout)
```

[Japan Digital Agency ABR geocoder](https://github.com/digital-go-jp/abr-geocoder) documents 4 orthographic normalization axes: kanji ↔ Arabic numerals, full ↔ half-width, old ↔ new character forms, connector variations (`ノ`, `之`, `の`). Each axis multiplies the number of valid surface forms.

### 2.7 Postal Code Reformatting

Country-specific postal code formats are normalized to a "generic" form.

```
Portugal: 8000-077   → 8000077     (hyphen removed)
UK:       SW1A 1AA   → SW1A1AA     (space removed - breaks Royal Mail sort)
Japan:    〒100-0000  → 100-0000    (〒 symbol removed)
          〒100-0000  → 〒 100-0000  (space inserted after 〒)
India:    462 001     → 462001      (space removed - both forms exist)
Canada:   K1A 0B1     → K1A-0B1    (space → dash)
```

### 2.8 "Looks Right" Hallucination

The model fills gaps with plausible-but-wrong values rather than signaling uncertainty.

```
INPUT:  Rua da Liberdade, Faro
OUTPUT: Rua da Liberdade, 1, 8000-001 Faro  (house number invented, postal code guessed)

INPUT:  港区六本木
OUTPUT: 港区六本木6-10-1  (block/house number fabricated from training data)
```

[Shirabe Address API](https://shirabe.dev/docs/address-normalize) explicitly warns: "LLMs hallucinate Japanese addresses - inventing house numbers that do not exist, 'correcting' town names into plausible-but-wrong alternatives, and silently reconciling ZIP/address mismatches." Address normalization is a dictionary-lookup problem, not a generation problem.

## 3. Real-World Examples by Region

### 3.1 Portugal / Southern Europe

**Address structure**: `Street, Number, Floor.Unit, PostalCode City`

```
AUTHORITATIVE: Av. 5 de Outubro, 53, 1.o Dto., 8000-077 Faro
GENAI ATTEMPT 1: Av. 5 de Outubro 53-D, 8000-077 Faro        (sub-premise lost)
GENAI ATTEMPT 2: Av.ª 5 de Outubro, 53 - 1.º Dto., Faro      (Unicode + postal code dropped)
GENAI ATTEMPT 3: Avenida 5 de Outubro, n.º 53, 1.º Direito   (expanded, postal code gone)
```

"1.o Dto." (primeiro andar direito = first floor right) is mandatory. The mailbox shows "1-D". Without the floor indicator, post is returned to sender.

### 3.2 India

**Address structure**: Highly variable. May include "S/O" (Son of), "D/O" (Daughter of), landmarks ("near old temple"), and plot notations ("2/1").

```
AUTHORITATIVE: Flat No. 32, Uttara Towers, MG Road, Guwahati 781029
GENAI ATTEMPT: MG Road, Guwahati, Assam 781029  (flat + building dropped)

AUTHORITATIVE: H.No. 2/1, S/O Rajesh Kumar, Gandhi Nagar, Bhopal 462001
GENAI ATTEMPT: 2-1, Gandhi Nagar, Bhopal 462001  (slash → dash, S/O dropped, H.No. dropped)
```

"2/1" and "2-1" route to different locations. "S/O Rajesh Kumar" may be required for delivery in residential areas without named streets.

### 3.3 Japan

**Address structure**: Large-to-small (Prefecture → City → District → Block → Building → Floor). Kanji/Arabic numeral mixing. Multiple valid surface forms per address.

```
AUTHORITATIVE: 東京都港区六本木6丁目10番1号 六本木ヒルズ森タワー 5階
GENAI ATTEMPT 1: 港区六本木6-10-1  (prefecture + building + floor stripped)
GENAI ATTEMPT 2: Roppongi 6-10-1, Minato, Tokyo  (script switched to romaji)
GENAI ATTEMPT 3: 東京都港区六本木六丁目１０番１号  (half-width → full-width numerals)
```

All three representations are "semantically equivalent" but may fail database lookups, postal sorting, or form validation that expects the exact registered form.

### 3.4 United Kingdom

**Address structure**: Flat/Unit, Building, Street, City, Postcode. Postcode format is critical: `SW1A 1AA` (outward code + space + inward code).

```
AUTHORITATIVE: Flat 3, 27 Crescent Road, London SW1A 1AA
GENAI ATTEMPT: 27 Crescent Road, London SW1A1AA  (flat dropped, postcode space removed)
```

Royal Mail sorting machines require the space in the postcode. Flat number omission means the letter reaches the building but not the recipient.

### 3.5 Financial Identifiers (Global)

```
IBAN:     DE89370400440532013000  → DE89 3704 0044 0532 0130 00  (spaces)
IBAN:     DE89370400440532013000  → DE89370400440532013000        (last 2 swapped, still valid MOD-97 checksum!)
Tax ID:   123456789              → 123 456 789  (spaces inserted)
VAT:      DE123456789            → DE 123456789  (space after country code)
```

[Qiniso](https://github.com/qinisolabs/qiniso) measured: "On arbitrary identifiers, a frontier LLM validates them wrong ~91% of the time, cold and silently."

## 4. How to Prevent It: The LITERAL Marker System

### 4.1 The `[LITERAL]` Tag

Mark values in-place where they are defined. No separate section, no duplication.

```
- **Street**: Rua da Liberdade, 42, 3.o Esq. [LITERAL: registration certificate 2026-01-15]
- **IBAN**: DE89370400440532013000 [LITERAL]
- **Tax ID**: 123456789 (obtained 2026-03-10) [LITERAL]
```

`[LITERAL]` signals: copy character-for-character. Optional source after colon identifies the authoritative document.

### 4.2 Rules Enforcing the Tag

The `[LITERAL]` system is enforced at multiple DevSystem layers:

- **Global rule** (`core-conventions.md`): "Authoritative Literals" section defines the tag format and all 8 corruption categories
- **Precision rule** (`APAPALAN_RULES.md`, AP-PR-13): BAD/GOOD examples for IBANs, addresses, postal codes across 4 countries
- **Conversation rule** (`CONVERSATION_RULES.md`, CV-LT-01): Outbound communication must copy from `[LITERAL]`-marked source or verify against official document
- **INFO rule** (`INFO_RULES.md`, INFO-SM-02): `[LITERAL]` documented as data-integrity label alongside confidence labels
- **Session MNF** (`NOTES.md`): Reminder with reference to triggering failure (EMIG-FL-016)

### 4.3 Workflow: Adding a New Literal

1. Obtain the value from the **official source document** (government registration, contract, bank confirmation)
2. Record the value in the appropriate data file at its natural location
3. Append `[LITERAL]` (or `[LITERAL: source document, date]`) to the line
4. Never copy literal values from secondary documents - always trace back to the official source

### 4.4 Workflow: Using a Literal in Outbound Communication

1. Find the `[LITERAL]`-marked value in the data file
2. Copy the exact character sequence - no reformatting
3. If the value does not exist with a `[LITERAL]` marker, find the official source document first
4. After drafting, verify the literal value in the draft matches the `[LITERAL]`-marked source character-for-character

### 4.5 Complementary Tools (External)

For high-stakes scenarios, validation APIs provide a second layer:

- **Identifier validation**: [Qiniso](https://github.com/qinisolabs/qiniso) - deterministic checksum verification for IBANs, VAT numbers, tax IDs across 30+ countries
- **Japanese addresses**: [Shirabe Address API](https://shirabe.dev/docs/address-normalize) - normalizes against Digital Agency ABR, returns match confidence
- **Indian addresses**: Google Maps Platform [India Address Feedback](https://developers.google.com/maps/architecture/india-address-feedback) - Gemini-powered parsing + geocoding verification
- **General**: Melissa.com, PostGrid - postal authority lookups

These are complementary to the `[LITERAL]` system, not replacements. The marker prevents corruption at the point of use; APIs verify correctness at the point of entry.

## 5. Next Steps

1. When adding new addresses, IBANs, or reference numbers to any document: mark with `[LITERAL]` and record the source
2. Before sending outbound communication containing any literal value: verify against the `[LITERAL]`-marked source
3. When the original failure (EMIG-FL-016) pattern recurs in a new context: add a FAILS entry and review whether the `[LITERAL]` system caught it or needs extension

## 6. Sources

**Primary Sources:**
- `LITRLPRVNT-IN01-SC-TPAN-ACCTNUM`: [The Account Number Your LLM Could Not Actually Copy](https://tianpan.co/blog/2026-05-31-the-account-number-your-llm-could-not-actually-copy) - BPE tokenization destroys identifier fidelity; 24 tokens/UUID; ~48 errors/200 items [VERIFIED]
- `LITRLPRVNT-IN01-SC-ACLNL-DNCM`: [Do Not Change Me (ACL 2025)](https://aclanthology.org/2025.mtsummit-1.19.pdf) - 36,000 sentences, 9 entity types, NMT models fail to preserve no-translate entities [VERIFIED]
- `LITRLPRVNT-IN01-SC-MLSA-ADDRVAL`: [Can AI Really Validate an Address?](https://blog.melissa.com/en-au/global-intelligence/ai-address-validation) - LLMs hallucinate addresses, staleness problem, lookup vs. generation distinction [VERIFIED]
- `LITRLPRVNT-IN01-SC-QNSO-REPO`: [Qiniso GitHub](https://github.com/qinisolabs/qiniso) - Frontier LLM validates identifiers wrong ~91% of the time [VERIFIED]
- `LITRLPRVNT-IN01-SC-SHRB-API`: [Shirabe Address API](https://shirabe.dev/docs/address-normalize) - Japanese address normalization, 4 orthographic axes, LLM hallucination warning [VERIFIED]
- `LITRLPRVNT-IN01-SC-GOOG-INDIA`: [Google Maps India Address Feedback](https://developers.google.com/maps/architecture/india-address-feedback) - Indian address complexity: sub-premise, S/O markers, PIN code inconsistency [VERIFIED]
- `LITRLPRVNT-IN01-SC-CLCD-26141`: [Claude Code Issue #26141](https://github.com/anthropics/claude-code/issues/26141) - Edit tool silently corrupts Unicode characters [VERIFIED]
- `LITRLPRVNT-IN01-SC-CLCD-38765`: [Claude Code Issue #38765](https://github.com/anthropics/claude-code/issues/38765) - Edit tool corrupts typographic quotes in C# string literals [VERIFIED]
- `LITRLPRVNT-IN01-SC-MSAF-4832`: [Microsoft Agent Framework #4832](https://github.com/microsoft/agent-framework/issues/4832) - Double JSON parsing corrupts Unicode escape sequences [VERIFIED]
- `LITRLPRVNT-IN01-SC-AIRW-FABR`: [AI Agent Email Address Fabrication](https://airweb.ai/blog-investigating-ai-agent-email-address-fabrication) - Voice agent fabricates email from name, overriding actual input [VERIFIED]
- `LITRLPRVNT-IN01-SC-JPGV-ABR`: [Japan Digital Agency ABR Geocoder](https://github.com/digital-go-jp/abr-geocoder) - Official address normalization, kanji/numeral/connector variation handling [VERIFIED]
- `LITRLPRVNT-IN01-SC-ARXV-FMTRB`: [Not as Sweet by Another Name (arXiv)](https://arxiv.org/html/2607.27648) - Format variation causes up to 53.63% accuracy drop and 41% decision drift in LLM workflows [VERIFIED]

## 7. Document History

**[2026-08-06 16:54]**
- Initial research document created from web research on GenAI literal value corruption
- 8 corruption categories identified with real-world examples across 5 regions
- [LITERAL] marker system documented as prevention mechanism
- 12 primary sources cited
