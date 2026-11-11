# New Model Scan (2026-11-11 NEWMODEL, read-only)

**Doc ID**: MDLRGUP-20261111-SCAN
**Goal**: New models since registry `1.12.1` (2026-11-02), with focus on `glm-ocr` and comparable OCR models. No canonical JSON changed.

## 1. Text models missing from the registry (vendor pages, accessed 2026-11-11)

- **Anthropic**
  - `claude-fable-5-2` - `$8` input, `$0.20` cached, `$40` output, 1M context, 128K output, adaptive thinking always on, default effort `high`, retirement not sooner than 2027-11-09. Source: `https://platform.claude.com/docs/en/models/overview`, `https://platform.claude.com/docs/en/about-claude/pricing`
    - Edge EC-1 candidate (E1): `claude-fable-5-2 > claude-opus-5-5`, statement "Use Claude Fable 5.2 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short."
  - `claude-mythos-5-2` (ID inferred, pricing page only) - `$8` input, `$0.20` cached, `$40` output. No model-overview entry. Treat as restricted-access twin of `claude-fable-5-2` (EC-3) only after a vendor "same model" statement is found
  - Existing Anthropic prices: no change versus `model-pricing.json`
- **Google**
  - `gemini-4-carbon` - 1M context, 65K / 1M max output. Standard price `$2.00` input, `$0.10` cached (implicit only), `$10.00` output through 2026-11-30, then `$4.00` / `$0.20` / `$20.00` from 2026-12-01. Not on Free tier. Source: `https://ai.google.dev/gemini-api/docs/models`, `https://ai.google.dev/gemini-api/docs/pricing`
    - Release date and tier relation to `gemini-4-argon`: vendor wording "Our strongest reasoning model" vs argon "efficient ... compared to Gemini 4 Carbon" = EC-1 candidate (E1) `gemini-4-carbon > gemini-4-argon`; quote still to be stored with access date
- **OpenAI** (text-capable, not in registry)
  - `gpt-6-cyber` (`$20` / `$2` cached / `$100`), `gpt-6-astra-law` (`$10` / `$1` / `$50`), `chat-latest` (`$5` / `$0.50` / `$30`). Source: `https://developers.openai.com/api/docs/pricing?latest-pricing=standard`
- **xAI**: no new text models
- **Z.AI**: no new text or vision models; `GLM-Image` (`$0.015` per image) is image generation only

## 2. Non-text models seen (not registered unless scope changes)

- OpenAI: `gpt-image-2`, `gpt-image-2.6-sunburst`, `gpt-image-2.6-flare`, `gpt-live-1`, `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-translate`, `gpt-live-transcribe`
- Google: Gemini 3.8 Live, Gemini 3.8 Flash TTS, Gemini 3.5 Transcribe, Gemini Omni 1.2 Flash, Nano Banana 2.1, Lyria 3.5, Gemini Embedding 2, Gemma 4 (free, open)
- xAI: `grok-imagine-*`, `grok-voice-3.0`

## 3. OCR models

- **`glm-ocr` (registered, needs correction)**
  - Release: 2026-02-02 (Z.AI announcement `https://www.zhipuai.cn/zh/research/150`; GitHub `zai-org/GLM-OCR` created 2026-02-02). Registry has `2025-10-15` with `release_date_assumed: true` (EC-9 correction)
  - Price unchanged: `$0.03` input and output per 1M tokens (`https://docs.z.ai/guides/overview/pricing`, Other Pricing group)
  - 0.9B parameters, OmniDocBench V1.5 `94.62` (vendor claim). Input PDF or image (image <= 10MB, PDF <= 50MB, <= 100 pages); output text, image links, Markdown
  - Not a chat-completions model: `POST https://api.z.ai/api/paas/v4/layout_parsing` with `{"model": "glm-ocr", "file": "<url>"}` (`https://docs.z.ai/guides/vlm/glm-ocr`). `call-llm.py` chat dispatch cannot call it. Registry `context_window: 8192` and prefix `method: temperature` are not backed by a vendor page (unverified)
- **Comparable OCR models, vendor API with price**
  - `mistral-ocr-4-1` (alias `mistral-ocr-latest`): GA 2026-07-16, `$4` per 1000 pages, `$5` per 1000 annotated pages, endpoint `/v1/ocr`, batch `/v1/batch`. Source: `https://docs.mistral.ai/models/ocr-4-1`
  - `mistral-ocr-2512` (OCR 3): `$2` per 1000 pages, `$0.2` cached (Mistral pricing page via search result; vendor page not opened). Mistral is not a registry provider
- **Comparable OCR models, open weights (no first-party price)**
  - OmniDocBench leaderboard snapshot 2026-10-05 (SoMark, third party, mixed environments): OXR-1.0 `97.18`, TeleOCR `96.91`, OvisOCR2 `96.47`, PaddleOCR-VL-1.6 `96.34`, MinerU2.5-Pro `95.75`, GLM-OCR `95.22`, DeepSeek-OCR-2 `90.25`, Gemini 3 Pro `92.91`, Gemini 3 Flash `92.62`
  - Newer than that snapshot: OvisOCR3 (0.8B, `96.74` on OmniDocBench v1.6, arXiv 2610.33066)
  - `deepseek-ocr-2`: open weights, third-party hosting only (Novita `$0.03` / `$0.03`, 8K); Doubleword shut it down 2026-10-30
- Source reliability: leaderboard and aggregator figures are third-party; vendor pages are the only registry-grade source

## 4. Pipeline notes

- Registry `1.12.1` is committed (git clean for `llm-tools`, `.devin/skills/llm-tools`, session folder)
- Epoch ECI has no OCR specialist rows; OCR models stay `D1*` (unplaced) under SP01 FR-01 unless a vendor escalation statement exists
