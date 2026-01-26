# SPEC: Text-to-Voice Realtime Script

**Doc ID**: TTV-SP01
**Goal**: Define requirements for a simple text-to-voice script using OpenAI's gpt-4o-mini-tts model
**Target file**: `ttv.py` (session folder)

## Functional Requirements

**FR-01**: Script accepts text input from command line argument
- Input: Single string argument (max 2000 characters per OpenAI limit)
- Validation: Reject empty input, warn if exceeding 2000 chars

**FR-02**: Script converts text to speech using OpenAI API
- Model: `gpt-4o-mini-tts`
- Voice: `coral` (default, configurable via optional flag)
- Response format: `wav` (fastest for streaming)
- Instructions: Optional parameter for tone/style control

**FR-03**: Script streams audio output in realtime
- Use async streaming to play audio as it arrives
- Do not wait for full audio generation before playback starts
- Output format: WAV (PCM recommended for lowest latency)

**FR-04**: Script handles errors gracefully
- Missing API key: Clear error message
- API errors: Display error details
- Invalid input: Validation before API call

## Design Decisions

**DD-01**: Use Python with OpenAI SDK
- Rationale: Async support, streaming helpers, minimal dependencies

**DD-02**: Streaming via `with_streaming_response`
- Rationale: Enables realtime playback, reduces perceived latency

**DD-03**: WAV output format
- Rationale: Fastest response time per OpenAI docs, good quality

**DD-04**: Single voice option (coral) with optional override
- Rationale: Simplicity for MVP, extensible for future

## Implementation Guarantees

**IG-01**: Script completes within 5 seconds for typical input (100 chars)
- Measured from API call to audio playback start

**IG-02**: Audio plays without buffering delays
- Streaming begins immediately upon first chunk arrival

**IG-03**: Script exits cleanly on completion or error
- No hanging processes or resource leaks

## Acceptance Criteria

**AC-01**: Script runs with: `python ttv.py "Hello world"`
**AC-02**: Audio output is audible and intelligible
**AC-03**: No API errors for valid input
**AC-04**: Script handles missing OPENAI_API_KEY gracefully

## Dependencies

- `openai>=1.0.0` (Python SDK with streaming support)
- `python-dotenv` (for .env file support)
- System audio playback (OS-native)

## Document History

**[2026-01-26 15:03]**
- Initial specification created
- Defined 4 FRs, 4 DDs, 3 IGs, 4 ACs
