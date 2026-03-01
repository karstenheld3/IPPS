# INFO: OpenClaw Personal AI Assistant

**Doc ID**: OCLAW-IN01
**Goal**: Comprehensive exploration of OpenClaw for remote interaction via WhatsApp and Cascade integration
**Research Date**: 2026-02-27
**Version Scope**: OpenClaw v2026.2.x (latest stable as of research date)

## Table of Contents

1. What is OpenClaw?
2. Use Cases and Applications
3. Features (Complete List)
4. Communication Channels
5. Windows Setup Guide
6. Security Considerations
7. Windsurf Cascade Integration Options
8. Multi-Machine Sync Strategies
9. Limitations and Known Issues
10. Sources

## 1. What is OpenClaw?

OpenClaw (formerly Clawdbot and Moltbot) is an autonomous, open-source AI assistant that runs locally on your machine and connects to messaging platforms. Created by Austrian developer Peter Steinberger (who announced joining OpenAI in February 2026), the project is MIT-licensed and community-driven with 877+ contributors.

**Core concept**: You message OpenClaw through WhatsApp, Telegram, Slack, Discord, or other chat apps, and it executes tasks on your behalf - running shell commands, controlling browsers, reading/writing files, managing calendars, sending emails - all triggered by a text message.

**Key differentiators**:
- **Self-hosted**: Gateway, tools, and memory live on your machine, not a vendor cloud
- **Local-first storage**: Conversations, memory, and skills stored as Markdown/YAML files under `~/.openclaw`
- **Model-agnostic**: Works with Anthropic, OpenAI, Google, or local models (Ollama, LM Studio)
- **Autonomous operation**: Runs on heartbeat schedule (every 30-60 minutes), can act without explicit prompts
- **Open source**: MIT license, fully auditable, forkable

**Architecture summary**:
```
WhatsApp / Telegram / Slack / Discord / Signal / iMessage / Teams / WebChat
                              |
                              v
                    ┌─────────────────────┐
                    │      Gateway        │
                    │   (control plane)   │
                    │  ws://127.0.0.1:18789│
                    └──────────┬──────────┘
                               |
           ┌───────────────────┼───────────────────┐
           |                   |                   |
      Pi agent (RPC)     CLI (openclaw)    iOS/Android nodes
```

## 2. Use Cases and Applications

### Primary Use Cases

- **Personal automation**: Calendar management, email triage, file organization
- **Remote task execution**: Run commands on home server from anywhere via WhatsApp
- **Multi-platform inbox**: Unified AI assistant across all messaging platforms
- **Browser automation**: Web scraping, form filling, data extraction
- **Scheduled tasks**: Heartbeat-driven periodic checks and actions
- **Team assistant**: Slack/Discord bot for community support

### Real-World Examples

- **Car purchase negotiation**: User tasked OpenClaw to buy a Hyundai Palisade. Agent scraped dealer inventories, filled contact forms, played dealers against each other via PDF quotes, secured $4,200 below sticker price while user slept.

- **Insurance dispute**: Agent discovered rejection email, drafted legal rebuttal citing policy language, sent it autonomously. Insurer reopened investigation.

- **Community support**: Zilliz deployed OpenClaw as Milvus community assistant on Slack. Setup took 20 minutes. Answers questions, troubleshoots errors, points to documentation.

- **Moltbook experiment**: Social network where only AI agents post. 1.5 million agents registered within a week. Demonstrated autonomous agent coordination at scale (also exposed security risks).

### Scenarios OpenClaw Excels At

- Always-on assistant accessible from mobile
- Long-running background tasks
- Cross-platform messaging consolidation
- Shell/system access from anywhere
- Autonomous monitoring and alerting

## 3. Features (Complete List)

### Core Platform

- **Gateway WebSocket control plane**: Sessions, presence, config, cron, webhooks, Control UI
- **CLI surface**: `openclaw gateway`, `agent`, `send`, `wizard`, `doctor`
- **Pi agent runtime**: RPC mode with tool streaming and block streaming
- **Session model**: Main session for DMs, isolated sessions for groups, activation modes, queue modes
- **Media pipeline**: Images/audio/video, transcription hooks, size caps, temp file lifecycle

### Communication Channels

- **WhatsApp** (Baileys library)
- **Telegram** (grammY)
- **Slack** (Bolt)
- **Discord** (discord.js)
- **Google Chat** (Chat API)
- **Signal** (signal-cli)
- **BlueBubbles** (iMessage, recommended)
- **iMessage** (legacy imsg, macOS-only)
- **Microsoft Teams** (extension)
- **Matrix** (extension)
- **Zalo** / **Zalo Personal** (extension)
- **WebChat** (built-in, served from Gateway)

### Apps and Nodes

- **macOS app**: Menu bar control plane, Voice Wake/PTT, Talk Mode overlay, WebChat, debug tools, remote gateway control
- **iOS node**: Canvas, Voice Wake, Talk Mode, camera, screen recording, Bonjour pairing
- **Android node**: Canvas, Talk Mode, camera, screen recording, optional SMS
- **macOS node mode**: `system.run`/`system.notify` + canvas/camera exposure

### Tools and Automation

- **Browser control**: Dedicated OpenClaw Chrome/Chromium with CDP control, snapshots, actions, uploads, profiles
- **Canvas (A2UI)**: Agent-driven visual workspace, push/reset, eval, snapshot
- **Node tools**: Camera snap/clip, screen record, `location.get`, notifications
- **Cron + wakeups**: Scheduled task execution
- **Webhooks**: External event triggers
- **Gmail Pub/Sub**: Email automation hooks
- **Skills platform**: Bundled, managed, and workspace skills with install gating + UI

### Runtime and Safety

- **Channel routing**: Per-channel message routing and isolation
- **Retry policy**: Configurable retry with exponential backoff
- **Streaming/chunking**: Long message handling across platforms
- **Presence + typing indicators**: Real-time status
- **Usage tracking**: Token and cost monitoring
- **Model failover**: Auth profile rotation, fallback chains
- **Session pruning**: Context window management
- **Sandboxing**: Docker-based isolation for non-main sessions

### Operations and Packaging

- **Control UI + WebChat**: Served directly from Gateway
- **Tailscale Serve/Funnel**: Secure remote access without port exposure
- **SSH tunnels**: Alternative remote access with token/password auth
- **Nix mode**: Declarative configuration
- **Docker**: Container-based deployment
- **Doctor migrations**: Health checks and config validation

### Skills System

- **Bundled skills**: Ship with npm package or app
- **Managed skills**: `~/.openclaw/skills` (shared across agents)
- **Workspace skills**: `<workspace>/skills` (per-agent)
- **ClawHub**: Public skills registry at https://clawhub.com
  - `clawhub install <skill-slug>`
  - `clawhub update --all`
  - `clawhub sync --all`
- **SKILL.md format**: AgentSkills spec with YAML frontmatter

### Voice Features

- **Voice Wake**: Always-on speech activation (macOS/iOS/Android)
- **Talk Mode**: Continuous voice conversation with ElevenLabs
- **PTT (Push-to-Talk)**: Manual voice activation

## 4. Communication Channels (Detailed)

### WhatsApp
- Uses Baileys library (unofficial WhatsApp Web API)
- Link device via: `openclaw channels login`
- Credentials stored in `~/.openclaw/credentials`
- Configure allowlist: `channels.whatsapp.allowFrom`
- Group access: `channels.whatsapp.groups`

### Telegram
- Uses grammY framework
- Set `TELEGRAM_BOT_TOKEN` or `channels.telegram.botToken`
- Optional webhook: `channels.telegram.webhookUrl` + `webhookSecret`
- Group config: `channels.telegram.groups`

### Slack
- Uses Bolt framework
- Set `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN`
- Or config: `channels.slack.botToken` + `channels.slack.appToken`

### Discord
- Uses discord.js
- Set `DISCORD_BOT_TOKEN` or `channels.discord.token`
- Optional: native commands, text commands, access groups
- Config: `channels.discord.allowFrom`, `channels.discord.guilds`

### Signal
- Requires signal-cli installation
- Configure `channels.signal` section

### iMessage (BlueBubbles - Recommended)
- BlueBubbles server runs on macOS
- Gateway can run on macOS or elsewhere
- Config: `channels.bluebubbles.serverUrl` + `password` + `webhookPath`

### Microsoft Teams
- Requires Teams app + Bot Framework setup
- Config: `msteams.allowFrom`, `msteams.groupAllowFrom`

### WebChat
- Built into Gateway WebSocket
- No separate configuration needed
- Access via Control UI at `http://127.0.0.1:18789/`

## 5. Windows Setup Guide

### Requirements
- Windows 10/11 with WSL2
- Ubuntu distribution (recommended: Ubuntu 24.04)
- Node.js 22+
- systemd enabled in WSL

### Step-by-Step Installation

**1. Install WSL2 + Ubuntu**
```powershell
wsl --install
# Or explicitly:
wsl --list --online
wsl --install -d Ubuntu-24.04
```

**2. Enable systemd (required for daemon)**
```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```
Then restart WSL:
```powershell
wsl --shutdown
```
Verify:
```bash
systemctl --user status
```

**3. Install OpenClaw (inside WSL)**
```bash
# Option A: From source
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
openclaw onboard

# Option B: Via npm
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**4. Run the Gateway**
```bash
openclaw gateway --port 18789 --verbose
# Or as daemon:
openclaw gateway install
```

**5. Verify installation**
```bash
openclaw doctor
openclaw gateway status
openclaw dashboard  # Opens Control UI
```

### Windows-Specific Considerations

- **Native Windows not supported**: WhatsApp Web protocol, iMessage integration, and Unix process management require POSIX environment
- **WSL2 IP changes**: WSL2 gets dynamic IP on restart. Use portproxy for LAN access:
```powershell
$WslIp = (wsl -d Ubuntu-24.04 -- hostname -I).Trim().Split(" ")[0]
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=18789 `
    connectaddress=$WslIp connectport=18789
```
- **Firewall rule** (if exposing to LAN):
```powershell
New-NetFirewallRule -DisplayName "OpenClaw Gateway" -Direction Inbound `
    -Protocol TCP -LocalPort 18789 -Action Allow
```

### Dependencies

- **Required**: Node.js 22+, pnpm (recommended), Git
- **Optional**: Docker (for sandboxing), Tailscale (for remote access), signal-cli (for Signal), Chromium (for browser control)

### Limitations on Windows

- No native Windows support - must use WSL2
- iMessage requires macOS (or BlueBubbles server on a Mac)
- Some tools assume Linux paths
- WSL2 networking adds complexity for remote access

## 6. Security Considerations

### Critical Security Issues

**CVE-2026-25253 (CVSS 8.8)** - Patched in v2026.1.29
- Cross-site WebSocket hijacking vulnerability
- Any website could steal auth token via malicious link
- One click = full RCE on machine
- **Action**: Ensure running v2026.1.29 or later

**Malicious Skills**
- 26% of audited skills (31,000 across platforms) had at least one vulnerability
- 230+ malicious skills uploaded to ClawHub in first week of February 2026
- "What Would Elon Do?" skill: used prompt injection to exfiltrate data
- **Action**: Fork, read, and audit every skill before installation

### Security Best Practices

1. **Run in isolated environment**: Dedicated VM or container, not your daily driver
2. **Keep loopback-only**: `gateway.bind: "loopback"` unless explicitly needed
3. **Use Tailscale Serve**: For remote access without public exposure
4. **Gate irreversible actions**: Human approval for payments, deletions, emails
5. **Set API spending limits**: At provider level, not just agent config
6. **Pin to latest version**: Keep up with security patches
7. **Don't expose to public internet**: Unless you understand the network config

### DM Security Model

Default behavior:
- `dmPolicy="pairing"`: Unknown senders receive pairing code, bot doesn't process
- Approve with: `openclaw pairing approve <channel> <code>`
- Public DMs require explicit opt-in: `dmPolicy="open"` + `"*"` in allowlist

Run `openclaw doctor` to detect risky DM policies.

### Sandbox Mode

For non-main sessions (groups/channels):
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"
      }
    }
  }
}
```
- Allowlist: bash, process, read, write, edit, sessions_*
- Denylist: browser, canvas, nodes, cron, discord, gateway

### Cost Awareness

- **Light usage**: $5-20/month (few heartbeats/day, Sonnet)
- **Active usage**: $50-150/month (frequent heartbeats, large prompts)
- **Heavy usage**: $270-540/month (12+ heartbeats/day on Opus)
- **Unoptimized**: $1000+/month reported

Set spending alerts at provider level. Misconfigured heartbeat can drain budget overnight.

## 7. Windsurf Cascade Integration Options

### Option A: MCP Server (Recommended)

**openclaw-mcp** by freema provides Model Context Protocol bridge between Claude.ai/Cascade and OpenClaw.

**Architecture**:
```
┌───────────────────────────────────────────────┐
│               Your Server                      │
│                                               │
│  ┌─────────────────┐  ┌────────────────────┐  │
│  │ OpenClaw Gateway│◄►│ OpenClaw MCP Bridge│  │
│  │     :18789      │  │       :3000        │  │
│  │                 │  │  - OAuth 2.1 auth  │  │
│  │ OpenAI-compat   │  │  - CORS protection │  │
│  │ /v1/chat/...    │  │  - Input validation│  │
│  └─────────────────┘  └─────────┬──────────┘  │
└─────────────────────────────────┼─────────────┘
                                  │ HTTPS + OAuth 2.1
                                  v
                        ┌─────────────────┐
                        │   Claude.ai /   │
                        │   Cascade MCP   │
                        └─────────────────┘
```

**Available Tools**:
- `openclaw_chat` - Sync chat with OpenClaw
- `openclaw_status` - Check gateway status
- `openclaw_chat_async` - Async chat for long-running ops
- `openclaw_task_status` - Check async task status
- `openclaw_task_list` - List running tasks
- `openclaw_task_cancel` - Cancel async task

**Setup**:
```bash
# Docker (recommended)
docker run -d -p 3000:3000 \
  -e OPENCLAW_GATEWAY_URL=ws://host.docker.internal:18789 \
  -e OPENCLAW_GATEWAY_TOKEN=your-token \
  freema/openclaw-mcp

# Or local
git clone https://github.com/freema/openclaw-mcp
cd openclaw-mcp
npm install && npm start
```

**Cascade Configuration** (`.windsurf/mcp.json`):
```json
{
  "mcpServers": {
    "openclaw": {
      "command": "npx",
      "args": ["-y", "openclaw-mcp"],
      "env": {
        "OPENCLAW_GATEWAY_URL": "ws://127.0.0.1:18789",
        "OPENCLAW_GATEWAY_TOKEN": "your-token"
      }
    }
  }
}
```

### Option B: Native MCP Support in OpenClaw

OpenClaw has native MCP server support via `@modelcontextprotocol/sdk@1.25.3`.

**Configuration** (`openclaw.json`):
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "mcp": {
          "servers": {
            "notion": {
              "command": "npx",
              "args": ["-y", "@notionhq/mcp-server"]
            }
          }
        }
      }
    ]
  }
}
```

This allows OpenClaw to connect to external MCP servers (Notion, Linear, Stripe, etc.) and expose their tools to the agent.

### Option C: Custom Skill

Create a Cascade-specific skill in your workspace:

**`~/.openclaw/workspace/skills/cascade-bridge/SKILL.md`**:
```markdown
---
name: cascade-bridge
description: Bridge for Windsurf Cascade integration
user-invocable: true
---

When invoked, expose OpenClaw capabilities to Cascade agent:
- Execute shell commands via `exec` tool
- Read/write workspace files
- Send messages to other channels
- Query session history

Use {baseDir} for skill-specific resources.
```

### Option D: Workflow Integration

Create a Windsurf workflow that calls OpenClaw CLI:

**`.windsurf/workflows/openclaw.md`**:
```markdown
---
description: Send task to OpenClaw for background execution
---

## Step 1: Send to OpenClaw

```bash
openclaw agent --message "[USER_TASK]" --thinking high
```

## Step 2: Check Status

```bash
openclaw status --deep
```
```

### Recommendation

**MCP Server (Option A)** is the best approach because:
- Standard protocol supported by Cascade
- Async task handling for long-running jobs
- OAuth 2.1 security
- Clean separation between Cascade and OpenClaw

## 8. Multi-Machine Sync Strategies

### Scenario

- **Laptop**: Mobile, on/off, used for starting work
- **Remote machine**: Always-on, used for long-running jobs
- **Goal**: Start work on laptop, hand over to remote machine

### Architecture Recommendation

**Single Gateway on Remote Machine**:
```
┌─────────────────────────────────────────────────┐
│           Remote Machine (Always-On)            │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │        OpenClaw Gateway                 │    │
│  │  - Channels (WhatsApp, Telegram, etc.)  │    │
│  │  - Sessions & Memory                    │    │
│  │  - Skills & Workspace                   │    │
│  │  - Cron & Heartbeat                     │    │
│  └─────────────────────────────────────────┘    │
│                      │                          │
│            Tailscale Serve / SSH                │
└──────────────────────┼──────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       v               v               v
   ┌───────┐      ┌───────┐      ┌───────┐
   │Laptop │      │ Phone │      │ WebUI │
   │ (CLI) │      │(WhatsApp)│   │       │
   └───────┘      └───────┘      └───────┘
```

**Why Single Gateway**:
- One source of truth for sessions and memory
- No sync conflicts
- Always-on for heartbeat and cron
- Laptop connects as client, not separate instance

### Remote Access Methods

**1. Tailscale Serve (Recommended)**
```json
{
  "gateway": {
    "bind": "loopback",
    "tailscale": {
      "mode": "serve"  // tailnet-only HTTPS
    }
  }
}
```
- No public exposure
- Automatic HTTPS via Tailscale
- Identity headers for auth

**2. SSH Tunnel**
```bash
# From laptop
ssh -N -L 18789:127.0.0.1:18789 user@remote-host
# Now localhost:18789 reaches remote Gateway
```

**3. Tailscale Funnel** (public access)
```json
{
  "gateway": {
    "bind": "loopback",
    "tailscale": {
      "mode": "funnel"
    },
    "auth": {
      "mode": "password"  // Required for Funnel
    }
  }
}
```

### File Sync Options

For workspace files (`~/.openclaw/workspace`) between machines:

**Option 1: Git (Best for Code/Skills)**
- Version controlled
- Conflict resolution
- Manual push/pull
- Good for: Skills, AGENTS.md, SOUL.md, TOOLS.md
```bash
cd ~/.openclaw/workspace
git init
git remote add origin <repo>
# Sync manually or via cron
```

**Option 2: Syncthing (Best for Real-Time)**
- Open source, peer-to-peer
- Real-time bidirectional sync
- No cloud dependency
- Good for: Workspace files, memory
- Limitation: Conflict handling can be tricky with rapid edits

**Option 3: Dropbox/OneDrive**
- Fast sync, good conflict handling
- Cloud dependency
- May have issues with `~/.openclaw` hidden folder paths
- Symlink workaround:
```bash
ln -s ~/Dropbox/openclaw-workspace ~/.openclaw/workspace
```

**Option 4: rsync + cron (Simple)**
```bash
# Push to remote
rsync -avz ~/.openclaw/workspace/ user@remote:~/.openclaw/workspace/

# Pull from remote
rsync -avz user@remote:~/.openclaw/workspace/ ~/.openclaw/workspace/
```

### Recommended Strategy

**For your scenario (laptop + always-on remote)**:

1. **Run Gateway only on remote machine**
   - All channels, sessions, memory on remote
   - Heartbeat runs 24/7

2. **Use Tailscale for access**
   - Laptop joins same tailnet
   - Access via `tailscale serve` URL or SSH

3. **Git for skills/workspace**
   - Version control for SKILL.md files
   - Push from laptop when done editing
   - Pull on remote (or use webhook trigger)

4. **Syncthing for hot files** (optional)
   - Real-time sync for files you're actively editing
   - Bidirectional between laptop and remote

### Task Handover Pattern

**Start on laptop**:
```bash
# Connect to remote gateway
ssh -N -L 18789:127.0.0.1:18789 user@remote &

# Send task
openclaw agent --message "Research OpenClaw integration options" --thinking high
```

**Monitor from anywhere** (WhatsApp, Telegram, WebChat):
- Agent runs on remote
- Responds via your configured channels
- Laptop can disconnect

**Check results**:
```bash
openclaw status --deep
openclaw sessions history main
```

### Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Session state sync | Single Gateway - no sync needed |
| Skill conflicts | Git with proper merge strategy |
| Memory conflicts | Single Gateway owns memory |
| Credentials sync | Don't sync - keep on Gateway host |
| Cost monitoring | Provider-level alerts, single billing point |
| Network reliability | Tailscale mesh survives outages |
| Laptop offline | Gateway continues, laptop reconnects |

## 9. Limitations and Known Issues

### Platform Limitations

- **No native Windows**: Requires WSL2
- **iMessage**: Requires macOS or BlueBubbles server
- **WhatsApp**: Uses unofficial Baileys library (could break)
- **Local models**: Need 64K+ context, 32B+ params, 24GB+ VRAM for reliable operation

### Security Concerns

- Young project with rapid development
- CVE history (cross-site WebSocket hijacking)
- Skills ecosystem has malware risk (26% vulnerability rate in audit)
- Autonomous operation can take unexpected actions

### Operational Considerations

- API costs can escalate quickly with frequent heartbeats
- Heartbeat loop may act without explicit permission
- No undo for autonomous actions
- Sandbox mode adds latency (Docker spin-up)

### Community Notes

- `[COMMUNITY]` Skills need manual auditing before use
- `[COMMUNITY]` WhatsApp link may need re-auth periodically
- `[COMMUNITY]` Large context windows can cause slow responses
- `[COMMUNITY]` Some channels have rate limits (Discord, Telegram)

## 10. Sources

### Official Sources

- **OCLAW-SC-GH-README**: https://github.com/openclaw/openclaw (Accessed: 2026-02-27)
- **OCLAW-SC-DOCS-WIN**: https://docs.openclaw.ai/platforms/windows (Accessed: 2026-02-27)
- **OCLAW-SC-DOCS-REMOTE**: https://docs.openclaw.ai/gateway/remote (Accessed: 2026-02-27)
- **OCLAW-SC-DOCS-SKILLS**: https://docs.openclaw.ai/tools/skills (Accessed: 2026-02-27)
- **OCLAW-SC-OFFICIAL**: https://openclaw.ai/ (Accessed: 2026-02-27)

### Community Sources

- **OCLAW-SC-MILVUS-GUIDE**: https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md (Accessed: 2026-02-27)
- **OCLAW-SC-GH-MCP**: https://github.com/freema/openclaw-mcp (Accessed: 2026-02-27)
- **OCLAW-SC-WIKI**: https://en.wikipedia.org/wiki/OpenClaw (Accessed: 2026-02-27)

### Related Projects

- **ClawHub**: https://clawhub.com - Skills registry
- **openclaw-mcp**: https://github.com/freema/openclaw-mcp - MCP bridge for Claude.ai
- **Moltbook**: https://moltbook.com - AI agent social network (demonstration)

## Document History

**[2026-02-27 14:50]**
- Initial research and document creation
- Covered all 6 user questions (OCLAW-PR-001 through OCLAW-PR-006)
- Sources: 8 primary, multiple community references
