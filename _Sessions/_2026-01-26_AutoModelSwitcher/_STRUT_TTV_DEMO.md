Goal: Build simple text-to-voice realtime script using gpt-4o-mini-tts

[ ] P1 [RESEARCH]: API and pricing
├─ Objectives:
│   └─ [ ] API usage and costs understood ← P1-D1
├─ Strategy: Fetch OpenAI TTS docs and pricing page
│   - Model: Sonnet 4.5
├─ [x] P1-S1 [FETCH](OpenAI TTS documentation)
├─ [x] P1-S2 [FETCH](OpenAI pricing page)
├─ Deliverables:
│   └─ [x] P1-D1: API findings (endpoint, params, pricing)
└─> Transitions:
    - P1-D1 checked → P2 [SPEC]

[ ] P2 [SPEC]: Write minimal spec
├─ Objectives:
│   └─ [ ] Script requirements defined ← P2-D1
├─ Strategy: Define what the script does, inputs, outputs
│   - Model: Opus 4.5 Thinking
├─ [x] P2-S1 [WRITE](spec in session folder)
├─ Deliverables:
│   └─ [x] P2-D1: _SPEC_TTV.md created
└─> Transitions:
    - P2-D1 checked → P3 [IMPLEMENT]

[ ] P3 [IMPLEMENT]: Build script
├─ Objectives:
│   └─ [ ] Working script exists ← P3-D1
├─ Strategy: Python script with streaming TTS
│   - Model: Sonnet 4.5
├─ [x] P3-S1 [CODE](create ttv.py)
├─ Deliverables:
│   └─ [x] P3-D1: ttv.py in session folder
└─> Transitions:
    - P3-D1 checked → P4 [TEST]

[ ] P4 [TEST]: Verify script works
├─ Objectives:
│   └─ [ ] Script tested successfully ← P4-D1
├─ Strategy: Run script with sample text
│   - Model: Haiku 4.5
├─ [x] P4-S1 [RUN](test with "Hello world")
├─ Deliverables:
│   └─ [x] P4-D1: Audio output confirmed
└─> Transitions:
    - P4-D1 checked → [END]

[x] [END]
