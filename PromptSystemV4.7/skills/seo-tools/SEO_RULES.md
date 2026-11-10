# SEO Rules

Normative, testable SEO and discoverability rules plus platform metadata limits. Procedures that apply these rules: `SEO_GUIDES.md`. Checklists, gates, scoring: `SEO_CHECKS.md`.

## MUST-NOT-FORGET

- Evidence labels: `[VERIFIED]` = official platform documentation or reproducible study; `[ASSUMED]` = engineering convention without causal proof; `[COMMUNITY]` = practitioner report. Cite the label when applying a rule
- `[LITERAL: 2026-11-03]` values (limits, prices, quotas, syntax) are copied character-for-character; re-verify at the source when older than 6 months
- All sources were checked on 2026-11-03 unless a rule states another date
- Rules state WHAT must hold; never invent limits that are not listed here

## Rule Index

Foundations (FND)
- SEO-FND-01: Technical eligibility for classic and generative search
- SEO-FND-02: Pre-JS and post-JS canonical consistency
- SEO-FND-03: Non-commodity content gate
- SEO-FND-04: No synthetic query fan-out doorway pages
- SEO-FND-05: Question-matched title and opening paragraph
- SEO-FND-06: No body-only stylistic GEO rewrites
- SEO-FND-07: Human fact-check and AI labeling of generated content
- SEO-FND-08: Active structured data scope and visible parity
- SEO-FND-09: No retired rich-result schema types
- SEO-FND-10: Dual first-party AI visibility measurement
- SEO-FND-11: Two-track brand vs niche discovery strategy
- SEO-FND-12: UGC and outbound link qualification

Demand (DMD)
- SEO-DMD-01: Google Ads keyword ideas seed and parameter limits
- SEO-DMD-02: Google Trends scaling and comparison cap
- SEO-DMD-03: Three-pillar demand triangulation
- SEO-DMD-04: YouTube search.list quota and sort discipline
- SEO-DMD-05: Pinterest Trends window, cap, and seasonal lead time
- SEO-DMD-06: SERP-overlap clustering
- SEO-DMD-07: AI Overview displacement pivot for question queries
- SEO-DMD-08: Search-safe naming gate
- SEO-DMD-09: LLM brand prior check before naming or category expansion
- SEO-DMD-10: Descriptive hyphenated filenames and URL slugs

Text and book media (MTX)
- SEO-MTX-01: Self-referential absolute canonical
- SEO-MTX-02: Concise headed structure for AI selection
- SEO-MTX-03: Article thumbnail parity and fake-freshness ban
- SEO-MTX-04: PDF canonical and hreflang via HTTP Link header
- SEO-MTX-05: Developer docs Markdown negotiation and /index.md fallback
- SEO-MTX-06: Hierarchical llms.txt for large documentation sites
- SEO-MTX-07: img src, alt text, and inline SVG title
- SEO-MTX-08: Merchant Center AI image IPTC labeling
- SEO-MTX-09: Amazon KDP title, subtitle, series, and description compliance
- SEO-MTX-10: Amazon KDP 7 keyword slots and 3 categories
- SEO-MTX-11: Apple Books RTF description, primary contributor, accessibility
- SEO-MTX-12: Google Play Books immutable ID, genres, contiguous series
- SEO-MTX-13: Kobo link ban, series separation, author consistency
- SEO-MTX-14: ONIX 3.1 master feed and overwrite prevention

Audio, video, social, apps, local business, localization (MAV)
- SEO-MAV-01: YouTube relevance, watch time, chapters
- SEO-MAV-02: Google video watch page, stream, thumbnail
- SEO-MAV-03: Apple Podcasts title indexing and anti-stuffing
- SEO-MAV-04: Podcast transcripts, show notes HTML, companion page
- SEO-MAV-05: GSC social and video platform properties, LinkedIn SEO fields
- SEO-MAV-06: Apple App Store lexical limits and keyword field
- SEO-MAV-07: Google Play lexical limits and anti-promotional policy
- SEO-MAV-08: Google Business Profile real-world name
- SEO-MAV-09: Google Business Profile description, category, service area
- SEO-MAV-10: Offline-to-online vanity URL, QR redirect, physical events
- SEO-MAV-11: Bidirectional hreflang with ISO codes
- SEO-MAV-12: Native keyword research per language and IndexNow push

Agent discoverability (AGT)
- SEO-AGT-01: robots.txt and Sitemap baseline
- SEO-AGT-02: Three-class AI crawler separation
- SEO-AGT-03: Content-Signal directive
- SEO-AGT-04: Markdown content negotiation and Vary: Accept
- SEO-AGT-05: /index.md fallback and non-recursive agent banner
- SEO-AGT-06: llms.txt scope for coding and documentation agents
- SEO-AGT-07: API catalog (RFC 9727) for public APIs
- SEO-AGT-08: MCP server card and agent skills index
- SEO-AGT-09: OAuth protected resource metadata (RFC 9728)
- SEO-AGT-10: WebMCP for interactive ecommerce storefronts
- SEO-AGT-11: Entity graph anchoring and third-party co-occurrence
- SEO-AGT-12: AI operator activity and mention vs citation gap monitoring

Audit (AUD)
- SEO-AUD-01: Pre-audit hygiene gate
- SEO-AUD-02: 3-month YoY window and 2025 impression anomaly
- SEO-AUD-03: First-party plus answer-engine gap audit for AI visibility
- SEO-AUD-04: Four-signature decay classification
- SEO-AUD-05: Cannibalization, 301 consolidation, safe pruning
- SEO-AUD-06: Gated multiplicative opportunity score (MOS)
- SEO-AUD-07: Monitoring alert thresholds

Campaigns (CMP)
- SEO-CMP-01: Baseline freeze, annotation, external changelog
- SEO-CMP-02: Pillar-spoke SERP-overlap gate
- SEO-CMP-03: Matched-cohort holdout for refresh waves
- SEO-CMP-04: Four competitive GEO gatekeepers on commercial pages
- SEO-CMP-05: 24-hour rapid response on social and video properties
- SEO-CMP-06: Multi-store lead times and evergreen seasonal URLs
- SEO-CMP-07: Third-party co-citation for B2B brands
- SEO-CMP-08: Multi-run AI visibility measurement

Metadata (MTD)
- SEO-MTD-01: title and h1 front-loading, script parity, no boilerplate
- SEO-MTD-02: Meta description, snippet directives, data-nosnippet
- SEO-MTD-03: og:image and primaryImageOfPage parity, YAML frontmatter
- SEO-MTD-04: Active Schema.org properties and retired-type ban
- SEO-MTD-05: Images, inline SVG, IPTC, PDF headers
- SEO-MTD-06: Video thumbnail opacity and chapters
- SEO-MTD-07: Podcast title indexing, 4,000-byte description, transcripts
- SEO-MTD-08: Cross-store book metadata and description variants
- SEO-MTD-09: Set-difference keyword packing for KDP and Apple
- SEO-MTD-10: App Store 30/30/100/170 and Google Play 30/80/4000
- SEO-MTD-11: Google Business Profile name and link-free description
- SEO-MTD-12: Social SEO fields and mandatory pre-publish gate

Tools and data (TLS)
- SEO-TLS-01: Free-first escalation
- SEO-TLS-02: Indexing API only for JobPosting and BroadcastEvent pages
- SEO-TLS-03: GSC access via service account script
- SEO-TLS-04: DataForSEO access via cost-gated script
- SEO-TLS-05: Pre-flight cost estimation with verified rates
- SEO-TLS-06: load_async_ai_overview on live SERP calls
- SEO-TLS-07: Bing JSON endpoint; Ahrefs and Semrush not integrated
- SEO-TLS-08: Plausible Stats API plan requirement and rate limit
- SEO-TLS-09: Multi-run requirement for AI visibility panels
- SEO-TLS-10: Credential path hygiene

Platform metadata field specifications: section "Platform Metadata Field Specifications" (10 groups).

## Foundations (FND)

### SEO-FND-01: Technical eligibility for classic and generative search
Every page meant to rank in Google or Bing or to be cited in AI Overviews, AI Mode, Copilot, ChatGPT, or Perplexity must return HTTP 200, allow `Googlebot`, `Bingbot`, and `OAI-SearchBot` in `robots.txt` and CDN/WAF rules, contain no `noindex` in the raw initial HTML, and allow text snippets (no `nosnippet`, no overly restrictive `max-snippet`).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide; https://developers.google.com/search/docs/appearance/ai-features; https://developers.google.com/search/updates
BAD: `<meta name="robots" content="noindex, nosnippet">` on a page targeting AI Overviews
GOOD: `<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">`

### SEO-FND-02: Pre-JS and post-JS canonical consistency
Pages that use client-side JavaScript must set the same `<link rel="canonical">` URL in raw HTML and rendered DOM, or omit it from raw HTML when it is set dynamically; Google evaluates canonicals before and after rendering (update 2025-12-17).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/updates
BAD: raw HTML canonical `https://example.com/page?ref=nav`, rendered canonical `https://example.com/page`
GOOD: both `https://example.com/page`

### SEO-FND-03: Non-commodity content gate
Before publishing or refreshing an informational or commercial page, confirm the main content adds value beyond common knowledge (first-hand experience, original data or benchmarks, expert analysis, or interactive tooling) and meets the four Search Quality Rater main content attributes: Effort, Originality, Talent/Skill, Accuracy (rater guidelines sections 4.6.5 and 4.6.6).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide; https://developers.google.com/search/docs/fundamentals/creating-helpful-content; https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

### SEO-FND-04: No synthetic query fan-out doorway pages
Never generate near-duplicate pages for synthetic query fan-out variants or minor long-tail rephrasings; consolidate sub-questions onto one sectioned page (Scaled Content Abuse and Doorway Abuse policies).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide; https://developers.google.com/search/docs/essentials/spam-policies
BAD: `/best-crm-for-dentists`, `/best-crm-for-dental-offices`, `/top-dental-crm` with the same body
GOOD: one `/dental-practice-crm` page with `<h2>` sections per sub-question

### SEO-FND-05: Question-matched title and opening paragraph
Align `<title>`, the primary `<h1>`/`<h2>` headings, and the opening 40-80 word paragraph with the core question and its sub-queries; state verifiable facts, explicit prices, and dates. Measured within-site AI citation lift: +14.1% to +33.6% per SD for title match, +15.5% to +25.7% per SD for best-paragraph match; cited pages have 11.9x the odds of uncited sitemap pages.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2610.15033; https://arxiv.org/abs/2607.14035
BAD: `<title>Welcome to Our Blog | Example</title>`
GOOD: `<title>How Much Does Kanban Software Cost in 2026? | Example</title>` + lead paragraph with the price range

### SEO-FND-06: No body-only stylistic GEO rewrites
Do not apply automated fluency, tone, or quote-stuffing rewrites to pages that already rank or get retrieved; in end-to-end tests they reduced top-20 retrieval by about 9%, top-10 reranking by 16%, and citation by 6%. Limit edits to factual enrichment, explicit question answering, and heading clarity.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2607.14035

### SEO-FND-07: Human fact-check and AI labeling of generated content
When generative AI drafts content, a human verifies every claim in body text and in all search-facing metadata (`<title>`, `<meta name="description">`, JSON-LD, `alt`) before publication. AI-generated product images for Merchant Center carry IPTC `DigitalSourceType` = `TrainedAlgorithmicMedia` [LITERAL: 2026-11-03]; AI-generated product titles and descriptions use the Merchant Center AI-generated attribute.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

### SEO-FND-08: Active structured data scope and visible parity
Use JSON-LD only from the 24 active Google Search Gallery features (plus `Book` for Book actions, `Dataset` for Dataset Search), matching visible text 1:1. Use `Organization`, `ProfilePage`, `Article`, `Product` for entity disambiguation and rich-result eligibility; schema alone does not raise AI citation (-5.3% within-site effect).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/structured-data/search-gallery; https://developers.google.com/search/docs/fundamentals/ai-optimization-guide; https://arxiv.org/abs/2610.15033

### SEO-FND-09: No retired rich-result schema types
Do not generate or recommend retired types for rich results: `FAQPage` (retired 2026-05-07, docs removed 2026-06-15), Practice Problem (removed 2026-01-06), standalone Course Info, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing (docs removed 2025-09-09), `ClaimReview` (retired 2025-06), `HowTo`, Sitelinks Search Box.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/updates
BAD: `{"@type": "FAQPage", "mainEntity": [...]}`
GOOD: visible Q&A sections in HTML without `FAQPage` markup

### SEO-FND-10: Dual first-party AI visibility measurement
Measure AI search performance with both the GSC Generative AI performance report (AI Overview and AI Mode impressions, `Web: text-based` and `Web: multimodal`) and Bing Webmaster Tools AI Performance (Grounding Queries, Citation Share, Intents, Topics, Compare); GSC does not expose grounding sub-queries and Bing does not cover Google AI surfaces.
Evidence: [VERIFIED]
Sources: https://support.google.com/webmasters/answer/16984139; https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/

### SEO-FND-11: Two-track brand vs niche discovery strategy
For unknown or niche brands (LLM prior recognition 2-16% in ChatGPT), prioritize citations on third-party comparison and industry pages that name the brand (ChatGPT naming odds x39.7, Gemini x17.7) plus sub-query retrieval optimization. For established brands (46% of ChatGPT mentions come from model memory without citation), monitor and correct entity associations in authoritative reference sources.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2610.15033

### SEO-FND-12: UGC and outbound link qualification
Set `noindex` on unvetted user-generated link-shared pages not meant for Search (spam update 2026-10-26); mark paid, sponsored, or incentivized outbound links `rel="sponsored"` or `rel="nofollow"` and user-submitted links `rel="ugc"`.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/essentials/spam-policies; https://developers.google.com/search/updates
BAD: `<a href="https://example.org/partner">partner tool</a>` in a paid placement
GOOD: `<a href="https://example.org/partner" rel="sponsored">partner tool</a>`

## Demand (DMD)

### SEO-DMD-01: Google Ads keyword ideas seed and parameter limits
For `POST https://googleads.googleapis.com/v26/customers/{customer_id}:generateKeywordIdeas` [LITERAL: 2026-11-03]: pass 1 to 20 strings in `keyword_seed` (or `keyword_and_url_seed`) or use `site_seed` (up to 250,000 ideas); at most 10 `geo_target_constants[]`; `page_size` at most 10,000; `keywordPlanNetwork` = `GOOGLE_SEARCH` for pure Google demand; request `KEYWORD_CONCEPT` annotations and `include_average_cpc = true` (history up to 4 years, default 12 months). Not scripted in this skill (needs Ads developer token); use `dataforseo/query.py search-volume` as paid fallback.
Evidence: [VERIFIED]
Sources: https://developers.google.com/google-ads/api/docs/keyword-planning/generate-keyword-ideas

### SEO-DMD-02: Google Trends scaling and comparison cap
Never compare separate 0-100 rescaled Google Trends web UI exports without one shared anchor term in every batch (max 8 terms per UI comparison [LITERAL: 2026-11-03]). With programmatic access, use the Google Trends API alpha (5-year / 1,800-day rolling window, consistent scaling at daily, weekly, monthly, yearly intervals) or the Google Trends BigQuery public dataset.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/apis/trends

### SEO-DMD-03: Three-pillar demand triangulation
Before recommending a new product, book, course, app, or pillar content build, validate demand with three independent signals: 1) volume or category sales depth (Keyword Planner, DataForSEO Labs, marketplace best-seller rank), 2) non-declining 24-60 month trajectory (Google Trends or Pinterest Trends), 3) verifiable supply gap or user pain (autocomplete modifiers, top-5 results that are forums or outdated, 1-3 star review complaints).
Evidence: [VERIFIED]
Sources: https://developers.google.com/google-ads/api/docs/keyword-planning/generate-keyword-ideas; https://developers.google.com/search/apis/trends; https://kdp.amazon.com/en_US/help/topic/G201298500

### SEO-DMD-04: YouTube search.list quota and sort discipline
Keep `GET https://www.googleapis.com/youtube/v3/search` at most 100 calls per day (documented as a separate Search Queries bucket of 100 calls; older documentation states 100 units per call of the 10,000-unit project quota; both give 100 searches per day), `maxResults` 0-50. Use `order=relevance` for topic discovery (other sort orders can return incomplete sets with date filters); use `playlistItems.list` for a channel's uploads; URL-escape the OR operator `|` as `%7C`.
Evidence: [VERIFIED]
Sources: https://developers.google.com/youtube/v3/docs/search/list

### SEO-DMD-05: Pinterest Trends window, cap, and seasonal lead time
Pinterest Trends: 2-year history indexed 0-100, 90-day daily window for business audiences; compare at most 4 keywords per query; publish seasonal content in the "approaching" phase, 45-90 days before peak, not at peak.
Evidence: [VERIFIED]
Sources: https://help.pinterest.com/en/business/article/pinterest-trends

### SEO-DMD-06: SERP-overlap clustering
Group keywords that share at least 3 of the top-10 organic URLs into one canonical page (secondary keywords become `<h2>` sections); create separate pages only when shared top-10 URLs are fewer than 3. Never create separate pages for close variants or fan-out rephrasings (SEO-FND-04).
Evidence: [VERIFIED] (Google doorway policy) / [COMMUNITY] (3-URL threshold)
Sources: https://searchengineland.com/keyword-clustering-tool-python-483977; https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
BAD: separate pages for "kanban board app" and "kanban board software" (7 shared top-10 URLs)
GOOD: one page; second keyword as `<h2>` section

### SEO-DMD-07: AI Overview displacement pivot for question queries
AI Overviews trigger on 64.7% of question-phrased queries; do not plan standalone commodity definition articles (SEO-FND-03). For high-AI-Overview question clusters, build an interactive tool or calculator, original benchmark, first-hand case study, or downloadable template.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2607.14035; https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

### SEO-DMD-08: Search-safe naming gate
Every proposed product, brand, book, show, episode, or app name passes: 1) exact-match SERP and store collision check (no dominant unrelated entity in top 5); 2) platform limits and bans (KDP title + subtitle < 200 characters [LITERAL: 2026-11-03] without "bestselling", "free", or competitor authors; App Store and Google Play title at most 30 characters [LITERAL: 2026-11-03] without "#1", "Free", emoji, or ALL-CAPS claims on Play; Google Business Profile real-world name only); 3) distinctive handle plus query-matched subtitle or descriptor.
Evidence: [VERIFIED]
Sources: https://kdp.amazon.com/en_US/help/topic/G201097560; https://developer.apple.com/app-store/product-page/; https://support.google.com/googleplay/android-developer/answer/9898842?hl=en; https://support.google.com/business/answer/3038177?hl=en; https://arxiv.org/abs/2610.15033

### SEO-DMD-09: LLM brand prior check before naming or category expansion
Before finalizing a brand name or extending a brand into a new category, ask target LLMs without search whether the name carries a conflicting category association; such associations reduced top-3 AI recommendation rates by up to 33 percentage points on identical product facts.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2610.15033

### SEO-DMD-10: Descriptive hyphenated filenames and URL slugs
Name downloadable files, images, PDFs, and URL slugs with lowercase descriptive keywords separated by hyphens, never underscores or opaque IDs (crawlable URL structure update 2026-10-23).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/updates; https://developers.google.com/search/docs/appearance/google-images
BAD: `IMG00023.JPG`, `/p?id=8812`, `kanban_guide.pdf`
GOOD: `autumn-leaves-photo.jpg`, `/kanban-board-guide`, `kanban-board-guide.pdf`

## Text and Book Media (MTX)

### SEO-MTX-01: Self-referential absolute canonical
Every indexable HTML page includes a self-referential `<link rel="canonical" href="https://...">` in `<head>` with an absolute HTTPS URL; never a relative path or fragment; never `robots.txt` or `noindex` as a substitute.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
BAD: `<link rel="canonical" href="/guide#intro">`
GOOD: `<link rel="canonical" href="https://example.com/guide">`

### SEO-MTX-02: Concise headed structure for AI selection
Use question-matched `<title>` and `<h1>`/`<h2>` headings (x1.28 ChatGPT selection odds at equal rank) and concise, fact-dense paragraphs (x0.59 odds per SD of excess word length); avoid generic listicles (x0.54) and shallow comparison roundups (x0.34).
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2610.15033

### SEO-MTX-03: Article thumbnail parity and fake-freshness ban
Use the same high-resolution representative image (no logo, no text overlay, no extreme aspect ratio) in `og:image` and in Schema.org `primaryImageOfPage` or `Article.image` (update 2026-03-02). Never change `dateModified` or visible dates without substantive content changes.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/google-images; https://developers.google.com/search/docs/fundamentals/creating-helpful-content

### SEO-MTX-04: PDF canonical and hreflang via HTTP Link header
Published PDFs have a native text layer, a filled PDF `Title` property, and a descriptive hyphenated filename. A PDF that duplicates an HTML page or `.docx` sends `Link: <https://example.com/canonical-url>; rel="canonical"` [LITERAL: 2026-11-03] (RFC 5988); localized PDFs declare `hreflang` through HTTP `Link` headers.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls; https://developers.google.com/search/docs/specialty/international/localized-versions

### SEO-MTX-05: Developer docs Markdown negotiation and /index.md fallback
Documentation sites serve Markdown (`Content-Type: text/markdown; charset=utf-8`, `Vary: Accept`, YAML frontmatter `title`/`description`/`image`, fenced JSON-LD; decompressed HTML < 6 MiB / 6,291,456 bytes [LITERAL: 2026-11-03]) when `Accept: text/markdown` is requested (up to 80% fewer tokens), and expose `{page-url}/index.md` for agents that do not send the header.
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/agent-readiness/; https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
Check: `agent-readiness/check.py URL --site-type B`

### SEO-MTX-06: Hierarchical llms.txt for large documentation sites
Above about 200 documentation pages, split into a root `/llms.txt` index pointing to per-directory `/{section}/llms.txt` files whose entries link to `/index.md` URLs with frontmatter descriptions; omit pages that only list links.
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/agent-readiness/

### SEO-MTX-07: img src, alt text, and inline SVG title
Embed content images with `<img src="..." alt="...">` (or `<picture>`/`srcset` with an `<img src>` fallback) in BMP, GIF, JPEG, PNG, WebP, SVG, or AVIF; never CSS `background-image`. Write descriptive non-stuffed `alt`; inline SVGs use `<svg aria-labelledby="..."><title id="...">`; use `<image:loc>` sitemaps for images on cross-domain CDNs.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/google-images
BAD: `<div style="background-image:url(chart.png)"></div>`, `alt="chart chart graph best chart"`
GOOD: `<img src="/img/kanban-cycle-time-chart.png" alt="Cycle time per column over 12 weeks">`

### SEO-MTX-08: Merchant Center AI image IPTC labeling
AI-generated product images for Google Merchant Center or product pages embed IPTC `DigitalSourceType` = `TrainedAlgorithmicMedia` [LITERAL: 2026-11-03].
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

### SEO-MTX-09: Amazon KDP title, subtitle, series, and description compliance
KDP: title + subtitle < 200 characters [LITERAL: 2026-11-03] (main title at most 60 characters recommended), matching cover text 1:1; series number digits only (`3`, not "Book 3"); no series for public-domain or low-content books; descriptions without URLs, email or physical addresses, phone numbers, reviews, quotes, testimonials, review requests, price or availability, or keyword tags; publisher field without "Amazon", "Kindle", "KDP", or URLs.
Evidence: [VERIFIED]
Sources: https://kdp.amazon.com/en_US/help/topic/G201097560; https://kdp.amazon.com/en_US/help/topic/G201298500
BAD: subtitle "Book 2 of the Example Series - Visit example.com"
GOOD: subtitle "A Field Guide to Team Workflow Design"; series number `2`

### SEO-MTX-10: Amazon KDP 7 keyword slots and 3 categories
Fill up to 7 keyword slots with 2-3 word phrases in natural reader order without quotation marks; omit words already in title, subtitle, contributors, or the 3 selected categories; exclude other authors or books, "bestselling", "free", "new", "on sale", "available now", "book", "Kindle+", "KDP Select", spacing or plural duplicates, HTML tags. Set Reading Age (0-2, 3-5, 6-8, 9-12, 13-17; 12-15 on Amazon.de) for children's and teen categories (72-hour category display window).
Evidence: [VERIFIED]
Sources: https://kdp.amazon.com/en_US/help/topic/G201298500; https://kdp.amazon.com/en_US/help/topic/G200652170
Check: `prepublish-lint.py` platform `kdp`

### SEO-MTX-11: Apple Books RTF description, primary contributor, accessibility
Apple Books: UTF-8 description of at least 50 characters in RTF with zero HTML tags; 1 main + 1 secondary BISAC/BIC category; all display contributors marked Primary; numeric series number; phonetic title and subtitle for Japanese and Chinese; fill Accessibility Features (landmark navigation, semantic roles, alternative text, MathML, high contrast, accessible color).
Evidence: [VERIFIED]
Sources: https://itunespartner.apple.com/books/support/12-metadata
Check: `prepublish-lint.py` platform `apple-books`

### SEO-MTX-12: Google Play Books immutable ID, genres, contiguous series
Never change a live book's identifier or ISBN (deactivates the book and deletes ratings and reviews); 1-3 genres from one subject standard (BISAC recommended, most relevant first); identical series name spelling and contiguous volume integers (no gaps, no overlap) for automated series pages (48-hour window); link alternate-format ISBNs in Related books; declare human vs synthesized narration on audiobooks.
Evidence: [VERIFIED]
Sources: https://support.google.com/books/partner/answer/3237055?hl=en

### SEO-MTX-13: Kobo link ban, series separation, author consistency
Kobo Writing Life: up to 50 contributors (1 per field) with identical author spelling across all books; never put series names or volume numbers in title or subtitle; remove all website links, contact data, and social handles from every metadata field and the cover (external links only inside the EPUB).
Evidence: [VERIFIED]
Sources: https://kobowritinglife.zendesk.com/hc/en-us/articles/360058975792-Metadata-Guidelines
Check: `prepublish-lint.py` platform `kobo`

### SEO-MTX-14: ONIX 3.1 master feed and overwrite prevention
Generate trade feeds in ONIX 3.1 (3.1.2) or 3.0.8 validated against EDItEUR XSD (never ONIX 2.1); include BISAC + Thema 1.7 subjects and Codelist 196 accessibility; edit metadata in the master ONIX source so later deliveries do not overwrite store portal settings.
Evidence: [VERIFIED]
Sources: https://www.editeur.org/83/overview/; https://support.google.com/books/partner/answer/3237055?hl=en

## Audio, Video, Social, Apps, Local Business, Localization (MAV)

### SEO-MAV-01: YouTube relevance, watch time, chapters
Optimize for the three documented YouTube search elements: relevance (title, description, spoken script and captions match the query), engagement (deliver the promised answer early; query-specific watch time and percentage viewed), quality (topical channel depth). Add description timestamps starting at `00:00` with at least 3 segments of at least 10 seconds for chapters and Google Key Moments.
Evidence: [VERIFIED]
Sources: https://support.google.com/youtube/answer/16090438?hl=en; https://support.google.com/youtube/answer/11914225?hl=en&co=YOUTUBE._YTVideoType%3Dvideo; https://developers.google.com/search/docs/appearance/video

### SEO-MAV-02: Google video watch page, stream, thumbnail
For Google video features, embed each video on an indexed dedicated watch page (`<video>`, `<embed>`, `<iframe>`, `<object>`; never `#fragment` or `data:` URLs); Googlebot can fetch the bytes (21 formats) at a stable `contentUrl`; stable thumbnail at least 60x30 pixels with at least 80% of pixels at alpha > 250 [LITERAL: 2026-11-03]; `VideoObject` + `Clip` (all languages) or `SeekToAction` (12 languages); `BroadcastEvent` for live streams.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/video

### SEO-MAV-03: Apple Podcasts title indexing and anti-stuffing
Apple Podcasts search indexes only show name, channel name, and episode title (not ratings, reviews, shares, descriptions). Front-load the episode topic or guest in `<title>`, no emojis, no repeated generic titles, never extra keywords (grounds for directory removal). RSS `<description>` at most 4,000 bytes [LITERAL: 2026-11-03] inside `<![CDATA[...]]>`; updates propagate within 24 hours.
Evidence: [VERIFIED]
Sources: https://podcasters.apple.com/support/3686-search-on-apple-podcasts; https://help.apple.com/itc/podcasts_connect/#/itcb54353390
BAD: `<title>Episode 42 - Productivity Tips Productivity Hacks Best Productivity</title>`
GOOD: `<title>Kanban for Remote Teams with Jane Smith</title>`

### SEO-MAV-04: Podcast transcripts, show notes HTML, companion page
Include `<podcast:transcript>` (`.vtt`/`.srt`) and `<podcast:chapters>` (`xmlns:podcast="https://podcastindex.org/namespace/1.0"`); Spotify show notes only with `<h1>`, `<h2>`, `<ul>`, `<ol>`, `<li>`, `<p>`, `<b>`, `<i>`, `<a href="https://...">`; publish a companion HTML episode page with the full transcript and question-matched `<h2>` headings.
Evidence: [VERIFIED]
Sources: https://support.spotify.com/us/creators/article/podcast-specification-doc/; https://github.com/podcastindex-org/podcast-namespace

### SEO-MAV-05: GSC social and video platform properties, LinkedIn SEO fields
Verify owned TikTok, Instagram, X, and YouTube accounts as Search Console platform properties (feature 2026-07-29); watch the 24-hour filter and format comparisons (`/watch` vs `/shorts/`, `/p/` vs `/reels/`). On LinkedIn articles set the custom SEO title at most 60 characters and SEO description 140-160 characters [LITERAL: 2026-11-03].
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/monitor-debug/analyze-social-video-content; https://www.linkedin.com/help/linkedin/answer/a6244140

### SEO-MAV-06: Apple App Store lexical limits and keyword field
App Name at most 30, Subtitle at most 30, Promotional Text at most 170 (not indexed, never for keywords), Keywords at most 100 characters [LITERAL: 2026-11-03], comma-separated without spaces around commas (`Property,House,Real Estate`), omitting words from name, subtitle, or category, plurals of included singulars, "app", "game", filler words, `#`/`@`, trademarks, celebrity and competitor names. In-app purchase name at most 35, description at most 55 (up to 20 items); unique keyword sets per Custom Product Page.
Evidence: [VERIFIED]
Sources: https://developer.apple.com/app-store/search/; https://developer.apple.com/app-store/product-page/
Check: `prepublish-lint.py` platform `apple-app-store`

### SEO-MAV-07: Google Play lexical limits and anti-promotional policy
Across all translations: title at most 30, short description at most 80, full description at most 4,000 characters [LITERAL: 2026-11-03]; short description not repeated in the full description; no emojis, emoticons, or repeated special characters in title, icon, developer name; no non-brand ALL CAPS, keyword blocks, unattributed testimonials, or ranking, award, price, or deal claims ("#1", "App of the year", "Best of Play", "Popular", "Free", "No Ads", "10% off", "$50 cash back") in text or graphics.
Evidence: [VERIFIED]
Sources: https://support.google.com/googleplay/android-developer/answer/9898842?hl=en; https://support.google.com/googleplay/android-developer/answer/13393723?hl=en
Check: `prepublish-lint.py` platform `google-play`

### SEO-MAV-08: Google Business Profile real-world name
GBP Name is the real-world name on signage and stationery, without the 11 prohibited additions: 1) taglines, 2) store codes, 3) `®` symbols, 4) non-acronym ALL CAPS, 5) hours ("Open 24 hours", "(Closed)"), 6) phone numbers or URLs, 7) special characters (`%$@/"`) or legal suffixes (LLC, LTD, INC) not on signage, 8) service or product descriptors, 9) highway or landmark directions, 10) containment ("(inside Best Buy)"), 11) repeated bilingual script transliterations (even when on signage).
Evidence: [VERIFIED]
Sources: https://support.google.com/business/answer/3038177?hl=en
BAD: `Example Plumbing - 24/7 Emergency Plumber Austin`
GOOD: `Example Plumbing`

### SEO-MAV-09: Google Business Profile description, category, service area
GBP description without links of any type and without price or sale promotions; choose the fewest, most specific categories completing "This business IS a" (not "HAS a"); service-area businesses without storefront hide the street address and keep the area within about 2 hours driving time [LITERAL: 2026-11-03]; never virtual offices or P.O. boxes.
Evidence: [VERIFIED]
Sources: https://support.google.com/business/answer/3038177?hl=en; https://support.google.com/business/answer/7091?hl=en
Check: `prepublish-lint.py` platform `gbp`

### SEO-MAV-10: Offline-to-online vanity URL, QR redirect, physical events
Every print, packaging, or booth touchpoint gets a typable short vanity URL (`example.com/slug`) and a first-party QR code that 301-redirects server-side to an HTTPS landing page with `utm_source`, `utm_medium`, `utm_campaign` and a clean self-referential canonical. `Event` JSON-LD only for events bookable by the public at a physical location.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls; https://developers.google.com/search/docs/appearance/structured-data/search-gallery

### SEO-MAV-11: Bidirectional hreflang with ISO codes
Use one method (HTML `<link>`, HTTP `Link` header for PDFs, or sitemap `<xhtml:link>`) with absolute `https://` URLs, self-referential and return links, same-language self-canonicals, `x-default`, and ISO 639-1 language + optional ISO 3166-1 Alpha 2 region (ISO 15924 script for `zh-Hans`/`zh-Hant`). Never country codes alone (`be` = Belarusian), numeric regions (`es-419`), or reserved codes (`en-UK` instead of `en-GB`, `EU`, `UN`).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/specialty/international/localized-versions
BAD: `<link rel="alternate" hreflang="en-UK" href="/uk/">`
GOOD: `<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/">`

### SEO-MAV-12: Native keyword research per language and IndexNow push
Research keyword demand natively per language and market before localizing (never translate keywords literally); localize text-bearing app screenshots and image filenames; push updated international URLs with IndexNow (up to 10,000 URLs per POST) to Bing, Yandex, Naver, Seznam, Yep.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/specialty/international/localized-versions; https://www.indexnow.org/documentation; https://support.google.com/googleplay/android-developer/answer/13393723?hl=en
Script: `indexnow/submit.py submit --file urls.txt --host example.com`

## Agent Discoverability (AGT)

### SEO-AGT-01: robots.txt and Sitemap baseline
Every public site serves HTTP 200 `/robots.txt` with at least one `Sitemap: https://.../sitemap.xml` line, and the sitemap carries accurate `<lastmod>` values; robots.txt (78% adoption in the top 200,000 domains) is the first endpoint crawlers and AI agents read.
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/agent-readiness/
Check: `agent-readiness/check.py URL`

### SEO-AGT-02: Three-class AI crawler separation
Separate AI user agents in robots.txt and CDN/WAF policies: 1) allow search and grounding crawlers (`Googlebot`, `Bingbot`, `OAI-SearchBot`, `PerplexityBot`, `Applebot`) on all public pages meant for search or AI citation; 2) configure training crawlers (`GPTBot`, `Google-Extended`, `ClaudeBot`, `Applebot-Extended`, `CCBot`, `Meta-ExternalAgent`) by training policy without blocking class 1; 3) allow user-triggered fetchers (`ChatGPT-User`, `Claude-Web`, `Perplexity-User`, `Google-NotebookLM`, `Google-CWS`, `Google-Pinpoint`).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/ai-features; https://developers.google.com/search/updates; https://contentsignals.org/
BAD: `User-agent: *` + `Disallow: /` to stop AI training
GOOD: `User-agent: GPTBot` + `Disallow: /` and `User-agent: OAI-SearchBot` + `Allow: /`
Check: `agent-readiness/check.py URL`

### SEO-AGT-03: Content-Signal directive
Declare AI usage preferences in `/robots.txt` (or a `Content-Signal` response header) with the exact syntax `Content-Signal: [optional-path] ai-train=yes|no, search=yes|no, ai-input=yes|no` [LITERAL: 2026-11-03]; to opt out of training while keeping search and grounding use `ai-train=no, search=yes, ai-input=yes`, with the EU Directive 2019/790 Article 4 reservation comment. Never `search=no` on pages meant to rank.
Evidence: [VERIFIED]
Sources: https://contentsignals.org/; https://blog.cloudflare.com/agent-readiness/
GOOD: `Content-Signal: ai-train=no, search=yes, ai-input=yes`
Check: `agent-readiness/check.py URL`

### SEO-AGT-04: Markdown content negotiation and Vary: Accept
On `Accept: text/markdown`, serve `Content-Type: text/markdown; charset=utf-8` (up to 80% fewer tokens; decompressed HTML at most 6 MiB / 6,291,456 bytes [LITERAL: 2026-11-03]); always send `Vary: Accept` so caches do not serve Markdown to browsers; prepend YAML frontmatter (`title`, `description`, `image`); keep JSON-LD as a fenced `json` block at the end.
Evidence: [VERIFIED]
Sources: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
Check: `agent-readiness/check.py URL`

### SEO-AGT-05: /index.md fallback and non-recursive agent banner
Only 3 of 7 tested coding agents send `Accept: text/markdown` by default; expose every documentation page at `{page-url}/index.md`. An HTML banner that points agents to `/index.md` or `/llms.txt` must be removed from the Markdown output to prevent loops.
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/agent-readiness/
Check: `agent-readiness/check.py URL --site-type B`

### SEO-AGT-06: llms.txt scope for coding and documentation agents
Use `/llms.txt` only for coding and documentation agents (Google Search ignores it; never a ranking tactic); split large sets into root and per-directory files that fit one context window (31% fewer tokens, 66% faster answers); omit pages that only list links; `/llms.txt` returns `text/plain` or `text/markdown`, never a soft-404 HTML page; 301/302-redirect training crawlers from deprecated `/v1/` docs to current docs.
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/agent-readiness/; https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
Check: `agent-readiness/check.py URL --site-type B`

### SEO-AGT-07: API catalog (RFC 9727) for public APIs
Sites with public HTTP APIs publish `/.well-known/api-catalog` (`Content-Type: application/linkset+json`, RFC 9264) linking each API's OpenAPI or AsyncAPI description (`rel="service-desc"`), documentation (`rel="service-doc"`), and status (`rel="status"`), and send `Link: </.well-known/api-catalog>; rel="api-catalog"` [LITERAL: 2026-11-03] (RFC 8288).
Evidence: [VERIFIED]
Sources: https://datatracker.ietf.org/doc/html/rfc9727; https://blog.cloudflare.com/agent-readiness/
Check: `agent-readiness/check.py URL --site-type D`

### SEO-AGT-08: MCP server card and agent skills index
Sites that expose an MCP server or coding skills publish `/.well-known/mcp/server-card.json` (and `/.well-known/mcp.json`; `$schema: "https://static.modelcontextprotocol.io/schemas/mcp-server-card/v1.json"`, `protocolVersion: "2025-06-18"`, `transport.type: "streamable-http"`) and/or `/.well-known/agent-skills/index.json` (RFC 8615).
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/agent-readiness/; https://isitagentready.com/
Check: `agent-readiness/check.py URL --site-type D`

### SEO-AGT-09: OAuth protected resource metadata (RFC 9728)
SaaS applications, gated portals, and authenticated MCP servers expose `/.well-known/oauth-protected-resource` (RFC 9728) and `/.well-known/oauth-authorization-server` (RFC 8414) with `WWW-Authenticate` challenges so user-authorized agents use scoped OAuth instead of shared browser cookies.
Evidence: [VERIFIED]
Sources: https://datatracker.ietf.org/doc/html/rfc9728; https://blog.cloudflare.com/agent-readiness/
Check: `agent-readiness/check.py URL --site-type D`

### SEO-AGT-10: WebMCP for interactive ecommerce storefronts
Interactive storefronts where browser agents search catalogs and build carts expose client-side tools (`search_products`, `add_to_cart`) through `document.modelContext` / `/.webmcp/bridge.js` (`data-mcp-url` pointing to the store MCP endpoint) with a fallback when WebMCP is unsupported.
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/webmcp-commerce/

### SEO-AGT-11: Entity graph anchoring and third-party co-occurrence
To build LLM brand memory (46% of ChatGPT mentions without citation; x5.8 naming odds from prior) and close the niche discovery gap (3.32% organic discovery vs 99.4% name recognition; x39.7 ChatGPT / x17.7 Gemini lift from third-party citation): publish `Organization` + `ProfilePage` JSON-LD with `sameAs` (Wikidata, Wikipedia, GitHub, official social profiles) and identifiers (`iso6523Code`, `duns`, `leiCode`, `vatID`); keep one identical 1-sentence brand-to-category definition on all surfaces; earn factual mentions on independent comparison and benchmark pages.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2610.15033; https://arxiv.org/abs/2607.14035; https://developers.google.com/search/docs/appearance/structured-data/search-gallery

### SEO-AGT-12: AI operator activity and mention vs citation gap monitoring
Monthly, check server or CDN logs and answer-engine panels for: 1) crawl-to-referral ratio and 403/404 errors per AI operator (OpenAI, Anthropic, Google, Microsoft, Perplexity); 2) mention rate vs citation rate gap (brand named without domain cited -> fix crawl access and title/lead question matching on owned pages).
Evidence: [VERIFIED]
Sources: https://blog.cloudflare.com/aeo/

## Audit (AUD)

### SEO-AUD-01: Pre-audit hygiene gate
Before diagnosing decay or scoring a URL, verify: 1) HTTP 200, indexed, snippets allowed, consistent pre/post-JS canonical, property set to "Include" in GSC Search generative AI control (1-2 day propagation); 2) the drop did not follow an owned page or template edit recorded in GSC Annotations (up to 200 per property, 120 characters, 500-day expiry); 3) GSC clicks and analytics (Plausible or GA4) agree on the drop.
Evidence: [VERIFIED]
Sources: https://support.google.com/webmasters/answer/16908024; https://support.google.com/webmasters/answer/16530728?hl=en; https://searchengineland.com/guide/content-decay
Script: `google-search-console/query.py inspect SITE URL`

### SEO-AUD-02: 3-month YoY window and 2025 impression anomaly
Diagnose decay with a 3-month year-over-year comparison (last 3 months vs same months 12 months earlier); it cancels seasonality and fits GSC 16-month retention [LITERAL: 2026-11-03]. For May-September 2025 baselines, anchor on clicks and live SERP inspection, because the May 2025 impression logging bug and the September 2025 `&num=100` removal inflated earlier impressions.
Evidence: [VERIFIED] (window) / [COMMUNITY] (anomaly handling)
Sources: https://searchengineland.com/content-decay-types-fix-482486
Script: `google-search-console/query.py decay SITE`

### SEO-AUD-03: First-party plus answer-engine gap audit for AI visibility
Combine: 1) GSC Generative AI performance report (rolled out 2026-08-31, 1,000-row UI cap, Pacific Time, `Web: text-based` and `Web: multimodal` filters); 2) Bing AI Performance (Grounding Queries, Citation Share, Intents, Topics, Compare); 3) mention rate vs citation rate gap. When mention rate is far above citation rate or Bing Citation Share is below 15% [ASSUMED], prioritize title and lead question matching (SEO-FND-05), the 4 competitive gatekeepers (SEO-CMP-04), and crawler access (SEO-AGT-01..04).
Evidence: [VERIFIED]
Sources: https://support.google.com/webmasters/answer/16984139; https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/; https://blog.cloudflare.com/aeo/; https://arxiv.org/abs/2605.25517

### SEO-AUD-04: Four-signature decay classification
Classify each decaying page (at least 20% 3-month YoY click loss and at least 50 lost clicks [ASSUMED]): 1) ranking decay (clicks down, impressions down, position worse) -> REFRESH with information gain + internal links; 2) zero-click capture (clicks down, impressions flat or up, position flat or better, AI Overview or SERP feature present) -> never a routine text refresh; UPGRADE to tool or dataset or shift effort to conversion pages; 3) intent drift (clicks down, SERP format changed) -> RE-FORMAT on the same URL; 4) demand decay (clicks and impressions down, position flat or better, confirmed in Google Trends) -> CONSOLIDATE via 301 or PRUNE.
Evidence: [VERIFIED] / [COMMUNITY] (thresholds [ASSUMED])
Sources: https://searchengineland.com/content-decay-types-fix-482486; https://arxiv.org/abs/2607.14035
Script: `google-search-console/query.py decay SITE`

### SEO-AUD-05: Cannibalization, 301 consolidation, safe pruning
Before creating or refreshing a page, check whether 2 or more owned URLs compete for the same query cluster (at least 3 shared top-10 URLs per SEO-DMD-06, or split impressions in GSC). If yes, merge unique content into the strongest URL, 301-redirect, set canonical, update internal links. PRUNE (HTTP 410 or `noindex`) only when the page is at least 12 months old [ASSUMED] AND has 0 clicks (< 50 impressions in 90 days [ASSUMED]), 0 AI citations, 0 external referring domains, 0 conversions, and no parent topic for a 301.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls; https://searchengineland.com/content-decay-types-fix-482486; https://searchengineland.com/guide/content-decay
Script: `google-search-console/query.py cannibalization SITE`

### SEO-AUD-06: Gated multiplicative opportunity score (MOS)
Rank audit fixes and new content candidates in one queue every 4-6 weeks with `MOS = 100 * ((D^0.20 * I^0.25 * F^0.25 * B^0.20 * C^0.10) / 5) * G_gate` and `MOS_ROI = (MOS * Confidence) / Effort_Hours` [ASSUMED]; no composite score has longitudinal causal proof. `G_gate = 0` when business relevance `B = 1` or unresolvable cannibalization `I = 1`. Prefer striking-distance updates (position 4.0-15.9, `F = 4-5`) over cold-start articles of equal `B`. Use the free-data fallback (GSC, Bing, Google Trends, browser SERP check, Plausible) when paid credits are unavailable. Rubrics: `SEO_CHECKS.md`.
Evidence: [VERIFIED] (inputs) / [ASSUMED] (formula and weights)
Sources: https://arxiv.org/abs/2607.14035; https://arxiv.org/abs/2610.15033; https://support.google.com/webmasters/answer/16984139

### SEO-AUD-07: Monitoring alert thresholds
Alert on: 1) at least 200% [ASSUMED] 24-hour Google click surge on a verified social or video property; 2) at least 5% [ASSUMED] 7-day drop in indexed pages, or more than 1% [ASSUMED] HTTP 403 rate for class 1 crawlers; 3) at least 20% [ASSUMED] 3-month YoY click loss on top-50 pages; 4) at least 25% [ASSUMED] 30-day drop in Bing Citation Share or GSC Generative AI impressions; 5) training bot crawl-to-referral ratio above 1,000:1 with fewer than 10 referrals per month [ASSUMED].
Evidence: [VERIFIED] (signals) / [ASSUMED] (thresholds)
Sources: https://developers.google.com/search/docs/monitor-debug/analyze-social-video-content; https://blog.cloudflare.com/aeo/; https://searchengineland.com/content-decay-types-fix-482486

## Campaigns (CMP)

### SEO-CMP-01: Baseline freeze, annotation, external changelog
Before any SEO, refresh, or cross-media campaign, export and freeze a 28-day and a 3-month YoY baseline (GSC clicks, impressions, position; GSC Generative AI impressions; Bing Citation Share; Plausible conversions). On deployment day add a GSC Annotation (at most 120 characters, max 200 per property, 500-day retention, not editable) [LITERAL: 2026-11-03] and mirror it into an external versioned changelog; GSC hides annotations in Compare mode and the 24-hour view.
Evidence: [VERIFIED]
Sources: https://support.google.com/webmasters/answer/16530728?hl=en; https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/; https://searchengineland.com/guide/content-decay

### SEO-CMP-02: Pillar-spoke SERP-overlap gate
In topic cluster campaigns, confirm before drafting that each spoke shares fewer than 3 top-10 URLs with the pillar and every other spoke (SEO-DMD-06); link pillar and spokes in both directions on publish day; never programmatic or fan-out doorway pages (SEO-FND-04).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide; https://developers.google.com/search/docs/essentials/spam-policies

### SEO-CMP-03: Matched-cohort holdout for refresh waves
For a refresh, re-title, or template wave on at least 20 URLs [ASSUMED], hold back a stratified 20% control cohort (at least 5-10 URLs [ASSUMED]) matched by position bucket and click volume for 28 days; evaluate lift by difference-in-differences `(Treated_Post / Treated_Pre) - (Control_Post / Control_Pre)` before rolling out to all pages.
Evidence: [VERIFIED] / [COMMUNITY]
Sources: https://arxiv.org/abs/2607.14035; https://searchengineland.com/guide/content-decay

### SEO-CMP-04: Four competitive GEO gatekeepers on commercial pages
Product launch, comparison, and commercial pages competing for AI citations include the 4 gatekeepers (odds ratios > 100 to > 10,000 across 252,000 trials and 6 LLMs): 1) on-topic query match, 2) explicit published price (never only "Contact us for pricing"), 3) recent genuine timestamp backed by updated substance (SEO-MTX-03), 4) upstream retrieval eligibility and rank (SEO-FND-01, SEO-FND-05); plus technical specifications, direct comparisons, evidence-backed claims. Formatting-only tweaks rank lowest (OR 0.78-1.68).
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2605.25517
BAD: pricing section "Contact sales for a quote"
GOOD: "Team plan: $12 per user per month, billed annually (updated 2026-10)"

### SEO-CMP-05: 24-hour rapid response on social and video properties
In cross-media and launch campaigns, verify owned YouTube, TikTok, Instagram, X accounts as GSC platform properties; check the 24-hour view and "Query groups -> Trending up" during the 7-day post-release window [ASSUMED]; when a post surges (at least 200% day-over-day clicks, SEO-AUD-07), expand the canonical HTML hub or publish a non-overlapping spoke within 48 hours [ASSUMED].
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/monitor-debug/analyze-social-video-content

### SEO-CMP-06: Multi-store lead times and evergreen seasonal URLs
Schedule uploads ahead of propagation: at most 72 hours for KDP categories, at most 48 hours for Google Play Books series bundles, at most 24 hours for Apple Podcasts RSS, 45-60 days [ASSUMED] before peak for seasonal web and Pinterest refreshes. Reuse one year-less evergreen URL for recurring annual campaigns (SEO-DMD-10); 301-redirect legacy year URLs (SEO-AUD-05).
Evidence: [VERIFIED]
Sources: https://kdp.amazon.com/en_US/help/topic/G200652170; https://support.google.com/books/partner/answer/3237055?hl=en; https://help.apple.com/itc/podcasts_connect/#/itcb54353390; https://help.pinterest.com/en/business/article/pinterest-trends
BAD: `/black-friday-2025`, `/black-friday-2026`
GOOD: `/black-friday` updated each year

### SEO-CMP-07: Third-party co-citation for B2B brands
On-page GEO rewrites by many competitors converge to zero-sum (3 of 54 positive), and non-incumbent B2B brands have 3.32% organic LLM discovery; spend launch and comparison campaign effort on factual inclusion (with price and specs) on third-party comparison, benchmark, and documentation pages that are already retrieved (x39.7 ChatGPT, x17.7 Gemini naming lift), plus `Organization` `sameAs` anchoring (SEO-AGT-11).
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2610.15033; https://arxiv.org/abs/2607.14035; https://arxiv.org/abs/2605.25517

### SEO-CMP-08: Multi-run AI visibility measurement
Measure AI outcomes as `Pr(cited) = Pr(search activated | q) * Pr(source retrieved | activated, q) * Pr(cited | retrieved, activated, q)` with at least 8 repetitions per prompt (research range 7-8), several paraphrases, dates, and surfaces (Google AI Overviews and AI Mode, Bing Copilot, ChatGPT, Gemini, Perplexity); canonicalize URLs before aggregation. Reason: daily source overlap (Jaccard) 0.34-0.42, 57.8% of ChatGPT runs do not search, cross-surface overlap 0.11-0.18.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2607.14035; https://blog.cloudflare.com/aeo/

## Metadata (MTD)

### SEO-MTD-01: title and h1 front-loading, script parity, no boilerplate
Each page has a unique `<title>` (no HTML character limit; display target 50-60 characters / about 580 px [ASSUMED]) and one dominant visual `<h1>` that: 1) front-load the primary query and current year or metric, 2) use the same language and script as the page content, 3) contain no site-wide boilerplate or keyword repetition, 4) end with a short brand name after a delimiter (`|`, `:`, `-`).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/title-link; https://arxiv.org/abs/2610.15033
BAD: `<title>Home | Example | Example Software | Best Software</title>`
GOOD: `<title>Kanban Board Templates for Remote Teams (2026) | Example</title>`

### SEO-MTD-02: Meta description, snippet directives, data-nosnippet
Each page has a unique `<meta name="description">` (display target 140-160 characters [ASSUMED]; programmatic key-value summaries allowed on database pages). Pages targeting rich previews and AI grounding set `max-snippet:-1, max-image-preview:large, max-video-preview:-1`. Use `data-nosnippet` only on closed `<span>`, `<div>`, or `<section>` elements in server HTML (never added by JS; `data-nosnippet="false"` still blocks). Keep section content visible (no collapsed tabs, no JS scroll forcing, no hash stripping) so Google can create "Read more" deep links (update 2026-04-20).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/snippet
BAD: `<p data-nosnippet>`
GOOD: `<div data-nosnippet>internal pricing note</div>`

### SEO-MTD-03: og:image and primaryImageOfPage parity, YAML frontmatter
Set `og:title`, `og:description`, `og:image` (at least 1200 px wide, representative, no logo, no overlaid brand text, no extreme aspect ratio) to match `Article.image` / `primaryImageOfPage` 1:1 (preferred thumbnail rule 2026-03-02); the same tags feed Markdown-for-agents frontmatter (`title`, `description`, `image`).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/google-images; https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/

### SEO-MTD-04: Active Schema.org properties and retired-type ban
Generate JSON-LD only from the 24 active Search Gallery types (+ `Book`, `Dataset`), including 2025-2026 `Product` properties (`offers.price`, `category`, `hasAdultConsideration`, `OfferShippingDetails`, `MerchantReturnPolicy`, `validFrom`/`validThrough`/`priceValidUntil`), `VideoObject` `creator`/`author`/`interactionStatistic`, `Event` for physical locations only, single-target non-incentivized `Review`. Remove retired types: `FAQPage`, `HowTo`, `PracticeProblem`, `SpecialAnnouncement`, `CourseInfo`, `EstimatedSalary`, `LearningVideo`, `VehicleListing`, `ClaimReview`.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/structured-data/search-gallery; https://developers.google.com/search/updates
Check: `prepublish-lint.py` (regex 5), `agent-readiness/check.py --site-type C` (Product present)

### SEO-MTD-05: Images, inline SVG, IPTC, PDF headers
Render content images with `<img src alt>` (BMP, GIF, JPEG, PNG, WebP, SVG, AVIF; descriptive hyphenated filename; concise alt; never CSS `background-image`); add `<title>` and `aria-labelledby` to inline `<svg>`; embed IPTC `DigitalSourceType` = `TrainedAlgorithmicMedia` [LITERAL: 2026-11-03] in AI-generated Merchant Center product images; send `Link: <https://...>; rel="canonical"` headers for duplicate PDFs.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/google-images; https://developers.google.com/search/docs/fundamentals/using-gen-ai-content; https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

### SEO-MTD-06: Video thumbnail opacity and chapters
Every web or YouTube video has a stable `contentUrl` (21 formats, no `data:` or `#fragment`), a stable thumbnail at least 60x30 pixels with at least 80% of pixels at alpha > 250 [LITERAL: 2026-11-03], `.srt`/`.vtt` captions, and at least 3 chapters starting at `00:00` (each at least 10 seconds) or `Clip`/`SeekToAction` JSON-LD (`SeekToAction` in 12 languages).
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/appearance/video
GOOD: description lines `00:00 Intro`, `01:15 Board setup`, `04:30 WIP limits`

### SEO-MTD-07: Podcast title indexing, 4,000-byte description, transcripts
Front-load topic and guest in `<item><title>` without keyword stuffing or emojis (Apple indexes only show name, channel name, episode title); `<description>` at most 4,000 bytes inside `<![CDATA[...]]>` [LITERAL: 2026-11-03] (24-hour propagation); Spotify show notes only with `h1, h2, ul, ol, li, p, b, i, a`; include `<podcast:transcript>` and `<podcast:chapters>` plus a full HTML transcript page.
Evidence: [VERIFIED]
Sources: https://podcasters.apple.com/support/3686-search-on-apple-podcasts; https://help.apple.com/itc/podcasts_connect/#/itcb54353390; https://support.spotify.com/us/creators/article/podcast-specification-doc/; https://github.com/podcastindex-org/podcast-namespace
Check: `prepublish-lint.py` platform `podcast`

### SEO-MTD-08: Cross-store book metadata and description variants
Across KDP, Apple Books, Google Play Books, Kobo, ONIX 3.1.2: 1) KDP title + subtitle < 200 characters (main title at most 60), cover text 1:1, no series names or volume numbers in title or subtitle; 2) series number as contiguous positive integer digits; 3) identical author spelling everywhere (Primary on Apple Books; narrator human vs synthesized on Google Play audiobooks; live ISBN on Google Play never changed); 4) link-free and quote-free descriptions in store formats: clean HTML for KDP, Kobo, Play; RTF with zero HTML tags and at least 50 characters for Apple Books; no URLs, emails, phone numbers, social handles, or review quotes anywhere [LITERAL: 2026-11-03].
Evidence: [VERIFIED]
Sources: https://kdp.amazon.com/en_US/help/topic/G201097560; https://itunespartner.apple.com/books/support/12-metadata; https://support.google.com/books/partner/answer/3237055?hl=en; https://kobowritinglife.zendesk.com/hc/en-us/articles/360058975792-Metadata-Guidelines; https://www.editeur.org/83/overview/
Check: `prepublish-lint.py` platforms `kdp`, `apple-books`, `google-play-books`, `kobo`

### SEO-MTD-09: Set-difference keyword packing for KDP and Apple
Fill KDP's 7 keyword slots (at most 50 characters each) and Apple's 100-character keyword field only with words not already in title, subtitle, author or developer, and categories. KDP: 2-3 word natural phrases, no quotation marks, no banned claims ("free", "bestselling", "Kindle", other authors). Apple: singular words or phrases joined by commas with zero spaces around commas (`a,b,c d`), no plurals, no "app", no `#`/`@`, no competitor trademarks [LITERAL: 2026-11-03].
Evidence: [VERIFIED]
Sources: https://kdp.amazon.com/en_US/help/topic/G201298500; https://developer.apple.com/app-store/product-page/
BAD: Apple keywords `planner, tasks, todo app` with name "Example: Task Planner"
GOOD: `todo,checklist,kanban,schedule`
Check: `prepublish-lint.py` set-difference checks

### SEO-MTD-10: App Store 30/30/100/170 and Google Play 30/80/4000
Apple App Store: Name at most 30, Subtitle at most 30, Promotional Text at most 170 (not indexed), Keywords at most 100, in-app purchase name at most 35 and description at most 55 (up to 20). Google Play: Title at most 30, Short Description at most 80, Full Description at most 4,000 without repeating the short description; no emojis in title or developer name; no "#1", "Free", "No Ads", "10% off" in text or graphics; no unattributed testimonials in any translation [LITERAL: 2026-11-03].
Evidence: [VERIFIED]
Sources: https://developer.apple.com/app-store/product-page/; https://support.google.com/googleplay/android-developer/answer/9898842?hl=en; https://support.google.com/googleplay/android-developer/answer/13393723?hl=en
Check: `prepublish-lint.py` platforms `apple-app-store`, `google-play`

### SEO-MTD-11: Google Business Profile name and link-free description
GBP Name equals real-world signage without the 11 banned additions (SEO-MAV-08); choose specific "IS a" categories; service areas within about 2 hours driving; Description at most 750 characters with no links and no price or discount claims [LITERAL: 2026-11-03].
Evidence: [VERIFIED]
Sources: https://support.google.com/business/answer/3038177?hl=en
Check: `prepublish-lint.py` platform `gbp`

### SEO-MTD-12: Social SEO fields and mandatory pre-publish gate
Set LinkedIn article custom SEO Title at most 60 characters and SEO Description 140-160 characters [LITERAL: 2026-11-03]; front-load target queries in the first 60 characters of TikTok, Instagram, YouTube, Pinterest, Reddit posts; run the 20-item pre-publish gate in `SEO_CHECKS.md` before publishing any asset.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/docs/monitor-debug/analyze-social-video-content; https://www.linkedin.com/help/linkedin/answer/a6244140
Check: `prepublish-lint.py` platform `linkedin`

## Tools and Data (TLS)

### SEO-TLS-01: Free-first escalation
Query $0 first-party sources first: GSC Search Analytics and URL Inspection, GSC Generative AI report (UI), GSC social and video properties (UI), Bing Webmaster API and AI Performance (UI), Google Trends (UI or API alpha), YouTube Data API, platform autocomplete, `agent-readiness/check.py`, Plausible Stats API. Escalate to paid DataForSEO only for unowned competitor data, keyword difficulty, bulk unowned SERPs (more than 10 queries), external backlink graphs, or multi-engine LLM prompt panels. Matrix: `SKILL.md`.
Evidence: [VERIFIED]
Sources: https://support.google.com/webmasters/answer/16984139; https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/; https://dataforseo.com/pricing

### SEO-TLS-02: Indexing API only for JobPosting and BroadcastEvent pages
Never call the Google Indexing API (`urlNotifications:publish`) for regular pages, posts, docs, or product pages; it is limited to pages with `JobPosting` or `BroadcastEvent` embedded in a `VideoObject` (200 URLs per day, 100 calls per batch) [LITERAL: 2026-11-03]. For other URLs: IndexNow for Bing, Yandex, Naver, Seznam, Yep (at most 10,000 URLs per POST); for Google, accurate sitemap `<lastmod>` and GSC URL Inspection.
Evidence: [VERIFIED]
Sources: https://developers.google.com/search/apis/indexing-api/v3/quickstart; https://www.indexnow.org/documentation
Script: `indexnow/submit.py`, `google-search-console/query.py inspect`

### SEO-TLS-03: GSC access via service account script
Access Search Console only through `google-search-console/query.py` with a service account (`GSC_SERVICE_ACCOUNT_FILE`); the service account is added as user on each property (Restricted for read, Full for sitemap submit). Derived analyses (`quick-wins`, `ctr-gap`, `decay`, `cannibalization`) run in the script with thresholds from `SEO_CHECKS.md`. No MCP server is used.
Evidence: [VERIFIED]
Sources: https://developers.google.com/webmaster-tools/v1/searchanalytics/query; https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect

### SEO-TLS-04: DataForSEO access via cost-gated script
Access DataForSEO only through `dataforseo/query.py` with `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`; the script prints an estimate and aborts when it exceeds `--max-cost` (default $0.10). No MCP server is used.
Evidence: [VERIFIED]
Sources: https://dataforseo.com/pricing; https://docs.dataforseo.com/v3/

### SEO-TLS-05: Pre-flight cost estimation with verified rates
Before a DataForSEO batch, check balance (`GET /v3/appendix/user_data`, $0) and compute cost with rates [LITERAL: 2026-11-03]: SERP Standard $0.0006/SERP, SERP Live $0.002/SERP, Labs $0.012/task + $0.00012/item, Keywords Data (Google or Bing Ads) $0.06/task with up to 700 keywords per task (never 1 keyword per task), Backlinks $0.024/task + $0.000036/row, On-Page from $0.00015/page, AI Keyword Search Volume $0.01/task + $0.0001/row, LLM Mentions $0.10/task + $0.001/row.
Evidence: [VERIFIED]
Sources: https://dataforseo.com/pricing
Script: `dataforseo/query.py balance`; every paid command prints the estimate

### SEO-TLS-06: load_async_ai_overview on live SERP calls
Live Google organic SERP requests (`POST /v3/serp/google/organic/live/advanced`) include `"load_async_ai_overview": true` so asynchronously rendered AI Overviews are captured.
Evidence: [VERIFIED]
Sources: https://dataforseo.com/pricing; https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/
Script: `dataforseo/query.py serp` (always set)

### SEO-TLS-07: Bing JSON endpoint; Ahrefs and Semrush not integrated
Use the Bing Webmaster JSON API `https://ssl.bing.com/webmaster/api.svc/json/{Method}` (SOAP and POX retired 2026-08-31) [LITERAL: 2026-11-03]. Ahrefs and Semrush are subscription alternatives without integration in this skill.
Evidence: [VERIFIED]
Sources: https://learn.microsoft.com/en-us/bingwebmaster/
Script: `bing-webmaster/query.py`

### SEO-TLS-08: Plausible Stats API plan requirement and rate limit
Query `POST https://plausible.io/api/v2/query` (`Authorization: Bearer {PLAUSIBLE_API_KEY}`, max 600 requests per hour); on Plausible Cloud the Stats API requires the Business plan (EUR 19/month at 10k pageviews); self-hosted Community Edition is $0; the key must belong to the site's owning team [LITERAL: 2026-11-03].
Evidence: [VERIFIED]
Sources: https://plausible.io/docs/stats-api
Script: `plausible/query.py`

### SEO-TLS-09: Multi-run requirement for AI visibility panels
For LLM visibility via DataForSEO AI Optimization (`llm_responses`, `llm_scraper`) or third-party trackers, require at least 8 repetitions per prompt (research range 7-8) across paraphrases and report all 3 stages (activation, retrieval, citation) instead of single-shot presence.
Evidence: [VERIFIED]
Sources: https://arxiv.org/abs/2607.14035

### SEO-TLS-10: Credential path hygiene
General-purpose docs and scripts reference credentials only as `[API_KEYS_FILE]` (default `[WORKSPACE_FOLDER]/../.tools/.api-keys.txt`, resolved from the script location; override `--keys-file`); file credentials are file names relative to that folder; never machine-specific drive paths.
Evidence: [ASSUMED] (engineering convention of this skill)
Sources: none (convention defined in `SKILL.md` section "Credential Keys")

## Platform Metadata Field Specifications

Format: Field | Indexed | Limit [LITERAL: 2026-11-03] | Truncation or behavior | Prohibited | Source. 54 entries covering 72 fields (combined entries such as `og:title` and `twitter:title`). Limits marked [ASSUMED] are display targets, not platform limits.

### Group 1: Web HTML head, snippets, canonicals, robots
- `<title>` | yes (title link, AI citation lift) | no HTML limit; display target 50-60 chars / ~580 px [ASSUMED] | truncated to device width; replaced from `<h1>`, `og:title`, anchors when boilerplate, obsolete year, or script mismatch | vague labels ("Home"), stuffing, site-wide boilerplate, mismatched script | https://developers.google.com/search/docs/appearance/title-link
- `<h1>` | yes (title link fallback, structure) | no hard limit; target 40-70 chars, one dominant heading | overrides stale `<title>` | several equally prominent top headings; topic mismatch with `<title>` | https://developers.google.com/search/docs/appearance/title-link
- `<meta name="description">` | display only (CTR, agent frontmatter) | no HTML limit; display target 140-160 chars / ~920 px [ASSUMED] | used when better than body text; key-value summaries allowed | keyword strings, duplicates across pages, fluff, unverified AI claims | https://developers.google.com/search/docs/appearance/snippet
- `<link rel="canonical">` | yes | 1 per page, absolute HTTPS URL | evaluated before and after JS | relative paths, fragments, cross-language targets, paginated pages to page 1 | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- `<link rel="alternate" hreflang>` | yes | ISO 639-1 + optional ISO 3166-1 Alpha 2 + `x-default` | ignored unless reciprocated | `en-UK`, `es-419`, `eu`, `un`, country code as language, relative URLs | https://developers.google.com/search/docs/specialty/international/localized-versions
- `<meta name="robots">` / `X-Robots-Tag` | yes | `noindex`, `nofollow`, `nosnippet`, `max-snippet:[n]`, `max-image-preview:[none|standard|large]`, `max-video-preview:[n]`, `notranslate`, `noimageindex`, `unavailable_after:[ISO-8601]` | most restrictive wins; `X-Robots-Tag` for PDFs and images | blocking in robots.txt a URL whose `noindex` must be read; `nosnippet` on pages for AI Overviews | https://developers.google.com/search/docs/appearance/snippet
- `data-nosnippet` | yes | only on `<span>`, `<div>`, `<section>` | boolean; `="false"` still blocks | on `<p>`/`<article>`; added by JS; unclosed tags | https://developers.google.com/search/docs/appearance/snippet
- `#fragment` deep links ("Read more") | display only | valid `id` on visible section headings | in-snippet jump links (2026-04-20) | content in collapsed tabs; JS scroll forcing; hash stripping | https://developers.google.com/search/docs/appearance/snippet

### Group 2: Open Graph, X cards, agent frontmatter
- `og:title` / `twitter:title` | yes (title link fallback, social card, frontmatter) | target <= 60-70 chars [ASSUMED] | used when `<title>` broken | boilerplate; mismatch with `<h1>` | https://developers.google.com/search/docs/appearance/title-link
- `og:description` / `twitter:description` | display only | target 140-160 chars [ASSUMED] | social embeds, frontmatter `description` | keyword lists, empty | https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
- `og:image` (+ width, height, alt) / `twitter:image` | yes (preferred thumbnail with `primaryImageOfPage`, 2026-03-02) | >= 1200 px wide (1200x675 or 1200x630), `max-image-preview:large` | Google chooses between `og:image` and `primaryImageOfPage` | site logo, overlaid brand text, extreme aspect ratios, low resolution | https://developers.google.com/search/docs/appearance/google-images
- `og:site_name` / `WebSite.name` | display only (site name) | concise brand, <= 30 chars [ASSUMED] | duplicate in `<title>` may be stripped | keywords in site name | https://developers.google.com/search/docs/appearance/title-link

### Group 3: Schema.org JSON-LD
- JSON-LD container | rich results and entity | strict parity with visible content | parsed by Rich Results Test | invisible content; retired types (`FAQPage`, `PracticeProblem`, `CourseInfo`, `EstimatedSalary`, `LearningVideo`, `SpecialAnnouncement`, `VehicleListing`, `ClaimReview`, `HowTo`, Sitelinks Search Box) | https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- `Article` / `NewsArticle` / `BlogPosting` | rich results and entity | `headline`, `image` (= `og:image`), `datePublished` and `dateModified` ISO 8601 with timezone, `author` (`name`, `url`) | byline dates, thumbnail | fake `dateModified`; unverified author claims | https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- `Organization` / `ProfilePage` | entity | `name`, `url`, `logo`, `sameAs` (Wikidata, Wikipedia, GitHub, social), `iso6523Code`, `duns`, `leiCode`, `naics`, `vatID` | links entity to authority graphs | unverified `sameAs` profiles | https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- `Product` (`Offer`, `AggregateRating`, `MerchantReturnPolicy`, `OfferShippingDetails`) | yes | `name`, `image`, `offers.price`, `offers.priceCurrency`, `offers.availability`, `category` (2026-07-07), `hasAdultConsideration` (2026-05-20), `validFrom`, `validThrough`, `priceValidUntil` | price drop badges, shipping, returns, AI shopping | fake or undisclosed incentivized reviews (2026-07-24); price mismatch with page | https://developers.google.com/search/updates
- `Event` | rich results and entity | `name`, `startDate`, `endDate`, `location` (`Place` with physical `PostalAddress`), `offers` | Google Events | online-only events | https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- `VideoObject` (`Clip`, `SeekToAction`, `BroadcastEvent`) | yes | `name`, `description`, `thumbnailUrl` (>= 60x30 px, >= 80% alpha > 250), `uploadDate`, `contentUrl`/`embedUrl`, `creator`/`author`/`interactionStatistic` (2026-09-24) | `SeekToAction` only EN, ES, PT, IT, ZH, FR, JA, DE, TR, KO, NL, RU | `data:` or `#fragment` URLs; video not main content | https://developers.google.com/search/docs/appearance/video
- Other active types | rich results | `BreadcrumbList`, `Carousel`, `Course`, `Dataset`, `DiscussionForumPosting`, `QAPage`, `Quiz`, `EmployerAggregateRating`, `ImageObject`, `JobPosting`, `LocalBusiness`, `MathSolver`, `Movie`, `Recipe`, `Review`, `SoftwareApplication`, `SpeakableSpecification`, paywalled content, `VacationRental`, `Book` | - | - | https://developers.google.com/search/docs/appearance/structured-data/search-gallery

### Group 4: Images, inline SVG, AI images, PDFs
- `<img src alt>` / `<picture>` / `srcset` | yes (Google Images, Lens, accessibility) | BMP, GIF, JPEG, PNG, WebP, SVG, AVIF; alt <= 125 chars [ASSUMED] | `<picture>` needs `<img src>` fallback | CSS `background-image`, `data:` URIs, generic filenames, alt stuffing | https://developers.google.com/search/docs/appearance/google-images
- Inline `<svg>` | yes when labeled | `<svg role="img" aria-labelledby="t d"><title id="t">...</title><desc id="d">...</desc>` | title and description exposed | unlabeled SVG | https://developers.google.com/search/docs/appearance/google-images
- IPTC photo metadata / Merchant Center AI attribute | yes | `DigitalSourceType` = `http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia` | required on AI product images | AI product images without IPTC label | https://developers.google.com/search/docs/fundamentals/using-gen-ai-content
- PDF properties / HTTP `Link` headers | yes | `Link: <https://example.com/canonical>; rel="canonical"`; `Link: <https://...>; rel="alternate"; hreflang="xx"` | consolidates PDF and HTML duplicates | image-only PDFs, empty `Title` property, uncanonicalized duplicates | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

### Group 5: Video and YouTube
- YouTube title / `VideoObject.name` | yes | <= 100 chars; display target <= 60-70 [ASSUMED] | front-load query | clickbait, deceptive metadata | https://support.google.com/youtube/answer/16090438?hl=en
- YouTube description and chapters | yes | <= 5,000 chars; chapters start `00:00`, >= 3 timestamps ascending, each >= 10 s | first ~100-150 chars above "Show more" | tag stuffing | https://developers.google.com/search/docs/appearance/video
- Captions `.srt` / `.vtt` | yes | full time-synced file per language | replaces ASR errors | unrelated text | https://support.google.com/youtube/answer/11914225?hl=en&co=YOUTUBE._YTVideoType%3Dvideo
- Web video file and thumbnail | yes | 21 formats (3GP, 3G2, ASF, AVI, DivX, M2V, M3U, M3U8, M4V, MKV, MOV, MP4, MPEG, OGV, QVT, RAM, RM, VOB, WebM, WMV, XAP); thumbnail >= 60x30 px, >= 80% pixels alpha > 250 | dedicated watch page, fetchable bytes | `data:`, `#fragment`, expiring signed URLs, transparent thumbnails | https://developers.google.com/search/docs/appearance/video

### Group 6: Podcasts
- Show title `<channel><title>` | yes (1 of 3 Apple search fields) | <= 255 chars RSS; < 60 display target [ASSUMED] | updates <= 24 h | keyword stuffing (directory removal) | https://podcasters.apple.com/support/3686-search-on-apple-podcasts
- Episode title `<item><title>` / `<itunes:title>` | yes | <= 255 chars; front-load first 50 chars | season and episode numbers in `<itunes:season>`/`<itunes:episode>` | stuffing, emojis, "Episode 42", show name repeated | https://help.apple.com/itc/podcasts_connect/#/itcb54353390
- `<description>` / `<content:encoded>` | no on Apple search; yes on Spotify and web | <= 4,000 bytes in `<![CDATA[...]]>`; Spotify tags `h1, h2, ul, ol, li, p, b, i, a` | over 4,000 bytes truncates or breaks ingestion | unescaped HTML outside CDATA; `<script>`, `<iframe>`, `<img>` | https://support.spotify.com/us/creators/article/podcast-specification-doc/
- Podcasting 2.0 tags | yes | `<podcast:transcript url type="text/vtt|application/srt|application/json">`, `<podcast:chapters type="application/json+chapters">`, `soundbite`, `person`, `guid`, `locked`, `funding`, `txt`, `podroll`, `updateFrequency` | in-app transcript search | broken relative URLs | https://github.com/podcastindex-org/podcast-namespace
- Artwork `<itunes:image>` | display only | 1400x1400 to 3000x3000 px square, JPEG or PNG, 72 dpi, RGB | validated on submission | CMYK, non-square, upscaled, platform logos | https://help.apple.com/itc/podcasts_connect/#/itcb54353390

### Group 7: Book stores
- Title and subtitle | yes (highest weight) | KDP title + subtitle < 200 chars, main title <= 60 recommended; cover text 1:1; phonetic fields for JA/ZH on Apple | KDP print titles locked after publication | series name or volume in title/subtitle, HTML, "bestseller", "free", "#1" | https://kdp.amazon.com/en_US/help/topic/G201097560
- Series name and number | yes | dedicated series field; number = positive integer digits (never "Book 1", "Vol. 1", "I", 0, decimals on Play) | contiguous numbering and identical spelling for Play bundles | series for public-domain or low-content books | https://support.google.com/books/partner/answer/3237055?hl=en
- Authors and contributors | yes | up to 50 on Kobo (1 per field); Primary on Apple; identical spelling everywhere; narrator + human vs AI voice on Play audiobooks | middle-initial mismatch splits catalogs | several authors in one field; unrelated famous authors | https://kobowritinglife.zendesk.com/hc/en-us/articles/360058975792-Metadata-Guidelines
- Description / synopsis | conversion, secondary search | Apple >= 50 chars RTF, zero HTML tags; KDP and Kobo clean HTML (`p`, `b`, `i`, `ul`, `li`) | raw HTML shows literally on Apple | URLs, emails, addresses, phone numbers, social handles, reviews, quotes, testimonials, review requests, prices, keyword blocks | https://itunespartner.apple.com/books/support/12-metadata
- KDP keyword boxes | yes | 7 fields x <= 50 chars; 2-3 word phrases | 24-72 h propagation; quotes restrict matching | words from title/subtitle/contributors/categories, quotes, other authors, "bestselling", "new", "on sale", "free", "book", "ebook", "Kindle", "KDP Select", plural and spacing duplicates, HTML | https://kdp.amazon.com/en_US/help/topic/G201298500
- Categories, BISAC, Thema, reading age | yes | KDP 3 per format (72 h lag; reading age 0-2, 3-5, 6-8, 9-12, 13-17; 12-15 on Amazon.de); Apple 1 main + 1 secondary; Play 1-3 genres one standard; ONIX 3.1.2 BISAC + Thema 1.7 | mixing BISAC and BIC on Play breaks mapping | inaccurate categories; missing reading age for juvenile categories | https://kdp.amazon.com/en_US/help/topic/G200652170
- Identifiers, publisher, ONIX Codelist 196 | yes | 13-digit ISBN; immutable when live on Play; Related books links formats; Codelist 196 accessibility | ONIX feed overwrites Play UI edits | "Amazon", "Kindle", "KDP", URLs in KDP publisher; ONIX 2.1 | https://www.editeur.org/83/overview/

### Group 8: App stores
- App name / title | yes (highest weight) | <= 30 chars on Apple and Google Play | Apple: changes need new version | Play: emojis, emoticons, kaomoji, repeated special chars, non-brand ALL CAPS, "#1", "App of the year", "Best of Play", "Free", "No Ads", "10% off" (all translations); Apple: clone names, competitor trademarks | https://support.google.com/googleplay/android-developer/answer/13393723?hl=en
- Apple subtitle | yes | <= 30 chars | new version needed | generic claims, words from name, competitor names | https://developer.apple.com/app-store/product-page/
- Apple keyword field | yes (private, per localization and Custom Product Page) | <= 100 chars total, commas without surrounding spaces (`Property,House,Real Estate`) | spaces waste quota | plurals of included singulars, category names, "app", "game", duplicates (incl. name/subtitle words), `#`, `@`, trademarks, celebrity and competitor names | https://developer.apple.com/app-store/search/
- Apple promotional text | no | <= 170 chars | editable without new version | keywords for ranking | https://developer.apple.com/app-store/product-page/
- Google Play short description | yes | <= 80 chars | top of listing | "free", "discount", "$50 cash back", "#1", "Best", profanity, repetition inside full description | https://support.google.com/googleplay/android-developer/answer/13393723?hl=en
- Full description (Apple and Play) | yes on Play; conversion on Apple | <= 4,000 chars | first 2-3 lines above "Read more" | unattributed testimonials (Play), keyword blocks, repeated short description (Play), regional prices (Apple), competitor or celebrity names | https://support.google.com/googleplay/android-developer/answer/9898842?hl=en
- In-app purchases, previews, screenshots | yes (Apple IAP in search) | IAP name <= 35, description <= 55, up to 20 items; up to 3 previews (<= 30 s); 10 screenshots (first 1-3 in search) | localizable | misleading badges in icons; "#1"/"Free"/"10% off" badges in Play graphics | https://developer.apple.com/app-store/product-page/

### Group 9: Google Business Profile
- Business name | yes (relevance) | real-world signage name | violations cause reversal or suspension | the 11 banned additions in SEO-MAV-08 | https://support.google.com/business/answer/3038177?hl=en
- Primary and additional categories | yes | 1 primary + few specific additional ("IS a", never "HAS a") | broad categories dilute | categories for amenities or departments | https://support.google.com/business/answer/7091?hl=en
- Business description | conversion and context | <= 750 chars (~250 visible [ASSUMED]) | Knowledge Panel, Maps | links of any type, price or sale claims, HTML, irrelevant text | https://support.google.com/business/answer/3038177?hl=en
- Address vs service area | yes (distance) | service-area businesses hide address; area within ~2 h driving | distance from verified location | virtual offices, co-working without signage and staff, P.O. boxes, whole country or state | https://support.google.com/business/answer/3038177?hl=en

### Group 10: Social platforms
- LinkedIn article SEO title and description | yes (external search) | title <= 60 chars; description 140-160 chars (Publishing menu -> Settings) | overrides default headline and snippet | blank when headline is vague; stuffing | https://www.linkedin.com/help/linkedin/answer/a6244140
- TikTok and Instagram captions, on-screen text, audio | yes (native search; GSC platform properties since 2026-07-29) | TikTok caption <= 4,000 chars, query in first 60-80 chars and on-screen text in first 3 s [COMMUNITY]; Instagram caption <= 2,200 chars + custom alt text | Google indexes public `/video/`, `/p/`, `/reels/` URLs | hashtag spam, reposted watermarked clips | https://developers.google.com/search/docs/monitor-debug/analyze-social-video-content
- Pinterest pin title, description, board, alt text | yes | title <= 100 chars (first 40 visible), description <= 500 (50-60 preview), alt <= 500; 2:3 image 1000x1500 px [COMMUNITY] | indexed with visual embeddings | hashtag stuffing, misleading links | https://help.pinterest.com/en/business/article/pinterest-trends
- Reddit post title and X post text | yes (Discussions and Forums; X in GSC properties) | Reddit title <= 300 chars, not editable; X post <= 280 chars (first 40-60 chars become title fallback) [COMMUNITY] | Reddit titles immutable | astroturfing, undisclosed self-promotion, vote manipulation | https://developers.google.com/search/docs/monitor-debug/analyze-social-video-content
