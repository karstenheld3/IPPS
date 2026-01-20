/session-new 

I want to improve the concept of AGEN (Agentic English), EDIRD, and the way windsurf workflws are designed. Prepare a new session

Problems:
- workflow implementations should have almost no information or dependencies about the applied phase model (EDIRD)
- workflows should contain knownledge about how to accomplish a task. What the task is, what a completed task looks like, what tools and context is needed to accomplish a task, what strategies can be used in different contexts.
- workflows should have dependencies to AGEN and the document writing skills
- Currently we can't exchange the EDIRD phase model against another one that would expose more higher level entry points (as EDIRD exposes "build" and "solve")
- Currently, verbs can't be extended within the cope of [WORKSPACE], [PROJECT], [SESSION]
- Currently, we don't have a central TOPIC ID registry in the [WORKSPACE].
- Current AGEN has 2 types: "Instruction Tokens" = stuff in [BRACKES] and "Context States" -> stuff in UPPERCASE. I want to generalize this so that TOPICs, Concepts and states are captured by stuff in UPPERCASE. We want workspace wide uniqueness for these constants. Maybe CONSTANT vs [INSTRUCTION] is good.
- Currently an IMPL plan is directly implemented. This gives the agent too much freedom to choose arbitrary strategies that might fail. We 

Goal:
- Formalize a concept and notation called STRUT ("Structured Thinking")
- Formalize the document writing skill as TRACTFUL ("Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle")
- Formalize the used document ID system that produces the [DOCID] ids as TDID ("Tractful Document ID system") see section below
  - replace "Doc ID" with "Doc ID (TDID)" in all templates
- add more verbs to AGEN and EDIRD:
  - recap -> analyzes conversation and context, revisits STRUCT plan and identifies status
  - continue -> forward-looking assessment of next things on the to-do list and execution
  - go -> the sequence of [RECAP] and [CONTINUE] the universal command for starting and resuming work until the final goal is reached and all STRUT phases have been traversed. replaces "next
  - learn -> Analyzes the conversation, context, session documents for fails and documents them in FAILS.md
  - read -> reads whatever we give it in the most careful 
  - research -> performs an interative research strategy using a special method: Striving for MEPI (Most Executable Point of Information), not MCPI (Most Complete Point of Information. Always evaluating options and sources against each other, dropping noise, redundancy, speculative content and unverified sources. Ranking sources and options by SOCAS: Signs of Carelessness and 
  - partition -> partition an existing IMPL, TEST, TASK plans into discreete (and testable) chunks of work with clear acceptance criteria. Allow for different partitioning strategies based on type of problem or task. Usually outputs a proposal for a TASKS plan.
- Guarantee, that TOPIC IDs are registered in the Workspace and a TOPIC-ID is never created twice (uniqueness)
- Revisit the current learning mechanism via FAILS.md: How willl this capture conceptual, planning, and assessment fails, not just technical and implementation fails?
- Add TASKS_TEMPLATE.md and "write-task-plan.md" skill
- Add new "AC" Acceptance Criteria section  to SPECs: These (together with proven IG Implementation Guarantees) should define, when a SPEC was implemented.


Acceptance Criteria (for this session):
- All specs are harmonized: Minimum overlap, clear responsibilities, support goal, all phases covered
- Agent can used formalized thinking using the SRUCT method (approach and notation) to plan, progress, update, verify, and complete VERY long runs (or projects, maybe divided into multiple sessions) of (software) development and problem solving tasks completely autonomously.
- Separation of concerns: STRUCT gives method and formal framework, EDIRD gives thinking logic and apprach, defines dependency tree and acceptance criteria options, TRACTFUL gives implementation framwork. AGEN gives language to ensure everything can work together and layers can cross-reference each other. TDID guarantees that documents and document items can be globally cross-referenced.
- After a run all work (session and outcome) is fully documented and packaged
- We have a working solution of solving workspace wide uniqueness for CONSTANTS
- We have added the new TASKS template and writing skill (as part of existing document writing skill)


Output:
- DevSystemV3.1 (you can already create folder)
- 3 x SPECs: SRTUT, TRACTFUL, TDID (dont create yet)
- Updated AGEN and EDIRD specs to reflect changes and new concepts (copy AGEN-SP01, EDIRD-SP04 to session folder and increase numbers)





# TRACTFUL Summary
TRACTFUL - Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle

Goal: Provide a structured, traceable documentation framework that guides software development from initial idea through deployment, ensuring nothing is lost between conception and delivery.

Scope: Full development lifecycle - EXPLORE (research) → DESIGN (specification) → IMPLEMENT (code) → REFINE (review) → DELIVER (deploy). Covers requirements, decisions, implementation, testing, fixes, and lessons learned.

Contents:

INFO - Research and analysis documents
SPEC - Technical specifications with FR/DD/IG
IMPL - Implementation plans with steps and edge cases
TEST - Test plans with cases and verification
FIX - Fix tracking during implementation
FAILS - Failure log (lessons learned)
REVIEW - Issue tracking and recommendations
Methods:

Universal ID system for cross-document traceability
Standardized templates per document type
Verb-driven actions ([WRITE-SPEC], [WRITE-IMPL-PLAN], etc.)
MUST-NOT-FORGET sections for critical constraints
Concise formatting (lists, ASCII diagrams, no tables)
Dependency declarations between documents
Reverse-chronological document history


# SOCAS
SOCAS — Signs of Carelessness and Sloppyness

- Inconsistent terminology: Same concept named multiple ways, or same word used for different things.
- Undefined or hand-wavy concepts: Key nouns or mechanisms introduced without clear definition or boundaries.
- Unnecessary complexity: Extra layers, abstractions, or frameworks that do not clearly earn their cost.
- Overlapping responsibilities: Two components, processes, or features partially doing the same job.
- Gaps in reasoning: Conclusions that are not traceably supported by stated premises or evidence.
- Implicit assumptions: Critical constraints, behaviors, or conditions left unstated or unexamined.
- Local optimization: Improvements that ignore system-level effects, tradeoffs, or failure modes.
- Ambiguity left unresolved: Known questions or conflicts deferred without decision, owner, or plan.
- Presentation sloppiness: Typos, mismatched diagrams, stale references, or structure that obscures the point.
- No explicit tradeoffs: Choices presented as obvious, with no discussion of alternatives or downsides.