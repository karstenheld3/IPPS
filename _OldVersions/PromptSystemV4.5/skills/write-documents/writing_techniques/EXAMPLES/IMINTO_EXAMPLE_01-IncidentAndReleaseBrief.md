# IMINTO Example 01: IncidentAndReleaseBrief

Customer-facing incident brief written `using IMINTO as TECHNICAL-WRITER`. All companies, products, and figures are fictional.

## Context

A payment platform had a 47-minute checkout outage. Merchant developers and operations leads receive the brief by email and on the status page. Most readers stop after the first paragraph; they need to know whether money was charged, what to do, and whether it can happen again.

## Document

```markdown
# Checkout API Rejected Card Payments for 47 Minutes on 2026-10-14; Fix Deployed

A faulty certificate rotation blocked card payments through the Ledgerline checkout API on 2026-10-14 from 09:12 to 09:59 CET, rejecting 3,180 transactions across 412 merchants; the fix was deployed at 09:59.

No cardholder was charged for a rejected transaction. If your customers saw error code `PAY-503` in that window, they can retry the payment now. To find affected orders, open Reports > Failed Payments and filter by 2026-10-14, 09:00-10:00 CET. This brief covers the cause, the fix, the prevention measures, and open points.

## Cause

At 09:12 CET, an automated renewal job installed a new TLS (Transport Layer Security) certificate whose intermediate certificate had expired. Card networks rejected every connection signed with it. The certificate vendor confirmed the faulty renewal in writing on 2026-10-15.

## Fix and Prevention

At 09:59 CET, the on-call engineer rolled back to the previous certificate, which remains valid until 2027-03-01. Starting 2026-10-20, every certificate renewal runs first against a staging connection to each card network; the renewal job stops automatically if any handshake fails.

Quick check: in your dashboard, the payment success rate for 2026-10-14 after 10:00 CET should be back above 99.5%.

## Open Points

Our review so far shows no exposure of card or customer data. The final security review completes on 2026-10-21, and we will update this page with its result.

## Background

Certificates for card-network connections are renewed every 90 days. The full post-incident review, including the timeline by minute, is available at https://status.example.com/incidents/2026-10-14.
```

## Key Decisions

- Lede of 31 words with time, scale, cause, and status: a reader who stops after one sentence knows what happened and that it is over (IMINTO-ST-01, IMINTO-CT-02)
- Reader action in paragraph 2: "was money charged?" and "what do I do?" are the reader's first two questions, so they precede the cause (IMINTO-ST-02)
- Open point labeled with a date instead of claiming "no data exposed" as final (IMINTO-EV-02)
- Persona `TECHNICAL-WRITER` (Technicality 3): TLS is spelled out and explained on first use; the persona's One-Line Verification Step appears once, at the end of the action-oriented section, never in the lede
- Background last and deletable: removing it keeps every fact the reader needs to act (IMINTO-ST-03)
