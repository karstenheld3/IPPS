# Technology Research Pattern

Systematic pattern for researching technologies, APIs, frameworks, and libraries for software development.

## When to Use

- Evaluating a new technology for adoption
- Understanding an API before integration
- Comparing frameworks for a specific use case
- Investigating a library's production readiness

## Research Phases

### Phase 1: Scope Definition

Before searching, define boundaries:

```
RESEARCH SCOPE
- Technology: [Name and version]
- Purpose: [Why we're researching this]
- Use Case: [Specific application context]
- Constraints: [Must-haves, deal-breakers]
- Time Budget: [Research depth limit]
```

**Questions to answer:**
- What problem does this solve for us?
- What are our hard requirements?
- What would make this a non-starter?

### Phase 2: Primary Source Survey

**2.1 Official Documentation**
- Read: Getting Started, Core Concepts, API Reference
- Note: Version, last updated, documentation quality
- Extract: Architecture, key abstractions, limitations

**2.2 GitHub/Source Repository**
- Check: Stars, forks, open issues, PR activity
- Read: README, CONTRIBUTING, recent commits
- Note: Release frequency, maintainer responsiveness
- Look for: Breaking change history, deprecation patterns

**2.3 Changelog/Release Notes**
- Scan: Last 3-6 months of releases
- Note: Breaking changes, security fixes, feature velocity
- Flag: Stability indicators (alpha/beta/stable)

### Phase 3: Technical Deep Dive

**3.1 Architecture Understanding**
- Core concepts and mental model
- Data flow and state management
- Extension points and plugin system
- Performance characteristics

**3.2 Integration Points**
- Installation and setup requirements
- Configuration options
- Dependencies (runtime, peer, dev)
- Build/bundle implications

**3.3 API Surface**
- Key functions/methods/classes
- Input/output contracts
- Error handling patterns
- Async/sync behavior

### Phase 4: Production Readiness Assessment

**4.1 Reliability**
- Error handling and recovery
- Logging and debugging support
- Known issues and workarounds

**4.2 Performance**
- Benchmarks (official and third-party)
- Memory footprint
- Startup time
- Scalability characteristics

**4.3 Security**
- Security advisories history
- Authentication/authorization patterns
- Data handling practices
- Dependency security

**4.4 Operational**
- Monitoring and observability
- Configuration management
- Upgrade path and migration
- Rollback capabilities

### Phase 5: Community and Ecosystem

**5.1 Adoption Indicators**
- npm downloads / PyPI downloads / etc.
- GitHub stars trajectory (not just count)
- Stack Overflow question volume and quality
- Corporate adopters (if disclosed)

**5.2 Community Health**
- Maintainer activity and responsiveness
- Community size and engagement
- Quality of third-party resources
- Conference talks and tutorials

**5.3 Ecosystem**
- Available plugins/extensions
- Integration with common tools
- Alternative implementations
- Migration tools from competitors

### Phase 6: Hands-On Verification

**6.1 Quick Proof of Concept**
- Implement minimal working example
- Test primary use case
- Verify claimed features work as documented

**6.2 Edge Case Testing**
- Test error scenarios
- Verify behavior at boundaries
- Check undocumented behavior

**6.3 Developer Experience**
- Setup friction
- Documentation accuracy
- Debugging ease
- IDE/tooling support

## Output Template

```markdown
# INFO: [Technology Name] Research

**Doc ID**: [TOPIC]-IN[NN]
**Goal**: Evaluate [technology] for [use case]
**Research Date**: YYYY-MM-DD

## MUST-NOT-FORGET

- [Critical finding 1]
- [Critical finding 2]

## Key Findings (MEPI Summary)

1. **[Main conclusion]**: [One sentence summary]
2. **[Second key point]**: [One sentence]
3. **[Third key point]**: [One sentence]

## Recommendation

[Clear recommendation with rationale]

## Detailed Analysis

### Overview
- **What it is**: [Brief description]
- **Version researched**: [X.Y.Z]
- **License**: [License type]
- **Maturity**: [Alpha/Beta/Stable/Mature]

### Architecture
[Key architectural concepts]

### Strengths
- [Strength 1]
- [Strength 2]

### Weaknesses
- [Weakness 1]
- [Weakness 2]

### Production Readiness
- **Reliability**: [Assessment]
- **Performance**: [Assessment]
- **Security**: [Assessment]
- **Operational**: [Assessment]

### Fit for Our Use Case
[Specific analysis against stated constraints]

## Not Considered / Out of Scope

- [Thing 1] - [Why excluded]
- [Thing 2] - [Why excluded]

## Sources

- [SC-01] Official Docs: [URL] (accessed YYYY-MM-DD) [VERIFIED]
- [SC-02] GitHub: [URL] (accessed YYYY-MM-DD) [VERIFIED]
- [SC-03] Blog Post: [URL] (accessed YYYY-MM-DD) [CLAIMED]

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial research completed
```

## Anti-Patterns to Avoid

- **Skipping primary sources** - Don't rely on blog summaries alone
- **Ignoring version mismatch** - Old tutorials may not apply
- **Hype-driven evaluation** - Popularity != fit for your use case
- **Skipping hands-on testing** - Documentation lies, code doesn't
- **Ignoring operational concerns** - Dev experience != production experience
- **Single-point-of-failure research** - Verify across multiple sources

## Research Depth Levels

**Level 1: Quick Assessment (1-2 hours)**
- Phase 1 + Phase 2.1-2.2 + Key findings only
- Output: Bullet points, go/no-go decision

**Level 2: Standard Evaluation (4-8 hours)**
- Phases 1-5 fully
- Output: INFO document with recommendations

**Level 3: Deep Evaluation (1-3 days)**
- All phases including hands-on verification
- Output: Comprehensive INFO + POC code
- Use for: Critical infrastructure, long-term commitments
