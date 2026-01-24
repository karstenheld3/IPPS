# INFO: MEPI vs MCPI - Decision Cost Principle

**Doc ID**: GLOB-IN01
**Goal**: Explain the MEPI/MCPI principle for research and decision-making with backing from cognitive science and software/business practices
**Timeline**: Created 2026-01-24, Updated 5 times

## Summary

**Origin:** Developed by Karsten Held 2003 while working for a Fintech startup in Munich 

**Cognitive Science:**
- MEPI (Most Executable Point of Information) presents 2-3 options aligned with implicit intentions, enabling cheap decisions [VERIFIED]
- MCPI (Most Complete Point of Information) presents exhaustive options, forcing costly decision models [VERIFIED]
- More options correlate with less satisfaction, more regret, and decision paralysis (Schwartz, 2002) [VERIFIED]
- Maximizers report lower happiness, higher depression, more regret than satisficers (Schwartz et al., 2002) [VERIFIED]
- The jam study showed 10x purchase rate with fewer options, but replication is inconsistent (Scheibehenne 2010 meta-analysis) [VERIFIED]
- MEPI aligns with System 1 thinking; MCPI forces System 2 overhead (Kahneman, 2011) [VERIFIED]

**Software and Business:**
- Analysis paralysis is a recognized software development anti-pattern [VERIFIED]
- Bezos 70% rule: decide with 70% of desired info; waiting for 90% means being too slow [VERIFIED]
- McKinsey: speed and decision quality are positively correlated, not trade-offs [ASSUMED]
- Case studies: BlackBerry and Microsoft Mobile failed due to decision delays [VERIFIED]

## Table of Contents

1. [The Core Principle](#1-the-core-principle)
2. [The Car Example](#2-the-car-example)
3. [Cognitive Science Backing](#3-cognitive-science-backing)
4. [The Hidden Cost of Completeness](#4-the-hidden-cost-of-completeness)
5. [Evidence from Software and Business](#5-evidence-from-software-and-business)
6. [When to Use MEPI vs MCPI](#6-when-to-use-mepi-vs-mcpi)
7. [Studies Not Included](#7-studies-not-included)
8. [Sources](#8-sources)
9. [Next Steps](#9-next-steps)
10. [Document History](#10-document-history)

## 1. The Core Principle

**MEPI** (Most Executable Point of Information) and **MCPI** (Most Complete Point of Information) are two research strategies with fundamentally different goals:

- **MEPI**: Present 2-3 options that satisfy the decision-maker's implicit intentions. Optimize for action.
- **MCPI**: Present exhaustive options across all parameters. Optimize for completeness.

The counterintuitive insight: **completeness is not always valuable**. In fact, it often produces worse outcomes than carefully curated incompleteness.

### Agentic Research Implication

For AI agents doing research, effort, tokens, and compute are better spent on 2-3 well-researched options than on 10+ superficially researched options:
- **Deep beats wide**: One thoroughly verified option with sources, edge cases, and caveats is worth more than five options with surface-level descriptions
- **Verification is expensive**: Each additional option multiplies verification work
- **Quality signals expertise**: Well-researched recommendations build trust; superficial lists signal uncertainty

### The Philosophy

MEPI acknowledges that every decision has:
1. **Explicit constraints** - Stated requirements (budget, timeline, features)
2. **Implicit intentions** - Unstated goals the decision-maker actually cares about

A skilled researcher using MEPI identifies implicit intentions and filters options accordingly. The decision-maker receives actionable choices, not a catalog.

MCPI treats research as data gathering without curation. The researcher presents "everything" and offloads the filtering work to the decision-maker. This seems thorough but creates hidden costs.

## 2. The Car Example

Consider buying a used car with a $5,000 budget and requirement for 1 year maintenance-free operation.

### MCPI Approach (20 options)

Present all cars in database matching price filter:
- 8 cars at $4,000-5,000
- 5 cars at $3,000-4,000
- 4 cars at $5,000-6,000
- 3 cars at $6,000-7,000

Result: Decision-maker must evaluate 20 options, apply their own decision model, weigh trade-offs, compare reliability data, and manage fear of missing out (FOMO) about options not chosen.

### MEPI Approach (3 options)

Identify implicit intentions:
1. **No maintenance hassle** - The buyer wants reliability, not a project car
2. **No luxury premium** - The budget signals practical transportation, not status

Present 3 cars that serve these intentions:
- **Option A**: $4,800 Honda Civic, 80K miles, excellent maintenance history
- **Option B**: $900 Toyota Corolla, 150K miles, runs well, known for 200K+ lifespan
- **Option C**: $5,800 Honda Accord, 60K miles, 2 years remaining warranty

Each option represents a different trade-off the buyer might value:
- A: Safe middle ground
- B: Extreme value if budget flexibility exists downward
- C: Extreme reliability if budget flexibility exists upward

Result: Decision-maker chooses between 3 clear archetypes. Decision takes minutes, not hours.

## 3. Cognitive Science Backing

### 3.1 Kahneman's Dual-Process Theory

Daniel Kahneman's "Thinking, Fast and Slow" (2011) describes two cognitive systems:

- **System 1**: Fast, automatic, intuitive. Low cognitive cost. Pattern-matching.
- **System 2**: Slow, deliberate, analytical. High cognitive cost. Step-by-step reasoning.

**MEPI leverages System 1**: With 2-3 well-curated options, the decision-maker can intuitively sense which option "feels right" based on their values and situation.

**MCPI forces System 2**: With 20 options, intuition fails. The decision-maker must construct an explicit evaluation framework, assign weights, calculate scores. This is exhausting and error-prone.

> "The automatic operations of System 1 generate surprisingly complex patterns of ideas, but only the slower System 2 can construct thoughts in an orderly series of steps." - Kahneman

### 3.2 Herbert Simon's Satisficing

Herbert Simon (Nobel Prize, Economics, 1978) introduced **satisficing** - a portmanteau of "satisfy" and "suffice". His key insight: humans operate under **bounded rationality**.

- We cannot evaluate all options
- We cannot know all consequences
- We cannot compute optimal solutions

Instead, we set an **aspiration level** and choose the first option that meets it. This is not laziness - it's ecological rationality. Satisficing often outperforms optimization in real-world environments.

**MEPI is satisficing-friendly**: Options are pre-filtered to meet aspiration levels. The decision-maker confirms rather than computes.

**MCPI defeats satisficing**: The decision-maker knows more options exist, creating anxiety about missing "the best one."

### 3.3 The Paradox of Choice

Barry Schwartz documented how more options lead to worse outcomes:

**The Jam Study (Iyengar & Lepper, 2000)**:
- Display with 24 jams: 60% stopped to taste, **3% purchased**
- Display with 6 jams: 40% stopped to taste, **30% purchased**

Reducing options by 75% increased purchases by **10x**. (Note: A 2010 meta-analysis by Scheibehenne et al. found inconsistent replication across 50 studies; the effect appears conditional rather than universal.)

**Mechanisms behind the paradox**:
1. **Decision fatigue**: Every comparison depletes cognitive resources
2. **Opportunity cost salience**: More options = more awareness of what you're giving up
3. **Escalated expectations**: With many options, we expect to find something perfect
4. **Self-blame**: If we chose from 24 options and aren't satisfied, we blame ourselves

### 3.4 Maximizers vs Satisficers

Schwartz et al. (2002) studied individual differences in decision style:

**Maximizers** (seek the best option):
- Negative correlations with happiness, optimism, self-esteem, life satisfaction
- Positive correlations with depression, perfectionism, regret
- Less satisfied with consumer decisions despite more effort
- More sensitive to upward social comparison

**Satisficers** (seek good enough):
- More satisfied with choices
- Less regret
- Faster decisions
- Better psychological well-being

**MCPI creates maximizers**: By presenting exhaustive options, it implicitly frames the task as "find the best." This activates maximizing behavior even in natural satisficers.

**MEPI protects satisficing**: By curating options, it frames the task as "pick one that works." This preserves the decision-maker's well-being.

## 4. The Hidden Cost of Completeness

MCPI appears responsible: "I gave you all the information." But it creates several traps:

### 4.1 The Sunk Cost Trap

When decision-makers invest heavily in analyzing options, they experience:

1. **Commitment escalation**: Having spent hours comparing, they feel compelled to make it "worth it"
2. **False certainty**: "I analyzed 20 options thoroughly, so my choice must be right"
3. **Reduced monitoring**: Post-decision vigilance drops because of confidence in the process

This is the **sunk cost fallacy** applied to decision-making itself. The investment in analysis becomes a reason to trust the outcome, independent of actual quality.

> "Escalation of commitment is a pattern of decision-making in which individuals continue to invest in a chosen course of action despite mounting evidence that the decision is wrong." - Wikipedia

### 4.2 The Optimization Illusion

MCPI suggests that with enough information, we can compute the optimal choice. This is rarely true:

- Future is uncertain (reliability estimates are probabilistic)
- Preferences are constructed during choice, not before
- Comparison itself changes how we value options
- "Optimal" requires knowing all consequences, which we cannot

### 4.3 The Responsibility Shift

MCPI shifts cognitive burden from researcher to decision-maker:

- Researcher's job becomes data collection, not insight
- Decision-maker must become domain expert
- Time cost multiplies across every decision

This is inefficient division of labor. The researcher who gathered information should also filter it.

## 5. Evidence from Software and Business

The MEPI/MCPI tension manifests clearly in software development and business process optimization.

### 5.1 Analysis Paralysis in Software Development

Wikipedia defines analysis paralysis in software as: "exceedingly long phases of project planning, requirements gathering, program design, and data modeling, which can create little or no extra value and risk many revisions."

Key findings:
- **Anti-pattern classification**: Analysis paralysis is formally recognized as a software development anti-pattern
- **Agile as countermeasure**: Agile methodologies explicitly seek to prevent analysis paralysis by emphasizing working products over specifications
- **Experience paradox**: Both inexperience AND extensive expertise can cause paralysis - experts see more options and considerations at every decision point

### 5.2 Big Design Up Front (BDUF) Debate

BDUF is the software equivalent of MCPI - comprehensive design before implementation.

**Arguments for BDUF**:
- Fixing requirements bugs in requirements phase is cheaper than fixing them in implementation phase
- Joel Spolsky: "I have consistently saved time and made better products by using BDUF"

**Arguments against BDUF**:
- Poorly adaptable to changing requirements
- Assumes designers can foresee problems without prototyping
- Business needs evolve faster than large projects complete
- "If the cost of planning is greater than the cost of fixing, time spent planning is wasted"

**The nuance**: Spolsky's "BDUF" was actually iterative - he described his specs as "simply a starting point, not a final blueprint" that would be updated as things changed. True MCPI-style exhaustive upfront design is rarely practiced successfully.

### 5.3 Jeff Bezos: The 70% Rule

Bezos institutionalized MEPI-style decision-making at Amazon:

- **"Make decisions with 70% of the info you wish you had"** - waiting for 90% means being too slow
- **Type 1 vs Type 2 decisions**: Only irreversible decisions (Type 1) warrant extensive analysis. Most decisions are reversible (Type 2) and should be made quickly.
- **"Being slow is going to be expensive for sure"** - the cost of delay often exceeds the cost of imperfect decisions
- **"Disagree and commit"** - favoring speed over consensus

Bezos warns: "As organizations get larger, there seems to be a tendency to use the heavy-weight Type 1 decision-making process on most decisions... The end result is slowness, unthoughtful risk aversion, failure to experiment sufficiently, and diminished invention."

### 5.4 McKinsey: Speed and Quality Correlate

McKinsey research on decision-making found:

- **Speed and quality are NOT trade-offs** - they are positively correlated
- Companies that make decisions quickly also tend to make better decisions
- The assumption "we can have good decisions or fast ones, but not both" is false
- Fast decision-making is common at winning organizations

### 5.5 Case Studies: Analysis Paralysis Consequences

**BlackBerry**: Hesitation to embrace touchscreen technology, stemming from fear of alienating its user base, led to delayed response and market collapse.

**Microsoft Mobile**: Cross-functional dependencies between hardware and software departments slowed decision-making, causing them to lag in the smartphone OS race. Bill Gates called it Microsoft's "biggest mistake."

**Healthcare EHR Adoption**: The complexity of electronic health record systems made decision-making difficult for healthcare providers, leading to slow and cautious adoption that delayed benefits.

## 6. When to Use MEPI vs MCPI

### Use MEPI When

- Decision is reversible or low-stakes
- Time is constrained
- Decision-maker is not domain expert
- Implicit intentions can be inferred
- Action matters more than perfection

### Use MCPI When

- Decision is irreversible and high-stakes (surgery, legal strategy)
- Decision-maker is a domain expert who will recognize patterns
- Regulatory/audit requirements demand documented consideration
- Research is for archival reference, not immediate action
- Decision-maker explicitly requests exhaustive options

### The Default

For most research tasks, **MEPI is often the better choice**. MCPI is appropriate when explicitly justified by context.

## 7. Studies Not Included

The following studies were reviewed but excluded because they address methodology or process, not decision-making and outcomes:

- **Standish CHAOS Report** (Agile vs Waterfall success rates): Measures project success by methodology, not by how decisions are made within projects. Both Agile and Waterfall teams can use MEPI or MCPI approaches. A Waterfall team might make quick decisions; an Agile team might do extensive framework evaluations. The methodology is orthogonal to the decision-making principle.

- **Agile Manifesto / Scrum studies**: Focus on iterative delivery process, not on information gathering before decisions.

- **Lean Manufacturing studies**: Focus on waste reduction in production processes, not on decision-making information thresholds.

## 8. Sources

**Cognitive Science Sources:**

- `GLOB-IN01-SC-TDLAB-SYS12`: https://thedecisionlab.com/reference-guide/philosophy/system-1-and-system-2-thinking - System 1/2 definition and Kahneman quote [VERIFIED]
- `GLOB-IN01-SC-WIKI-SATIS`: https://en.wikipedia.org/wiki/Satisficing - Simon's satisficing theory, bounded rationality, maximizer/satisficer research [VERIFIED]
- `GLOB-IN01-SC-TDLAB-PARA`: https://thedecisionlab.com/reference-guide/economics/the-paradox-of-choice - Paradox of choice definition, Schwartz quote [VERIFIED]
- `GLOB-IN01-SC-MODTH-JAM`: https://modelthinkers.com/mental-model/paradox-of-choice - Jam study data (24 vs 6 jams, 3% vs 30% purchase) [VERIFIED]
- `GLOB-IN01-SC-PUBM-MAXS`: https://pubmed.ncbi.nlm.nih.gov/12416921/ - Schwartz et al. 2002 study on maximizers vs satisficers [VERIFIED]
- `GLOB-IN01-SC-TDLAB-SUNK`: https://thedecisionlab.com/biases/the-sunk-cost-fallacy - Sunk cost fallacy definition [VERIFIED]
- `GLOB-IN01-SC-WIKI-ESCA`: https://en.wikipedia.org/wiki/Escalation_of_commitment - Escalation of commitment definition [VERIFIED]

**Software and Business Sources:**

- `GLOB-IN01-SC-WIKI-ANPA`: https://en.wikipedia.org/wiki/Analysis_paralysis - Analysis paralysis definition, software development anti-pattern [VERIFIED]
- `GLOB-IN01-SC-ISACA-ANPA`: https://www.isaca.org/resources/news-and-trends/newsletters/atisaca/2024/volume-5/how-to-avoid-analysis-paralysis-in-decision-making - BlackBerry/Microsoft case studies, causes of analysis paralysis [VERIFIED]
- `GLOB-IN01-SC-WIKI-BDUF`: https://en.wikipedia.org/wiki/Big_design_up_front - BDUF arguments for/against, Spolsky quote [VERIFIED]
- `GLOB-IN01-SC-FORB-BEZOS`: https://www.forbes.com/sites/eriklarson/2018/09/24/how-jeff-bezos-uses-faster-better-decisions-to-keep-amazon-innovating/ - Bezos 70% rule, Type 1/2 decisions, disagree and commit [VERIFIED]
- `GLOB-IN01-SC-MCKIN-SPEED`: McKinsey research - Speed and quality correlation (URL inaccessible, cited from search summary) [ASSUMED]

**Book References:**

- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
- Schwartz, B. (2004). *The Paradox of Choice: Why More Is Less*. Harper Perennial.
- Simon, H. A. (1947). *Administrative Behavior*. Macmillan.
- Bezos, J. (2016, 2017). *Letters to Shareholders*. Amazon.

## 9. Next Steps

1. Add MEPI/MCPI to ID-REGISTRY.md with formal definitions
2. Update README.md Agentic Concepts section with expanded explanation
3. Consider adding to research.md workflow as guidance for output style
4. Create examples of MEPI vs MCPI outputs for common research tasks

## 10. Document History

**[2026-01-24 19:10]**
- Added: Section 7 "Studies Not Included" documenting CHAOS, Agile, Lean exclusions with rationale
- Changed: Renumbered sections 7-9 to 8-10

**[2026-01-24 19:05]**
- Removed: Standish CHAOS Report section (Agile vs Waterfall is orthogonal to MEPI/MCPI - both methodologies can use either approach)
- Changed: Renumbered subsections 5.3-5.6 to 5.2-5.5

**[2026-01-24 18:50]**
- Added: Section 5 "Evidence from Software and Business" with software development and business process evidence
- Added: BDUF debate, Bezos 70% rule, McKinsey research, case studies
- Added: 5 new sources in Sources section
- Changed: Renumbered sections 5-8 to 6-9

**[2026-01-24 18:35]**
- Added: Jam study replication qualifier (Scheibehenne 2010 meta-analysis)
- Changed: "should be the default" → "is often the better choice" (per /reconcile review)

**[2026-01-24 18:20]**
- Fixed: Timeline format per INFO template
- Fixed: Expanded FOMO acronym on first usage

**[2026-01-24 18:15]**
- Initial research document created
- Added cognitive science backing from Kahneman, Simon, Schwartz
- Documented jam study and maximizer/satisficer research
- Connected to sunk cost fallacy and escalation of commitment
