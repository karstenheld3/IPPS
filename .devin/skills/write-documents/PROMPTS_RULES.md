# Prompts File Rules

Rules for `_PROMPTS_[Topic].md` files. Verifiable from the artifact alone.

**Writing quality:** Apply `APAPALAN_RULES.md` to all prompt content. Key rules: AP-PR-07 (be specific), AP-BR-02 (sacrifice grammar for brevity), AP-ST-01 (goal first), AP-NM-01 (one name per concept).

## Rule Index

Format (FT)
- PRMT-FT-01: First non-empty line is an opening fence
- PRMT-FT-02: Fence length 3-9 backticks, outer exceeds deepest inner
- PRMT-FT-03: Separator `---` between every pair of consecutive prompts
- PRMT-FT-04: Commentary only between separator and next fence
- PRMT-FT-05: At least one prompt per file
- PRMT-FT-06: No content outside fences intended for the model

Structure (ST)
- PRMT-ST-01: Every prompt has an identifiable objective
- PRMT-ST-02: Implementation prompts include constraints
- PRMT-ST-03: Implementation prompts include verification criteria
- PRMT-ST-04: One reasoning mode per prompt
- PRMT-ST-05: Limit high-priority instructions to ~5-8 per prompt

Sequence (SQ)
- PRMT-SQ-01: No contradiction between prompts
- PRMT-SQ-02: Dependent prompts reference prior output explicitly
- PRMT-SQ-03: Commentary documents expected state between prompts

Content (CT)
- PRMT-CT-01: Objectives are specific and verifiable
- PRMT-CT-02: Constraints state what NOT to do
- PRMT-CT-03: Verification criteria are observable or machine-checkable
- PRMT-CT-04: No micromanaged implementation steps as objectives
- PRMT-CT-05: Precision over token savings (APAPALAN priority order)
- PRMT-CT-06: Signal redundancy preserved (MECT deliberate redundancy)
- PRMT-CT-07: Examples over descriptions for format and behavior

Naming (NM)
- PRMT-NM-01: Filename follows `_PROMPTS_[Topic].md` pattern
- PRMT-NM-02: Topic is CamelCase description of purpose

## PRMT-FT-01: Leading Fence Required

The first non-empty line of the file MUST be an opening fence. No header block, no frontmatter, no markdown title.

**BAD:**
```markdown
# Setup Prompts

This file sets up the project environment.

`` `
Create a new Next.js project with TypeScript.
`` `
```

**GOOD:**
`````markdown
```
Create a new Next.js project with TypeScript.
```
`````

## PRMT-FT-02: Fence Length

Each prompt chooses its own fence length (3-9 backticks). The outer fence MUST be longer than the deepest inner fence within that prompt.

**BAD** (inner fence closes the outer fence):
``````markdown
```
Write a README containing:
```bash
npm install
```
```
``````

**GOOD** (outer fence longer than inner):
``````markdown
````
Write a README containing:
```bash
npm install
```
````
``````

## PRMT-FT-03: Separator Between Prompts

Every pair of consecutive prompts requires a `---` separator line between the closing fence and the next opening fence.

**BAD** (missing separator):
`````markdown
```
First prompt.
```

```
Second prompt.
```
`````

**GOOD:**
`````markdown
```
First prompt.
```

---

```
Second prompt.
```
`````

## PRMT-FT-04: Commentary Placement

Commentary (headings, notes, explanations) is allowed ONLY between a `---` separator and the next opening fence. Commentary is for human readers and is never sent to the model.

**BAD** (commentary before first prompt):
`````markdown
## Setup Phase

This prompt creates the project.

```
Create a new project.
```
`````

**GOOD** (commentary between separator and next fence):
`````markdown
```
Create a new project.
```

---

## Step 2 - Add authentication

Previous step created the project skeleton. Now add auth.

```
Add JWT authentication to the Express server.
```
`````

## PRMT-FT-05: Minimum One Prompt

The file must contain at least one fenced prompt block. Empty files or files with only commentary are invalid.

## PRMT-FT-06: No Model-Intended Content Outside Fences

Any text outside fences is either commentary (never sent) or a format error. If content is intended for the model, it must be inside a fenced block.

**BAD** (instruction outside fence, silently dropped):
`````markdown
```
Create the database schema.
```

---

Also make sure to add indexes on the email column.

```
Write the migration script.
```
`````

**GOOD** (all model instructions inside fences):
`````markdown
```
Create the database schema. Add indexes on the email column.
```

---

```
Write the migration script for the schema created above.
```
`````

## PRMT-ST-01: Identifiable Objective

Every prompt must contain a clear objective: what the finished state looks like. The reader (human or `/verify`) should be able to state in one sentence what the prompt asks for.

**BAD:**
`````markdown
```
Look at the auth code and maybe fix some things if needed, also check tests.
```
`````

**GOOD:**
`````markdown
```
Fix the validateToken middleware so expired JWTs return 401 instead of crashing the server.
```
`````

## PRMT-ST-02: Constraints for Implementation

Prompts that modify files, install packages, or change configuration must include constraints (what not to do).

**BAD** (no boundaries):
`````markdown
```
Add user authentication to the API.
```
`````

**GOOD:**
`````markdown
```
Add JWT authentication to the Express API.

Constraints:
- No new npm dependencies (use existing jsonwebtoken package)
- Do not modify the database schema
- Do not change the existing /health endpoint
```
`````

## PRMT-ST-03: Verification for Implementation

Prompts that produce testable output must include verification criteria.

**BAD:**
`````markdown
```
Fix the payment calculation bug.
```
`````

**GOOD:**
`````markdown
```
Fix the payment calculation bug where tax is applied twice on discounted items.

Verify: Run `pnpm test:payments`. All tests pass. Order total for a 100 EUR item with 10% discount and 19% tax equals 106.29 EUR.
```
`````

## PRMT-ST-04: One Reasoning Mode Per Prompt

Each prompt should perform one type of cognitive work. Mixing modes degrades quality because the model has no signal which role it is playing.

Reasoning modes: research, analysis, planning, implementation, testing, formatting, review.

**BAD** (research + implement + test in one prompt):
`````markdown
```
Research the best auth library for Express, implement it, and write tests.
```
`````

**GOOD** (split into focused prompts):
`````markdown
```
Research JWT authentication libraries for Express. Compare jsonwebtoken, jose, and passport-jwt. Recommend one with rationale.
```

---

## Step 2 - implement the recommended library

```
Using the recommended library from step 1, add JWT authentication to the Express API. Issue tokens on POST /login, validate on protected routes.
```

---

```
Write tests for the authentication endpoints. Cover: valid login, invalid credentials, expired token, missing token.
```
`````

## PRMT-ST-05: Instruction Density Limit

Practitioner heuristic: limit each prompt to ~5-8 high-priority rules or instructions. Beyond that, the model tends to skip items in the middle of long lists (lost-in-the-middle effect). The exact threshold varies by model and task.

**BAD** (12 constraints in one prompt):
`````markdown
```
Build the dashboard.
- Use React 18
- Use TypeScript strict mode
- Use Tailwind CSS
- Use shadcn/ui components
- Use React Query for data fetching
- Use Zod for validation
- Use React Hook Form for forms
- Support dark mode
- Support i18n
- Add error boundaries
- Add loading skeletons
- Add analytics tracking
```
`````

**GOOD** (split across setup + implementation prompts):
`````markdown
```
Create a React 18 dashboard with TypeScript strict mode, Tailwind CSS, and shadcn/ui. Set up the project skeleton with routing and layout.
```

---

## Step 2 - features and data layer

```
Add data fetching with React Query and form handling with React Hook Form + Zod validation. Implement the user list and edit form.

Constraints:
- Follow existing component patterns from step 1
- No additional UI libraries
```
`````

## PRMT-SQ-01: No Contradictions

Later prompts must not contradict constraints or decisions from earlier prompts in the same file.

**BAD:**
`````markdown
```
Set up the project with SQLite for the database. No external database services.
```

---

```
Connect the API to PostgreSQL for better query performance.
```
`````

**GOOD** (consistent throughout):
`````markdown
```
Set up the project with SQLite for the database. No external database services.
```

---

```
Optimize the SQLite queries for the user search endpoint. Add appropriate indexes.
```
`````

## PRMT-SQ-02: Explicit Dependency References

When a prompt depends on output from a prior prompt, name the dependency.

**BAD** (implicit dependency):
`````markdown
```
Write tests for all the functions.
```
`````

**GOOD** (names what was produced):
`````markdown
```
Write tests for the calc.py file created in step 1. Cover add(), subtract(), and multiply() with edge cases: zero, negative numbers, floating point.
```
`````

## PRMT-SQ-03: Commentary Documents State

Commentary sections between prompts should document expected state for human readers: what the previous prompt should have produced, what the next prompt expects.

**BAD** (empty commentary, no context):
`````markdown
```
Create the config file.
```

---

```
Deploy the application.
```
`````

**GOOD:**
`````markdown
```
Create config.yaml with database connection settings, API keys from environment variables, and logging configuration.
```

---

## Step 2 - deploy with the generated config

Previous step created config.yaml. The application should now be configurable via environment variables.

```
Deploy the application to the staging environment. Verify config.yaml is loaded and database connection succeeds.
```
`````

## PRMT-CT-01: Specific Objectives

Objectives must be specific enough that two readers would agree on whether the prompt was fulfilled.

**BAD:** "Improve the code", "Clean up the project", "Make it better"

**GOOD:** "Reduce the average API response time below 200ms for the /users endpoint", "Remove all unused imports from src/utils/"

## PRMT-CT-02: Negative Constraints

Constraints state boundaries in negative form: what the agent must NOT do.

**BAD:** "Use the existing libraries" (positive instruction, not a constraint)

**GOOD:** "Do not install new dependencies. Use only libraries already in package.json"

## PRMT-CT-03: Observable Verification

Verification criteria must be observable (you can see the result) or machine-checkable (a command produces pass/fail).

**BAD:** "Make sure it works correctly", "Code should be clean"

**GOOD:** "Run `pnpm test`. All tests pass", "Endpoint returns 200 with JSON body containing `{ status: 'ok' }`"

## PRMT-CT-04: Objectives Not Implementation Steps

The objective describes the desired outcome, not the steps to get there. The agent determines implementation.

**BAD:** "Open auth.ts, find line 42, change the timeout from 30 to 60"

**GOOD:** "The auth token expires too quickly for long-running API operations. Increase the token TTL to 60 seconds"

## PRMT-CT-05: Precision Over Token Savings

APAPALAN's priority order applies to prompts: Precision (Priority 1) before Brevity (Priority 2). Never remove tokens that carry meaning to save context window space. One failed re-execution costs 10-50x more tokens than the precision tokens saved.

**BAD** (saves ~40 tokens by cutting precision):
`````markdown
```
Fix expired JWT handling in validateToken. No new deps. Run tests.
```
`````

**GOOD** (invests tokens in disambiguation):
`````markdown
```
Fix the validateToken middleware so expired JWTs return 401 instead of crashing the server.

Constraints:
- Do not modify the token generation logic in auth/issuer.ts
- Do not change the JWT secret rotation schedule

Verify: Run `pnpm test:auth`. All tests pass.
```
`````

The GOOD prompt costs ~35 more tokens. It succeeds on first execution. The BAD prompt omits the failure symptom (crash vs wrong status), scopes constraints too broadly ("no new deps" vs naming specific files to protect), and uses generic verification ("run tests" vs naming the test suite). Each omission is a guess the model must make - and may guess wrong.

**Token budget priority** (spend first on highest-impact items):
1. Constraints (prevent wrong actions - highest ROI per token)
2. Verification criteria (define done - prevents unbounded work)
3. Disambiguation (resolve ambiguous referents - prevents wrong targets)
4. Objective specificity (narrow scope - prevents over-engineering)
5. Examples (show format - replaces verbose descriptions)

## PRMT-CT-06: Signal Redundancy Preserved

MECT's deliberate redundancy principle: words that strengthen the model's association field are signal, not waste. Restating a referent, repeating a constraint qualifier, or naming a specific entity costs tokens but prevents the model from guessing wrong.

**BAD** (compressed - model may bind "it" to wrong referent):
`````markdown
```
Fix it. Also update the tests for it. Make sure it works with the new version.
```
`````

**GOOD** (referents restated - no ambiguity):
`````markdown
```
Fix the rate limiter in api/middleware.ts. Update the rate limiter tests in tests/middleware.test.ts. Verify the rate limiter works with Redis 7.x (the version deployed in staging).
```
`````

The GOOD prompt repeats "rate limiter" three times. Each repetition anchors the model to the correct target. Replacing any with "it" creates a potential misresolution that costs far more than 2 tokens per instance.

**Test**: "If I replace this noun with 'it' or 'this', could the model bind it to the wrong thing?" If yes, keep the explicit referent.

## PRMT-CT-07: Examples Over Descriptions for Format and Behavior

When a prompt must produce output in a specific format, show one example instead of describing the format in prose. AP-BR-05 (show format over describing format) applies directly. Examples are simultaneously more precise AND more token-efficient than descriptions.

**BAD** (describes format - 45 tokens, still ambiguous):
`````markdown
```
Generate a config file with database settings. It should have a top-level key for the database section, containing host, port, username, password, and database name fields, formatted as a YAML file with proper indentation.
```
`````

**GOOD** (shows format - 30 tokens, unambiguous):
``````markdown
````
Generate config.yaml with database connection settings.

Example output format:
```yaml
database:
  host: localhost
  port: 5432
  username: app_user
  password: ${DB_PASSWORD}
  name: myapp_production
```

Use environment variables for secrets.
````
``````

**Rules for examples in prompts:**
- One example per format. The model generalizes from one representative instance
- Place after objective and constraints, before verification
- Use realistic but generic values (privacy gate applies - no real credentials, addresses, or identifiers)
- If the codebase already contains the pattern, reference the file instead: "Follow the pattern in `src/api/users.py`"

## PRMT-NM-01: Filename Pattern

`_PROMPTS_[Topic].md` where Topic is CamelCase.

**BAD:** `prompts.md`, `PROMPTS-setup.md`, `_PROMPTS_setup project.md`

**GOOD:** `_PROMPTS_SetupProject.md`, `_PROMPTS_MigrateAuth.md`, `_PROMPTS_AnalyzePerformance.md`

## PRMT-NM-02: Topic Describes Purpose

The Topic in the filename describes the prompts file purpose, not the project or session.

**BAD:** `_PROMPTS_MyProject.md`, `_PROMPTS_Session3.md`

**GOOD:** `_PROMPTS_SetupCICD.md`, `_PROMPTS_RefactorAuthModule.md`
