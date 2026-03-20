# Update Model Registry Workflow

**Goal**: Capture model overview pages, transcribe to markdown, update `model-registry.json` with current models, context windows, deprecation status

## Placeholders

- `[SKILL_FOLDER]`: Folder containing this workflow (e.g., `.windsurf/skills/llm-evaluation`)
- `[REGISTRY_SOURCES]`: `[SKILL_FOLDER]/registry-sources`
- `[SCREENSHOTS]`: `[WORKSPACE_FOLDER]/../.tools/_screenshots`
- `[DATE]`: Current date `YYYY-MM-DD`
- `[VENV_PYTHON]`: llm-transcription venv Python (e.g., `../.tools/llm-venv/Scripts/python.exe`)
- `[TRANSCRIPTION_SCRIPT]`: Path to `transcribe-image-to-markdown.py` in llm-transcription skill
- `[KEYS_FILE]`: Path to API keys file

## Sources

- Anthropic Models Overview: `https://platform.claude.com/docs/en/about-claude/models/overview`
- Anthropic Model Deprecations: `https://platform.claude.com/docs/en/about-claude/model-deprecations`
- OpenAI Model Compare: `https://platform.openai.com/docs/models/compare`

## Step 1: Capture Model Info Screenshots

Create subfolders under `[SCREENSHOTS]` before capturing:
- `[SCREENSHOTS]/[DATE]_Anthropic-ModelOverview/`
- `[SCREENSHOTS]/[DATE]_Anthropic-ModelDeprecations/`
- `[SCREENSHOTS]/[DATE]_OpenAI-ModelCompare/`

### Common Steps (all pages)

For each page:

1. `browser_navigate(url: "<URL>")`
2. `browser_wait_for(time: 2)`
3. **Dismiss cookie popup**:
   - `browser_snapshot()` - check for cookie consent banner
   - If accept button found: click "Accept" / "Accept All Cookies"
   - If no button found, use JavaScript removal fallback:
     ```
     browser_evaluate(function: "(() => {
       ['#cookie-banner','#cookieModal','.cookie-consent','[class*=\"cookie\"]',
        '[id*=\"cookie\"]','.gdpr-banner','#onetrust-consent-sdk'].forEach(sel =>
         document.querySelectorAll(sel).forEach(el => el.remove()));
       document.querySelectorAll('.modal-backdrop,[class*=\"overlay\"]').forEach(el => el.remove());
       document.body.style.overflow = 'auto';
     })()")
     ```
4. Remove fixed/sticky headers:
   ```
   browser_evaluate(function: "() => {
     document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]')
       .forEach(el => { el.style.position = 'relative'; });
   }")
   ```

### 1a. Capture Anthropic Models Overview

URL: `https://platform.claude.com/docs/en/about-claude/models/overview`

Anthropic docs use document body for scrolling. Viewport-chunk capture:

```
browser_run_code(code: "async (page) => {
  await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    let prevHeight = -1;
    for (let i = 0; i < 50; i++) {
      window.scrollBy(0, 500); await delay(300);
      if (document.body.scrollHeight === prevHeight) break;
      prevHeight = document.body.scrollHeight;
    }
    window.scrollTo(0, 0);
    document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]')
      .forEach(el => { el.style.position = 'relative'; });
  });
  const totalHeight = await page.evaluate(() => document.body.scrollHeight);
  const viewportHeight = await page.evaluate(() => window.innerHeight);
  const pages = Math.ceil(totalHeight / viewportHeight);
  for (let i = 0; i < pages; i++) {
    await page.evaluate(y => window.scrollTo(0, y), i * viewportHeight);
    await page.waitForTimeout(500);
    const suffix = String(i + 1).padStart(2, '0');
    await page.screenshot({
      path: '[SUBFOLDER]/' + suffix + '.jpg',
      scale: 'css', type: 'jpeg', quality: 90
    });
  }
  return { pages };
}")
```

Replace `[SUBFOLDER]` with: `[SCREENSHOTS]/[DATE]_Anthropic-ModelOverview`

### 1b. Capture Anthropic Model Deprecations

URL: `https://platform.claude.com/docs/en/about-claude/model-deprecations`

Same viewport-chunk technique as 1a. Replace `[SUBFOLDER]` with: `[SCREENSHOTS]/[DATE]_Anthropic-ModelDeprecations`

### 1c. Capture OpenAI Model Compare

URL: `https://platform.openai.com/docs/models/compare`

**IMPORTANT**: Page shows comparison table for up to 3 models. Capture all models via interactive batched loop.

**IMPORTANT**: OpenAI docs use scrollable inner container (`div.docs-scroll-container`), not document body.

#### Step 1c-i: Get full model list

```
browser_run_code(code: "async (page) => {
  const selectors = await page.locator('[data-testid=\"model-selector\"], button:has-text(\"Select a model\"), .model-picker button').all();
  if (selectors.length > 0) await selectors[0].click();
  await page.waitForTimeout(500);
  const models = await page.evaluate(() => {
    const items = document.querySelectorAll('[role=\"option\"], [role=\"menuitem\"], .model-option, li[data-value]');
    return Array.from(items).map(el => el.textContent.trim());
  });
  return { models, count: models.length };
}")
```

If selectors don't match, use `browser_snapshot()` to inspect and adapt.

#### Step 1c-ii: Capture in batches of 3

For N models, need `ceil(N / 3)` batches. Per batch: select 3 models, wait for table, scroll inner container, screenshot as viewport chunks.

```
browser_run_code(code: "async (page) => {
  const container = await page.evaluate(async () => {
    const c = document.querySelector('.docs-scroll-container');
    const delay = ms => new Promise(r => setTimeout(r, ms));
    let prevHeight = -1;
    for (let i = 0; i < 50; i++) {
      c.scrollBy(0, 500); await delay(300);
      if (c.scrollHeight === prevHeight) break;
      prevHeight = c.scrollHeight;
    }
    c.scrollTo(0, 0);
    document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]')
      .forEach(el => { el.style.position = 'relative'; });
    return { totalHeight: c.scrollHeight, viewportHeight: c.clientHeight };
  });
  const pages = Math.ceil(container.totalHeight / container.viewportHeight);
  for (let i = 0; i < pages; i++) {
    await page.evaluate(idx => {
      const c = document.querySelector('.docs-scroll-container');
      c.scrollTo(0, idx * c.clientHeight);
    }, i);
    await page.waitForTimeout(500);
    const suffix = 'B[BATCH_NUM]_' + String(i + 1).padStart(2, '0');
    await page.screenshot({
      path: '[SUBFOLDER]/' + suffix + '.jpg',
      scale: 'css', type: 'jpeg', quality: 90
    });
  }
  return { pages };
}")
```

Replace `[SUBFOLDER]` with `[SCREENSHOTS]/[DATE]_OpenAI-ModelCompare`, `[BATCH_NUM]` with zero-padded batch number (01, 02, ...).

Files named `B01_01.jpg`, `B01_02.jpg`, `B02_01.jpg` etc. for correct sort order. Use `browser_snapshot()` before each batch to identify correct selectors.

## Step 2: Transcribe Screenshots to Markdown

### 2a-2c. Transcribe each source

Run for each of the three screenshot folders (`Anthropic-ModelOverview`, `Anthropic-ModelDeprecations`, `OpenAI-ModelCompare`):

```powershell
& [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
  --input-folder "[SCREENSHOTS]/[DATE]_[SOURCE_NAME]" `
  --output-folder "[SCREENSHOTS]/[DATE]_[SOURCE_NAME]" `
  --model gpt-5-mini --initial-candidates 1 --keys-file [KEYS_FILE] --force
```

### 2d. Stitch into combined markdowns

```powershell
# For each source: Anthropic-ModelOverview, Anthropic-ModelDeprecations, OpenAI-ModelCompare
Get-ChildItem "[SCREENSHOTS]/[DATE]_[SOURCE_NAME]/*.md" |
  Sort-Object Name |
  ForEach-Object { Get-Content $_.FullName -Raw } |
  Out-File "[REGISTRY_SOURCES]/[DATE]_[SOURCE_NAME].md" -Encoding utf8
```

Clean up per-page files:
```powershell
"Anthropic-ModelOverview", "Anthropic-ModelDeprecations", "OpenAI-ModelCompare" | ForEach-Object {
  Remove-Item "[SCREENSHOTS]/[DATE]_$_/*.md" -Force -ErrorAction SilentlyContinue
  Remove-Item "[SCREENSHOTS]/[DATE]_$_/_batch_summary.json" -Force -ErrorAction SilentlyContinue
}
```

## Step 3: Update model-registry.json

### 3a-3b. Extract model data

Read all three combined files from `[REGISTRY_SOURCES]`. Extract per model: Model ID, Provider (`openai`/`anthropic`), Display name, Context window, Max output tokens, Deprecation status/dates.

Rules:
- Full API model ID for Anthropic (with date suffix)
- Short model name for OpenAI (e.g., `gpt-5-mini`)
- "200K context" = 200,000 tokens

### 3c. Update `models[]`

1. **Add** new models with `"enabled": false, "status": "untested"`
2. **Update** `context_window` for existing models if now known
3. **Update** `status` to `"deprecated"` + `"enabled": false` for deprecated models
4. **NEVER remove** existing models
5. Insert new models at top of provider group, newest first

### 3d. Update `model_id_startswith[]`

1. **Update** `max_input` based on context window data
2. If new model doesn't match any prefix, **report** it (do NOT auto-add - requires manual config)

### 3e. Update metadata

- `_updated` = today's `[DATE]`
- Bump `_version` patch number

### 3f. Verify

- Valid JSON, no syntax errors
- All `context_window` and `max_input` are positive integers
- No duplicate model entries or prefixes
- Every model matches at least one `model_id_startswith` prefix
- `_updated` matches today

## Step 4: Report Changes

Summarize: models added (with context window/status), updated context windows (old vs new), newly deprecated, new `max_input` values, unmatched models (require manual config), skipped models (with reason).

## Notes

- OpenAI compare page UI may change - always `browser_snapshot()` before interacting with selectors
- Anthropic overview lists context/output per family - map to specific date-suffixed IDs from pricing/deprecation pages
- Deprecation page takes precedence over overview for status
- `model_id_startswith` uses longest-prefix-wins ordering