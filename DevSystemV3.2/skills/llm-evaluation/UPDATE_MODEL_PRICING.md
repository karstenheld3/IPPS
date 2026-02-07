# Update Model Pricing Workflow

**Goal**: Capture current pricing pages, transcribe to markdown, and update `model-pricing.json`

## Placeholders

- `[SKILL_FOLDER]`: The folder containing this workflow file (e.g., `.windsurf/skills/llm-evaluation`)
- `[PRICING_SOURCES]`: `[SKILL_FOLDER]/pricing-sources`
- `[DATE]`: Current date in `YYYY-MM-DD` format
- `[VENV_PYTHON]`: Path to the llm-transcription venv Python (e.g., `.tools/llm-venv/Scripts/python.exe`)
- `[TRANSCRIPTION_SCRIPT]`: Path to `transcribe-image-to-markdown.py` in the llm-transcription skill folder
- `[KEYS_FILE]`: Path to API keys file

## Sources

- Anthropic: `https://docs.anthropic.com/en/docs/about-claude/pricing`
- OpenAI: `https://platform.openai.com/docs/pricing`

## Step 1: Capture Pricing Page Screenshots

Use the playwriter MCP tool to capture full-page screenshots of both pricing pages. Pages may be long and contain lazy-loaded content, so scroll fully before capturing.

### 1a. Capture Anthropic Pricing

Use the **Playwright MCP** tools (`browser_navigate`, `browser_snapshot`, `browser_click`, etc.).

1. `browser_navigate(url: "https://docs.anthropic.com/en/docs/about-claude/pricing")`
2. `browser_wait_for(time: 2)` - Wait for initial load

**Dismiss cookie popup** (see `@ms-playwright-mcp` PLAYWRIGHT_ADVANCED_WORKFLOWS.md Section 1):

3. `browser_snapshot()` - Check for cookie consent banner
4. Look for "Accept All Cookies" or similar button in the snapshot
5. `browser_click(element: "Accept All Cookies button", ref: "<ref from snapshot>")` - Click to dismiss
6. `browser_snapshot()` - Verify popup dismissed

**If no clickable button found**, fall back to JavaScript removal:
```
browser_evaluate(function: "(() => {
  const selectors = ['#cookie-banner', '#cookieModal', '.cookie-consent',
    '[class*=\"cookie\"]', '[id*=\"cookie\"]', '.gdpr-banner', '#onetrust-consent-sdk'];
  selectors.forEach(sel => document.querySelectorAll(sel).forEach(el => el.remove()));
  document.querySelectorAll('.modal-backdrop, [class*=\"overlay\"]').forEach(el => el.remove());
  document.body.style.overflow = 'auto';
})()")
```

Scroll to load all lazy content, then remove sticky headers:

Scroll incrementally to trigger lazy loading (see `@ms-playwright-mcp` FULL_PAGE_SCREENSHOT.md):

```
browser_evaluate(function: "async () => {
  const delay = ms => new Promise(r => setTimeout(r, ms));
  let prevHeight = -1;
  for (let i = 0; i < 50; i++) {
    window.scrollBy(0, 500);
    await delay(300);
    const newHeight = document.body.scrollHeight;
    if (newHeight === prevHeight) break;
    prevHeight = newHeight;
  }
  window.scrollTo(0, 0);
}")
```

Remove fixed/sticky headers to prevent repeating in screenshot:

```
browser_evaluate(function: "() => {
  document.querySelectorAll('header, nav, [class*=\"sticky\"], [class*=\"fixed\"]')
    .forEach(el => { el.style.position = 'relative'; });
}")
```

Take full-page screenshot:

```
browser_screenshot(fullPage: true)
```

Save the screenshot to `[PRICING_SOURCES]/[DATE]_Anthropic-ModelPricing.jpg`.

**If the page is very tall** (screenshot > 2MB or height > 16000px), split into viewport-sized chunks by scrolling and saving numbered files (`-01.jpg`, `-02.jpg`, etc.).

### 1b. Capture OpenAI Pricing

Repeat the same process for OpenAI:

1. `browser_navigate(url: "https://platform.openai.com/docs/pricing")`
2. `browser_wait_for(time: 2)`
3. Dismiss cookie popup (same approach as 1a)
4. Scroll for lazy content, remove sticky headers
5. `browser_screenshot(fullPage: true)`
6. Save to `[PRICING_SOURCES]/[DATE]_OpenAI-ModelPricing-Standard.jpg`

Split into numbered files if too large (`[DATE]_OpenAI-ModelPricing-Standard-NN.jpg`).

**IMPORTANT**: The OpenAI pricing page uses a scrollable inner container (`div.docs-scroll-container`), not the document body. `fullPage: true` will NOT capture the full content. Instead, scroll the inner container and take viewport-sized screenshots:

```
browser_run_code(code: "async (page) => {
  const container = await page.evaluate(() => {
    const c = document.querySelector('.docs-scroll-container');
    return { totalHeight: c.scrollHeight, viewportHeight: c.clientHeight };
  });
  const pages = Math.ceil(container.totalHeight / container.viewportHeight);
  for (let i = 0; i < pages; i++) {
    await page.evaluate((idx) => {
      const c = document.querySelector('.docs-scroll-container');
      c.scrollTo(0, idx * c.clientHeight);
    }, i);
    await page.waitForTimeout(500);
    const suffix = String(i + 1).padStart(2, '0');
    await page.screenshot({
      path: `[PRICING_SOURCES]/[DATE]_OpenAI-ModelPricing-Standard-${suffix}.jpg`,
      scale: 'css', type: 'jpeg', quality: 90
    });
  }
}")
```

## Step 2: Transcribe Screenshots to Markdown

Use the `transcribe-image-to-markdown.py` script from the llm-transcription skill to transcribe each set of screenshots.

**Important**: The transcription script processes folders of images. Create temporary input folders per source, or use `--input-file` for individual images.

### 2a. Transcribe Anthropic Screenshots

```powershell
& [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
  --input-folder "[PRICING_SOURCES]" `
  --output-folder "[PRICING_SOURCES]" `
  --model gpt-5-mini `
  --initial-candidates 3 `
  --keys-file [KEYS_FILE] `
  --force
```

**Note**: If using `--input-folder`, the script processes ALL images in the folder. To transcribe only today's Anthropic screenshots, either:
- Use `--input-file` per image (for single files)
- Create a temp subfolder with only the target images, transcribe, then move results back

**Per-file approach** (recommended):

```powershell
# For each Anthropic screenshot file matching [DATE]_Anthropic-ModelPricing*.jpg
Get-ChildItem "[PRICING_SOURCES]" -Filter "[DATE]_Anthropic-ModelPricing*.jpg" | ForEach-Object {
  $outFile = $_.FullName -replace '\.jpg$', '.md'
  & [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
    --input-file $_.FullName `
    --output-file $outFile `
    --model gpt-5-mini `
    --initial-candidates 3 `
    --keys-file [KEYS_FILE] `
    --force
}
```

### 2b. Transcribe OpenAI Screenshots

```powershell
Get-ChildItem "[PRICING_SOURCES]" -Filter "[DATE]_OpenAI-ModelPricing-Standard*.jpg" | ForEach-Object {
  $outFile = $_.FullName -replace '\.jpg$', '.md'
  & [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
    --input-file $_.FullName `
    --output-file $outFile `
    --model gpt-5-mini `
    --initial-candidates 3 `
    --keys-file [KEYS_FILE] `
    --force
}
```

## Step 3: Read Transcriptions and Update model-pricing.json

### 3a. Read All Transcribed Markdown Files

Read all `[DATE]_Anthropic-ModelPricing*.md` and `[DATE]_OpenAI-ModelPricing-Standard*.md` files from `[PRICING_SOURCES]`.

### 3b. Extract Pricing Data

From the transcribed markdown, extract for each model:
- **Model ID** (API identifier, e.g., `claude-opus-4-6-20260204`, `gpt-5.2`)
- **Input price per 1M tokens**
- **Output price per 1M tokens**

**Rules:**
- Use the full API model ID for Anthropic (with date suffix)
- Use the short model name for OpenAI (e.g., `gpt-5-mini`, not a dated version)
- Only include models that have clear per-token pricing (skip batch-only or special pricing tiers)
- Currency is always `USD`

### 3c. Update model-pricing.json

Read the existing `[SKILL_FOLDER]/model-pricing.json` and update:

1. **Add** new models not yet present (insert at top of their provider section, newest first)
2. **Update** prices for existing models if they changed
3. **NEVER remove** existing models - they may be legacy but still valid for cost calculation
4. **Update** `last_updated` to today's `[DATE]` (YYYY-MM-DD)
5. **Update** `sources` URLs if they changed
6. Maintain the existing JSON structure and formatting

**CRITICAL:** Always update `last_updated`. Always keep all existing models.

### 3d. Verify

After updating, verify:
- JSON is valid (no syntax errors)
- All prices are positive numbers
- No duplicate model entries
- `last_updated` matches today's date

## Step 4: Report Changes

Summarize what changed:
- Models added (with prices)
- Models with price changes (old vs new)
- Models unchanged
- Any models found in screenshots but skipped (with reason)

## Notes

- Screenshots may span multiple pages/images. Read ALL numbered files for a source before extracting prices.
- The OpenAI pricing page may have separate sections for standard and batch pricing. Only extract **standard** (non-batch) pricing.
- If a model has different pricing tiers (e.g., long context), use the **standard** tier pricing.
- The Anthropic pricing page uses full model IDs with date suffixes. Always use the full ID as it appears in the API.
