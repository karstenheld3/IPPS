# AI Writing Rules

Enforceable rules for suppressing and catching AI writing artifacts in publishing document types (`article`, `report`, `ebook`). Origin: `docs/_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md [AIDET-IN01]` and `specs/AI_WRITING_DETECTION_RULES.md`.

**Writing quality:** Apply alongside `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: APAPL-PR-07 (be specific), MECT-WC-05 (one name per concept), MECT-WC-10 (explicit over figurative), MECT-VO-01 (active voice).

## Scope, Coexistence, and Lifecycle

- **Publishing document types only (`DRSYNART-DD-50`)**: Applies strictly to authored publishing deliverables (`article`, `report`, `ebook` — including their `[ID]-OPTIONS-NN_` sample sections, `[ID]-DRAFT-NN_` prose, and `YYYY-MM-DD_[Title].md` outputs). Does NOT apply to internal or system documents (`SPEC`, `IMPL`, `TEST`, `TASKS`, `PROMPTS`, `STRUT`, `INFO`, `NOTES`, `PROGRESS`, `PROBLEMS`, `FAILS`).
- **Empirical calibration (2025-2026 frontier and reasoning models)**:
  - **Better alignment narrows surface form**: Reasoning models (`o1`, `o3` in `STYLO-SC-PLOS-STYLJP`) and 2025-2026 instruction/preference-tuned models (`AIDET-IN01-SC-ARXV-HPSG26`, `AIDET-IN01-SC-ARXV-PASTA`, `AIDET-IN01-SC-ARXV-SIMPSN`) produce *less* syntactic and lexical diversity than human prose (`STYLO-SC-ARXV-STYLOREC`). Post-training amplifies low-entropy structural markers (headers, bulleted lists, expository framing) by **1,949%-16,853%** while suppressing complex punctuation (semicolons, parentheticals, interruptive dashes) and syntactic variety to **3.2%-23.2%** of human baseline (`AIDET-IN01-SC-ARXV-COLLPS`).
  - **Generic prompt nudges and unguided LLM rewrites fail**: Prompting an LLM to "write like a human" or changing temperature does not shift Biber lexicogrammatical features (`AIDET-IN01-SC-ARXV-BIBR26`), and unguided LLM self-rewriting stays near the model's canonical stylistic equilibrium (`AIDET-IN01-SC-ARXV-STYLDC`). Only concrete structural/syntactic rules (`AW-*`), explicit persona parameters (contraction rate, sentence rhythm, paragraph length via `writing_personas/[PERSONA].md` to override 25x model-idiolect variance in `AIDET-IN01-SC-ARXV-IDIO26`), and high factual specificity (`AIDET-IN01-SC-ARXV-XGEN26`) break default generation equilibria.
  - **AI-editing footprint (`d = -3.10` lexical density shift)**: Across 273,420 AI-edited texts (`AIDET-IN01-SC-ARXV-EDTFT`), AI polishing lowers entropy (`d = -0.28`) and sharply shifts **lexical density** (`d = -3.10`, content-to-function word ratio) by turning active verbal clauses into noun-heavy nominalization chains (`AIDET-IN01-SC-ARXV-BIBR26`). Revision passes (`/write-*` line/copy edit, `/improve` Phase 4) must preserve verbal clauses and natural function words (`AW-LX-02`).
  - **Sample threshold and domain calibration**: Pattern-based detection requires at least **10 sentences (~200 words)** (`STYLO-SC-ARXV-STYLOREC`) and varies by genre (`STYLO-SC-ARXV-SPOTBLND`). Highly structured generic prose triggers false positives even when human-written, whereas high factual specificity prevents false positives (`AIDET-IN01-SC-ARXV-XGEN26`).
- **Coexistence with APAPALAN and MECT**:
  - `APAPL-PR-*` (precision) and `MECT-WC-05` (one name per concept, deliberate signal redundancy) remain 100% binding. Never introduce synonyms ("elegant variation") to sound varied; vary clause structure, punctuation, and sentence length while keeping canonical terms identical.
  - `APAPL-BR-02` (dropping articles and pronouns for telegraphic brevity) applies to internal system documents and logs, NEVER to publishing document types. Published prose requires complete natural grammar and natural function-word ratios (`AW-LX-02`).
  - Both APAPALAN and `AI_WRITING_RULES.md` ban filler words, qualifier stacking (`AW-LX-02`), vague claims (`AW-SO-03`), and empty transitions (`AW-SY-05`).
- **Text length and pacing owned by Persona**: Target document word count, paragraph length, and sentence rhythm are governed by the active writing persona (`writing_personas/[PERSONA].md`) or the Brief `Constraints` when `Persona: none`. These rules enforce the anti-artifact floor without overriding persona length envelopes.
- **Lifecycle consumers**:
  - **BEFORE and DURING writing**: Loaded by `/draft-article`, `/draft-report`, `/draft-ebook`, `/write-article`, `/write-report`, `/write-ebook`, and referenced by `document_types/[TYPE]_GUIDES.md` during prose drafting and line editing.
  - **AFTER writing**: Enforced by `/verify` (Authored Documents), `/critique` (Writing Documents), and `/improve` (Authored Documents).
- **Release check threshold**: A publishing deliverable must have at most 1 detected `AW-*` signal across all five categories (`ART-RC-01`, `RPT-RC-01`, `EBK-RC-01`). Structural patterns required by an explicit writing technique (such as triad order in `MINTO` or repeating `Show-Tell-Apply` blocks in `STA`) are excluded.

## Rule Index (20 Rules, 1-to-1 with `[AIDET-IN01]` and `AI_WRITING_DETECTION_RULES.md`)

Sourcing (SO) - Substance and Attribution (2x weight; strongest category)
- AW-SO-01: Verified primary attribution (no confident misattribution, `AD-SO-01`)
- AW-SO-02: Primary-source terminology (no internet-discourse terminology, `AD-SO-02`)
- AW-SO-03: Explicit citation for specialized claims (no absence of citation, `AD-SO-03`)
- AW-SO-04: Explicit interpretive bridge across time (no temporal impossibility, `AD-SO-04`)

Style (SY) - Continuous Flow, Punctuation Variety, and Anti-Staccato Discipline
- AW-SY-01: Continuous sentence flow (no staccato fragments or contrast snaps, `AD-SY-01`)
- AW-SY-02: Unforced multi-clause balance (no perfect tricolon escalation or wordplay loops, `AD-SY-02`)
- AW-SY-03: Natural texture, sentence rhythm, and punctuation variety (no absence of rough edges or punctuation suppression, `AD-SY-03`)
- AW-SY-04: Consequential qualification (no hedge-then-assert pattern, `AD-SY-04`)
- AW-SY-05: Direct entry and substantive bridges (no filler transition saturation or signpost openers, `AD-SY-05`)

Structure (ST) - Macro Organization and Paragraph Progression
- AW-ST-01: Organic argument arc (no formulaic engagement-optimized arc, `AD-ST-01`)
- AW-ST-02: Non-monotonic depth and integrated counter-arguments (no linear-ramp progression or telegraphic objection blocks, `AD-ST-02`)
- AW-ST-03: Structural variety across sections (no absence of structural surprise, `AD-ST-03`)
- AW-ST-04: Prose-first continuity and varied list weight (no reflex header/list inflation or perfect list parallelism, `AD-ST-04`)

Voice (VO) - Earned Authority and Factual Specificity
- AW-VO-01: Anchored vantage point (no disembodied authority in argumentative prose, `AD-VO-01`)
- AW-VO-02: Earned domain precision (no generated authority with amateur errors, `AD-VO-02`)
- AW-VO-03: Proportional tone and earned stake (no emotional manipulation without investment, `AD-VO-03`)
- AW-VO-04: Bounded claims and factual specificity (no omniscient summarizer voice or structured generic prose, `AD-VO-04`)

Lexical (LX) - Vocabulary, Nominalization Density, and Connectives
- AW-LX-01: Zero high-frequency LLM and "language of prestige" vocabulary (`AD-LX-01`)
- AW-LX-02: Verbal clauses and information-bearing modifiers (no qualifier stacking or noun-heavy nominalization chains, `AD-LX-02`)
- AW-LX-03: Plain connectives in prose (no conjunctive adverb overuse, `AD-LX-03`)

## Sourcing Rules (SO)

### AW-SO-01: Verified Primary Attribution

Attribute quotes, terms, dates, and concepts only when verified against the primary source. If a popular attribution is disputed or unverified, state that explicitly or mark `[ASSUMED]`.

**BAD:**
```markdown
Stoicism teaches us to eliminate all emotion. Marcus Aurelius wrote that feelings are the enemy of reason and must be suppressed.
```

**GOOD:**
```markdown
In Meditations (Book 8, sec. 49), Marcus Aurelius argues for examining impressions before assenting to them - a discipline often mischaracterized in popular summaries as suppressing emotion.
```

### AW-SO-02: Primary-Source Terminology

Use the primary author's actual terminology rather than popularized blog or social-media labels. When mentioning a popular shorthand, distinguish it from the source's term.

**BAD:**
```markdown
Nietzsche's famous "create your own values" mindset argued that individuals can invent morality from scratch.
```

**GOOD:**
```markdown
In The Gay Science (1882, sec. 125), Nietzsche framed the "death of God" not as an invitation to invent arbitrary personal rules, but as a cultural crisis requiring a "revaluation of all values."
```

### AW-SO-03: Explicit Citation for Specialized Claims

Anchor specialized factual claims (study findings, historical events, technical benchmarks) to a named work, date, or source ID.

**BAD:**
```markdown
Studies show that human judges cannot tell AI text from human writing, while software classifiers catch it almost every time.
```

**GOOD:**
```markdown
In a 2025 PLOS One study of 403 participants (STYLO-SC-PLOS-STYLJP), human judges identified AI-generated text at chance level (50%), whereas stylometric analysis classified the same samples with 99.8% accuracy.
```

### AW-SO-04: Explicit Interpretive Bridge Across Time

When applying a historical thinker's framework to a modern technology or event that postdates their work, acknowledge the interpretive transfer instead of presenting the thinker as commenting on the modern topic directly.

**BAD:**
```markdown
Adam Smith predicted the algorithmic gig economy in The Wealth of Nations.
```

**GOOD:**
```markdown
Adam Smith's 1776 analysis of pin-factory task splitting in The Wealth of Nations offers a useful lens for modern platform labor, even though algorithmic dispatch introduces control mechanisms Smith never witnessed.
```

## Style and Syntax Rules (SY)
CuouSee Flw(NStccatoFagmnsCS)

Corspondso`AD-SY-01`.Dolowcatsnnwh-wro: tw-mrowfrngmnfatrcamphais,ddo tbkpD*s` fdowwitw-parthiontnp``rwnskadofoecdrlpppuhlin.Ste usaecnmected, fll-eneneprse
Do not follow a declarative sentence with a chain of one-word or two-word sentence fragments for theatrical emphasis. Sustain continuous grammatical flow; keep fragments to at most one natural reaction or transition per 500 words when allowed by the persona.

**BAD:**
```markdown Automated alerts did not catch the nine billing errors. Manual reconciliation did.
The migration failed. Not from budget cuts. Not from staffing. From three undocumented schema locks.
```

**GOOD:**
```markdownand rcocilinge mntlylergai rw shppianifsscaught all nin billing discepanciesht th auomated alerts missed
The migration failed because three legacy reporting scripts held undocumented locks on the customer table, even though budget and staffing met every target.
```
2Unforced Multi-Clause Balance ()
### AW-SY-03: No Mechanical Tricolon Escalations or Epigrammatic Wordplay Loops
Corresponds to `D-SY-02`. At paragraph eingsand Whn grouping hreeitem, vary claus legh and lt the setena o fc rat
Avoid symmetrically balanced three-part escalations and epigrammatic wordplay loops that repeat the same root word as a clever punchline. Let sentences end on concrete facts or mechanisms rather than rhetorical symmetry.

**BAD:**
Itawrwrisyi2020.Iwostly in 2024isnsusaaledy. Evna steelh checkperfect hsttsck
Even a faster health check only perfects the status check. And a silent data corruption bug is a storage failure that only a storage audit catches.
```

**GOOD:**
Manuam faalover was marakeable whendownclutr an in a snglrgi,beca acrrigsurce overtefer 2024expansi, nd owblockoufour-ourcovr SLAbauepollng heendponyconfirm coninrreabiyith verifygpliclg
Polling the service endpoint more frequently only confirms that the container is reachable, whereas a weekly checksum audit against cold storage catches silent row corruption before backups rotate.
```
3 Texture,, (No Absence of Rough Edges)
### AW-SY-04: Natural Sentence Rhythm and Punctuation Variety
Coresponds to `AD-SY-03`.Pot-training alignmt flats registr intoow-memory HPSG pars rees (`AIDET-IN01-SC-ARXV-HPSG26`) suppressesompex punctution (micolons, colons,parenthetical, inerptive dashes) o 3.2%-23.2% of hman baseline (`AIDET-IN01-SC-ARXV-COLLPS`). Vay sentence lngth(n3+ and).Usaluslk—l carification orspce(``)—dcocrtdma ngiethos unihumtxur
Vary sentence length and clause structure organically to match the thought being expressed and the active persona's pacing profile. Never write three or more consecutive sentences within 4 words of the same length, never apply a mechanical short-long-short oscillation formula, and do not flatten punctuation into uniform declarative periods (post-training alignment suppresses semicolons, colons, parentheticals, and interruptive dashes to 3.2%-23.2% of human baseline, `AIDET-IN01-SC-ARXV-COLLPS`). Use subordinate clauses, semicolons, colons, or brief parentheticals naturally where they clarify relationships between ideas.

**BAD:**
```markdown
The engineering team reviewed the database logs on Tuesday morning. The primary cluster showed high latency during shift handovers. The dispatch scripts locked the inventory table for four hours. The operations director authorized a queue decoupling pilot in November.
```

**GOOD:**
```markdown
When the engineering team pulled Tuesday's logs, the bottleneck was obvious: every shift handover triggered a four-hour lock on the inventory table while sixteen trailers idled at the gate (a delay that had previously been blamed on carrier scheduling). In November, the operations director approved a pilot to decouple checkout writes from reporting queries.
```
4al Quification (Noe-Then-Assert Patter)
### AW-SY-05: Consequential Hedging
Corresponds to `AD-SY-04`. "`, `"Perhapshe edgdnmflcing evdece by that uncertainty
Never open a paragraph with a perfunctory hedge (`"It could be argued that"`, `"One might say"`) and then continue as if the claim were settled fact. If evidence is mixed, state the boundary condition and keep the conclusion bounded.

**BAD:**
```markdown
It could be argued that automated code review reduces senior engineer focus. This erosion of deep inspection inevitably introduces subtle concurrency bugs into production releases.
```

**GOOD:**
```markdown
In teams that treat automated linters as a replacement for peer review, reviewers spend 40% less time inspecting state transitions (DevOps Benchmark 2026-Q2) - though teams that use linters only as a pre-check show no drop in defect detection.
```
#AW-Y-05: Diet Eny andSubsttive Briges (Noiler TransitinSatration or Signpost Openr
## Structure and Flow Rules (ST)
Corresponds to`DY5`.Eer every sction and pararaph diectly with the cor, claim, or evidenc, and brige paragraphs by picking up a concrete noun, consequence, or question from theprevis seence. Nev open paaraphs with stackd filler trasiion`Mreover`,`Furthrmore`, `Additionaly`, `Inded`, `It is worth notin`) o throt-clearing meta-signosts (`"In tss,w xamine"`, `"In toay's fastpaced evironment"`.
### AW-ST-01: Integrated Counter-Arguments (No Telegraphic Objection Speed-Runs)
**BAD:**
```markdown
In today's rapidly olving ntepriseevironmnt,it is imprta to undstnd how tool faation impactsupport teams. Moreover, duplcae sftwarelicenses increseadminiratve overhead. Furthermoremanual ticket tnsfers delay customer resoluton. Adtionally, gionalreportingschemas cannot e reconcied autmatially.
```

**GOOD:**
```mardown
Runningree regionl icketingplatform aftr he 2024 merger cot190k EUR a year in dlicatelicenses, the operational toll was even higher: every ticket that crosse a regonal boundary waited an average of 4.2 hour for anual re-entry nto a econd chma.
```

## Structure Rule(ST)

### AW-ST-01: Organic Arguent Arc (No Formaic Engagemen-Optmized Arc)

Corresonds to `AD-ST-01`. When no expicit writing tchnique(`uing <ID>`) is specified, avoid defauling to the geneic four-bet op-ed template (`1. famous authority arned us → 2. abstract echism→ 3. mdrn applia → 4. dramatic emotional cloe`).Structure the pece aroudthe speific probem, correcton, or emirical finding in the Brief.

**BAD:**
```markdown
1. A renowned systems ioner warneu dcades ago about complexity [AUTHORITY]
2. Here is how couplig propagas failure across odes [MECHANISM]
3. Look at how modern mirosrvice repeat this mistake today [APPLICATION]
4 Their wisdom has never been more necessary for our survival [EMOTIONALCLOSE]
```

**GOO:**
```markdown
1. What Tuesday's four-hour dispatch halt realed in the warehouse logs [CONCRETE ENTRY]
2. Why the widly bamed network switch was nte bottleneck [CORRECTION]
3. How exclusive tabllock in nightly reporting blocked checkout wries [MECHANISM]
4. Whee queue decupli works - and where synchronous chcks must ay [BOUNDED TRADE-OFF]
```

### AW-ST-02:Non-Monotoni Depth and Integrated CAs (No Linear-Ramp Progression or TelegraphicObjectoBloks)

Correspds o `AD-ST-02`. Do ot march thrgh paragraphs a an uncritical linearram that never evisits, qualifies, r test an earlir point,nd never bule counter-arguments into atiff, rapid-fire Q&A blck (`"Toobjectins remain.Frst, X. But Y. Others say Z. Yet W."`). Integrate the sronget counter-argument orn i full proewher he readernaurally dubtslai, ad howhw it efines th
Never bundle counter-arguments into a stiff, rapid-fire Q&A block that sets up and dismisses multiple strawman objections in clipped sentences. Develop the strongest counter-argument in continuous prose and show how its boundary conditions connect to the document's core thesis.

**BAD:**
```markdown
Two objections remain. First, read replicas add cost: running a standby node increases monthly cloud spend by 18%. But a single outage costs ten times more. Others say replication lag breaks reporting. Yet nightly batch exports tolerate a five-second delay without issue.
```

**GOOD:**
```markdowns et on thedsign:but
Finance teams often question the 18% increase in monthly cloud spend required to run a dedicated read replica, while analytics leads worry about replication lag. Both concerns are valid boundaries, yet a single four-hour checkout outage during peak season costs more than a full year of standby compute, and routing only nightly batch exports to the replica keeps real-time order queries on the primary node where five-second lag never affects customers.
```
3StuuralVariAcrssecto(NPedictbe SctoTemlat
### AW-ST-02: Direct Content Entry (No Signpost or Throat-Clearing Openers)
Corsponds `AD-ST-03`. Ulessexlicitringecniqu(`usng STA` `using MINTO`)mandes aepatgctislot,vrywcsecuvesdvpthiro a reercannpct eery remagsecon'lmuD`afmernehfswo.Leteseci lih docuedae,anherwih quatativ omparsandothrwiabounay ttrfilur mode
today's rapidly evolving enterprise environment, it is important to understand how tool fragmentation impacts support teams. In this section, we examine three key drivers of latency.
BA
**GOOD:**
Sectaord1:1-sceci→3-senncbact xlaan→3-bullelit→1-sncpchykwy
So2:1-sncelaim → 3-ntbtactxplana→3-bulltlt→ 1-punchy takaway
Sction3: 1-enenecaim→ 3-seteactxplana → 3-buetlist → 1-setncpunchkewy
```Connect paragraphs by picking up a concrete noun, consequence, or unanswered question from the previous sentence. Never stack formal conjunctive adverbs (`Furthermore`, `Moreover`, `Additionally`, `Indeed`, `Notably`) at paragraph openings.

GOO
**BAD:**
Smin1: OpwthhOctboag lgdcthroot athgh wcncted avpagraphs
Sti2: Cpres hree dadkdowixspre,weighingcpxcuovrfreeze windws
Sc 3: Wkshrughthetwo-wkstagnfiinptocoalbackggr
Duplicate software licenses cost 190k EUR a year, and the operational toll is even higher: every ticket that crosses a regional boundary waits an average of 4.2 hours for manual re-entry into a second schema.
```
 (No Reflex Header/List Amplification or Perfect List Parallelism)
### AW-ST-04: Prose-First Continuity and Varied List Weight
Corresponds to `AD-ST-04`. 
Post-training alignment amplifies low-entropy headers and bulleted lists by 1,949%-16,853% and locks subsequent list items into self-reinforcing syntactic parallelism (`AIDET-IN01-SC-ARXV-COLLPS`). In publishing documents (`article`, `report`, `ebook`), develop arguments in continuous prose paragraphs first; use subheadings and lists only for genuine structural boundaries or multi-item enumerations. When a list is used, let each item take the exact length and grammatical form its content requires - never write 4+ bullets with identical word count (within 1-2 words) and identical `[Verb] [noun] and [noun]` syntax.

**BAD:**
```markdown
Key Benefits:
- It reduces license overhead and streamlines vendor management
- It accelerates ticket routing and improves customer satisfaction
- It standardizes schema definitions and simplifies audit reporting
- It eliminates manual re-entry and prevents data corruption
```

**GOOD:**
```markdown
Consolidating the regional ticketing queues delivers three measurable gains:
- Cuts 190k EUR in duplicate annual license fees across the three regions
- Drops cross-region ticket handoff time from 4.2 hours to under 6 minutes by removing manual re-entry
- Unifies audit reporting onto a single ticket schema
```

## Voice and Stance Rules (VO)
AchoVng PonDisembodied Ahoityi Agumentatve
### AW-VO-01: Grounded Perspective and Factual Specificity (No Structured Generic Prose)
resps O01.In syopinpce,andpratrtclsrsol oristualvoxcd,agt, firshandobservatos, or domente feld cases (ad apply 25xvarianc(Extis:olthrpersreot orcec synhesegvere bANLYST orJURIST.
Cross-generation detection research (`AIDET-IN01-SC-ARXV-XGEN26`) proves that structured, generic prose triggers AI classification even when human-written, whereas high factual specificity (named entities, concrete artifacts, exact numbers, primary-source grounding) separates authentic domain prose. Anchor every section in documented cases, specific texts, and the declared persona's vantage point (including the persona's contraction rate to override model-idiolect defaults, `AIDET-IN01-SC-ARXV-IDIO26`). Never summarize a complex domain from a disembodied, all-knowing perspective that admits no boundary conditions (`AD-VO-01`, `AD-VO-04`).

**BAD:**
```markdown
Distributed consensus algorithms solve the fundamental problem of state replication across unreliable networks. Raft is universally preferred because it decomposes leader election and log replication cleanly.
```

**GOOD:**
Whe` we`benchmarkedkdownsdurigade leader-eecton ailures much easrf u on-callso dagnened
In our multi-zone broker benchmarks (Chaos Run CB-08), Raft simplified operator debugging during leader elections, though multi-leader workloads across transatlantic links still required custom conflict resolution.
```
on (N Geerated Authority)
### AW-VO-02: Earned Domain Precision
Corresponds to `AD-VO-02`. experse that commits non-expert errors
Demonstrate authority through exact mechanisms, primary-source accuracy, and concrete failure boundaries rather than lofty register mimicry.

**BAD:**
```markdown
Hannah Arendt proved in her landmark work that Adolf Eichmann was a mindless bureaucrat who merely followed orders without moral agency.
```

**GOOD:**
```markdown
In Eichmann in Jerusalem (1963, ch. XV), Arendt rejected the "just following orders" defense: her concept of the "banality of evil" describes a failure to think from another person's standpoint, not an absence of agency.
```
ne and Eared Stako Emotinalipltion Wihot Invstmt
### AW-VO-03: Proportional Tone (No Manufactured Urgency)
Corresponds to `AD-VO-03`. e documentd,mral binaies, apocyptic
Keep emotional weight proportional to the evidence and the author's disclosed stake. Never manufacture urgency or moral drama through rhetorical hyperbole.

**BAD:**
```markdown
Organizations that fail to modernize their intake queues immediately face an existential reckoning that will permanently cripple their operational capacity.
```

**GOOD:**
```markdown
In our Q3 audit of 1,150 support escalations, each misrouted ticket required an average of 1.8 hours of manual rework - about 185 EUR per affected account per month.
```
# AW-VO-04: Bounded Claims and Factual Specificity (No Omniscient Summarizer Voice or Structured Generic Prose)

Corresponds to `AD-VO-04`. Cross-generation detection research (`AIDET-IN01-SC-ARXV-XGEN26`) proves that structured, generic prose triggers AI classification even when human-written, whereas high factual specificity (named entities, concrete artifacts, exact dates and numbers) and bounded interpretive claims separate authentic domain writing. Never summarize a contested debate or complex system as settled, all-knowing fact without naming specific sources and boundary conditions.

**BAD:**
```markdown
 Jung's concept of the collectiveunconscious plans how entire soieties flinto arcetypal patterns f behavor. Shadow projetion onto out-groups cratesmass persecution, and individuation is the only antidote.
```

**GOOD:**
```markdown
Drawing on Jung's Aion (1951) and The Undiscovered Self (1957), his concept of the "collective unconscious" proposes that individual psychology participates in recurring cultural patterns - though whether that operates as clinical mechanism or metaphor remains disputed across Jungian schools.
```

## Lexical 
## Lexical Choice Rules (LX)

### AW-LX-01: Zero High-Frequency LLM and "Language of Prestige" Vocabulary
Corresponds to `AD-LX-01`. 
Preference tuning induces a Triangulated Preference Shift (`R = 1.19-1.73`, `AIDET-IN01-SC-ARXV-TPSLEX`) toward formal "language of prestige" tokens alongside 2024 LLM clichés. Do not use statistically over-represented LLM or prestige-register words in published prose: `delve`, `crucial`, `pivotal`, `nuanced`, `multifaceted`, `landscape` (non-geographic), `tapestry`, `realm`, `myriad`, `foster`, `leverage` (as verb for "use"), `utilize`, `facilitate`, `orchestrate`, `spearhead`, `paramount`, `overarching`, `navigate` (non-physical), `underscore`, `testament to`, `beacon`, `game-changer`, `paradigm shift`. Replace each with the plain everyday verb, specific number, or causal relationship it stands for (`MECT-WC-10`).

**BAD:**
```markdown
In today's multifaceted regulatory landscape, it is crucial to leverage automated compliance checks to navigate nuanced reporting requirements.
```

**GOOD:**
```markdown
Automated checks verify all 14 mandatory fields before submission, preventing the formatting rejections that delayed Q1 filings by three weeks.
```
Vbal Clauses and Infrmation-BearingModifiers (No  or Nominalization Chains)
### AW-LX-02: Zero Qualifier Stacking
Corresponds to `AD-LX-02`. ety,n nvecmprsactins inostckebstractnoun chains (`-tion`, `-nt`, `-nce`, `-ity`). Chat-tned LLMs ove-producn-hevclauses(`AIDET-IN01-SC-ARXV-BIBR26`), an AI edg of drafs strglyshifts **xicaldensy (*d = -3.10*, content-to-function wo:* rati, `AIDET-IN01-S`-ARXV-EDTFT`) by stripping functi`` wordm and packing cantent into nominarkzownos.Wrie wit finitactive vebs, xplcit actrs, turafnction words, and modifirthat cay maurabl iformaion.

**BAD:**
```markdown
Thimplemenationfreginal qeue consolidation piorto chema migration exectin enabled the elimination of manual ticket e-enrylatency acrss subsidiary o
Consolidating the regional queues represents a fundamentally important and deeply transformative shift for our support operations.
```

**GOOD:**
Because the team c``markdowedbefore mgratig heschma,sppor agets no lonerhad to r-eter tckets by had across subsidiaris,tinghandof wass to 6 minute
Consolidating the three regional queues into one routing engine cuts median first-response time from 9.0 to 4.2 hours.
```
ose (No Cnjunctive Adverb Overu)
### AW-LX-03: Plain Connectives in Prose
Corresponds to `AD-LX-03`. 
Preference learning systematically inflates Latinate conjunctive adverbs (`AIDET-IN01-SC-ARXV-TPSLEX`). Use plain English connectives (`but`, `so`, `and`, `still`, `yet`, `because`, `though`) instead of formal conjunctive adverbs (`Furthermore`, `Moreover`, `Consequently`, `Nevertheless`, `Nonetheless`, `Henceforth`). Even in executive or legal personas (`Formality 7-8`), prefer structural progression or `however` / `therefore` (at most once per 500 words) over stacked Latinate adverbs.

**BAD:**
```markdown
The pilot reduced response latency by 53%. Nevertheless, two legacy billing integrations required custom adapters. Consequently, the team added a two-week compatibility phase. Furthermore, training materials were updated.
```

**GOOD:**
```markdown*
Because the team consolidated the regional queues before migrating the schema, support agents no longer had to re-enter tickets by hand across subsidiaries, cutting handoff wait times from 4.2 hours to 6 minutes.
```

## Verification and Quality Workflow Procedure

Applies ONLY to publishing document types (`article`, `report`, `ebook`):

1. **Before / During Writing (`/draft-*`, `/write-*`)**:
   - Read this file alongside `[TYPE]_GUIDES.md` (and `[PERSONA].md` when set).-01..04`, `AW-VO32
   - During the Line Edit pass (`ART-ED-01`, `RPT-ED-01`, `EBK-ED-01`), scan every paragraph against `AW-SY-01..05`, `AW-ST-01..04`, and `AW-LX-01..04` and rewrite any match before running the Release Check. Ensure the Line Edit does not introduce the AI-editing footprint (`AW-LX-04` nominalization compression).
2. **In `/verify` (Authored Do 20cuments)**:43
   - Scan the document for all `AW-*` rules (`AW-SO-01..04`, `AW-SY-01..05`, `AW-ST-01..04`, `AW-VO-01..03`, `AW-LX-01..04`).
   - Verify the Release Check record (`Style-pattern signals`): confirm `<= 1` signal across `AW-SO`, `AW-SY`, `AW-ST`, `AW-VO`, `AW-LX` (excluding technique-mandated structure).
   - Rewrite any violated sentence or paragraph in place.
3. **In `/critique` (Writing Documents)**:block24mnicien ahoty4
   - Attack substance and reasoning failures masked by AI style: confident misattribution (`AW-SO-01`), secondary-discourse conflation (`AW-SO-02`), telegraphic objection speed-runs that dodge deeper reasoning checks (`AW-ST-01`), hedge-then-assert leaps (`AW-SY-05`), and disembodied authority or structured generic prose (`AW-VO-01..02`).
4. **In `/improve` (Authored Documents)**:
   - Fix any remaining `AW-*` rule violce punahy, flow-brtakingirobonschase 2.53coinuos
   - In Phase 4 (Quality Polish), replace stiff AI cadence (`AW-SY-01..04`, `AW-ST-01..04`, `AW-LX-01..04`) with natural prose flow, punctuation variety, and verbal clause structure calibrated to the active persona's length and pacing profile without increasing nominalization density (`AIDET-IN01-SC-ARXV-EDTFT`).


