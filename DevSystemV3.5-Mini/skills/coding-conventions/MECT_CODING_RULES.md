# MECT Coding Rules

MECT = Minimal Explicit Consistent Terminology
APAPALAN = As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)

Actionable rules for identifiers, functions, types, comments, logs, errors, and APIs.

## Rule Index

Precision (PR) - Every name and message unambiguous
- MC-PR-01: One name per concept across codebase
- MC-PR-02: Unambiguous compound names (word order determines meaning)
- MC-PR-03: No dangerous meta-words without qualifier
- MC-PR-04: Be specific in comments - concrete, verifiable statements
- MC-PR-05: Error messages state what failed, why, and recovery action
- MC-PR-06: Log messages: self-contained, full disclosure
- MC-PR-07: Include canonical identifiers in errors (file, line, entity ID)

Brevity (BR) - Minimal without losing meaning
- MC-BR-01: Simplest verb - no hidden verbs in names
- MC-BR-02: Comments: drop filler, be direct
- MC-BR-03: Function names describe output, not mechanism
- MC-BR-04: Boolean functions: is_/has_/can_ prefix, no "check_"

Consistency (CO) - Same pattern everywhere
- MC-CO-01: Corresponding pairs use same word stem
- MC-CO-02: Consistent key=value format in logs
- MC-CO-03: Convergent naming - same terms in URL, payload, docs, logs
- MC-CO-04: Consistent patterns across all similar constructs
- MC-CO-05: Keep established API names - don't rename working terms

Naming Design (ND) - Structure for scalable naming
- MC-ND-01: Naming structure method (explicit -> specifiers -> states -> mnemonics)
- MC-ND-02: Canonical form for IDs and data structures
- MC-ND-03: No recursive/implicit naming
- MC-ND-04: No product-as-term collision
- MC-ND-05: Type name = domain concept, not implementation detail
- MC-ND-06: Disambiguate by qualifying, not renaming
- MC-ND-07: Intuitive opposites for paired parameters

Documentation (DC) - Code-adjacent writing
- MC-DC-01: Four description types (what/why/how/where)
- MC-DC-02: Match description type to audience
- MC-DC-03: Plain language in user-facing messages

## Precision Rules (PR)

### MC-PR-01: One Name Per Concept Across Codebase

One concept = one name everywhere: variables, functions, classes, database columns, API fields, log messages, documentation. No synonyms, no polysemy.

GOOD:
```python
def get_workshop(id): ...  # One name everywhere

class MeterPoint:      # connection point
class MeterDevice:     # physical device
class MeterContract:   # customer relationship
```

Cross-boundary rule: If the database column is `workshop_id`, the API field, variable, and log all use `workshop_id`. Never translate between layers.

### MC-PR-02: Unambiguous Compound Names

If a compound name has multiple readings, restructure it.

- BAD: `empty_collection_key` -> GOOD: `key_of_empty_collection`
- BAD: `invalid_user_input` -> GOOD: `input_from_invalid_user`

Test: If a colleague could reasonably interpret it two ways, restructure.

### MC-PR-03: No Dangerous Meta-Words Without Qualifier

Dangerous words: Module, Service, Manager, Handler, Helper, Utility, Provider, Processor, Controller, Check, Asset, Payload.

- BAD: `ProductModule`, `UserService`, `check(order)`, `DataProcessor`
- GOOD: `ProductCatalog`, `UserAuthProvider`, `validate_order(order)`, `CsvRowParser`

Rule: Qualify until the name answers "what does it contain/do/provide?"

### MC-PR-04: Be Specific in Comments

Every comment must add concrete, verifiable information the code doesn't express.

- BAD: `# Handle errors appropriately`
- GOOD: `# Retry 3 times with exponential backoff (1s, 2s, 4s), then raise TimeoutError`

Test: Delete the comment. If nothing is lost, it was useless.

### MC-PR-05: Error Messages State What Failed, Why, and Recovery

```python
raise ValueError(
    f"Order quantity must be 1-999, got {quantity}. "
    f"Check input validation in checkout_form.py."
)
raise ConnectionError(
    f"Failed to connect to database at {host}:{port} after 3 retries. "
    f"Verify DB_HOST and DB_PORT environment variables."
)
```

### MC-PR-07: Include Canonical Identifiers in Errors

Every error must contain at least one canonical identifier enabling `grep` to find related context.

```python
raise ValueError(
    f"Invalid order id='{order_id}' in file='orders.csv' line={line_num}: "
    f"missing required field 'sku'"
)
```

### MC-PR-06: Log Messages Are Self-Contained

Each log line understandable without reading other lines. Include operation, data, count, parameters.

- BAD: `logger.info("Starting...")` / `logger.info("Done.")`
- GOOD: `logger.info("Starting order export for date='2026-03-17', format='csv'...")`
- GOOD: `logger.info("Order export complete: exported=341, failed=1, duration=12.3s")`

## Brevity Rules (BR)

### MC-BR-01: Simplest Verb in Names

- `perform_validation` -> `validate`
- `execute_data_cleanup` -> `cleanup_data`
- `make_determination_of` -> `determine`

### MC-BR-02: Comments Drop Filler

- BAD: `# This function is responsible for the retrieval of the user object from the database based on the provided identifier. It should be noted that this may return None.`
- GOOD: `# Retrieve user by ID from database. Returns None if not found.`

### MC-BR-03: Function Names Describe Output, Not Mechanism

- BAD: `iterate_and_filter_orders`, `apply_regex_to_extract_emails`
- GOOD: `active_orders`, `extract_emails`

Exception: When mechanism IS the distinguishing factor (`sort_by_merge` vs `sort_by_quick`).

### MC-BR-04: Boolean Functions Use Predicate Prefix

`is_/has_/can_` = returns bool, never raises. Action verbs (`validate`, `ensure`, `require`) = may raise. Never use ambiguous `check_`.

```python
def is_valid(order): ...         # Returns bool
def has_permission(user, action): ... # Returns bool
def validate(order): ...         # Raises on invalid
```

## Consistency Rules (CO)

### MC-CO-01: Corresponding Pairs Use Same Word Stem

- BAD: `encode_url` / `plain_text` -> GOOD: `encode_url` / `decode_url`
- BAD: `serialize` / `load` -> GOOD: `serialize` / `deserialize`
- BAD: `open_connection` / `destroy_connection` -> GOOD: `open_connection` / `close_connection`

### MC-CO-02: Consistent Key=Value Format in Logs

Convention: `key='value'` for strings, `key=value` for numbers/booleans. Consistent everywhere.

```python
logger.info(f"Processing file='{filename}'...")
logger.info(f"Processing complete: file='{filename}' status='{status}' duration={elapsed}s")
```

### MC-CO-03: Convergent Naming

Same concept uses same term in URL, payload, response, database column, variable, log message, and documentation.

- BAD: userId (URL), customer_id (payload), client_id (DB), person_id (var), account (log), buyer (docs)
- GOOD: `user_id` everywhere

### MC-CO-04: Consistent Patterns Across Similar Constructs

Same type of thing = same code pattern. One pattern for all entity retrieval, not three different approaches.

### MC-CO-05: Keep Established API Names

Don't rename working terms even if they became misnomers. Users predict behavior by evoked association, not literal name. Keep `login()`, keep `save()`. New genuinely different behavior gets new name (`sso_connect()`).

## Naming Design Rules (ND)

### MC-ND-01: Naming Structure Method

1. Start explicit: `project_start_date`
2. Add specifiers BEFORE: `planned_project_start_date`, `actual_project_start_date`
3. Add states AFTER: `planned_project_start_date_accepted`
4. Define short forms: external `ACTUAL_PROJECT_START_DATE` (`APSD`), internal `start_date` (`sd`)

### MC-ND-02: Canonical Form for IDs and Data Structures

If data comes from multiple sources in different formats, define a canonical form and convert at the boundary.

```python
canonical_id = "CALL-DJESTOXX50@4400EX2008-02"
def to_canonical(order_text: str) -> str: ...
```

### MC-ND-03: No Recursive/Implicit Naming

- BAD: `class Name: name: str` (recursive Name.name)
- GOOD: `class PersonName: given_name: str`
- BAD: `InfoMeasurementModule` storing license plates -> GOOD: `VehicleRegistry`

### MC-ND-04: No Product-as-Term Collision

- BAD: `team = teams_client.get_team(team_id)` (Microsoft Teams collision)
- GOOD: `ms_team = teams_client.get_team(team_id)`

### MC-ND-05: Type Name = Domain Concept, Not Implementation

- BAD: `UserHashMap`, `OrderLinkedList`, `StringWrapper`, `DataObject`
- GOOD: `UserDirectory`, `OrderQueue`, `EmailAddress`, `ShippingLabel`

### MC-ND-06: Disambiguate by Qualifying, Not Renaming

- BAD: `Order` + `Sequence` (renamed from "sort order") -> GOOD: `PurchaseOrder` + `SortOrder`
- BAD: `process()` + `handle()` -> GOOD: `process_data()` + `process_request()`

Renaming to unrelated term breaks the association field. Qualifying preserves the concept while adding precision.

### MC-ND-07: Intuitive Opposites for Paired Parameters

- BAD: `reference_object`/`difference_object`, `finish_time`
- GOOD: `source`/`target`, `end_time`

## Documentation Rules (DC)

### MC-DC-01: Four Description Types

- Intentional - WHY: What problem does this solve?
- Functional - WHAT: What does it accept, return, and guarantee?
- Technical - HOW: What algorithms, data structures, trade-offs?
- Contextual - WHERE: What depends on this? What does this depend on?

```python
"""
Rate limiter for API endpoints.

WHY: Prevents API abuse by limiting request frequency per client.
WHAT: Counts requests per client IP within sliding window. Returns 429 when limit exceeded. Default: 100 req/min.
HOW: Redis sorted set per IP. Score = timestamp. ZRANGEBYSCORE counts window. ZADD + EXPIRE on each request.
WHERE: Between API gateway and application handlers. Depends on Redis. Bypassed for /health endpoints. Configured in rate_limits.yaml.
"""
```

### MC-DC-02: Match Description Type to Audience

- README - intentional + functional (why + what)
- Docstrings - functional + technical (what + how)
- Architecture docs - intentional + contextual (why + where)
- Onboarding - all four: why -> what -> how -> where

### MC-DC-03: Plain Language in User-Facing Messages

No internal jargon, abbreviations, or code references in user-facing text.

- BAD: `"ERR: ECONNREFUSED on tcp://db:5432 - check pg_hba.conf"`
- GOOD: `"Cannot connect to database. Check that the database server is running."`

Developer-facing messages (logs, debug) can use technical terms (see MC-DC-02).