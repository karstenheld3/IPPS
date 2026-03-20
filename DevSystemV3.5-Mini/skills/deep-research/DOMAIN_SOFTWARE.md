# Domain Profile: Software

Research domain for software APIs, frameworks, libraries, SDKs, and developer tools.

## When to Use

- Subject is a software API, framework, library, SDK, or developer tool
- Prompt mentions: API, SDK, library, framework, package, module, endpoint, rate limit, authentication
- Output consumed by developers or architects

## Source Tiers

- **Tier 1 (official/primary)**: Official documentation, API references, SDK source code, official PDFs/specs
- **Tier 2 (vendor/issuer)**: Official blog, GitHub repo, release notes, changelog, conference talks by maintainers
- **Tier 3 (community/analyst)**: Stack Overflow, expert blogs, GitHub issues/discussions, Reddit, Discord

## Document Handling

- Read API docs fully (not just selected endpoints)
- Code examples must be syntactically correct for target language
- Version-match all sources to documented version
- Download and transcribe official PDFs via source processing pipeline
- Large API references: transcribe fully, use `<transcription_json>` extraction for endpoint tables

## Template Additions

- **SDK Examples** - Adapt to relevant languages (C#, Python, TypeScript, PowerShell, JavaScript, Go, etc.)
- **Error Responses** - Error codes with descriptions and resolution
- **Rate Limiting / Throttling** - Limits, headers, retry strategies
- **Authentication** - Auth methods, token lifecycle, scopes
- **Gotchas and Quirks** - Undocumented behavior, edge cases from community sources

## Quality Criteria

- All code examples syntactically correct (or marked `[ASSUMED]` if untested)
- Version scope explicitly stated in every topic document
- Rate limiting section populated (or explicitly noted as "not applicable")
- Error codes documented with resolution guidance
- Community-sourced limitations cross-referenced with official bug trackers where available
- No Markdown tables (use lists per core conventions)