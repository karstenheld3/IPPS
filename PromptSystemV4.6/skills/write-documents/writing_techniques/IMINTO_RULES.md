# IMINTO Rules

Output standards for documents written `using IMINTO` (lede, nut graf, decreasing-priority body).

**Writing quality:** Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: AP-PR-01 (datetime format), AP-PR-07 (be specific), MW-VO-01 (active voice), AP-ST-05 (general to specific).

## Rule Index

Structure (ST)
- IMINTO-ST-01: Lede is the first 1-2 sentences and has 25-40 words
- IMINTO-ST-02: Nut graf appears within 2 paragraphs after the lede
- IMINTO-ST-03: Body paragraphs are ordered by decreasing importance
- IMINTO-ST-04: No closing summary paragraph

Content (CT)
- IMINTO-CT-01: Headline states the news (actor, action, result)
- IMINTO-CT-02: Lede uses active voice and contains the most important facts
- IMINTO-CT-03: Body delivers every promise the lede makes

Evidence (EV)
- IMINTO-EV-01: Times, dates, and counts are exact and include timezone where relevant
- IMINTO-EV-02: Unconfirmed facts are labeled as unconfirmed
- IMINTO-EV-03: Statements are attributed to a named source or role

## IMINTO-ST-01: Lede of 25-40 Words

**BAD:**
```
Over the past months our team has worked hard to improve reliability, and we want to share
some updates about recent events that affected some customers.
```

**GOOD:**
```
Card payments through the checkout API failed for 47 minutes on 2026-10-14 (09:12-09:59 CET),
rejecting 3,180 transactions; a faulty certificate rotation caused the outage and is fixed.
```

## IMINTO-ST-02: Nut Graf Within 2 Paragraphs

**BAD:** Impact on customers is first explained in paragraph 6.

**GOOD:** Paragraph 2: "If you saw error code PAY-503 during that window, no money was charged. Retry the payment or use the refund report described below."

## IMINTO-ST-03: Decreasing Importance

**BAD:** Paragraph 2 describes the history of the certificate system; the customer action appears in paragraph 5.

**GOOD:** Paragraph order: impact and action, root cause, fix, prevention, background.

## IMINTO-ST-04: No Closing Summary

**BAD:** "In summary, a certificate issue caused a 47-minute outage that is now resolved."

**GOOD:** The last paragraph contains the least important context, such as a link to the full post-incident review.

## IMINTO-CT-01: News Headline

**BAD:** `Update on Recent Events`

**GOOD:** `Checkout API Rejected Card Payments for 47 Minutes on 2026-10-14; Fix Deployed`

## IMINTO-CT-02: Active Lede with Key Facts

**BAD:** "Some transactions were affected by an issue that was identified by the team."

**GOOD:** "A faulty certificate rotation blocked 3,180 card payments for 47 minutes."

## IMINTO-CT-03: Lede Promise Kept

**BAD:** The lede says "is fixed" but the body never states what was fixed or how recurrence is prevented.

**GOOD:** The body contains one paragraph on the fix and one on the prevention measure.

## IMINTO-EV-01: Exact Times and Counts

**BAD:** "Yesterday morning, a few thousand payments failed."

**GOOD:** "On 2026-10-14 between 09:12 and 09:59 CET, 3,180 payments failed."

## IMINTO-EV-02: Unconfirmed Facts Labeled

**BAD:** "No customer data was exposed."

**GOOD:** "Our review so far shows no customer data exposure; the final security review completes on 2026-10-21."

## IMINTO-EV-03: Attribution

**BAD:** "It is believed the vendor caused the issue."

**GOOD:** "The certificate vendor confirmed in writing on 2026-10-15 that a renewal job sent an expired intermediate certificate."
