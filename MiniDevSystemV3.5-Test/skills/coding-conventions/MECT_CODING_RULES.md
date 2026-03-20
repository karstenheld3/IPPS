# MECT Coding Rules

MECT (Minimal Explicit Consistent Terminology) + APAPALAN (Precise first, Brief second) applied to code quality.

## Rule Index

Precision (PR)
- MC-PR-01: One name per concept across codebase
- MC-PR-02: Unambiguous compound names (word order determines meaning)
- MC-PR-03: No dangerous meta-words without qualifier
- MC-PR-04: Be specific in comments - concrete, verifiable statements
- MC-PR-05: Error messages state what failed, why, and recovery action
- MC-PR-06: Log messages: self-contained, full disclosure
- MC-PR-07: Include canonical identifiers in errors (file, line, entity ID)

Brevity (BR)
- MC-BR-01: Simplest verb - no hidden verbs in names
- MC-BR-02: Comments: drop filler, be direct
- MC-BR-03: Function names describe output, not mechanism
- MC-BR-04: Boolean functions: is_/has_/can_ prefix, no "check_"

Consistency (CO)
- MC-CO-01: Corresponding pairs use same word stem
- MC-CO-02: Consistent key=value format in logs
- MC-CO-03: Convergent naming - same terms in URL, payload, docs, logs
- MC-CO-04: Consistent patterns across all similar constructs
- MC-CO-05: Keep established API names - don't rename working terms

Naming Design (ND)
- MC-ND-01: Naming structure method (explicit -> specifiers -> states -> mnemonics)
- MC-ND-02: Canonical form for IDs and data structures
- MC-ND-03: No recursive/implicit naming
- MC-ND-04: No product-as-term collision
- MC-ND-05: Type name = domain concept, not implementation detail
- MC-ND-06: Disambiguate by qualifying, not renaming
- MC-ND-07: Intuitive opposites for paired parameters

Documentation (DC)
- MC-DC-01: Four description types (what/why/how/where)
- MC-DC-02: Match description type to audience
- MC-DC-03: Plain language in user-facing messages

## Precision Rules (PR)

### MC-PR-01: One Name Per Concept Across Codebase

One concept = one name everywhere (variables, functions, classes, DB columns, API fields, logs, docs). No synonyms, no polysemy.

```python
# BAD: get_workshop() / fetch_garage() / load_service_center()
# BAD: class Meter (connection point? device? contract?)
# GOOD: get_workshop() everywhere
# GOOD: MeterPoint / MeterDevice / MeterContract
```

Cross-boundary: DB column `workshop_id` = API field `workshop_id` = variable `workshop_id` = log `workshop_id='abc'`.

### MC-PR-02: Unambiguous Compound Names

If a compound name has multiple readings, restructure it.

```python
# BAD: empty_collection_key / invalid_user_input / active_session_count
# GOOD: key_of_empty_collection / input_from_invalid_user / count_of_active_sessions
```

Test: If a colleague could interpret it two ways, restructure.

### MC-PR-03: No Dangerous Meta-Words Without Qualifier

Ambiguous words: Module, Service, Manager, Handler, Helper, Utility, Provider, Processor, Controller, Check, Asset, Payload.

```python
# BAD: ProductModule / UserService / check(order) / DataProcessor
# GOOD: ProductCatalog / UserAuthProvider / validate_order(order) / CsvRowParser
```

Qualify until the name answers "what does it contain/do/provide?"

### MC-PR-04: Be Specific in Comments

Every comment must add concrete, verifiable information the code doesn't express.

```python
# BAD: "Handle errors appropriately" / "Process the data"
# GOOD: "Retry 3x with exponential backoff (1s, 2s, 4s), then raise TimeoutError"
# GOOD: "Parse CSV rows into OrderLine objects, skip rows with missing SKU"
```

Test: Delete the comment. If nothing is lost, it was useless.

### MC-PR-05: Error Messages State What Failed, Why, and Recovery

```python
# BAD: raise ValueError("Invalid input")
# GOOD:
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

Every error must contain at least one identifier enabling `grep` to find context.

```python
# BAD: raise ValueError("Invalid order")
# GOOD:
raise ValueError(f"Invalid order id='{order_id}' in file='orders.csv' line={line_num}: missing required field 'sku'")
logger.error(f"Processing failed for batch_id='{batch_id}' at step=3: timeout after 30s. See request_id='{req_id}'")
```

### MC-PR-06: Log Messages Are Self-Contained

Each log line understandable alone. Include: operation, data, count, parameters.

```python
# BAD: "Starting..." / "Processing..." / "Done."
# GOOD:
logger.info("Starting order export for date='2026-03-17', format='csv'...")
logger.info("Processing 342 orders from region='eu-west'...")
logger.info("Order export complete: exported=341, failed=1, duration=12.3s")
```

## Brevity Rules (BR)

### MC-BR-01: Simplest Verb in Names

```python
# BAD: perform_validation() / execute_data_cleanup() / make_determination_of()
# GOOD: validate() / cleanup_data() / determine()
```

### MC-BR-02: Comments Drop Filler

```python
# BAD: "This function is responsible for the retrieval of the user object
#       from the database based on the provided identifier."
# GOOD: "Retrieve user by ID from database. Returns None if not found."
```

### MC-BR-03: Function Names Describe Output, Not Mechanism

```python
# BAD: iterate_and_filter_orders() / apply_regex_to_extract_emails()
# GOOD: active_orders() / extract_emails()
```

Exception: When mechanism IS the distinguishing factor (`sort_by_merge` vs `sort_by_quick`).

### MC-BR-04: Boolean Functions Use Predicate Prefix

`is_/has_/can_/should_/needs_` = returns bool, never raises. Action verbs (`validate`, `ensure`, `require`) = may raise.

```python
# BAD: check(order) / check_permission() / validate_active()
# GOOD: is_valid(order) / has_permission(user, action) / is_active(subscription)
```

## Consistency Rules (CO)

### MC-CO-01: Corresponding Pairs Use Same Word Stem

```python
# BAD: encode_url() / plain_text() — GOOD: encode_url() / decode_url()
# BAD: serialize() / load() — GOOD: serialize() / deserialize()
# BAD: open_connection() / destroy_connection() — GOOD: open_connection() / close_connection()
```

Standard pairs: open/close, read/write, get/set, add/remove, create/delete, start/stop, begin/end, push/pop, encode/decode, serialize/deserialize, connect/disconnect, acquire/release, lock/unlock, show/hide, enable/disable, attach/detach, subscribe/unsubscribe, marshal/unmarshal

### MC-CO-02: Consistent Key=Value Format in Logs

Convention: `key='value'` for strings, `key=value` for numbers/booleans. One format everywhere.

```python
# BAD: mixed formats across log lines
# GOOD:
logger.info(f"Processing file='{filename}'...")
logger.info(f"Processing complete: file='{filename}' status='{status}' duration={elapsed}s")
```

### MC-CO-03: Convergent Naming

Same concept = same term across URL, payload, response, DB column, variable, log, docs.

```
BAD: userId (URL) / customer_id (payload) / client_id (DB) / person_id (var) / account (log)
GOOD: user_id everywhere
```

### MC-CO-04: Consistent Patterns Across Similar Constructs

Same operation type = same code pattern.

```python
# BAD: get_user() uses query(), fetch_order() uses execute(), load_product() uses objects.get()
# GOOD: All use db.query(Model).filter_by(id=id).first()
```

### MC-CO-05: Keep Established API Names

Don't rename working terms even if misnomers. Association field > literal name.

```python
# Keep login() even if credentials no longer required
# Keep save() even if it writes to cloud
# New behavior = new name: sso_connect()
```

## Naming Design Rules (ND)

### MC-ND-01: Naming Structure Method

1. Most explicit name: `project_start_date`
2. Add specifiers BEFORE: `planned_project_start_date`
3. Add states AFTER: `planned_project_start_date_accepted`
4. Define short forms: `APSD` (external), `sd` (internal)

### MC-ND-02: Canonical Form for IDs and Data Structures

Multiple representations of same concept must converge to one canonical form. Convert at boundary.

```python
# BAD: Three text variants for same order — unmatchable
# GOOD: canonical_id = "CALL-DJESTOXX50@4400EX2008-02"
```

### MC-ND-03: No Recursive/Implicit Naming

Name must not contain itself. Container describes contents.

```python
# BAD: class Name: name: str — GOOD: class PersonName: given_name: str
# BAD: InfoMeasurementModule with license_plate — GOOD: VehicleRegistry
```

### MC-ND-04: No Product-as-Term Collision

Don't name products with common domain terms.

```python
# BAD: team = teams_client.get_team(team_id)  # "Teams" collides with "team"
# GOOD: ms_team = teams_client.get_team(team_id)
```

### MC-ND-05: Type Name = Domain Concept, Not Implementation

```python
# BAD: UserHashMap / OrderLinkedList / StringWrapper / DataObject
# GOOD: UserDirectory / OrderQueue / EmailAddress / ShippingLabel
```

### MC-ND-06: Disambiguate by Qualifying, Not Renaming

Renaming breaks association field. Qualify both sides instead.

```python
# BAD: Order + Sequence (renamed from "sort order")
# GOOD: PurchaseOrder + SortOrder
# BAD: process() + handle() — GOOD: process_data() + process_request()
```

### MC-ND-07: Intuitive Opposites for Paired Parameters

```python
# BAD: compare(reference_object, difference_object) — GOOD: compare(source, target)
# BAD: "finish_time" — GOOD: "end_time"
```

Standard opposites: start/end, min/max, first/last, source/target, input/output, request/response, before/after, current/previous, local/remote, internal/external, public/private

## Documentation Rules (DC)

### MC-DC-01: Four Description Types

- **Intentional** (WHY): What problem does this solve?
- **Functional** (WHAT): What does it accept, return, guarantee?
- **Technical** (HOW): What algorithms, data structures, trade-offs?
- **Contextual** (WHERE): What depends on this? What does this depend on?

```python
"""
Rate limiter for API endpoints.
WHY: Prevents API abuse by limiting request frequency per client.
WHAT: Counts requests per client IP within sliding window. Returns 429 when limit exceeded. Default: 100 req/min.
HOW: Redis sorted set per IP. Score = timestamp. ZRANGEBYSCORE counts window.
WHERE: Between API gateway and handlers. Depends on Redis. Configured in rate_limits.yaml.
"""
```

### MC-DC-02: Match Description Type to Audience

- README: intentional + functional (why + what)
- Docstrings: functional + technical (what + how)
- Architecture docs: intentional + contextual (why + where)
- Onboarding: all four (why -> what -> how -> where)

### MC-DC-03: Plain Language in User-Facing Messages

No jargon, no abbreviations, no code references in user-facing text.

```python
# BAD: "ERR: ECONNREFUSED on tcp://db:5432"
# GOOD: "Cannot connect to database. Check that the database server is running."
# BAD: "Invalid JWT: exp claim < now()"
# GOOD: "Your session has expired. Please sign in again."
```

Developer-facing messages (logs, debug) can use technical terms (MC-DC-02).