# AI Writing Detection Rules

Concrete enforceable rules for detecting AI-assisted writing. Each rule has measurable criteria and BAD/GOOD examples showing what to look for.

**Principle**: Detection through signal convergence across five categories. No single signal is conclusive. Confidence increases with the number of independent signals detected.

**Calibration note**: These rules were developed from analysis of temperature-based LLM output (GPT-3.5/4, Claude 2/3, LLaMA). Effectiveness against reasoning models (o1, o3, DeepSeek-R1) is not yet empirically validated. Sourcing signals (SO) are expected to remain robust because reasoning models still hallucinate. Style and structure signals (SY, ST) may weaken as reasoning models produce more varied, less uniform text.

**Abstraction levels:**
- **_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md [AIDET-IN01]** = Concept, background, why detection matters
- **AI_WRITING_DETECTION_RULES.md** (this file) = Concrete detection rules with examples. Answers: "How do I check a specific text?"
- **`/detect-ai` workflow** = Step-by-step procedure for applying these rules

## Rule Index

Sourcing (SO) - Strongest category
- AD-SO-01: Confident misattribution
- AD-SO-02: Internet-discourse terminology
- AD-SO-03: Absence of citation for specific claims
- AD-SO-04: Temporal impossibility without acknowledgment

Style (SY) - Supporting category
- AD-SY-01: Staccato fragment pattern
- AD-SY-02: Perfect tricolon escalation
- AD-SY-03: Absence of rough edges
- AD-SY-04: Hedge-then-assert pattern
- AD-SY-05: Filler transition saturation

Structure (ST) - Supporting category
- AD-ST-01: Engagement-optimized arc
- AD-ST-02: Perfect paragraph progression
- AD-ST-03: Absence of structural surprise
- AD-ST-04: Perfect list parallelism

Voice (VO) - Supporting category
- AD-VO-01: No personal reference
- AD-VO-02: Generated authority
- AD-VO-03: Emotional manipulation without emotional investment
- AD-VO-04: Omniscient summarizer voice

Lexical (LX) - Supporting category
- AD-LX-01: High-frequency LLM vocabulary
- AD-LX-02: Qualifier stacking
- AD-LX-03: Conjunctive adverb overuse

## Scoring

**Assessment procedure:**
1. Read the text once for comprehension
2. Evaluate each rule independently (DETECTED / NOT DETECTED / INCONCLUSIVE)
3. Count detected signals per category
4. Apply convergence assessment

**Convergence thresholds:**
- 0-3 signals: LOW - Insufficient evidence. Text may be human-written or heavily edited LLM output
- 4-7 signals: MODERATE - Warrants source verification. Text may be AI-assisted
- 8-13 signals: HIGH - Multiple convergent signals. Text very likely AI-assisted
- 14-18 signals: VERY HIGH - Signals across all categories. Text almost certainly AI-generated

**Category weighting:** Sourcing signals (SO) carry 2x weight. A text with 3/4 sourcing signals is more diagnostic than one with 10/14 non-sourcing signals. If SO >= 3, assessment is minimum HIGH regardless of total count.

## Sourcing Rules (SO)

### AD-SO-01: Confident Misattribution

The text attributes a specific claim (quote, term, date, concept) to a named source with authority, but verification reveals the attribution is wrong. The error is stated without hedging, qualification, or uncertainty.

**Why this detects AI:** LLMs generate plausible attributions from training data distribution. The model does not verify claims against primary sources. Confidence is a generation artifact, not a knowledge signal.

**Detection test:** Can the attributed claim be verified against the named source? If no, and the text shows no uncertainty, score DETECTED.

**AI-LIKELY** (confident, wrong):
```
Stoicism teaches us to eliminate all emotion. Marcus Aurelius wrote
that feelings are the enemy of reason and must be suppressed.
```
Aurelius never wrote this. Stoicism advocates managing impressions, not eliminating emotion. Stated as fact without hedging.

**HUMAN-LIKELY** (hedged, correct):
```
In Meditations (c. 170 CE), Marcus Aurelius advocates examining one's
impressions before assenting to them (Book 8, sec. 49) - a practice
often simplified in popular discourse as "eliminating emotion," though
Aurelius himself emphasized judgment over suppression.
```
Correct concept. Named source. Popular simplification acknowledged as such.

**AI-LIKELY** (specific but fabricated):
```
As Einstein famously said, "The definition of insanity is doing the same
thing over and over and expecting different results."
```
Widely attributed to Einstein online. No verified Einstein source exists.

**HUMAN-LIKELY** (attribution-aware):
```
The quote "insanity is doing the same thing over and expecting different
results" is commonly attributed to Einstein, but no verified source exists.
It likely originates from Narcotics Anonymous literature (1981).
```

### AD-SO-02: Internet-Discourse Terminology

The text uses terms popularized by secondary sources (blog posts, YouTube videos, social media commentary) instead of the primary source's own terminology. The borrowed term is presented as if it were the original author's language.

**Why this detects AI:** LLMs cannot distinguish between primary sources and commentary about those sources in their training data. The most frequently occurring formulation wins, regardless of origin.

**Detection test:** Does the terminology match the claimed source's actual language? If the term exists only in internet commentary about the source, score DETECTED.

**AI-LIKELY** (secondary-source term presented as primary):
```
Freud's concept of "daddy issues" explains why people struggle
with authority figures throughout their lives.
```
"Daddy issues" is a pop-psychology term. Freud wrote about the Oedipus complex, father-imago, and transference.

**HUMAN-LIKELY** (primary-source terminology):
```
Freud's concept of the Oedipus complex - particularly as elaborated
in The Interpretation of Dreams (1900) and Three Essays (1905) -
addresses how early parental relationships shape adult psychology.
```

**AI-LIKELY** (internet-discourse framing):
```
Nietzsche's famous "God is dead" philosophy argued that humanity
needed to create its own meaning.
```
Reduces a complex passage in *The Gay Science* (section 125, the Madman parable) to a bumper sticker.

**HUMAN-LIKELY** (source-aware framing):
```
Nietzsche's Madman parable in The Gay Science (1882, section 125) -
"God is dead. God remains dead. And we have killed him" - is not a
triumphant declaration but a terrified diagnosis of cultural consequence.
```

### AD-SO-03: Absence of Citation for Specific Claims

The text makes specific factual claims (dates, direct quotes, named concepts, historical events) without citing any source - not by name, title, page, or URL. The claims are presented as common knowledge when they require expertise.

**Why this detects AI:** Citation requires retrieval capability the base LLM lacks. The model generates claims from statistical patterns, not from source documents it can point to.

**Detection test:** Count specific factual claims. Count citations. If the ratio of claims to citations exceeds 5:1 on specialized topics, score DETECTED.

**AI-LIKELY** (6 claims, 0 citations):
```
Hannah Arendt warned that evil is banal. She studied the Eichmann trial.
She showed that ordinary people commit atrocities. Her conclusion was
that thoughtlessness, not malice, enables genocide. She described the
collapse of moral judgment. The antidote was thinking itself.
```
Six factual claims about Arendt's work. Zero sources named.

**HUMAN-LIKELY** (claims anchored to sources):
```
In Eichmann in Jerusalem (1963), Arendt argued that Eichmann's evil
was not demonic but bureaucratic - what she termed "the banality of
evil" (chapter XV). Her analysis drew on her courtroom observations
for The New Yorker (1961-1962).
```

**Calibration note:** Popular-knowledge claims ("Shakespeare wrote Hamlet") do not require citation. The rule applies to specialized claims that presuppose domain expertise.

### AD-SO-04: Temporal Impossibility Without Acknowledgment

The text applies a historical figure's ideas to events postdating their work (or death) without acknowledging the interpretive leap. The application is presented as if the original author addressed the modern topic.

**Why this detects AI:** LLMs treat all training data as contemporaneous. A historical text and a modern event exist in the same token space. The model does not track that decades (or centuries) and the author's death separate them.

**Detection test:** Does the text present a historical figure as commenting on events they could not have known about? If yes, and no interpretive framing is provided, score DETECTED.

**AI-LIKELY** (presented as direct commentary):
```
Adam Smith predicted the gig economy in The Wealth of Nations.
```
Smith died in 1790. He described 18th-century markets, not digital labor platforms.

**HUMAN-LIKELY** (interpretive framing explicit):
```
Smith's analysis of the division of labor in The Wealth of Nations (1776)
has been applied by some economists to gig-economy dynamics - though
Smith was writing about pin factories and colonial trade, not algorithmic
task allocation.
```

**AI-LIKELY** (historical figure as prophet):
```
Orwell predicted our surveillance society in 1984.
```

**HUMAN-LIKELY** (influence acknowledged, not prophecy):
```
Orwell's 1984 (1949) depicted state surveillance as a tool of
totalitarian control. Modern surveillance capitalism differs
fundamentally in mechanism and motive, though Orwell's
vocabulary ("Big Brother," "thoughtcrime") shapes how we discuss it.
```

## Style Rules (SY)

### AD-SY-01: Staccato Fragment Pattern

Short declarative sentence followed by one-word or two-word fragments used for rhetorical emphasis. Multiple occurrences in the same text.

**Why this detects AI:** LLM persuasive outputs over-produce this pattern because it is heavily represented in engagement-optimized training data (blog posts, tweets, LinkedIn posts). Humans use it occasionally; LLMs use it systematically.

**Detection test:** Count fragment-after-sentence patterns. If 3+ occur in a text under 1000 words, score DETECTED.

**AI-LIKELY** (systematic use):
```
We were warned. Not by politicians. Not by journalists. By history itself.

Collective madness doesn't announce itself. It feels like clarity. Like truth.
Like finally seeing what was always there.

They weren't just wrong. They were dangerous. Morally compromised.
```
Three instances in 50 words. Systematic rhetorical device.

**HUMAN-LIKELY** (occasional use, varied rhythm):
```
Arendt's argument in The Origins of Totalitarianism is fundamentally
about the preconditions that make populations susceptible. She wasn't
writing prophecy. Her target was the structural loneliness of mass
society - a loneliness she'd experienced firsthand as a stateless
refugee for eighteen years.
```
One fragment ("She wasn't writing prophecy"), embedded in varied sentence structures.

### AD-SY-02: Perfect Tricolon Escalation

Three parallel phrases with ascending intensity, cleanly balanced in rhythm and length. Especially when appearing at paragraph endings or as standalone conclusions.

**Why this detects AI:** LLMs produce rhetorically polished tricolons because the pattern is strongly reinforced in persuasive writing training data. Human tricolons tend to be rougher - uneven length, imperfect parallelism, interrupted rhythm.

**Detection test:** Identify tricolon structures. If the three elements are rhythmically balanced, semantically escalating, AND appear at a structural climax point, score DETECTED.

**AI-LIKELY** (perfect balance, perfect escalation):
```
It was dangerous in the 1930s.
It was catastrophic in the 1940s.
And it is happening again.
```
Identical syntactic structure. Clean escalation. Paragraph-final position.

**HUMAN-LIKELY** (rough tricolon, uneven rhythm):
```
Critical thinking was difficult in Arendt's time, it's arguably harder now
with algorithmic feeds amplifying every tribal impulse, and yet -
paradoxically - access to primary sources has never been easier.
```
Same three-beat structure but uneven length, embedded in a run-on, self-interrupting dash.

### AD-SY-03: Absence of Rough Edges

The text contains no idiosyncratic word choices, no unexpected metaphors, no self-corrections, no tangents, no humor, and no personal register shifts. Every sentence maintains the same tone and cadence throughout.

**Why this detects AI:** LLMs optimize for coherent continuation. Token-by-token generation produces uniform register. Human writers have personality artifacts: a distinctive word they favor, an odd metaphor, a parenthetical aside, a tonal shift when the topic engages them personally.

**Detection test:** Read 500+ words. If no sentence surprises you stylistically - no word makes you pause, no structure breaks the pattern - score DETECTED.

**AI-LIKELY** (uniform throughout):
```
The crowd was projecting its own terror onto a designated out-group.
And in doing so, it felt unified. Righteous. Momentarily relieved of the
unbearable anxiety of uncertainty. The institutions were not outside
the delusion. They were, in many cases, its official voice.
```
Every sentence sounds like the same speaker at the same emotional temperature.

**HUMAN-LIKELY** (personality artifacts):
```
What Arendt called "organized loneliness" - and god, it's an uncomfortably
accurate term once you've watched a comment section turn into a loyalty
test - describes the precondition for totalitarian thinking. Not because
people are stupid. Because the alternative, thinking for yourself when
everyone agrees, is physiologically terrifying. Your amygdala doesn't
care about epistemology.
```
Personal anecdote ("comment section"), colloquial register ("god, it's"), specific technical reference ("amygdala"), humor ("doesn't care about epistemology").

### AD-SY-04: Hedge-Then-Assert Pattern

The text introduces a claim with a hedge ("It could be argued that," "Perhaps," "One might say") then immediately follows with an unhedged assertion that treats the claim as established. The hedge performs intellectual humility without delivering it.

**Why this detects AI:** LLMs learn to produce hedges because academic and journalistic training data contains them. But the model's next-token prediction then continues as if the hedged claim were fact, because forward momentum is more probable than sustained qualification.

**Detection test:** Identify hedged statements. Check whether the paragraph continues as if the hedge were absent. If hedges appear 3+ times but never alter the conclusion, score DETECTED.

**AI-LIKELY** (hedge without consequence):
```
It could be argued that social media has fundamentally altered our
capacity for sustained attention. The resulting fragmentation of thought
has produced a generation incapable of deep reading. This cognitive
erosion threatens the foundations of democratic deliberation.
```
"It could be argued" in sentence 1. By sentence 3, the claim is treated as fact ("cognitive erosion threatens").

**HUMAN-LIKELY** (hedge with consequence):
```
It could be argued that social media has altered our attention spans,
though the evidence is mixed - Naomi Baron's research suggests reading
comprehension hasn't declined so much as reading preferences have
shifted. I'm not convinced the "erosion" framing is right.
```
Hedge introduces genuine uncertainty. Conclusion reflects that uncertainty.

### AD-SY-05: Filler Transition Saturation

The text uses transition phrases ("Moreover," "Furthermore," "Additionally," "It is worth noting that," "Indeed") at the start of multiple consecutive paragraphs or sentences without these transitions carrying logical weight.

**Why this detects AI:** LLMs use transition words as low-cost coherence signals. Each paragraph opening is a high-uncertainty position where a generic transition is the safest next token. Human writers vary their paragraph openings and often omit transitions entirely when the logical connection is obvious.

**Detection test:** Count paragraph-initial transition phrases. If >50% of paragraphs begin with a filler transition (Furthermore, Moreover, Additionally, Indeed, It is worth noting, Importantly), score DETECTED.

**AI-LIKELY** (transition-saturated):
```
Moreover, the implications extend beyond individual psychology.
Furthermore, institutional responses have been inadequate.
Additionally, the historical precedents suggest escalation.
Indeed, the pattern matches what scholars have long warned about.
It is worth noting that prevention requires collective action.
```
Five consecutive paragraphs, all opening with filler transitions.

**HUMAN-LIKELY** (varied openings):
```
The implications go beyond individual psychology.
Institutions haven't responded well - but that's a separate problem.
Historical precedents? Mixed. Some suggest escalation, others don't.
What scholars actually say (when you read them rather than cite them)
is more nuanced than the summary above suggests.
```
No filler transitions. Varied sentence structures. Conversational register shifts.

## Structure Rules (ST)

### AD-ST-01: Engagement-Optimized Arc

The text follows a predictable persuasive template: 1) establish authority, 2) explain mechanism, 3) apply to current events, 4) emotional close with call to action or reflection.

**Why this detects AI:** This arc dominates LLM training data (blog posts, op-eds, thought leadership). The model reproduces it as default essay structure because it is the most probable continuation pattern for persuasive openings.

**Detection test:** Map the text's sections to the four-beat template. If the match is exact, score DETECTED. If the text deviates, revisits, or omits beats, score NOT DETECTED.

**AI-LIKELY** (exact template match):
```
1. A great thinker warned us decades ago [AUTHORITY]
2. Here is the psychological mechanism [MECHANISM]
3. Look at what is happening today [APPLICATION]
4. Their wisdom was never more necessary [EMOTIONAL CLOSE]
```

**HUMAN-LIKELY** (deviates from template):
```
1. Here's what I noticed reading this book last year [PERSONAL ENTRY]
2. It's actually about something different than people claim [CORRECTION]
3. But the mechanism described does have modern relevance [MECHANISM]
4. I'm not sure it maps as cleanly as the internet suggests [DOUBT]
5. Here's what transfers and what doesn't [NUANCED ANALYSIS]
```
Five beats. Starts personal. Includes doubt and correction. No emotional climax.

### AD-ST-02: Perfect Paragraph Progression

Every paragraph advances exactly one conceptual step beyond the previous. No paragraph revisits, qualifies, or contradicts an earlier paragraph. The text reads as a linear ramp with no backtracking.

**Why this detects AI:** Token-by-token generation produces forward momentum. The model rarely generates "However, my earlier point requires qualification" because backward reference is statistically less probable than forward continuation.

**Detection test:** Summarize each paragraph in one sentence. If the summaries form a strictly monotonic sequence (each builds on the last, none revises), score DETECTED.

**AI-LIKELY** (monotonic):
```
P1: A great thinker warned us.
P2: They lived through terrible times.
P3: They identified the mechanism.
P4: The danger doesn't announce itself.
P5: Look at what is happening now.
P6: A group is being scapegoated.
P7: The thinker would have recognized it.
P8: Their antidote was never more necessary.
```
Eight paragraphs. Strictly forward. Zero revision.

**HUMAN-LIKELY** (non-monotonic):
```
P1: This book makes bold claims.
P2: Some hold up remarkably well.
P3: But the analysis was rooted in a specific historical moment.
P4: Let me show you what the text actually says.
P5: Here's the key passage.
P6: Now - does this apply today? Partially.
P7: The mechanism transfers. The specific application is ours.
P8: I'm less convinced than I was when I started writing this.
```
Revision at P6. Self-doubt at P8. Non-linear.

### AD-ST-03: Absence of Structural Surprise

After reading two sections, the reader can predict the function (though not the content) of every remaining section. The text follows the most common structural template for its genre without deviation.

**Why this detects AI:** LLMs reproduce the most probable structure from training data. If the most common blog essay has 8 sections in a specific order, the model will produce that order. Structural novelty is a low-probability generation path.

**Detection test:** After reading 30% of the text, write down what you expect the remaining sections to cover. If your prediction matches >80%, score DETECTED.

### AD-ST-04: Perfect List Parallelism

Bulleted or numbered lists where every item follows identical grammatical structure, identical length (within 1-2 words), and identical rhetorical weight. No item breaks the pattern.

**Why this detects AI:** LLMs generate list items by repeating the syntactic pattern of the first item. Each subsequent item is a high-probability continuation of the established template. Human writers create lists with varied item lengths, occasional sub-points, and items that don't quite fit the pattern.

**Detection test:** Identify lists with 4+ items. If all items are within 2 words of the same length AND follow identical grammatical structure AND carry identical rhetorical weight, score DETECTED.

**AI-LIKELY** (mechanical parallelism):
```
Key benefits of mindfulness practice:
- It reduces cortisol levels and promotes physiological calm
- It strengthens prefrontal cortex activity and executive function
- It improves emotional regulation and interpersonal awareness
- It enhances cognitive flexibility and creative problem-solving
- It builds resilience against stress and psychological burnout
```
Five items. Identical structure ("It [verb] [noun phrase] and [noun phrase]"). Near-identical length.

**HUMAN-LIKELY** (natural list variation):
```
What mindfulness actually does (based on the meta-analyses I've read):
- Reduces cortisol - this one's solid, replicated many times
- Probably helps with emotional regulation, though the effect sizes
  are smaller than the apps claim
- Executive function improvements are real but modest
- The "creativity" claims are oversold. One study, small sample.
- Resilience? Hard to measure. I'm skeptical but hopeful.
```
Varied length. Different grammatical structures. Personal commentary. Uncertainty expressed.

## Voice Rules (VO)

### AD-VO-01: No Personal Reference

The text contains no first-person statements, no anecdotes, no disclosed expertise, and no specific professional or personal experience. The author is invisible.

**Why this detects AI:** LLMs have no personal experience to draw on. They can simulate first-person writing when prompted ("write as if you are a therapist") but default to third-person authority when not prompted.

**Detection test:** Search for "I," "my," "we" (inclusive), personal anecdotes, professional disclosures. If none appear in 500+ words of argumentative prose, score DETECTED.

**Calibration:** Academic writing, journalism, and encyclopedic writing are conventionally impersonal. Apply this rule only to argumentative, persuasive, or opinion-style texts where personal voice is expected.

**AI-LIKELY** (disembodied authority):
```
Arendt would have recognized it immediately. The crowd was projecting
its own terror onto a designated out-group.
```

**HUMAN-LIKELY** (anchored in experience):
```
I've been reading Arendt for twenty years, and the passage that keeps
coming back to me is her description of "organized loneliness" - the
moment when belonging to the movement feels not like conformity
but like rescue from isolation.
```

### AD-VO-02: Generated Authority

The text reads as if written by a domain expert but contains errors that a genuine expert would not make. The expertise is performed through tone and vocabulary, not demonstrated through accurate knowledge.

**Why this detects AI:** LLMs generate expert-sounding prose by mimicking the register and vocabulary of expert writing in training data. But register mimicry does not confer knowledge. The model sounds like a domain scholar but makes errors an actual scholar would catch.

**Detection test:** Identify the domain expertise the text implies. Check 2-3 falsifiable claims against primary sources. If the tone implies expertise but the facts contain errors an expert would avoid, score DETECTED.

**AI-LIKELY** (expert tone, non-expert error):
```
Arendt called it the banality of evil. She proved that Eichmann was
just following orders - a cog in the machine with no moral agency.
```
Sounds like an Arendt scholar. But Arendt explicitly rejected the "just following orders" defense. Her point was that Eichmann failed to think, not that he lacked agency. A scholar would know the distinction.

**HUMAN-LIKELY** (expertise demonstrated through precision):
```
Arendt's "banality of evil" is routinely misread as excusing Eichmann.
Her actual argument in Eichmann in Jerusalem (1963, ch. XV) is that
his evil arose from thoughtlessness - an inability or refusal to think
from another's perspective - not from obedience or absent agency.
```

### AD-VO-03: Emotional Manipulation Without Emotional Investment

The text generates emotional responses in the reader (urgency, moral clarity, righteous anger, existential concern) through rhetorical technique, but the author shows no personal emotional stake in the argument.

**Why this detects AI:** LLMs produce emotion through pattern reproduction, not felt experience. The text deploys emotional triggers (apocalyptic framing, moral binary, us-vs-them) without the personal vulnerability that accompanies genuine emotional writing.

**Detection test:** Identify the emotional response the text aims to produce. Check whether the author reveals any personal stake, risk, or vulnerability. If emotion is produced entirely through technique with no personal exposure, score DETECTED.

**AI-LIKELY** (technique without stake):
```
It was nearly impossible then. But it has never been more necessary.
```
Produces urgency and moral weight. Author has no disclosed stake.

**HUMAN-LIKELY** (technique with vulnerability):
```
I lost friends over this. Not because I was right - I'm still not sure I was -
but because the conversation itself became impossible. That's what
Arendt was describing: the moment when thinking becomes threatening.
```
Personal cost disclosed. Uncertainty admitted. Emotional weight earned, not generated.

### AD-VO-04: Omniscient Summarizer Voice

The text summarizes a thinker's entire body of work, a historical period, or a complex debate in confident declarative statements, as if the author has complete knowledge of the subject and no uncertainty about interpretation.

**Why this detects AI:** LLMs produce summaries from training data distributions. The model has no awareness of interpretive disputes, scholarly disagreements, or the limits of its own knowledge. The result is a voice that sounds like an encyclopedia written by someone who has read everything and doubts nothing.

**Detection test:** Check whether the text acknowledges interpretive complexity, scholarly disagreement, or limits of the author's knowledge. If the text summarizes complex topics without any "however," "scholars disagree," "my reading of this is," or "one interpretation suggests," score DETECTED.

**AI-LIKELY** (omniscient summary):
```
Jung's concept of the collective unconscious explains how entire
societies can fall into archetypal patterns of behavior. The shadow,
when projected onto out-groups, creates the conditions for mass
persecution. Individuation is the only antidote.
```
Summarizes Jung's entire framework as settled fact. No interpretive framing. No acknowledgment that "collective unconscious" is contested, that "shadow projection" is one interpretation among many.

**HUMAN-LIKELY** (bounded knowledge):
```
Jung's "collective unconscious" - and I'm drawing mainly on Aion (1951)
and The Undiscovered Self (1957) here - proposes that individual
psychology participates in larger patterns. Whether this is metaphor,
mechanism, or mysticism depends on which Jungian school you ask.
```
Names specific sources. Acknowledges interpretive disagreement. Bounds the claim.

## Lexical Rules (LX)

### AD-LX-01: High-Frequency LLM Vocabulary

The text contains multiple words or phrases that appear with disproportionate frequency in LLM outputs compared to human writing. These are not wrong or unusual words - they are statistically over-represented in generated text.

**Why this detects AI:** LLMs have vocabulary biases. Certain words occupy high-probability positions in common contexts. Human writers have individual vocabularies shaped by reading history, profession, and personality. LLM outputs converge on the same high-probability choices.

**Detection test:** Count occurrences of known high-frequency LLM terms. If 5+ appear in a single text <1000 words, score DETECTED.

**High-frequency LLM terms** (non-exhaustive):
- "delve," "crucial," "pivotal," "nuanced," "multifaceted"
- "landscape" (non-geographic), "tapestry," "realm," "myriad"
- "foster," "leverage," "navigate" (non-physical), "underscore"
- "It's important to note that," "It's worth mentioning"
- "In today's [X] landscape," "In the realm of"
- "This speaks to," "This underscores"

**AI-LIKELY** (5 high-frequency terms in 80 words):
```
In today's rapidly evolving digital landscape, it is crucial to
navigate the multifaceted challenges of information literacy.
This pivotal moment underscores the need to foster critical
thinking skills. Delving into the nuances of media consumption
reveals a tapestry of interconnected factors.
```

**HUMAN-LIKELY** (same content, natural vocabulary):
```
We're drowning in information and most people can't tell good
sources from bad ones. This isn't new - but the scale is. If you
want to fix it, you have to understand why people share garbage
in the first place. It's not stupidity. It's trust misplacement.
```
No high-frequency LLM terms. Colloquial register. Direct.

### AD-LX-02: Qualifier Stacking

Multiple qualifiers, intensifiers, or modifiers stacked on a single claim without adding precision. The qualifiers create an impression of thoroughness or nuance without changing the meaning.

**Why this detects AI:** LLMs generate qualifiers because they appear in formal writing training data. Each qualifier is a safe, low-cost token that maintains coherent continuation. The result is sentences that sound careful but say nothing more than the unqualified version.

**Detection test:** Remove all qualifiers from a sentence. If the meaning is unchanged, and this pattern appears 3+ times, score DETECTED.

**AI-LIKELY** (qualifiers add nothing):
```
This fundamentally important and deeply significant development
represents a truly unprecedented and remarkably transformative shift
in our collective understanding of this critically vital issue.
```
Remove "fundamentally," "deeply," "truly," "unprecedented," "remarkably," "collective," "critically" - same meaning.

**HUMAN-LIKELY** (modifiers carry information):
```
This is the first time a sitting president has been indicted.
That's not hyperbole - there's no precedent in 234 years.
```
"First time" is factual. "234 years" is specific. No wasted modifiers.

### AD-LX-03: Conjunctive Adverb Overuse

Heavy reliance on formal conjunctive adverbs ("However," "Nevertheless," "Consequently," "Furthermore," "Nonetheless") where simpler connectives ("but," "so," "and," "still") would serve the same function without register inflation.

**Why this detects AI:** LLMs trained on formal writing default to high-register connectives. Human writers in non-academic contexts use informal connectives naturally. The consistent use of formal adverbs in conversational or persuasive text signals register mismatch.

**Detection test:** Count formal conjunctive adverbs per 500 words. If >4 appear in non-academic prose, score DETECTED.

**AI-LIKELY** (formal adverbs in casual context):
```
Social media has changed how we communicate. Nevertheless, the
fundamental human need for connection remains unchanged.
Consequently, platforms that prioritize engagement over
authenticity face a reckoning. Furthermore, younger generations
are increasingly aware of these dynamics. Nonetheless, breaking
free from algorithmic influence proves challenging.
```
Five formal adverbs in conversational topic. Register mismatch.

**HUMAN-LIKELY** (natural connectives):
```
Social media changed how we talk to each other, but the need for
real connection didn't go anywhere. So platforms built on outrage
are going to have problems - and younger people already see through
it. Still, knowing the game doesn't mean you can stop playing.
```
"But," "so," "and," "still" - natural register. Same logical connections, no inflation.

## Application Procedure

Use the `/detect-ai` workflow for step-by-step guided execution. Summary below.

### Step 1: First Read

Read the text without scoring. Note your intuitive response: Does anything feel "off"? Does the text feel too smooth, too perfect, too confident?

### Step 2: Sourcing Check (Most Important)

Evaluate AD-SO-01 through AD-SO-04. Pick 2-3 specific factual claims and verify them against primary sources. This step is the most diagnostic because sourcing errors arise directly from LLM generation mechanics and cannot be replicated by competent human writers.

### Step 3: Style and Lexical Check

Evaluate AD-SY-01 through AD-SY-05 and AD-LX-01 through AD-LX-03. These categories often co-occur because both arise from the same token-prediction mechanic.

### Step 4: Structure and Voice Check

Evaluate AD-ST-01 through AD-ST-04 and AD-VO-01 through AD-VO-04. Apply calibration notes (VO-01 exemption for academic writing, ST exemption for conventionally structured genres).

### Step 5: Convergence Assessment

Count detected signals. Apply thresholds. Weight sourcing signals 2x. State confidence level.

### Step 6: Report

Format: `[SIGNAL COUNT] / 18 signals detected. Categories: SO [n/4], SY [n/5], ST [n/4], VO [n/4], LX [n/3]. Assessment: [LOW/MODERATE/HIGH/VERY HIGH].`

Example: `11/18 signals detected. Categories: SO 4/4, SY 3/5, ST 2/4, VO 2/4, LX 3/3. Assessment: HIGH.`

## Document History

**[2026-06-05 19:20]**
- Added: Calibration note on reasoning model scope (from `/reconcile` review AIDET-IN09-RV01)

**[2026-06-05 17:18]**
- Added: 6 new rules (AD-SY-04, AD-SY-05, AD-ST-04, AD-VO-04, AD-LX-01, AD-LX-02, AD-LX-03)
- Added: Lexical (LX) category - word-level generation artifacts
- Changed: Scoring thresholds updated for 18-rule set (was 12)
- Changed: Category weighting clarified (SO >= 3 = minimum HIGH)
- Added: `/detect-ai` workflow reference
- Changed: Application procedure updated to 6 steps covering 5 categories

**[2026-06-05 16:51]**
- Changed: Generalized all examples, removed references to specific analyzed text

**[2026-06-05 16:48]**
- Initial rules document created
- 12 rules across 4 categories (SO, SY, ST, VO)
- Scoring system with convergence thresholds
- Application procedure with 5 steps
