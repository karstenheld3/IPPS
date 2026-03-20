# Update Model Pricing Workflow

**Goal**: Capture current pricing pages, transcribe to markdown, and update `model-pricing.json`

## Placeholders

- `[SKILL_FOLDER]`: Folder containing this workflow (e.g., `.windsurf/skills/llm-evaluation`)
- `[PRICING_SOURCES]`: `[SKILL_FOLDER]/pricing-sources`
- `[SCREENSHOTS]`: `[WORKSPACE_FOLDER]/../.tools/_screenshots`
- `[DATE]`: Current date `YYYY-MM-DD`
- `[VENV_PYTHON]`: llm-transcription venv Python (e.g., `../.tools/llm-venv/Scripts/python.exe`)
- `[TRANSCRIPTION_SCRIPT]`: `transcribe-image-to-markdown.py` in llm-transcription skill folder
- `[KEYS_FILE]`: Path to API keys file

## Sources

- Anthropic: `https://docs.anthropic.com/en/docs/about-claude/pricing`
- OpenAI: `https://developers.openai.com/api/docs/pricing?latest-pricing=batch`

## Step 1: Capture Pricing Page Screenshots

Use Playwright MCP to capture viewport-sized screenshot chunks. Each provider gets its own subfolder:
- `[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing/`
- `[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing/`

Create folders before capturing.

### Common Steps (both providers)

1. `browser_navigate(url: "<pricing URL>")`
2. `browser_wait_for(time: 2)`
3. Dismiss cookie popup (see `@skills:ms-playwright-mcp` PLAYWRIGHT_ADVANCED_WORKFLOWS.md Section 1):
   - `browser_snapshot()` - check for consent banner
   - Click accept button if found
   - Fallback JS removal:
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
5. Scroll and capture viewport chunks (see provider-specific sections)

### 1a. Capture Anthropic Pricing

URL: `https://docs.anthropic.com/en/docs/about-claude/pricing`

Uses document body for scrolling. Scroll to load lazy content, then take viewport chunks:

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
      path: '[SUBFOLDER_ANTHROPIC]/' + suffix + '.jpg',
      scale: 'css', type: 'jpeg', quality: 90
    });
  }
  return { pages };
}")
```

Replace `[SUBFOLDER_ANTHROPIC]` with: `[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing`

### 1b. Capture OpenAI Pricing

URL: `https://developers.openai.com/api/docs/pricing?latest-pricing=batch`

**IMPORTANT**: URL includes `?latest-pricing=batch` for Batch pricing tier. "All models" table is collapsed - must click "View more". Page uses scrollable inner container `.docs-scroll-container`, not document body.

```
browser_run_code(code: "async (page) => {
  await page.evaluate(async () => {
    const delay = ms => new Promise(r => setTimeout(r, ms));
    const viewMoreButtons = document.querySelectorAll('button');
    for (const btn of viewMoreButtons) {
      if (btn.textContent.toLowerCase().includes('view more')) {
        btn.click();
        await delay(500);
      }
    }
  });
  await page.waitForTimeout(1000);
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
    const suffix = String(i + 1).padStart(2, '0');
    await page.screenshot({
      path: '[SUBFOLDER_OPENAI]/' + suffix + '.jpg',
      scale: 'css', type: 'jpeg', quality: 90
    });
  }
  return { pages };
}")
```

Replace `[SUBFOLDER_OPENAI]` with: `[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing`

## Step 2: Transcribe Screenshots to Markdown

Use `transcribe-image-to-markdown.py` from llm-transcription skill. `--input-folder` transcribes all images at once.

### 2a. Transcribe Anthropic

```powershell
& [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
  --input-folder "[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing" `
  --output-folder "[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing" `
  --model gpt-5-mini --initial-candidates 1 --keys-file [KEYS_FILE] --force
```

### 2b. Transcribe OpenAI

```powershell
& [VENV_PYTHON] [TRANSCRIPTION_SCRIPT] `
  --input-folder "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing" `
  --output-folder "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing" `
  --model gpt-5-mini --initial-candidates 1 --keys-file [KEYS_FILE] --force
```

### 2c. Stitch into Combined Markdowns

Concatenate per-page .md files in sort order, then clean up:

```powershell
# Anthropic
Get-ChildItem "[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing/*.md" |
  Sort-Object Name | ForEach-Object { Get-Content $_.FullName -Raw } |
  Out-File "[PRICING_SOURCES]/[DATE]_Anthropic-ModelPricing.md" -Encoding utf8

# OpenAI
Get-ChildItem "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing/*.md" |
  Sort-Object Name | ForEach-Object { Get-Content $_.FullName -Raw } |
  Out-File "[PRICING_SOURCES]/[DATE]_OpenAI-ModelPricing-Batch.md" -Encoding utf8
```

Delete individual .md files and batch summaries from screenshot subfolders (keep JPGs as archival reference):

```powershell
Remove-Item "[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing/*.md" -Force
Remove-Item "[SCREENSHOTS]/[DATE]_Anthropic-ModelPricing/_batch_summary.json" -Force
Remove-Item "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing/*.md" -Force
Remove-Item "[SCREENSHOTS]/[DATE]_OpenAI-ModelPricing/_batch_summary.json" -Force
```

**Expected output**: `[PRICING_SOURCES]/[DATE]_Anthropic-ModelPricing.md`, `[PRICING_SOURCES]/[DATE]_OpenAI-ModelPricing-Batch.md`

## Step 3: Read Transcriptions and Update model-pricing.json

### 3a. Read Combined Markdowns

Read both files from `[PRICING_SOURCES]`: `[DATE]_Anthropic-ModelPricing.md` and `[DATE]_OpenAI-ModelPricing-Batch.md`

### 3b. Extract Pricing Data

For each model extract: Model ID, Input price per 1M tokens, Output price per 1M tokens.

**Rules:**
- Anthropic: full API model ID with date suffix (e.g., `claude-opus-4-6-20260204`)
- OpenAI: short model name (e.g., `gpt-5-mini`)
- Only models with clear per-token pricing (skip batch-only or special tiers)
- Currency: USD

### 3c. Update model-pricing.json

Read existing `[SKILL_FOLDER]/model-pricing.json` and:

1. **Add** new models (top of provider section, newest first)
2. **Update** changed prices
3. **NEVER remove** existing models
4. **Update** `last_updated` to `[DATE]`
5. **Update** `sources` URLs if changed
6. Maintain existing JSON structure and formatting

### 3d. Verify

- JSON valid (no syntax errors)
- All prices positive numbers
- No duplicate model entries
- `last_updated` matches today

## Step 4: Report Changes

Summarize: models added (with prices), price changes (old vs new), unchanged models, skipped models (with reason).

## Notes

- Read ALL numbered screenshot files per source before extracting prices
- OpenAI URL uses `?latest-pricing=batch` for **batch** tier pricing (50% of standard)
- If model has different pricing tiers (e.g., long context), use **standard** tier
- Anthropic uses full model IDs with date suffixes - always use the full ID as it appears in the API