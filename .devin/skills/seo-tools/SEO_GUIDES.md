# SEO Guides

Numbered procedures per lifecycle stage. Each step names the rules it applies (`SEO_RULES.md`), the checks it runs (`SEO_CHECKS.md`), and the script command that supplies data. Scripts run from the skill folder with the shared venv Python.

## MUST-NOT-FORGET

- Tier order: Tier 1 free first and complete, then Tier 2 prepaid to enrich and verify, then probe Tier 3 subscription and enrich and verify again; report per claim the sources and agreement (SEO-TLS-01, SEO-TLS-11)
- Run `dataforseo/query.py balance` before paid DataForSEO batches (SEO-TLS-05)
- Google Indexing API only for `JobPosting` or `BroadcastEvent` pages, never for regular pages (SEO-TLS-02)
- Run the pre-publish gate (`SEO_CHECKS.md` section 2) before anything goes live (SEO-MTD-12)
- State evidence labels when recommending; practices in the Do-Not-Do list are never recommended
- Examples use `example.com`; never invent limits not in `SEO_RULES.md`

## Stage Index

- IDEATE: before building a product, book, course, app, video, podcast, or new page
- CREATE: while drafting or architecting any asset
- PUBLISH: immediately before and after an asset goes live
- IMPROVE: every 4-6 weeks, after an alert, on a traffic or citation drop, or when planning a campaign
- RESEARCH: whenever a step needs data
- MONITOR: scheduled daily and 4-6 week runs

## IDEATE: Demand-First Opportunity Finding, Shaping, Naming

### Demand validation (5 steps)

1. Expand seeds: collect 5-20 seed phrases for the user problem and solution category. Sources: platform autocomplete (Google, Bing, Amazon, YouTube, App Store), `youtube/query.py search "SEED"` for video and courses, `google-search-console/query.py analytics SITE --dimensions query` for owned sites. Tier 2 enrich and verify: `scrapecreators/query.py tiktok-suggestions|youtube-typeahead "SEED"`, `dataforseo/query.py keywords "SEED" --limit 100` ($0.024) (SEO-DMD-01, SEO-DMD-04, SEO-TLS-11)
2. Cluster and size demand: cluster keywords by SERP overlap (step "SERP-overlap clustering" below); record cluster volume and CPC with `dataforseo/query.py search-volume --file cluster.txt` ($0.09 per 1,000 keywords, Live). High CPC (> $2.00 B2C, > $8.00 B2B) or strong category best-seller rank confirms willingness to pay [VERIFIED] (SEO-DMD-03)
3. Verify trajectory: check the head term in Google Trends (5-year window; one shared anchor term per batch of max 8 terms) or Pinterest Trends (2-year window, max 4 terms). Classify: evergreen stable (12-month coefficient of variation < 0.25, 3-year slope within +-15%/year), recurring seasonal (> 2x baseline in the same 1-2 months yearly; publish 45-90 days before peak), breakout growth (90-day average > 1.5x prior year), fad or structural decline (spike then > 60% collapse, or > -25%/year for 3 years) -> stop or pivot on decline (SEO-DMD-02, SEO-DMD-05). To find or compare candidates across platforms, use this order: free sources first; then one `trendsmcp/query.py board --type "Google Trends"` or `growth KEYWORD --source S` call per candidate (credits, estimate printed); then depth calls with `scrapecreators/query.py` only for the top 1-2 candidates. The Trends MCP `value` is a 0-100 momentum index, not search volume; size demand with step 2
4. Audit supply weakness and AI displacement: inspect top-10 on the target surface. Web: does an AI Overview answer fully without clicks; forum threads or pages older than 24 months in top 5. Books: top-10 in the 3 target categories, recurring 2-3 star complaints. Apps: top-10 for the target title keywords, feature gaps in recent reviews. Tools: `dataforseo/query.py serp "QUERY"` shows `AI Overview present` and feature types ($0.002) (SEO-DMD-03, SEO-DMD-07)
5. Derive the specification: map every validated sub-cluster to a product feature, calculator input, book chapter, course module, or `<h2>` section, using the exact question phrasing of users and grounding queries (SEO-FND-05)

### SERP-overlap clustering

1. Fetch top-10 organic URLs per candidate keyword (`dataforseo/query.py serp "KEYWORD" --format json`, $0.002 each; for > 10 keywords use the task_post pattern in `dataforseo/ENDPOINTS.md`) or check samples in a browser
2. Pre-group large lists with Keyword Planner concepts or embedding similarity >= 0.75, then verify boundary pairs with SERP overlap [COMMUNITY]
3. Keywords sharing >= 3 of the top-10 URLs -> one canonical page (highest-volume query = `<title>`/`<h1>`; others = `<h2>` sections); < 3 -> separate pages (SEO-DMD-06)
4. Never create separate pages for close variants or fan-out rephrasings (SEO-FND-04)

### Intent and shape

1. Classify each cluster: informational, commercial investigation, transactional, navigational
2. Inspect the dominant top-5 format; if >= 3 of top 5 are calculators, tools, or videos, a static article fails intent [VERIFIED]
3. For question clusters with AI Overviews (64.7% trigger rate on question queries), shape the asset as tool, calculator, original benchmark, first-hand case study, downloadable template, or comparison workflow (SEO-DMD-07)
4. Score candidates with MOS; cold-start Confidence_Factor 0.6-0.8 (`SEO_CHECKS.md` section 6)

### Naming (4 gates)

1. Collision gate: search the exact name in quotes on Google and the target platform (store, podcast directory, GitHub, npm, PyPI); pass = no trademark, no dominant unrelated entity in top 5, no common dictionary word with unrelated high-volume intent (SEO-DMD-08)
2. Platform gate: check limits and bans (KDP title + subtitle < 200 chars, no "bestselling", "free", other authors; app title <= 30 chars, Play without "#1", "Free", emoji, ALL CAPS; GBP real-world name; podcast title without stuffing); run `prepublish-lint.py` on a draft payload (SEO-DMD-08, SEO-MTD-10)
3. Dual-component gate: distinctive handle + query-matched descriptor in subtitle or after a colon, within platform limits, e.g. `ExampleFlow: Invoice Reconciliation for Small Teams` (SEO-DMD-08, SEO-FND-05)
4. LLM prior gate: ask target LLMs without search "What category, strengths, and limitations do you associate with [Name]?"; reject names with a conflicting category association (up to -33 percentage points in top-3 recommendations) (SEO-DMD-09)
5. Slugs and filenames: lowercase, hyphenated, descriptive (SEO-DMD-10)

## CREATE: Media-Specific Structure, Agent Readiness, Entity Anchoring

### Web foundation (every HTML page)

1. Ensure HTTP 200, `index, follow`, snippets allowed, consistent pre/post-JS canonical (SEO-FND-01, SEO-FND-02)
2. Confirm non-commodity value: first-hand data, original benchmark, expert analysis, or interactive tooling (SEO-FND-03)
3. Write a question-matched `<title>`, one `<h1>`, question `<h2>`/`<h3>` sub-headings, and a 40-80 word opening paragraph that answers with numbers, dates, prices (SEO-FND-05, SEO-MTX-02)
4. On commercial pages add the 4 gatekeepers: on-topic terms, published price, genuine current timestamp, specification table; plus direct comparisons and evidence-backed claims (SEO-CMP-04)
5. Add active JSON-LD matching visible text; never retired types (SEO-FND-08, SEO-FND-09, SEO-MTD-04)
6. Qualify paid and UGC links; `noindex` unvetted UGC pages (SEO-FND-12)
7. Never apply stylistic GEO rewrites to pages that already rank (SEO-FND-06)

### Media playbooks

Requirements per media type: `SEO_CHECKS.md` section 4. Procedure per type:
1. Articles and blog posts: web foundation; SERP-overlap check against owned pages; same image in `og:image` and `Article.image`; dates change only with substantive edits (SEO-MTX-03)
2. PDFs and whitepapers: native text layer, PDF `Title`, hyphenated filename; companion HTML page; `Link: <...>; rel="canonical"` header when duplicating HTML (SEO-MTX-04)
3. Developer documentation: Markdown negotiation with `Vary: Accept`, `/index.md` fallback, hierarchical `llms.txt` above ~200 pages; verify with `agent-readiness/check.py URL --site-type B` (SEO-MTX-05, SEO-MTX-06, SEO-AGT-04..06)
4. Images and infographics: `<img src alt>`, `<svg><title>`, IPTC label on AI product images, `<image:loc>` sitemap for CDN images (SEO-MTX-07, SEO-MTX-08)
5. Books: metadata per store (SEO-MTX-09..14); generate fields with the PUBLISH metadata pipeline
6. Video: query-matched title and spoken hook, captions, `00:00` chapters (>= 3 x >= 10 s), dedicated watch page, opaque thumbnail, `VideoObject` + `Clip` (SEO-MAV-01, SEO-MAV-02)
7. Podcasts: topic and guest first in episode title, description <= 4,000 bytes, transcript and chapters tags, companion HTML transcript page (SEO-MAV-03, SEO-MAV-04)
8. Social posts: verify accounts as GSC platform properties; target query in the first 60 chars; alt text; LinkedIn SEO fields (SEO-MAV-05, SEO-MTD-12)
9. Apps: Apple 30/30/100/170 and Play 30/80/4000 limits, set-difference keywords, Custom Product Pages per segment, localized screenshots (SEO-MAV-06, SEO-MAV-07)
10. Local business: GBP real-world name, "IS a" categories, link-free description, service area within ~2 h (SEO-MAV-08, SEO-MAV-09)
11. Offline and print: vanity URL + QR 301 to HTTPS page with UTM and clean canonical; `Event` JSON-LD only for public physical events (SEO-MAV-10)

### Agent readiness by site type

1. Type A (every site): robots.txt with `Sitemap:`, 3-class AI bot separation, `Content-Signal`, Markdown negotiation with `Vary: Accept` (SEO-AGT-01..04)
2. Type B (documentation): A + `/index.md` fallback, banner removed from Markdown, hierarchical `llms.txt`, redirects for training bots on deprecated docs (SEO-AGT-05, SEO-AGT-06)
3. Type C (ecommerce): A + `Product` JSON-LD with 2025-2026 properties + WebMCP tools (SEO-MTD-04, SEO-AGT-10)
4. Type D (API or SaaS): A + B + `/.well-known/api-catalog`, MCP server card, agent skills index, OAuth protected resource metadata (SEO-AGT-07..09)
5. Verify: `agent-readiness/check.py URL --site-type A|B|C|D` returns no FAIL

### Entity and brand memory

1. Publish `Organization` + `ProfilePage` JSON-LD with verified `sameAs` (Wikidata, Wikipedia, GitHub, official social profiles) and company identifiers (SEO-AGT-11)
2. Use one identical 1-sentence brand-to-category definition on every surface (site, profiles, store listings, press kit) (SEO-AGT-11)
3. Niche or new brand: list third-party comparison, benchmark, and documentation pages that AI engines already cite for category queries and earn factual inclusion with price and specs (SEO-FND-11, SEO-CMP-07)
4. Established brand: check what LLMs say without search; correct wrong associations in authoritative reference sources (SEO-FND-11)

### Localization

1. Research keyword demand natively per language and market; never translate keywords (SEO-MAV-12)
2. Implement hreflang with one method, ISO codes, return links, `x-default`, same-language self-canonicals (SEO-MAV-11)
3. Match `<title>` language and script to the page; Apple Books phonetic fields for Japanese and Chinese (SEO-MTD-01, SEO-MTX-11)
4. Localize screenshots and image filenames; push localized URLs with `indexnow/submit.py` (SEO-MAV-12)

## PUBLISH: Metadata, Pre-Publish Gate, Indexing Push

### Metadata pipeline (5 steps)

1. Front-load: one primary query per asset; place it with the current year or metric in the first 35-55 chars of `<title>`, `<h1>`, video or podcast title, book subtitle, or app name and subtitle (SEO-MTD-01, SEO-FND-05)
2. Pack backend keywords by set difference: `pool = candidate keywords - words(title, subtitle, author or developer, categories) - banned terms`; KDP: 7 slots of 2-3 word phrases without quotes; Apple: singular words joined by commas without spaces; pack by descending search volume (SEO-MTD-09)
3. Write 5 description variants from one fact-checked brief: 140-160 char web, social, LinkedIn summary; <= 80 char Google Play short description not repeated in the full description; clean HTML without links or quotes for KDP, Kobo, Play Books; RTF with zero HTML tags and >= 50 chars for Apple Books; plain text <= 750 chars without links or promotions for GBP (SEO-MTD-02, SEO-MTD-08, SEO-MTD-10, SEO-MTD-11)
4. Set schema, thumbnails, snippet controls: active JSON-LD with visible parity; `og:image` = `primaryImageOfPage` (>= 1200 px); `max-snippet:-1, max-image-preview:large, max-video-preview:-1`; `data-nosnippet` only on `<span>`, `<div>`, `<section>` (SEO-MTD-02..04)
5. Add accessibility and AI provenance: human fact-check of all AI-assisted text and metadata; IPTC label on AI product images; alt text, SVG titles, captions, chapters, podcast transcripts, ONIX Codelist 196 (SEO-FND-07, SEO-MTD-05..07)

### Gate

1. Build a JSON payload per platform (format: `prepublish-lint.py --help`) and run `prepublish-lint.py payload.json`; fix every FAIL and re-run
2. Run `agent-readiness/check.py URL --site-type X` for web assets
3. Execute the manual gate items in `SEO_CHECKS.md` section 2 that apply
4. Publish only when all applicable items PASS

### Post-publish push

1. Bing, Yandex, Naver, Seznam, Yep: `indexnow/submit.py submit URL... --host example.com` (SEO-TLS-02)
2. Google: update sitemap `<lastmod>`; inspect with `google-search-console/query.py inspect SITE URL`; request indexing in the Search Console UI when needed; Indexing API only for `JobPosting` and `BroadcastEvent` pages (SEO-TLS-02)
3. Log a GSC Annotation (<= 120 chars) and mirror it into the project changelog with date and URLs (SEO-CMP-01)
4. Respect propagation windows: KDP categories <= 72 h, Play Books series <= 48 h, Apple Podcasts RSS <= 24 h, Apple keyword index 24-48 h after approval (SEO-CMP-06)

## IMPROVE: Audit, Scoring, Decay Triage, Competitor Gaps, Campaigns

### Audit cycle (every 4-6 weeks)

1. Hygiene gate: self-inflicted edits, analytics vs GSC agreement, technical state, 2025 impression anomaly (SEO-AUD-01, SEO-AUD-02; `SEO_CHECKS.md` section 7)
2. Run the 7-layer audit (`SEO_CHECKS.md` section 5) with `google-search-console/query.py quick-wins`, `ctr-gap`, `decay`, `cannibalization`; `bing-webmaster/query.py page-stats`, `query-stats`; `agent-readiness/check.py`; `plausible/query.py goals`
3. Classify decaying pages into signatures S1-S5 and assign one action per URL (`SEO_CHECKS.md` section 7) (SEO-AUD-04)
4. Score every fix and new opportunity with MOS and MOS_ROI in one queue (`SEO_CHECKS.md` section 6) (SEO-AUD-06)
5. Execute in MOS_ROI order; for waves of >= 20 URLs keep a 20% matched holdout (SEO-CMP-03)
6. Measure at 14 and 28 days with difference-in-differences `(Treated_Post / Treated_Pre) - (Control_Post / Control_Pre)` (SEO-CMP-03)

### AI visibility gap audit

1. Export GSC Generative AI report and Bing AI Performance (UI) for the target pages (SEO-FND-10)
2. Run a prompt panel with >= 8 repetitions per prompt, paraphrases, and surfaces; record mention rate and citation rate (SEO-CMP-08)
3. Mention rate far above citation rate, or Bing Citation Share < 15% [ASSUMED] -> RE-TITLE (title and lead question match), GATE-WEB-04 gatekeepers, crawler access check (SEO-AUD-03)

### Competitor gap method (6 steps)

1. Identify search and AI competitors: domains in top-10 and AI citations for core topics; paid: `python tiers.py run competitors example.com` (about $0.03; SERP-based set confirmed by `dataforseo competitors`, plus ads of the top 2) (SEO-TLS-01, SEO-TLS-11)
2. Extract three gap types: A) classic keyword gap (>= 2 of 3 competitors rank 1-20, own domain > 20 or absent; paid Labs data); B) first-party AI citation gap (Bing grounding queries with Citation Share < 15% [ASSUMED], $0); C) third-party co-citation gap (comparison pages cite competitors, not the brand)
3. Remove competitor brand terms (unless an "alternatives" or "vs" page is planned), unoffered features, and B = 1 queries
4. Cluster by SERP overlap (>= 3 shared URLs); if an owned page ranks 4-30 for a cluster, route it to REFRESH or EXPAND on that URL instead of a new page (SEO-DMD-06, SEO-AUD-05)
5. Score each cluster with MOS_ROI and merge into the audit queue (SEO-AUD-06)
6. Route gap type C to campaign template 8 (digital PR and entity seeding) instead of new owned posts (SEO-CMP-07)

### Campaign execution

1. Freeze baselines (28 days and 3-month YoY) for clicks, impressions, position, Generative AI impressions, Bing Citation Share, conversions (SEO-CMP-01)
2. Choose a template below; check every planned page with SERP overlap < 3 against pillar and siblings (SEO-CMP-02)
3. Log a GSC Annotation on each release day and mirror it into the changelog (SEO-CMP-01)
4. Sequence work by time to effect: band 1 = 24-72 h (IndexNow, store indexes, social surges), band 2 = 1-4 weeks (re-titles, Bing grounding, third-party inclusions), band 3 = 4-12 weeks (Google rankings, earned links), band 4 = 3-9+ months (LLM parametric memory)
5. Measure AI visibility with >= 8 repetitions per prompt; measure refresh waves against the holdout (SEO-CMP-03, SEO-CMP-08)

### Campaign templates (9)

Cadence day counts are [ASSUMED] unless stated.

1. Topic cluster (pillar + 4-8 spokes)
   - Assets: 1 pillar page or tool; spokes with < 3 shared URLs each; pillar links to every spoke, every spoke links back in its first 200 words and to 1-2 siblings; all URLs in sitemap, IndexNow, Markdown
   - Cadence: week 1 demand, clustering, MOS; week 2 pillar + 2 best spokes + links from 5 strong pages + annotation; weeks 3-5 1-2 spokes per week; weeks 6-8 RE-TITLE spokes at 4-15 with low CTR
   - KPIs: cluster clicks and conversions, Bing Topics and Citation Share, spokes in 4.0-15.9
   - Time to effect: Bing 24-72 h index, 2-4 weeks grounding; Google 2-4 weeks impressions, 6-12 weeks top-10 [COMMUNITY]
2. Refresh and consolidation wave (4-week sprint, every 4-6 weeks)
   - Assets: triage queue by signature and MOS_ROI; 4 gatekeepers on refreshed commercial pages; 301 redirect map
   - Cadence: days 1-3 audit and 20% holdout; week 1 RE-TITLE and CONSOLIDATE; weeks 2-3 REFRESH and UPGRADE; week 4 inspect and compare at 14 and 28 days
   - KPIs: treated vs holdout clicks and conversions; position lift 4-15 -> 1-3; Bing Citation Share 30-day Compare
   - Time to effect: RE-TITLE 3-14 days after recrawl; REFRESH and 301 2-6 weeks [COMMUNITY]
3. Book launch (KDP, Apple Books, Play Books, Kobo, web hub)
   - Assets: metadata package from the PUBLISH pipeline; 3 categories per format; ONIX 3.1 feed; tracked interior URL (`https://example.com/books/{slug}?utm_source=ebook&utm_medium=interior`); HTML book hub with `Book` JSON-LD and canonicalized sample PDF
   - Cadence: T-30d subtitle demand, autocomplete for 7 slots, category research, lock ISBNs; T-14d pre-order listings (ONIX or portal, never both on Play) and book hub; T-3d verify categories; T-0 to T+7d concentrate promotion in one 7-day window [COMMUNITY]; T+14d to T+30d rotate weak keyword slots
   - KPIs: unit sales, category rank, store conversion, hub clicks, interior UTM signups
   - Time to effect: KDP index 24-72 h; Play series bundle <= 48 h; hub and AI citations 2-6 weeks
4. App launch (App Store, Google Play)
   - Assets: Apple and Play listings within limits; Custom Product Pages; web landing page with `SoftwareApplication` JSON-LD, price, specs
   - Cadence: T-21d native keyword research per language and lint; T-7d submit binary and listings, publish landing page; T-0 to T+7d initial installs, review prompt after a completed core value event; T+14d and T+28d rotate Apple keywords on the next release
   - KPIs: store search impressions, conversion rate, non-brand keyword ranks, rating >= 4.5
   - Time to effect: Apple keyword index 24-48 h after approval; Play behavioral ranking 2-6 weeks
5. Podcast launch and episode cycle
   - Assets: topic-first episode titles, transcript and chapters tags, YouTube video with chapters, companion HTML transcript page with `VideoObject` + `Clip`
   - Cadence: T-14d trailer + first 3 episodes, verify YouTube in GSC; each episode day RSS + transcript + video + HTML page + IndexNow; T+24-48 h check GSC 24-hour view and refine titles
   - KPIs: directory search plays and followers, YouTube query watch time, transcript page clicks and AI citations
   - Time to effect: Apple RSS <= 24 h; YouTube and GSC platform property 24-72 h; transcript page 1-4 weeks
6. Product, SaaS, or API launch
   - Assets: product and pricing pages with the 4 gatekeepers and specification tables; 2-3 neutral comparison pages; agent-ready docs and well-known endpoints by site type
   - Cadence: T-14d naming check, deploy agent endpoints, `agent-readiness/check.py --site-type D`; T-0 publish pages, IndexNow, annotation; T+1d to T+14d third-party inclusions (template 8); T+30d and T+60d Citation Share and mention-citation gap
   - KPIs: conversions by organic and AI referrer, Bing commercial Citation Share, mention and citation rates
   - Time to effect: agent endpoints immediate; Bing and Perplexity grounding 2-14 days; Google and AI Overviews 2-8 weeks
7. Seasonal and physical event
   - Assets: evergreen year-less URL updated each year (legacy year URLs 301); `Offer` sale dates; `Event` JSON-LD for public physical events; vanity URL + QR with UTM
   - Cadence: T-60d to T-45d find ramp date in 24-month Trends and Pinterest Trends, refresh the URL; T-30d images and pins, IndexNow; T-0 monitor 24-hour view and conversions; T+14d keep URL live (HTTP 200)
   - KPIs: peak clicks, Event impressions, UTM conversions, YoY rank retention
   - Time to effect: web refresh 2-6 weeks; Pinterest 3-8 weeks lead; QR and Event 1-3 days
8. Digital PR, original benchmark, entity seeding
   - Assets: one reproducible dataset or benchmark with CSV or JSON download, `Dataset` or `Article` JSON-LD, methodology; `Organization` `sameAs` graph; target list of third-party pages cited by AI engines where competitors appear and the brand is missing; editorial links only
   - Cadence: weeks 1-2 build and publish; weeks 3-4 pitch findings, price, specs to authors of the top-20 cited third-party pages; weeks 5-8 track links and mentions, link from the benchmark to commercial pages
   - KPIs: page-level referring domains, third-party co-citations, mention rate, citation rate, Citation Share
   - Time to effect: third-party inclusion to RAG naming 1-4 weeks; earned links 4-12 weeks; LLM memory 3-9+ months
9. Cross-media repurposing chain and surge loop
   - Assets: anchor HTML article (day 0) -> YouTube long-form with chapters (day 0-1) -> Shorts, TikTok, Reels (day 1-2) -> podcast episode (day 2-3) -> LinkedIn article with SEO fields (day 2-3) -> PDF checklist with canonical header (day 3); every asset links to the anchor
   - Cadence: days 0-3 release and annotation; days 1-7 check GSC platform properties 24-hour view and "Trending up"; on >= 200% surge add an `<h2>` to the anchor (EXPAND) or a spoke when overlap < 3
   - KPIs: cross-surface impressions and clicks, trending query velocity, attributed conversions
   - Time to effect: platform property surges 24-48 h; anchor and LinkedIn in Google 3-21 days

## RESEARCH: When-to-Query-What and Cost Discipline

1. Probe the tiers once per task: `python tiers.py probe --balances`; note which tiers are unavailable (SEO-TLS-11)
2. Find the question type in the `SKILL.md` matrix; run all its Tier 1 sources and keep their results (SEO-TLS-01)
3. Tier 2: matrix rows 2, 3, 4: `python tiers.py run keywords|serp|competitors TARGET` (checks between steps, budget `--max-usd`, claim labels); other rows: run the row's prepaid sources cheap to expensive on the candidates found so far; compare with Tier 1 and label CONFIRMED, CONFLICT, or SINGLE-SOURCE; rows marked "none needed" end at Tier 1 (SEO-TLS-11)
4. Before a paid DataForSEO batch: `dataforseo/query.py balance`; compute the estimate with the price table in `dataforseo/ENDPOINTS.md`; batch up to 1,000 keywords per search-volume task (SEO-TLS-05)
5. Run the command; the script prints the estimate and aborts above `--max-cost` (default $0.10) or `--max-credits` (default 20); raise the limit only for a stated reason
6. Tier 3: when the probe lists a Tier 3 provider, state the estimated vendor units, call its REST API for the same claims, and compare with Tiers 1 and 2; otherwise record "Tier 3 unavailable"
7. Answer with a ledger per claim (tier, source, date, cost, agreement) and record the actual costs printed by the scripts in the project notes
8. Live SERP calls always include AI Overviews (`load_async_ai_overview`) (SEO-TLS-06)
9. AI visibility panels: >= 8 repetitions per prompt, 3 stages reported (SEO-TLS-09)

## MONITOR: Scheduled Alert Runs

1. Daily (or every 48 h): GSC 24-hour view on platform properties; Search generative AI control and Pages report; server or CDN logs for AI bot 403/404; `agent-readiness/check.py` on top templates (`SEO_CHECKS.md` section 8, alerts 1-3)
2. Every 4-6 weeks: `google-search-console/query.py decay SITE`; Bing AI Performance Compare and GSC Generative AI report (alerts 4-5)
3. Monthly: training bot crawl-to-referral ratio from logs (alert 6)
4. On alert: social surge -> campaign template 9; technical drop -> CREATE web foundation and GATE-WEB items; decay or citation drop -> IMPROVE audit cycle

## Do-Not-Do List

Practices with null, negative, or no evidence. Never recommend them as SEO or AI citation levers; use them only for their documented user-experience or rich-result function.

- FAQ blocks for AI citation: -3.4% within-site, x0.93 citation odds at equal rank; `FAQPage` markup is retired for rich results (https://arxiv.org/abs/2610.15033; https://developers.google.com/search/updates)
- Schema.org markup as an AI citation lever: -5.3% within-site, x0.92 odds (https://arxiv.org/abs/2610.15033)
- Author boxes for AI citation: -4.6% within-site, x0.77 odds (https://arxiv.org/abs/2610.15033)
- Summary or TL;DR boxes, word-count targets, content chunking: not significant within-site; Google states no chunking or ideal word count is required (https://arxiv.org/abs/2610.15033; https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- Body-only stylistic GEO rewrites and fixed-recipe GEO prompts: -9% top-20 retrieval, -16% reranking, -6% citation; only 3 of 54 method-domain pairs positive (https://arxiv.org/abs/2607.14035)
- "GEO raises visibility by 40%": a relative gain inside a fixed 5-document simulator, rejected as a general claim (https://arxiv.org/abs/2607.14035; https://arxiv.org/abs/2311.09735)
- `/llms.txt` for Google Search ranking: Google Search ignores it (https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- Synthetic query fan-out or doorway pages: Scaled Content Abuse (https://developers.google.com/search/docs/essentials/spam-policies)
- Fake freshness (changing `dateModified` without substantive edits) (https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- Google Indexing API for regular pages; it accepts only pages with `JobPosting` or `BroadcastEvent` (https://developers.google.com/search/apis/indexing-api/v3/quickstart)
- Apple Podcasts rating or review campaigns for search ranking: Apple search does not use ratings, reviews, shares, or descriptions (https://podcasters.apple.com/support/3686-search-on-apple-podcasts)
- Keywords in Apple App Store promotional text: not indexed (https://developer.apple.com/app-store/product-page/)
- Unofficial Google Trends scraping libraries (archived, unscaled exports): use the Trends UI with an anchor term or the Trends API alpha (https://developers.google.com/search/apis/trends)
