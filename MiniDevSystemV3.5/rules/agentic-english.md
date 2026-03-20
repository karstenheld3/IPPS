# Agentic English (AGEN)

Planning vocabulary for agent reasoning and problem decomposition.

## Scope

Used in: STRUT plans (`[ ] P1-S1 [VERB](params)`), EDIRD phase planning, skill verb mappings, document planning.

NOT used in: Workflow step instructions, agent skills (unless explicitly referencing AGEN), code comments, user-facing docs.

Formal `[VERB](params)` notation is reserved for STRUT plans and planning documents.

## Syntax

### Instructions `[BRACKETS]`

Tokens the agent reads and executes:
- `[VERB]` - Action to execute
- `[PLACEHOLDER]` - Value to substitute
- `[LABEL]` - Classification to apply

Verb modifiers: `[VERB]-OK` (proceed), `[VERB]-FAIL` (re-iterate/escalate), `[VERB]-SKIP` (intentionally skipped)

### States `NO-BRACKETS`

Tokens for conditions/branching: `PREFIX-VALUE` format (e.g., `COMPLEXITY-HIGH`, `HOTFIX`). Used in conditional headers. Never substituted or executed.

## Placeholders

- **[ACTOR]** - Decision-making entity (default: user, in /go-autonomous: agent)
- **[WORKSPACE_FOLDER]** - Absolute path of root folder where agent operates
- **[PROJECT_FOLDER]** - Absolute path of project folder (same as workspace if no monorepo)
- **[SESSION_FOLDER]** - Absolute path of currently active session folder
- **[SRC_FOLDER]** - Absolute path of source folder
- **[AGENT_FOLDER]** - Agent config folder (`.windsurf/` or `.claude/`)
- **[DEVSYSTEM]** - Current DevSystem version
- **[DEVSYSTEM_FOLDER]** - Path to DevSystem folder

## Verbs

### Information Gathering
- **[RESEARCH]** - Web search, read docs, explore options
- **[ANALYZE]** - Study code, data, or documents
- **[EXPLORE]** - Open-ended investigation without specific target
- **[INVESTIGATE]** - Focused inquiry into specific issue
- **[GATHER]** - Collect information, logs, context, requirements
- **[PRIME]** - Load most relevant information into context
- **[READ]** - Careful, thorough reading with attention to detail

### Thinking and Planning
- **[SCOPE]** - Define boundaries and constraints
- **[FRAME]** - Structure the problem or approach
- **[PLAN]** - Create structured approach with steps
- **[PARTITION]** - Break large plan into small testable steps (TASKS document)
- **[DECIDE]** - Make a choice between options
- **[ASSESS]** - Assess effort, time, risk, or complexity
- **[PRIORITIZE]** - Order by importance or urgency
- **[EVALUATE]** - Compare options against criteria, score, rank
- **[SYNTHESIZE]** - Combine findings into coherent understanding
- **[CONCLUDE]** - Draw conclusions from analysis
- **[DEFINE]** - Establish clear definitions or criteria
- **[RECAP]** - Analyze context, revisit plan, identify current status
- **[CONTINUE]** - Forward-looking assessment, execute next items on plan
- **[GO]** - Sequence of [RECAP] + [CONTINUE] until goal reached

### Validation and Proof
- **[PROVE]** - POC, spike, minimal test to validate idea
- **[PROTOTYPE]** - Build working draft to test approach
- **[VERIFY]** - Check against formal rules, specs, conventions (compliance)
- **[TEST]** - Run automated tests
- **[REVIEW]** - Inspect work (open-minded)
- **[CRITIQUE]** - Find flaws in logic, strategy, goal alignment (disregards formal rules)
- **[RECONCILE]** - Bridge ideal and feasible, balance trade-offs (disregards formal rules)

### Documentation
- **[WRITE]** - Generic write action
- **[WRITE-INFO]** - Write INFO document (research findings)
- **[WRITE-SPEC]** - Write SPEC document (specification)
- **[WRITE-IMPL-PLAN]** - Write IMPL document (implementation plan)
- **[WRITE-TEST-PLAN]** - Write TEST document (test plan)
- **[OUTLINE]** - Create high-level structure
- **[SUMMARIZE]** - Create concise summary
- **[DRAFT]** - Create initial version for review

### Implementation
- **[IMPLEMENT]** - Write code or implement proposed changes
- **[CONFIGURE]** - Set up or update environment/settings
- **[INTEGRATE]** - Connect components
- **[REFACTOR]** - Restructure code per stated goal
- **[FIX]** - Correct issues
- **[IMPROVE]** - General quality improvements
- **[OPTIMIZE]** - Performance, memory, or efficiency improvements only

### Communication
- **[CONSULT]** - Request input, clarification, decisions from [ACTOR]
- **[CLARIFY]** - Make something clearer or resolve ambiguity
- **[QUESTION]** - Ask specific questions to gather information
- **[STATUS]** - Write status report
- **[PROPOSE]** - Present multiple options for [ACTOR] to choose from
- **[RECOMMEND]** - Suggest single option with rationale
- **[CONFIRMS]** - Confirm approach or result with [ACTOR]
- **[PRESENT]** - Share findings or results with [ACTOR]

### Completion
- **[HANDOFF]** - Transfer to next phase/person
- **[COMMIT]** - Git commit
- **[MERGE]** - Combine branches
- **[DEPLOY]** - Push to environment
- **[FINALIZE]** - Perform all activities to allow for task closure
- **[CLOSE]** - Mark as done and sync data to container
- **[ARCHIVE]** - Archive closed

## Labels

### Assumption Labels
- **[UNVERIFIED]** - Assumption made without evidence
- **[CONTRADICTS]** - Logic conflicts with other statement/code
- **[OUTDATED]** - Assumption may no longer be valid
- **[INCOMPLETE]** - Reasoning missing critical considerations

### Status Labels
- **[RESOLVED]** - Issue fixed, documented for reference
- **[WONT-FIX]** - Acknowledged risk, accepted trade-off
- **[NEEDS-DISCUSSION]** - Requires [CONSULT] with [ACTOR]

## States

### Workspace Context
- **SINGLE-PROJECT** - Workspace contains one project
- **MONOREPO** - Workspace contains multiple independent projects
- **SESSION-MODE** - Time-limited session with specific goals
- **PROJECT-MODE** - Work spans entire project without session boundaries

### Complexity Assessment
Maps to semantic versioning:
- **COMPLEXITY-LOW** - Single file, clear scope, no dependencies (patch)
- **COMPLEXITY-MEDIUM** - Multiple files, some dependencies (minor)
- **COMPLEXITY-HIGH** - Breaking changes, new patterns, external APIs (major)

### Problem Type (SOLVE workflow)
- **RESEARCH** - Explore topic, gather information
- **ANALYSIS** - Deep dive into data or situation
- **EVALUATION** - Compare options, make recommendations
- **WRITING** - Create documents, books, reports
- **DECISION** - Choose between alternatives
- **HOTFIX** - Production down
- **BUGFIX** - Defect investigation