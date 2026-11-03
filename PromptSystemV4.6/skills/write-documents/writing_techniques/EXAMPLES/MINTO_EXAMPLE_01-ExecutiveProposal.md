# MINTO Example 01: ExecutiveProposal

Answer-first board proposal written `using MINTO as CXO-ADVISOR`. All companies, people, and figures are fictional.

## Context

A mid-sized logistics company runs three regional ticketing tools after a merger. The executive board must approve or reject a consolidation budget in a 10-minute agenda slot. The reader needs the decision, the price, the payback, and the one risk they must accept.

## Document

```markdown
# Recommendation: Consolidate Customer Support on One Ticketing Platform (280k EUR; 10-Month Payback)

Since the 2024 merger, customer support has run on three regional ticketing tools. Since Q1 2026, median first-response time has doubled from 4.5 to 9 hours, and the enterprise churn report names slow support as the top cancellation reason. The board must decide whether to keep the current setup or invest. We recommend approving 280k EUR to move all three regions to one platform by the end of Q2 2027; reduced license and routing costs repay the investment in 10 months.

## 1. Three tools cost 190k EUR a year in duplicate licenses and manual routing

Finance booked 118k EUR for overlapping licenses and 72k EUR for manual ticket transfers between regions in fiscal year 2025 (cost-center report 2025-12). Manual transfer affects 31% of all tickets: a customer in one region who contacts an agent in another region waits until a coordinator re-enters the case.

One shared platform removes the overlapping contracts and the transfer step. Projected annual saving: 190k EUR minus 24k EUR additional platform fees = 166k EUR.

## 2. One platform halves first-response time

A four-month pilot in the northern region moved 6,400 tickets to a single queue on the candidate platform. Median first response fell from 9 to 4.2 hours; the share of tickets answered within one business day rose from 58% to 87% (pilot report 2026-08).

The alternative, an integration layer between the three existing tools, costs 90k EUR once. It shortens transfers but keeps three license contracts and three admin teams. Its projected saving is 30k EUR a year versus 166k EUR for consolidation.

## 3. Migration risk is limited to a four-week freeze

The vendor migrates historical tickets region by region. During each region's four-week window, workflow rule changes are frozen and agents work in both tools for five business days. The pilot region completed this window without missed service-level targets.

The largest remaining risk is the southern region's custom invoice-dispute workflow, which the new platform supports only through a configuration project of 35k EUR, already included in the 280k EUR budget. The catch: the saving starts only after the third region migrates, so the first quarter after go-live carries both cost bases.

## Decision and Next Steps

Consolidating support on one platform cuts response time in half and repays its cost in 10 months.

- Action: Approve 280k EUR capital expenditure for platform consolidation
- Owner and deadline: Head of Customer Operations, contract signature by 2026-11-30
- We would change this recommendation if: pilot response time rises above 6 hours before contract signature; the vendor raises license prices by more than 15%
```

## Key Decisions

- Answer in the fourth and last sentence of the opening: the board reads the decision, price, and payback before any analysis (MINTO-ST-01)
- Three key-line claims ordered cost, benefit, risk: matches the order in which this board evaluates capital requests
- Alternative named inside claim 2: the integration layer was the option a board member was most likely to raise, so it is answered where the speed argument is made (MINTO-EV-02)
- Persona `CXO-ADVISOR` (Formality 7, Density 8): executive register and packed sentences; two of its traits appear once each, Inline Sanity Math in section 1 and The Catch at the end of section 3, never in the same paragraph
- Change conditions in the closing: gives the board measurable reasons to revisit the decision instead of a courtesy sentence (MINTO-ST-04)
