# SEO Checks

Executable checks: pre-publish gate, prohibited-token regexes, minimal requirements per media type, 7-layer audit, opportunity scoring, decay triage, monitoring alerts. Rules referenced by ID live in `SEO_RULES.md`; procedures that call these checks live in `SEO_GUIDES.md`.

## MUST-NOT-FORGET

- Item format: `ID [automation] title (rules)` + Action / Evidence / Failure. Automation: `lint` = `prepublish-lint.py`, `probe` = `agent-readiness/check.py`, `script` = provider script, `manual` = agent or human inspection
- A FAIL on any applicable gate item blocks publication until fixed and re-checked
- Constants marked [ASSUMED] are engineering conventions; change them only in section 1 and keep script defaults identical
- Thresholds apply to clicks when comparisons include May-September 2025 (SEO-AUD-02)

## 1. Constants

Scoring
- MOS weights: D 0.20, I 0.25, F 0.25, B 0.20, C 0.10 [ASSUMED] (SEO-AUD-06)
- MOS gate: G_gate = 0 when B = 1, I = 1, or page technically blocked and task is not a technical fix [ASSUMED]
- Confidence_Factor: 1.0 first-party data >= 30 days; 0.8 third-party or autocomplete proxies; 0.6 cold start [ASSUMED]
- Effort_Hours defaults: RE-TITLE 0.5; REFRESH 2.0-3.0; EXPAND 2.0 (section) or 4.0 (spoke); CONSOLIDATE 2.0-3.0; RE-FORMAT or UPGRADE 4.0-8.0; PRUNE 0.25 [ASSUMED]

GSC derived analyses (defaults in `google-search-console/query.py`)
- quick-wins: average position 4.0-15.0, sorted by impressions, 28 days [ASSUMED]
- ctr-gap (RE-TITLE): position 1.0-10.9, >= 1,000 impressions in 90 days, CTR < 0.60 x expected CTR [ASSUMED]
- ctr-gap expected CTR: median page CTR of the site in the same bucket over the same 90 days; buckets 1.0-1.9, 2.0-2.9, 3.0-3.9, 4.0-5.9, 6.0-10.9; fewer than 5 pages in a bucket = INSUFFICIENT_BASELINE [ASSUMED]
- decay: >= 20% and >= 50 lost clicks, last 3 full months vs same months one year earlier [ASSUMED] (SEO-AUD-02, SEO-AUD-04)
- cannibalization: >= 2 pages each with >= 10% of a query's impressions; query total >= 100 impressions in 28 days [ASSUMED] (SEO-AUD-05)

Triage
- Ranking decay position drop: >= 2.0 positions [ASSUMED]
- REFRESH stagnation trigger: position 4.0-15.9 for >= 90 days with MOS >= 55 [ASSUMED]
- EXPAND trigger: emerging query >= 100 impressions in 90 days at position 11.0-30.0 [ASSUMED]
- RE-TITLE question-match trigger: title or lead paragraph similarity to top queries < 0.65 [ASSUMED]
- PRUNE preconditions: age >= 12 months, 0 clicks and < 50 impressions in 90 days, 0 AI citations, 0 referring domains, 0 conversions, no 301 target [ASSUMED] (SEO-AUD-05)

Campaigns and measurement
- Holdout: 20% matched control, >= 5-10 URLs, 28 days, for waves of >= 20 URLs [ASSUMED] (SEO-CMP-03)
- AI visibility sampling: >= 8 repetitions per prompt [VERIFIED range 7-8] (SEO-CMP-08)
- Bing Citation Share action threshold: < 15% [ASSUMED] (SEO-AUD-03)

Cost
- DataForSEO `--max-cost` default: $0.10 per command [ASSUMED]

## 2. Pre-Publish Gate (20 Items)

Run every item that applies to the asset type. Web items apply to every HTML page, including landing pages for books, apps, videos, and podcasts.

### Universal and web (GATE-WEB-01..09)

- GATE-WEB-01 [probe] HTTP 200 and index and snippet eligibility (SEO-FND-01, SEO-MTD-02)
  - Action: run `agent-readiness/check.py URL`; inspect `<meta name="robots">` and `X-Robots-Tag`
  - Evidence: "Page returns HTTP 200" PASS, "Page indexable (no noindex)" PASS; robots meta `index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1`
  - Failure: non-200, `noindex`, `nosnippet`, or restrictive `max-snippet` on a page meant to rank
- GATE-WEB-02 [manual] Pre-JS and post-JS canonical parity (SEO-FND-02, SEO-MTX-01)
  - Action: compare `<link rel="canonical">` in raw HTML (view-source or `curl`) with the rendered DOM
  - Evidence: one absolute HTTPS canonical, identical in both
  - Failure: relative URL, fragment, missing in one view, or different values
- GATE-WEB-03 [manual] title and h1 question match, script match, freshness (SEO-FND-05, SEO-MTD-01)
  - Action: read `<title>` (target 50-60 chars) and the single dominant `<h1>`
  - Evidence: primary query in the first 35-55 chars, same language and script as body, current year when the topic is dated, no boilerplate
  - Failure: generic title ("Home"), boilerplate, keyword repetition, obsolete year, script mismatch
- GATE-WEB-04 [manual] Four competitive GEO gatekeepers on commercial pages (SEO-CMP-04)
  - Action: on product, pricing, comparison, or launch pages check on-topic terms, published price, real timestamp, specification table
  - Evidence: all four visible in HTML
  - Failure: price hidden behind "contact sales", no date, no specs
- GATE-WEB-05 [manual] og:image and primaryImageOfPage parity (SEO-MTX-03, SEO-MTD-03)
  - Action: compare `og:image` with `primaryImageOfPage` or `Article.image`
  - Evidence: same URL, >= 1200 px wide, representative image
  - Failure: different images, site logo, text banner, extreme aspect ratio
- GATE-WEB-06 [lint] Active Schema.org and retired-type ban (SEO-FND-08, SEO-FND-09, SEO-MTD-04)
  - Action: run `prepublish-lint.py` with the page JSON-LD in field `jsonld`; validate in Rich Results Test
  - Evidence: regex 5 PASS; every marked-up value visible on the page
  - Failure: `FAQPage`, `HowTo`, `PracticeProblem`, `SpecialAnnouncement`, or invisible marked-up content
- GATE-WEB-07 [manual] img src alt, svg title, IPTC AI label (SEO-MTX-07, SEO-MTX-08, SEO-MTD-05)
  - Action: inspect content images and inline SVGs; check IPTC metadata of AI product images
  - Evidence: `<img src alt>` for every content image, `<svg><title>`, `TrainedAlgorithmicMedia` on AI product images
  - Failure: CSS `background-image`, missing or stuffed alt, unlabeled SVG, AI product image without IPTC label
- GATE-WEB-08 [manual] hreflang ISO codes and reciprocity (SEO-MAV-11)
  - Action: list all `hreflang` annotations of the page and each alternate
  - Evidence: valid ISO 639-1 (+ ISO 3166-1 Alpha 2) codes, return links, `x-default`, same-language self-canonical
  - Failure: `en-UK`, `es-419`, country code alone, missing return link
- GATE-WEB-09 [probe] Agent Markdown and non-recursive banner (SEO-AGT-04, SEO-AGT-05)
  - Action: run `agent-readiness/check.py URL --site-type B` for docs, `A` otherwise
  - Evidence: Markdown response with `Vary: Accept` and frontmatter (docs: `/index.md` PASS); agent banner absent from Markdown output
  - Failure: HTML returned for `Accept: text/markdown` on docs, missing `Vary: Accept`, banner repeated in Markdown

### Book stores (GATE-BOOK-01..04)

- GATE-BOOK-01 [lint] Title, subtitle, series separation (SEO-MTX-09, SEO-MTX-12, SEO-MTX-13)
  - Action: run `prepublish-lint.py` platform `kdp`, `kobo`, or `google-play-books`
  - Evidence: KDP title + subtitle < 200 chars, title <= 60; series number digits only; no series name or volume in title or subtitle
  - Failure: length FAIL, "Book 2" in subtitle, non-digit series number
- GATE-BOOK-02 [manual] Author string and identifier immutability (SEO-MTX-12, SEO-MTX-13)
  - Action: compare author string with the existing catalog; check ISBN of live Google Play books
  - Evidence: character-identical author string; unchanged live ISBN
  - Failure: different initials or spelling; ISBN change on a live Play book
- GATE-BOOK-03 [lint] Description format and link and quote ban (SEO-MTX-09, SEO-MTX-11, SEO-MTX-13)
  - Action: run `prepublish-lint.py` for each store variant
  - Evidence: regex 1 PASS (KDP, Kobo); regex 2 PASS and >= 50 chars (Apple Books)
  - Failure: URL, email, handle, or phone in description; HTML tag in Apple Books description; review quotes
- GATE-BOOK-04 [lint] KDP 7 keyword slots and 3 categories (SEO-MTX-10, SEO-MTD-09)
  - Action: run `prepublish-lint.py` platform `kdp` with `keywords` (list of 7) and `context.categories`
  - Evidence: each slot <= 50 chars, no quotes, no words from title, subtitle, author, categories, no banned terms
  - Failure: any slot FAIL

### Apps, video, podcast, local, social, compliance (GATE-APP-01..02, GATE-VID-01, GATE-POD-01, GATE-GBP-01, GATE-SOC-01, GATE-COMPL-01)

- GATE-APP-01 [lint] Apple App Store 30/30/100/170 (SEO-MAV-06, SEO-MTD-10)
  - Action: run `prepublish-lint.py` platform `apple-app-store`
  - Evidence: name <= 30, subtitle <= 30, promotional text <= 170, keywords <= 100 with no spaces around commas, no words from name or subtitle, no plurals of included singulars, no "app"
  - Failure: any check FAIL
- GATE-APP-02 [lint] Google Play 30/80/4000 and anti-promotion (SEO-MAV-07, SEO-MTD-10)
  - Action: run `prepublish-lint.py` platform `google-play` per translation
  - Evidence: title <= 30, short description <= 80 and not inside full description, full description <= 4,000, regex 3 PASS, no emoji in title
  - Failure: any check FAIL; manual: unattributed testimonials, promo badges in graphics
- GATE-VID-01 [manual] Watch page, thumbnail opacity, 00:00 chapters (SEO-MAV-01, SEO-MAV-02, SEO-MTD-06)
  - Action: run `prepublish-lint.py` platform `youtube` for title and chapters; inspect watch page and thumbnail
  - Evidence: dedicated watch page, fetchable stream, thumbnail >= 60x30 px with >= 80% pixels alpha > 250, captions, >= 3 chapters >= 10 s from 00:00
  - Failure: video only in a carousel or fragment URL, transparent thumbnail, missing captions, chapters not starting at 00:00
- GATE-POD-01 [lint] Episode title, 4,000-byte description, transcript (SEO-MAV-03, SEO-MAV-04, SEO-MTD-07)
  - Action: run `prepublish-lint.py` platform `podcast`; check RSS for `<podcast:transcript>` and the HTML transcript page
  - Evidence: description <= 4,000 UTF-8 bytes in CDATA, title without stuffing or emoji, transcript tag present, transcript page live
  - Failure: byte limit FAIL, emoji or repeated keywords in title, no transcript
- GATE-GBP-01 [lint] GBP name and link-free description (SEO-MAV-08, SEO-MAV-09, SEO-MTD-11)
  - Action: run `prepublish-lint.py` platform `gbp`; compare name with signage
  - Evidence: description <= 750 chars, regex 1 PASS, no price claims; name equals signage
  - Failure: URL or promotion in description; city or service keywords in name
- GATE-SOC-01 [lint] LinkedIn SEO fields and PDF canonical header (SEO-MAV-05, SEO-MTX-04)
  - Action: run `prepublish-lint.py` platform `linkedin`; `curl -I` downloadable PDFs
  - Evidence: SEO title <= 60, SEO description 140-160; PDF responses carry `Link: <...>; rel="canonical"` when duplicating HTML
  - Failure: blank or over-length LinkedIn fields; duplicate PDF without canonical header
- GATE-COMPL-01 [manual] Human fact-check and outbound link qualification (SEO-FND-07, SEO-FND-12)
  - Action: a human verifies every AI-assisted claim in body, title, description, JSON-LD, alt; check rel attributes of paid and UGC links
  - Evidence: reviewer name and date recorded; `rel="sponsored"`, `rel="ugc"`, or `rel="nofollow"` on qualifying links
  - Failure: unverified claims; paid links without qualification

## 3. Prohibited-Token Regexes

Implemented in `prepublish-lint.py`; case-insensitive where noted. [VERIFIED] (SEO-MTD-04..12)

1. Links and contact data in KDP, Kobo, GBP descriptions: `https?://|www\.|@\w+|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b`
2. HTML tags in Apple Books description: `<[a-zA-Z/][^>]*>`
3. Promotional claims in Google Play title and descriptions (case-insensitive): `#1|best of play|\bfree\b|no ads|% off`
4. Spaces around commas in Apple keywords: `,\s+|\s+,`
5. Retired schema types in JSON-LD: `"@type"\s*:\s*"(FAQPage|HowTo|PracticeProblem|SpecialAnnouncement)"`

## 4. Minimal Requirements per Media Type (12)

Each line: action -> evidence of PASS -> failure indicator (rules). Items already in the gate reference the gate ID.

1. Web pages and commercial landing pages
   - GATE-WEB-01, GATE-WEB-02, GATE-WEB-03, GATE-WEB-06 apply
   - Write a 40-80 word opening answer -> first paragraph answers the core question with numbers or dates -> intro without the answer (SEO-FND-05)
   - Commercial pages: GATE-WEB-04
   - Agent readiness Type A -> `agent-readiness/check.py` without FAIL -> any FAIL (SEO-AGT-01..04)
2. Articles and blog posts
   - All web page items
   - Check SERP overlap with owned pages -> < 3 shared top-10 URLs -> >= 3 shared URLs (cannibalization) (SEO-DMD-06, SEO-FND-04)
   - Headings and length -> question `<h2>`/`<h3>`, concise paragraphs, no stylistic GEO rewrite -> listicle padding, generic roundup (SEO-MTX-02, SEO-FND-06)
   - GATE-WEB-05, GATE-COMPL-01; `dateModified` changed only with substantive edits (SEO-MTX-03)
3. PDFs and whitepapers
   - Text layer, `Title` property, hyphenated filename -> text selectable, title set -> scanned image PDF, "Untitled-1" (SEO-MTX-04, SEO-DMD-10)
   - Canonical header for duplicates -> `curl -I` shows `Link: <...>; rel="canonical"` -> header missing (SEO-MTX-04)
   - Companion HTML landing page -> indexable page with summary and schema -> PDF-only publication (SEO-MTX-04)
4. Developer documentation and API references
   - `agent-readiness/check.py URL --site-type B` (docs) or `D` (public API) -> no FAIL -> FAIL on Markdown, `/index.md`, `/llms.txt`, or well-known endpoints (SEO-MTX-05, SEO-MTX-06, SEO-AGT-04..09)
   - Large docs (> ~200 pages) -> per-directory `llms.txt` -> one oversized root file (SEO-MTX-06)
5. Images and infographics
   - GATE-WEB-07; descriptive hyphenated filename; alt <= 125 chars; `<image:loc>` sitemap for cross-domain CDNs (SEO-MTX-07, SEO-DMD-10)
6. Ebooks and print books
   - GATE-BOOK-01..04
   - Master ONIX 3.1.2 feed with Thema 1.7 and Codelist 196 -> feed validates against XSD -> ONIX 2.1 or manual portal edits only (SEO-MTX-14)
   - Reader-magnet URL only inside the book interior -> no URL in store metadata -> URL in description (SEO-MTX-13)
7. Video (YouTube, Shorts, web video)
   - GATE-VID-01; query-matched title and spoken hook; captions uploaded (SEO-MAV-01, SEO-MAV-02)
8. Podcasts
   - GATE-POD-01; Spotify show notes only with allowed tags; companion HTML episode page with transcript (SEO-MAV-03, SEO-MAV-04)
9. Social posts
   - Owned accounts verified as GSC platform properties -> visible in Search Console -> not verified (SEO-MAV-05)
   - GATE-SOC-01 for LinkedIn; target query in the first 60 chars of TikTok, Reels, Shorts, Pinterest, Reddit posts plus alt text (SEO-MTD-12)
10. Mobile and desktop apps
    - GATE-APP-01, GATE-APP-02; up to 3 previews and 10 screenshots; localized screenshots per market (SEO-MAV-06, SEO-MAV-07, SEO-MAV-12)
11. Local businesses
    - GATE-GBP-01; categories complete "This business IS a"; service area within ~2 h driving (SEO-MAV-08, SEO-MAV-09)
12. Offline and print media
    - Vanity URL + QR code -> QR 301-redirects to HTTPS page with `utm_source`, `utm_medium`, `utm_campaign` and clean canonical -> QR to homepage without UTM or to a redirect chain (SEO-MAV-10)
    - `Event` JSON-LD only for public physical events -> event has a `PostalAddress` -> online-only event marked up (SEO-MAV-10)

## 5. Seven-Layer Audit

Run per URL or URL group after the hygiene gate (SEO-AUD-01). Free source first, paid source optional.

1. Technical and indexability
   - Action: HTTP status, `noindex`/`nosnippet`, Search generative AI control = Include, canonical integrity, Core Web Vitals (LCP, INP, CLS)
   - Evidence: `google-search-console/query.py inspect SITE URL` verdict PASS; `agent-readiness/check.py`; PageSpeed Insights
   - Failure: Excluded, canonicalized elsewhere, non-200, poor Core Web Vitals (paid: DataForSEO On-Page from $0.00015/page)
2. Content quality and structured data parity
   - Action: check non-commodity elements, 4 GEO gatekeepers, heading density vs filler length, active schema parity, thumbnail parity
   - Evidence: GATE-WEB-04, GATE-WEB-05, GATE-WEB-06 PASS
   - Failure: commodity summary, hidden price, fake `dateModified`, retired schema (SEO-FND-03, SEO-CMP-04, SEO-MTX-02)
3. Intent and question match
   - Action: compare title, `<h1>`, opening paragraph with top GSC queries and Bing Grounding Queries; check SERP format against top-5; check owned cannibalization
   - Evidence: `google-search-console/query.py analytics SITE --dimensions query,page --filter page:equals:URL`; `cannibalization SITE`; live SERP check (browser or `dataforseo/query.py serp`)
   - Failure: question-match < 0.65 [ASSUMED], format differs from >= 3 of top-5, >= 2 owned pages split impressions (SEO-FND-05, SEO-DMD-06)
4. Authority and links
   - Action: page-level referring domains, domain authority gap vs top-5 median, internal inlinks
   - Evidence: GSC Links report (UI), `bing-webmaster/query.py links SITE`, own crawl; paid: `dataforseo/query.py backlinks DOMAIN`
   - Failure: orphan page (0-1 internal links), 0 referring domains on a competitive query
5. Classic SERP performance and CTR gap
   - Action: position bucket, CTR gap, 3-month YoY click delta
   - Evidence: `google-search-console/query.py quick-wins`, `ctr-gap`, `decay`; `bing-webmaster/query.py page-stats`
   - Failure: RE-TITLE or decay candidates listed (section 7)
6. AI citation and brand mention visibility
   - Action: GSC Generative AI report (UI), Bing AI Performance (UI), mention rate vs citation rate (multi-run panel, >= 8 runs per prompt)
   - Evidence: impressions and citation share exported with date
   - Failure: Citation Share < 15% [ASSUMED] or mention rate far above citation rate (SEO-AUD-03, SEO-CMP-08)
7. Agent readiness and conversion attribution
   - Action: agent readiness by site type; crawl-to-referral ratio and bot errors from server or CDN logs; conversions by source
   - Evidence: `agent-readiness/check.py`; `plausible/query.py goals SITE`, `sources SITE`
   - Failure: probe FAIL, class 1 bot 403s, traffic without conversions (SEO-AGT-12)

## 6. Opportunity Score (MOS)

`MOS = 100 * ((D^0.20 * I^0.25 * F^0.25 * B^0.20 * C^0.10) / 5) * G_gate`
`MOS_ROI = (MOS * Confidence_Factor) / Effort_Hours`
Weights and gate: section 1. [ASSUMED] engineering convention (no composite score has longitudinal causal proof); input signals [VERIFIED] (SEO-AUD-06).

D - Demand (paid: Keyword Planner, DataForSEO Labs, search volume; free: GSC 90-day impressions, Bing impressions; new pages: anchored Google Trends + autocomplete depth)
- 5: >= 5,000 impressions/90d or >= 2,000 searches/month, or breakout trend > +50% YoY
- 4: 1,500-4,999 impressions/90d (500-1,999 searches/month), stable or growing
- 3: 400-1,499 impressions/90d (150-499 searches/month), or B2B niche 50-149 searches/month with CPC >= $8.00
- 2: 100-399 impressions/90d (30-149 searches/month)
- 1: < 100 impressions/90d (< 30 searches/month) and flat or declining

I - Intent, format, question-match opportunity (free: page vs top GSC queries, Bing Grounding Queries, top-5 SERP)
- 5: page ranks 4-20 or gets impressions but title or lead mismatches the query, or mention-citation gap fixable by rewrite
- 4: strong fit for new or refreshed page, SERP format matches capability, < 3 shared URLs with owned pages
- 3: decent title match, missing `<h2>` sub-question coverage
- 2: broad intent, already optimized title and lead
- 1: mismatched intent, or duplicates an owned canonical page when scored as "create" (G_gate = 0)

F - Ranking and retrieval feasibility (free: GSC position, Bing Citation Share, SERP vulnerability check; paid: referring-domain gap)
- 5: position 4.0-10.9 (or 1-15% Bing Citation Share, store rank 4-10)
- 4: position 11.0-20.9, or new page in a SERP with a forum or outdated result in top 5
- 3: position 1.0-3.9 with CTR < 0.6 x expected, or competitors of comparable authority
- 2: position 21.0-50.0 or unranked vs mid-tier competitors
- 1: unranked vs entrenched domains with no SERP vulnerability

B - Business value and conversion proximity (free: offer alignment, `plausible/query.py goals`, Keyword Planner top-of-page bid)
- 5: transactional or bottom-of-funnel (pricing, product, store listing, converting tool)
- 4: commercial investigation ("best", "vs", "alternatives")
- 3: mid-funnel problem adjacent to the offer with a natural CTA
- 2: top-of-funnel education for the target audience
- 1: no connection to any offer (G_gate = 0)

C - SERP and AI clickability (free: live SERP, GSC Generative AI report, Bing Intents)
- 5: tool, calculator, transactional, or complex comparison SERP requiring a click
- 4: clean organic SERP, or AI Overview on a non-commodity topic where original data earns citations
- 3: AI Overview + 1-2 features, organic and citations still prominent
- 2: AI Overview + ads + packs push organic below the fold
- 1: commodity fact fully answered in place by AI Overview

Worked check: D 4, I 5, F 5, B 4, C 3, G_gate 1 -> weighted geometric mean = 4^0.2 * 5^0.25 * 5^0.25 * 4^0.2 * 3^0.1 = 4.345 -> MOS = 100 * 4.345 / 5 = 86.9; RE-TITLE 0.5 h, confidence 1.0 -> MOS_ROI = 173.8

## 7. Decay Triage and Actions

Hygiene first (SEO-AUD-01): 1) self-inflicted edit in GSC Annotations or changelog -> restore; 2) analytics drop without GSC click drop -> tracking error; 3) deindexed or canonical shift -> fix technical layer; 4) May-September 2025 comparisons -> use clicks, verify live SERP and Trends.

Signatures (input: `google-search-console/query.py decay SITE`; thresholds section 1) (SEO-AUD-04)
- S1 Ranking decay: clicks down >= 20%, impressions down, position worse >= 2.0 -> REFRESH
- S2 Zero-click capture: clicks down >= 20%, impressions flat or up (>= -5%), position flat or better, AI Overview or SERP feature present -> RE-FORMAT/UPGRADE if B >= 4; stop investing if B <= 2
- S3 Intent drift: clicks down, position roughly held or 5-12, live SERP shows a new dominant format -> RE-FORMAT (same URL)
- S4 Demand decay: clicks down >= 20%, impressions down >= 25% (outside 2025 anomaly window), position held or better, Google Trends declining over 24 months -> CONSOLIDATE or PRUNE
- S5 Site-wide date-aligned drop: many pages drop on the same date -> check Google core or spam update and site-wide regressions before page fixes

Actions (one primary action per URL)
- RE-TITLE (0.5 h): position 1.0-10.9, >= 1,000 impressions/90d, and CTR < 0.60 x expected or question-match < 0.65, or mention >> citation -> rewrite title, `<h1>`, opening 40-80 words with numbers, dates, prices; body unchanged. Evidence: `ctr-gap` row with status RE-TITLE. Failure: body rewritten instead (SEO-FND-06)
- REFRESH (2.0-3.0 h): S1, or stagnation at 4.0-15.9 for >= 90 days with MOS >= 55 -> add first-hand data, explicit pricing and specs, current benchmarks, missing `<h2>` sub-questions from Grounding Queries, 3-5 internal links. Failure: date swap without substance (SEO-MTX-03)
- RE-FORMAT / UPGRADE (4.0-8.0 h): S2 with B >= 4, or S3 with >= 3 of top-5 in another format -> reshape to the winning format or embed a tool or dataset on the same URL (SEO-DMD-07)
- EXPAND (2.0 h section / 4.0 h spoke): emerging query >= 100 impressions/90d at 11.0-30.0 -> >= 3 shared top-10 URLs: add `<h2>` section; < 3: new spoke page with bidirectional links (SEO-DMD-06)
- CONSOLIDATE (2.0-3.0 h): >= 2 owned URLs at 5-30 for the same cluster, or S4 page that belongs to a broader pillar -> merge unique content into the strongest URL, 301 + canonical, update internal links (SEO-AUD-05)
- PRUNE (0.25 h): all PRUNE preconditions in section 1 -> HTTP 410 (or 404) and remove internal links; `noindex` when the page must stay reachable (SEO-AUD-05, SEO-FND-12)

## 8. Monitoring Alerts

Cadence -> signal -> threshold [ASSUMED] -> source -> action (SEO-AUD-07, SEO-CMP-05, SEO-AGT-12)
1. Daily: social or video search surge -> >= 200% day-over-day Google clicks on a verified platform property -> GSC 24-hour view (UI) -> repurpose into the HTML hub or a spoke within 48 h (campaign template 9)
2. Daily: indexation or generative control drop -> Search generative AI control switched to Exclude, >= 5% 7-day drop in indexed pages, or non-200 / canonical mismatch on top-20 URLs -> GSC Pages report, `google-search-console/query.py inspect` -> fix technical layer first
3. Daily: AI crawler errors -> > 1% HTTP 403 rate for class 1 bots, or any 404 on `/llms.txt`, `/index.md`, `/.well-known/*` -> server or CDN logs, `agent-readiness/check.py` -> fix WAF rules or endpoints
4. Every 4-6 weeks: page click decay -> >= 20% and >= 50 clicks 3-month YoY loss on a top-50 page -> `google-search-console/query.py decay` -> run section 7
5. Every 4-6 weeks: AI citation drop -> >= 25% 30-day drop in Bing Citation Share or GSC Generative AI impressions -> Bing AI Performance Compare, GSC Generative AI report (UI) -> run audit layers 3 and 6 and GATE-WEB-04
6. Monthly: training bot load -> class 2 bot crawls >= 10,000 pages/month with < 10 referrals (ratio > 1,000:1) -> server or CDN logs -> evaluate `Content-Signal: ai-train=no` (SEO-AGT-03)
