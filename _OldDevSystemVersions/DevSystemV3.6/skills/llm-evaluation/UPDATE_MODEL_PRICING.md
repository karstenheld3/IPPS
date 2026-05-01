# Update Model Pricing Workflow

**Goal**: Refresh `model-pricing.json` and `model-registry.json` with current OpenAI + Anthropic pricing and model metadata.

**Design principle**: Document Object Model (DOM) extraction is the authoritative source of numeric data. Screenshots and markdown transcriptions are archival references only. Every phase has a verification gate.

**Code block convention**: Blocks showing `browser_navigate(...)`, `browser_evaluate(...)`, `browser_run_code(...)` illustrate Playwright Model Context Protocol (MCP) tool invocations. The string inside `function:` / `code:` is the actual JavaScript argument to pass.

## Placeholders

- `[SKILL_FOLDER]`: Folder containing this workflow
- `[PRICING_SOURCES]`: `[SKILL_FOLDER]/pricing-sources`
- `[SCREENSHOTS]`: `[WORKSPACE_FOLDER]/../.tools/_screenshots`
- `[DATE]`: Today in `YYYY-MM-DD`
- `[VENV_PYTHON]`: `../.tools/llm-venv/Scripts/python.exe`
- `[TRANSCRIPTION_SCRIPT]`: `.../llm-transcription/transcribe-image-to-markdown.py`
- `[KEYS_FILE]`: API keys file path

## Sources

- Anthropic pricing: `https://docs.anthropic.com/en/docs/about-claude/pricing`
- Anthropic models (for API IDs): `https://docs.anthropic.com/en/docs/about-claude/models`
- OpenAI Standard: `https://developers.openai.com/api/docs/pricing?latest-pricing=standard`
- OpenAI Batch: `https://developers.openai.com/api/docs/pricing?latest-pricing=batch`

## Pricing Dimensions

For every model, capture all available:

- **Input** per 1M tokens
- **Cached input** per 1M tokens (null if not offered)
- **Output** per 1M tokens
- **Tier**: Standard and Batch (captured as separate datasets)
- **Context window** (K tokens)

`model-pricing.json` stores **Anthropic Standard** and **OpenAI Batch** by convention. Both tiers are still captured for the archive.

---

## Phase 1: Pre-Flight Checks

Before any capture:

1. Read current `last_updated` from `model-pricing.json` and `_updated` from `model-registry.json`.
2. If either equals today's `[DATE]` → confirm with user whether to re-run (prevents silent no-op loops).
3. Confirm `[PRICING_SOURCES]` exists.
4. Create folders (pre-existing files in these paths **will be overwritten** on re-run — confirm before proceeding):
   - `[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing/`
   - `[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Standard/`
   - `[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Batch/`

**Gate 1**: Only proceed if `last_updated < [DATE]` or user explicitly confirmed re-run.

---

## Common: Cookie / Overlay Dismissal Block

Used by both Phase 2 (DOM) and Phase 3 (screenshots). Run once per page after `browser_navigate` + `browser_resize`:

```
browser_evaluate(function: "(() => {
  ['#cookie-banner','#cookieModal','.cookie-consent','[class*=\"cookie\"]',
   '[id*=\"cookie\"]','.gdpr-banner','#onetrust-consent-sdk']
    .forEach(sel => document.querySelectorAll(sel).forEach(el => el.remove()));
  document.querySelectorAll('.modal-backdrop,[class*=\"overlay\"]').forEach(el => el.remove());
  document.body.style.overflow = 'auto';
  document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]')
    .forEach(el => { el.style.position = 'relative'; });
})()")
```

---

## Phase 2: DOM Extraction (Primary Data Source)

This phase produces the **authoritative** machine-readable pricing data. It runs independently of screenshots and does not depend on image transcription.

For each page:
1. `browser_navigate(url)`
2. `browser_resize(width: 1920, height: 1080)` — ensures all columns render
3. `browser_wait_for(time: 2)`
4. Run the Common Dismissal Block above.
5. Click every "All models" / "View more" / "Show all" button to expand collapsed tables.
6. Extract all tables via `browser_evaluate`.
7. Save raw extraction as JSON artifact.

### 2.1 Anthropic

Navigate: `https://docs.anthropic.com/en/docs/about-claude/pricing`

Expand everything:

```js
browser_evaluate(function: "async () => {
  const delay = ms => new Promise(r => setTimeout(r, ms));
  for (const btn of document.querySelectorAll('button, [role=\"button\"]')) {
    const t = btn.textContent.toLowerCase().trim();
    if (/all models|view more|show all|expand/.test(t)) { btn.click(); await delay(400); }
  }
}")
```

Extract:

```js
browser_evaluate(function: "() => {
  const tables = Array.from(document.querySelectorAll('table'));
  return tables.map((t, idx) => ({
    idx,
    caption: (t.caption?.textContent || t.closest('section,div')?.querySelector('h1,h2,h3,h4')?.textContent || '').trim().slice(0,120),
    headers: Array.from(t.querySelectorAll('thead th, tr:first-child th, tr:first-child td')).map(h => h.textContent.trim()),
    rows: Array.from(t.querySelectorAll('tbody tr')).map(r =>
      Array.from(r.querySelectorAll('td')).map(c => c.textContent.trim()))
  })).filter(t => t.rows.length);
}")
```

Save to: `[PRICING_SOURCES]/[DATE]_Anthropic-DOM.json`

### 2.2 OpenAI Standard

Navigate: `https://developers.openai.com/api/docs/pricing?latest-pricing=standard`

Run the same expand + extract blocks. Save to: `[PRICING_SOURCES]/[DATE]_OpenAI-Standard-DOM.json`

### 2.3 OpenAI Batch

Navigate: `https://developers.openai.com/api/docs/pricing?latest-pricing=batch`

Run the same expand + extract blocks. Save to: `[PRICING_SOURCES]/[DATE]_OpenAI-Batch-DOM.json`

### 2.4 Anthropic Model ID Resolution

The pricing page shows friendly names ("Claude Opus 4.7") without API date suffixes. Resolve the exact API ID using the fallback chain:

1. Navigate `https://docs.anthropic.com/en/docs/about-claude/models` and extract full page text. Search for `claude-<family>-<version>-YYYYMMDD` patterns.
2. If not found, query the live API (user must provide key):
   ```
   curl https://api.anthropic.com/v1/models -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01"
   ```
3. If still missing, write the undated alias (e.g. `claude-opus-4-7`) and add a sibling key-value pair flagging it: `"_note_<alias>": "date suffix pending — resolved alias only"` (JSON has no real comments; the `_note_` prefix is the project convention for metadata keys). Do **NOT** skip the entry.

Save resolved IDs to: `[PRICING_SOURCES]/[DATE]_Anthropic-ModelIDs.json`

**Gate 2**: Every model visible on the pricing page has:
- numeric input / output prices captured
- cached price captured or explicitly `null`
- (Anthropic) resolved or flagged API ID

If any check fails, retry or escalate to user before Phase 3.

---

## Phase 3: Screenshot Archive (Reference Only)

Screenshots serve as a visual audit trail. They are NOT used to derive prices — Phase 2 DOM extraction already did that. Run the Common Dismissal Block (above Phase 2) on each page after navigate + resize.

### 3.1 Anthropic

Body-scroll page. Scroll to preload, then chunk screenshots at viewport height.

```js
browser_run_code(code: "async (page) => {
  await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    let prev = -1;
    for (let i = 0; i < 80; i++) {
      window.scrollBy(0, 600); await delay(250);
      if (document.body.scrollHeight === prev) break;
      prev = document.body.scrollHeight;
    }
    window.scrollTo(0, 0);
  });
  const total = await page.evaluate(() => document.body.scrollHeight);
  const vh = await page.evaluate(() => window.innerHeight);
  const n = Math.ceil(total / vh);
  for (let i = 0; i < n; i++) {
    await page.evaluate(y => window.scrollTo(0, y), i * vh);
    await page.waitForTimeout(400);
    const s = String(i + 1).padStart(2, '0');
    await page.screenshot({ path: '[FOLDER]/' + s + '.jpg', scale: 'css', type: 'jpeg', quality: 90 });
  }
  return { n };
}")
```

Folder: `[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing`

### 3.2 OpenAI (both tiers)

Inner-scroll container page. Fallback to body if selector fails.

```js
browser_run_code(code: "async (page) => {
  // Expand All models buttons
  await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    for (const btn of document.querySelectorAll('button')) {
      if (/all models|view more/i.test(btn.textContent)) { btn.click(); await delay(400); }
    }
  });
  await page.waitForTimeout(800);

  const info = await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    const c = document.querySelector('.docs-scroll-container') || document.scrollingElement || document.body;
    const useBody = c === document.body || c === document.scrollingElement;
    let prev = -1;
    for (let i = 0; i < 80; i++) {
      if (useBody) window.scrollBy(0, 600); else c.scrollBy(0, 600);
      await delay(250);
      const h = useBody ? document.body.scrollHeight : c.scrollHeight;
      if (h === prev) break;
      prev = h;
    }
    if (useBody) window.scrollTo(0, 0); else c.scrollTo(0, 0);
    return {
      total: useBody ? document.body.scrollHeight : c.scrollHeight,
      vh: useBody ? window.innerHeight : c.clientHeight,
      useBody
    };
  });

  const n = Math.ceil(info.total / info.vh);
  for (let i = 0; i < n; i++) {
    await page.evaluate((idx, ub) => {
      const c = ub ? null : document.querySelector('.docs-scroll-container');
      if (ub) window.scrollTo(0, idx * window.innerHeight);
      else c.scrollTo(0, idx * c.clientHeight);
    }, i, info.useBody);
    await page.waitForTimeout(400);
    const s = String(i + 1).padStart(2, '0');
    await page.screenshot({ path: '[FOLDER]/' + s + '.jpg', scale: 'css', type: 'jpeg', quality: 90 });
  }
  return { n };
}")
```

Run once per tier. Folders:
- `[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Standard`
- `[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Batch`

**Gate 3**: Each folder contains ≥ 1 .jpg. Spot-check one screenshot per folder to confirm the Output column is visible. If clipped → increase viewport width and re-run the affected folder only.

---

## Phase 4: Transcribe Screenshots (Archival Markdown)

Produces human-readable markdown alongside raw screenshots.

```powershell
foreach ($folder in @(
  "[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing",
  "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Standard",
  "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Batch"
)) {
  & [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
    --input-folder $folder `
    --output-folder $folder `
    --model gpt-5-mini --initial-candidates 1 `
    --keys-file [KEYS_FILE] --force
}
```

Stitch and clean:

```powershell
$stitch = @{
  "[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing"          = "[PRICING_SOURCES]/[DATE]_Anthropic-ModelPricing.md"
  "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Standard"    = "[PRICING_SOURCES]/[DATE]_OpenAI-ModelPricing-Standard.md"
  "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing-Batch"       = "[PRICING_SOURCES]/[DATE]_OpenAI-ModelPricing-Batch.md"
}
foreach ($src in $stitch.Keys) {
  Get-ChildItem "$src/*.md" | Sort-Object Name |
    ForEach-Object { Get-Content $_.FullName -Raw } |
    Out-File $stitch[$src] -Encoding utf8
  Remove-Item "$src/*.md" -Force -ErrorAction SilentlyContinue
  Remove-Item "$src/_batch_summary.json" -Force -ErrorAction SilentlyContinue
}
```

**Gate 4**: Three combined markdowns exist in `[PRICING_SOURCES]`. No action is blocked by transcription quality — Phase 5 uses DOM data.

---

## Phase 5: Update `model-pricing.json`

Input: `[PRICING_SOURCES]/[DATE]_Anthropic-DOM.json`, `[DATE]_OpenAI-Batch-DOM.json`, `[DATE]_Anthropic-ModelIDs.json`

Rules:

1. **Add** new models not currently in the file.
2. **Update** prices for existing models if changed.
3. **Never remove** legacy entries — even deprecated models stay for historical cost calc.
4. **Tier selection:**
   - Anthropic → **Standard tier** prices.
   - OpenAI → **Batch tier** prices (half of standard).
5. **Column mapping** (source → schema field):
   - Anthropic: `Base Input Tokens` → `input_per_1m`, `Cache Hits & Refreshes` → `cached_per_1m`, `Output Tokens` → `output_per_1m`. Ignore `5m Cache Writes` and `1h Cache Writes` (not stored).
   - OpenAI: `Input` → `input_per_1m`, `Cached input` → `cached_per_1m`, `Output` → `output_per_1m`.
6. **Short/Long context split** (OpenAI only, e.g. gpt-5.4): store **Short context** numbers under the flat keys. Long context is not represented in the current schema — flag in Phase 8 report only.
7. Every entry: `{input_per_1m, cached_per_1m|omit if null, output_per_1m, context_window_k, currency: "USD"}`.
8. Bump `last_updated` to `[DATE]`.
9. Update `sources` array if URLs drifted.

**Gate 5 (Persistence Check, MANDATORY)**:

`$newIds` is the list of model IDs added or changed during this run — derive it from the DOM artifacts written in Phase 2 (`[PRICING_SOURCES]/[DATE]_*-DOM.json` and `[DATE]_Anthropic-ModelIDs.json`).

```powershell
$p = Get-Content "[SKILL_FOLDER]/model-pricing.json" -Raw | ConvertFrom-Json
# 1. last_updated equals today
if ($p.last_updated -ne "[DATE]") { throw "last_updated not bumped" }
# 2. Every new model_id from Phase 2 is present
foreach ($id in $newIds) {
  if (-not $p.pricing.anthropic.$id -and -not $p.pricing.openai.$id) { throw "Missing $id" }
}
# 3. JSON parses (implicit from ConvertFrom-Json above)
```

If any check fails: re-apply edit, re-run gate. Do not proceed.

---

## Phase 6: Update `model-registry.json`

Input: same DOM artifacts + resolved model IDs.

Rules:

1. **Add** every model_id present in `model-pricing.json` that's missing from the registry.
2. New entries default to `enabled: false, status: "untested"` unless user specifies otherwise.
3. `context_window` in tokens (e.g., 200000), not K.
4. Reconcile `model_id_startswith` prefixes if a new family (e.g., `claude-opus-4-7`) needs different `max_output` / `thinking_max` / `effort` semantics.
5. Bump `_updated` to `[DATE]`.
6. **Never remove** entries — mark with `status: "deprecated"` or `status: "legacy"` instead.

**Gate 6 (Persistence + Consistency Check)**:

```powershell
$r = Get-Content "[SKILL_FOLDER]/model-registry.json" -Raw | ConvertFrom-Json
$p = Get-Content "[SKILL_FOLDER]/model-pricing.json" -Raw | ConvertFrom-Json
if ($r._updated -ne "[DATE]") { throw "registry _updated not bumped" }

# Every priced model_id exists in registry
$priced = @()
$priced += $p.pricing.openai.PSObject.Properties.Name
$priced += $p.pricing.anthropic.PSObject.Properties.Name
$registered = $r.models.model_id
$missing = $priced | Where-Object { $_ -notin $registered }
if ($missing) { throw "Priced but not registered: $missing" }
```

If any check fails: re-apply edit, re-run gate.

---

## Phase 7: Sync to Dependent Skills

`model-pricing.json` and `model-registry.json` live in `@skills:llm-evaluation` but are also consumed by other skills that keep their own copies. After Gates 5 and 6 pass, copy the canonical files to every dependent skill.

**Dependent skills:**
- `@skills:llm-transcription` — uses model metadata for transcription model selection and cost reporting

```powershell
$src = "[SKILL_FOLDER]"
$targets = @(
  "[AGENT_FOLDER]/skills/llm-transcription"
)
foreach ($dst in $targets) {
  Copy-Item "$src/model-pricing.json"  "$dst/model-pricing.json"  -Force
  Copy-Item "$src/model-registry.json" "$dst/model-registry.json" -Force
}
```

**Gate 7 (Sync Check, MANDATORY)**: Byte-compare each target against source.

```powershell
foreach ($dst in $targets) {
  foreach ($f in @('model-pricing.json','model-registry.json')) {
    $a = (Get-FileHash "$src/$f").Hash
    $b = (Get-FileHash "$dst/$f").Hash
    if ($a -ne $b) { throw "Sync mismatch: $dst/$f" }
  }
}
```

Adding a new dependent skill: append its folder path to `$targets` above and add it to the "Dependent skills" list.

---

## Phase 8: Report

Print a concise summary:

- **Added models**: `<provider>/<id>` with prices
- **Price changes**: `<id>: old → new`
- **Unchanged**: count only
- **Registry additions**: `<provider>/<id>` with `context_window`, `status`
- **Pending resolution**: any undated Anthropic aliases or long-context values not stored
- **Sources archived**: list of generated files in `[PRICING_SOURCES]` and `[SCREENSHOTS]`

---

## Failure Modes and Recovery

- **DOM extraction returns empty tables**: page DOM changed. Inspect via `browser_snapshot`, update selectors. Screenshots still valid.
- **Output column clipped in screenshots**: Phase 2 (DOM) already captured the data. Fix viewport to 1920+ and re-run Phase 3 only if the archive matters.
- **Anthropic API ID unresolvable**: write the alias, add `_note_<alias>` comment, flag in Phase 8 report. Do not block the run.
- **Gate 5, 6 or 7 fails**: the edit did not persist or the sync copy did not complete. Most common cause: file was edited in memory but never written. Re-read file from disk, re-apply, re-verify.
- **New dependent skill added elsewhere**: add its folder to Phase 7's `$targets` list so the sync stays in lockstep.
- **Duplicate model in pricing vs registry**: reconcile toward the pricing file (prices are authoritative for existence); registry must follow.
