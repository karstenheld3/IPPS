# Agent Skill Development Rules

Rules for building agent skills that integrate external tools, MCP servers, or system capabilities.

## Target Audience

Skill files are consumed by LLMs, not humans. Optimize for medium-reasoning models with low context windows.

Design principles:
1. Maximum clarity - one interpretation per instruction
2. Numbered steps - LLMs follow sequences better than prose
3. MUST-NOT-FORGET technique for complex skills with verification
4. No `**bold**` in LLM-consumed files - adds tokens without improving comprehension
5. `#` and `##` headers are parsing boundaries LLMs rely on
6. Compact format for lookups - one line per resource
7. Verbose format only when justified (multi-step reasoning, troubleshooting, code with explanation)
8. JSON intermediate output for multi-step workflows to enforce explicit reasoning:
```
## Step 2: Classify skill type
Emit before proceeding:
{"skill_type": "resource_lookup|instructional|setup", "format": "compact|rich|verbose", "reason": "..."}
```

Exception: SETUP.md and UNINSTALL.md may use richer formatting for human users.

## 1. Research First

Before writing skill documentation:
1. Understand the technology
2. Verify compatibility with target agent (Windsurf/Cascade)
3. Identify dependencies and versions
4. Find known issues (GitHub issues, forums)
5. Test manually first

Document research in INFO document or SKILL.md.

## 2. Skill File Structure

Required: `SKILL.md` (see 2.1)
Conditional: `SETUP.md` (if install needed) + `UNINSTALL.md` (required if SETUP.md exists)
Optional: supporting docs, templates, examples

### 2.1 SKILL.md Required Content

Required sections:
1. Frontmatter - `name` and `description`
2. When to Use / When NOT to Use
3. Architecture - how components connect (diagram preferred)
4. Technical Details
5. Capabilities
6. Limitations
7. Sources

Technical depth requirements:
- Tool actions/API with parameters
- Dependencies
- Platform specifics (Windows, macOS, Linux)
- Model requirements (if applicable)
- Execution flow

```markdown
# GOOD: Specific and actionable
## Tool Actions
- `screenshot` - Capture full screen, returns base64 PNG
- `mouse_move` - Move cursor to (x, y) coordinates
- `left_click` - Single left click at current position
- `key` - Press key combination (e.g., `ctrl+c`)
- `type` - Type text string character by character

## Architecture
┌─────────────────────────────────────────┐
│ Agent → MCP Protocol → Server → Library │
│                              └→ OS APIs │
└─────────────────────────────────────────┘
```

## 3. SETUP.md Requirements

### 3.1 Pre-Installation Verification

MUST verify before modifying system:
1. Verify all prerequisites exist
2. Test core functionality in isolation
3. Check current system state
4. Provide expected output for each step

Include Pre-Installation Checklist with checkboxes. Only proceed to installation after all checks pass.

### 3.2 Installation Section

After pre-installation passes:
1. Backup existing configuration
2. Make minimal changes
3. Provide rollback instructions inline
4. Show expected results after each step

### 3.2.1 MCP Config Modification Pattern (Windsurf)

For `~/.codeium/windsurf/mcp_config.json`, key requirements:
- Idempotent - running twice produces same result
- Backup first - always backup before modifying
- Handle PSCustomObject - convert to Hashtable after JSON parsing
- Compare before write - don't modify if already correct

```powershell
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
$targetServer = @{ command = "npx"; args = @("package-name") }

if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json -AsHashtable
} else { $config = @{ mcpServers = @{} } }

if ($config.mcpServers -isnot [System.Collections.Hashtable]) {
    $serversHash = @{}
    $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
    $config.mcpServers = $serversHash
}

if ($config.mcpServers.ContainsKey("server-name")) {
    $currentJson = $config.mcpServers["server-name"] | ConvertTo-Json -Compress
    $targetJson = $targetServer | ConvertTo-Json -Compress
    if ($currentJson -eq $targetJson) { Write-Host "Already configured" -ForegroundColor Green; return }
}

$backupPath = "$configPath._backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $configPath $backupPath -ErrorAction SilentlyContinue
$config.mcpServers["server-name"] = $targetServer
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
```

### 3.3 Post-Installation Verification

1. Verify installation succeeded
2. Test actual functionality
3. Document expected behavior with specific prompts
4. Provide troubleshooting for common failures

## 4. UNINSTALL.md Requirements

### 4.1 Pre-Uninstall Verification

1. Verify what is currently installed
2. Check for dependencies that might break
3. Identify all affected files/configs
4. Include Pre-Uninstall Checklist

### 4.2 Uninstall Section

Remove in reverse order of installation. Show what each step removes. Verify after each step.

### 4.3 Post-Uninstall Verification

Confirm all components removed. Verify clean state. Note manual cleanup needed.

## 5. Test Before Writing

CRITICAL: Test all code snippets WITHOUT modifying the system before including in SETUP/UNINSTALL.

1. Read-only tests first
2. Isolated tests in temporary location
3. Destructive tests last - only after read-only pass

```powershell
# GOOD: Test before config
npx -y some-mcp-server --help

# GOOD: Check state before modifying
if (Test-Path $configPath) { Get-Content $configPath }
```

## 6. Documentation Quality

Every skill MUST include:
- Compatibility notes (verified vs expected)
- Expected output at each step
- Troubleshooting for common errors
- References to official docs/repos

Avoid: untested commands, vague success criteria, missing error handling, system state assumptions.

## 7. Case Study: computer-use-mcp Skill

Lessons learned:
1. Research before writing - found compatibility gap early (not officially verified for Windsurf)
2. Test commands first - `npx -y computer-use-mcp --help` before documenting
3. Verify then modify - pre-installation checks prevent broken installs
4. Expected output is crucial - user knows if something went wrong
5. Sources matter - link to primary documentation

Initial SETUP.md jumped to installation without verification. Fixed by adding pre-installation verification sections, checklist, and clear separator before installation.

## 8. Token Optimization for Skill Files

### 8.1 Core Principle

Never sacrifice clarity for brevity. Never add formatting that only helps human eyes.

### 8.2 What to Remove

- `**Bold**` markup, unnecessary bullet prefixes, sub-sub-headers when labels suffice
- Blank lines between list items, verbose prefixes (`- **URL:** `)
- Sections restating the Keywords line, descriptions restating headings
- Filler phrases: "This section covers", "The following resources"

### 8.3 What to Keep

- `#` and `##` headers (parsing boundaries)
- Keywords/trigger lines
- Parenthetical notes with critical context
- Concrete examples
- All URLs, parameters, technical detail

### 8.4 Compact Format for Resource/Lookup Skills

```
# Title
Keywords: term1, term2, term3

## Category
Name: https://url.com (notes if needed)
Name2: https://url2.com
```

### 8.5 When Verbose Format is Justified

Multi-step reasoning, complex parameter interactions, detailed troubleshooting, code with explanation.

### 8.6 Review Metric

"If I remove this token, does the LLM lose information or context?" If no, remove it.

## 9. Skill Review Checklist

- [ ] Research documented (INFO or SKILL.md)
- [ ] SKILL.md has "when to use" and "when NOT to use"
- [ ] SETUP.md has pre-installation verification
- [ ] SETUP.md tests before modifying
- [ ] UNINSTALL.md exists if SETUP.md exists
- [ ] UNINSTALL.md has pre-uninstall verification
- [ ] All code snippets tested manually
- [ ] Expected output documented for each step
- [ ] Troubleshooting covers common errors
- [ ] References link to primary sources
- [ ] Token optimization applied: no visual-only formatting in LLM-consumed files