# INFO: OpenClaw Skills Reference

**Doc ID**: OCLAW-IN04
**Goal**: Comprehensive reference for all bundled OpenClaw skills - descriptions, costs, use cases, and example prompts
**Created**: 2026-03-01

## Summary

This document covers the 27 skills shown during OpenClaw onboarding. Each skill entry includes:
- Description and purpose
- API keys or subscriptions required
- Platform requirements
- Use cases
- 10+ example prompts

**Cost Legend:**
- **FREE** - No API key or subscription required
- **FREEMIUM** - Free tier available, paid for higher usage
- **PAID** - Requires paid subscription or API key
- **OAUTH** - Requires OAuth authorization (free but needs account)

## Table of Contents

1. [1password](#1-1password)
2. [blogwatcher](#2-blogwatcher)
3. [blucli](#3-blucli)
4. [camsnap](#4-camsnap)
5. [clawhub](#5-clawhub)
6. [eightctl](#6-eightctl)
7. [gemini](#7-gemini)
8. [gifgrep](#8-gifgrep)
9. [github](#9-github)
10. [gog](#10-gog)
11. [goplaces](#11-goplaces)
12. [himalaya](#12-himalaya)
13. [mcporter](#13-mcporter)
14. [nano-banana-pro](#14-nano-banana-pro)
15. [nano-pdf](#15-nano-pdf)
16. [obsidian](#16-obsidian)
17. [openai-whisper](#17-openai-whisper)
18. [openhue](#18-openhue)
19. [oracle](#19-oracle)
20. [ordercli](#20-ordercli)
21. [sag](#21-sag)
22. [songsee](#22-songsee)
23. [sonoscli](#23-sonoscli)
24. [summarize](#24-summarize)
25. [video-frames](#25-video-frames)
26. [wacli](#26-wacli)
27. [xurl](#27-xurl)

---

## 1. 1password

**Description**: Access and manage 1Password vault entries. Look up passwords, auto-login, fill forms.

**Cost**: PAID (requires 1Password subscription)
**API Key**: 1Password Connect API or CLI authentication
**Platform**: All (requires 1Password CLI `op`)

**Security Warning**: All-or-nothing access to entire vault. Cannot limit to specific entries.

**Use Cases**:
- Look up credentials for services
- Auto-fill login forms
- Generate new passwords
- Share credentials securely

**Example Prompts**:
1. "What's my password for AWS Console?"
2. "Log me into my DigitalOcean account"
3. "Generate a new secure password for my Netflix account"
4. "Show me all my saved logins for google.com"
5. "Update my GitHub password to this new one"
6. "What credit card do I have saved for Amazon?"
7. "Copy my SSH key for the production server"
8. "Find all logins that haven't been updated in 2 years"
9. "What's the 2FA recovery code for my Coinbase account?"
10. "Create a new login entry for this new service I signed up for"
11. "Share my Netflix password with the family vault"
12. "Check which passwords are weak or reused"

---

## 2. blogwatcher

**Description**: Monitor blogs and RSS/Atom feeds for updates. Get notified when new posts appear.

**Cost**: FREE
**API Key**: None required
**Platform**: All

**Use Cases**:
- Track competitor blogs
- Monitor tech news feeds
- Get alerts for new releases
- Research aggregation

**Example Prompts**:
1. "Watch the OpenAI blog for new announcements"
2. "Add this RSS feed to my watchlist: [URL]"
3. "What new posts appeared on Hacker News today?"
4. "Check if there are any new posts on the Anthropic blog"
5. "List all blogs I'm currently watching"
6. "Remove the TechCrunch feed from my watchlist"
7. "Summarize new posts from all my watched feeds"
8. "Alert me when Simon Willison posts something new"
9. "Find RSS feeds for these 5 AI research labs"
10. "What did the Tailscale blog post about this week?"
11. "Check for new releases on the Next.js changelog"
12. "Monitor this GitHub releases page for updates"

---

## 3. blucli

**Description**: Control Bluetooth devices and connections via CLI.

**Cost**: FREE
**API Key**: None required
**Platform**: macOS, Linux (limited Windows support)

**Use Cases**:
- Connect/disconnect Bluetooth headphones
- Manage paired devices
- Audio routing automation

**Example Prompts**:
1. "Connect to my AirPods"
2. "List all paired Bluetooth devices"
3. "Disconnect from the current Bluetooth speaker"
4. "Switch audio output to my Sony headphones"
5. "Is my keyboard connected via Bluetooth?"
6. "Pair with this new Bluetooth device"
7. "Forget the old Bluetooth speaker I no longer use"
8. "Check battery level of my Bluetooth headphones"
9. "Connect to my car's Bluetooth when I say 'driving mode'"
10. "Why isn't my Bluetooth mouse connecting?"
11. "Turn off Bluetooth completely"
12. "Scan for nearby Bluetooth devices"

---

## 4. camsnap

**Description**: Capture frames or clips from RTSP/ONVIF cameras (security cameras, IP cameras).

**Cost**: FREE
**API Key**: None required (needs camera credentials)
**Platform**: macOS primarily, limited other OS support

**Use Cases**:
- Security camera snapshots
- Time-lapse creation
- Motion detection alerts
- Remote monitoring

**Example Prompts**:
1. "Take a snapshot from the front door camera"
2. "Show me what the backyard camera sees right now"
3. "Record a 30-second clip from the garage camera"
4. "Is anyone at the front door?"
5. "Take snapshots from all cameras"
6. "Set up motion alerts for the driveway camera"
7. "What happened on the porch camera at 3pm?"
8. "Create a time-lapse from the garden camera today"
9. "Check if the package was delivered (front camera)"
10. "List all configured cameras"
11. "Add my new Wyze camera to the system"
12. "Compare current view with yesterday at same time"

---

## 5. clawhub

**Description**: Search, install, update, and publish agent skills from ClawHub marketplace.

**Cost**: FREE
**API Key**: None for browsing/installing; ClawHub account for publishing
**Platform**: All

**Use Cases**:
- Discover new skills
- Install community skills
- Update installed skills
- Publish your own skills

**Example Prompts**:
1. "Search ClawHub for PDF-related skills"
2. "Install the weather skill"
3. "Update all my installed skills"
4. "What are the most popular skills on ClawHub?"
5. "Uninstall the food-order skill"
6. "Show me skills for home automation"
7. "Publish my custom skill to ClawHub"
8. "Find skills that work with Notion"
9. "What new skills were added this week?"
10. "Check if there's an update for the github skill"
11. "List all skills I have installed"
12. "Find skills for transcription and audio processing"

---

## 6. eightctl

**Description**: Control Eight Sleep smart mattress - temperature, schedules, sleep tracking.

**Cost**: FREE (requires Eight Sleep mattress + subscription)
**API Key**: Eight Sleep account credentials
**Platform**: All

**Use Cases**:
- Adjust bed temperature
- View sleep scores
- Set sleep schedules
- Automate bed warming

**Example Prompts**:
1. "Set my side of the bed to -2 cooling"
2. "Warm up the bed, I'm going to sleep soon"
3. "What was my sleep score last night?"
4. "Show my sleep trends for the past week"
5. "Turn off the bed heating"
6. "Set the bed to warm at 10pm and cool at 2am"
7. "How many hours did I sleep?"
8. "Compare my sleep this week vs last week"
9. "Set both sides of the bed to neutral"
10. "What's the current bed temperature?"
11. "Enable the alarm vibration for 7am"
12. "Show my heart rate variability from last night"

---

## 7. gemini

**Description**: Use Google Gemini AI models for tasks, analysis, and generation.

**Cost**: FREEMIUM (free tier available, paid for high usage)
**API Key**: `GEMINI_API_KEY` or `GOOGLE_API_KEY`
**Platform**: All

**Use Cases**:
- Alternative AI model for specific tasks
- Multimodal analysis (images, video)
- Long context processing
- Code generation

**Example Prompts**:
1. "Use Gemini to analyze this image"
2. "Ask Gemini to summarize this long document"
3. "Have Gemini review my code for security issues"
4. "Use Gemini Flash for this quick translation"
5. "Process this video with Gemini and describe what happens"
6. "Compare Claude's answer with Gemini's on this question"
7. "Use Gemini Pro for this complex reasoning task"
8. "Generate code using Gemini instead of Claude"
9. "Analyze this chart image with Gemini"
10. "Use Gemini for this 1 million token context task"
11. "Have Gemini transcribe this audio file"
12. "Ask Gemini about recent events (grounded search)"

---

## 8. gifgrep

**Description**: Search and find GIFs by description or keyword.

**Cost**: FREE
**API Key**: Optional (Giphy/Tenor API for better results)
**Platform**: All

**Use Cases**:
- Find reaction GIFs
- Add humor to messages
- Create presentations
- Social media content

**Example Prompts**:
1. "Find a GIF of someone facepalming"
2. "Get me a celebration GIF"
3. "Find a 'mind blown' reaction GIF"
4. "Search for cat GIFs"
5. "Find a GIF that says 'thank you'"
6. "Get a GIF of The Office 'that's what she said'"
7. "Find an 'awkward' reaction GIF"
8. "Search for a 'working hard' GIF"
9. "Get a 'Friday mood' GIF"
10. "Find a GIF of someone slow clapping"
11. "Search for 'confused math' meme GIF"
12. "Get a 'mic drop' GIF"

---

## 9. github

**Description**: Full GitHub operations via `gh` CLI - repos, PRs, issues, actions, releases.

**Cost**: FREE (GitHub account required)
**API Key**: OAuth via `gh auth login`
**Platform**: All

**Use Cases**:
- Manage repositories
- Review and merge PRs
- Track issues
- Monitor CI/CD pipelines
- Release management

**Example Prompts**:
1. "Show my open pull requests"
2. "What failed in the latest CI build?"
3. "Create a new issue: 'Fix login bug on mobile'"
4. "Merge PR #42 after checks pass"
5. "List recent commits on main branch"
6. "Who's assigned to issue #15?"
7. "Create a new release v2.1.0 with these notes"
8. "Clone this repository to my projects folder"
9. "Show all repos I've starred recently"
10. "What PRs need my review?"
11. "Check the status of GitHub Actions for this repo"
12. "Fork this repository to my account"
13. "Close all issues labeled 'wontfix'"
14. "Show diff between main and feature branch"

---

## 10. gog

**Description**: Google Workspace integration - Gmail, Calendar, Drive, Contacts, Tasks, Sheets, Docs.

**Cost**: FREE (Google account required)
**API Key**: OAuth via `gog auth`
**Platform**: All

**Security Note**: Full access to your Google account data. Consider using a dedicated Google account.

**Use Cases**:
- Email management
- Calendar scheduling
- File organization
- Task tracking
- Spreadsheet automation

**Example Prompts**:
1. "Check my Gmail for unread messages"
2. "What meetings do I have today?"
3. "Send an email to john@example.com about the project update"
4. "Create a calendar event for tomorrow at 2pm"
5. "Find the document I was working on yesterday"
6. "Add a task: 'Review quarterly report'"
7. "Upload this file to my Google Drive"
8. "Who's invited to the meeting at 3pm?"
9. "Search my emails for invoices from last month"
10. "Create a new Google Sheet for expense tracking"
11. "Share this document with my team"
12. "Cancel my 4pm meeting and notify attendees"
13. "What's on my calendar for next week?"
14. "Mark all promotional emails as read"

---

## 11. goplaces

**Description**: Search for places, businesses, and locations using Google Places API.

**Cost**: FREEMIUM (Google Cloud free tier, then pay-per-use)
**API Key**: `GOOGLE_PLACES_API_KEY`
**Platform**: All

**Use Cases**:
- Find nearby restaurants
- Business information lookup
- Travel planning
- Location research

**Example Prompts**:
1. "Find Italian restaurants near me"
2. "What's the best-rated coffee shop within walking distance?"
3. "Is the Apple Store open right now?"
4. "Find pharmacies open 24 hours"
5. "What's the phone number for that Thai place on Main St?"
6. "Find hotels near the airport"
7. "Are there any coworking spaces nearby?"
8. "What are the hours for the DMV?"
9. "Find gas stations along my route to Portland"
10. "What's the address of the nearest FedEx?"
11. "Find vegan restaurants with good reviews"
12. "What gyms are open at 6am near my office?"

---

## 12. himalaya

**Description**: Email via IMAP/SMTP - send, receive, search emails across any email provider.

**Cost**: FREE
**API Key**: IMAP/SMTP credentials for your email account
**Platform**: All

**Use Cases**:
- Email for non-Google accounts
- Corporate email access
- Multi-account email management
- Email automation

**Example Prompts**:
1. "Check my work email for new messages"
2. "Send an email from my Outlook account"
3. "Search my iCloud mail for receipts"
4. "List unread emails in my work inbox"
5. "Reply to the latest email from my boss"
6. "Move this email to the Archive folder"
7. "Delete all emails from this sender"
8. "Forward this email to my personal account"
9. "Mark this thread as important"
10. "Search for emails with attachments from last week"
11. "What emails did I send yesterday?"
12. "Create a draft reply to this message"

---

## 13. mcporter

**Description**: MCP (Model Context Protocol) server integration - connect to external MCP servers.

**Cost**: FREE
**API Key**: Depends on MCP server being connected
**Platform**: All

**Use Cases**:
- Connect to custom MCP servers
- Extend OpenClaw with MCP tools
- Bridge different AI systems
- Custom integrations

**Example Prompts**:
1. "Connect to the MCP server at localhost:3000"
2. "List available MCP tools"
3. "Call the weather tool from MCP"
4. "Disconnect from the current MCP server"
5. "What MCP servers are currently connected?"
6. "Add a new MCP server configuration"
7. "Test the connection to my custom MCP"
8. "List resources from the Notion MCP server"
9. "Call the database query tool via MCP"
10. "Show MCP server logs"
11. "Refresh the MCP tool list"
12. "Configure authentication for this MCP server"

---

## 14. nano-banana-pro

**Description**: Image generation and manipulation using Banana.dev or similar GPU services.

**Cost**: PAID (Banana.dev credits or similar)
**API Key**: `BANANA_API_KEY`
**Platform**: All

**Use Cases**:
- AI image generation
- Image editing
- Style transfer
- Background removal

**Example Prompts**:
1. "Generate an image of a futuristic cityscape"
2. "Create a logo for my new startup"
3. "Generate a profile picture in anime style"
4. "Create an illustration for my blog post"
5. "Generate variations of this image"
6. "Remove the background from this photo"
7. "Create an image in the style of Van Gogh"
8. "Generate a product mockup"
9. "Create a thumbnail for my YouTube video"
10. "Generate an abstract art piece with blue tones"
11. "Create a cartoon version of this photo"
12. "Generate a book cover design"

---

## 15. nano-pdf

**Description**: Edit PDFs with natural language - extract, merge, split, watermark.

**Cost**: FREE
**API Key**: None required
**Platform**: All (requires `nano-pdf` CLI)

**Use Cases**:
- Extract pages from PDFs
- Merge multiple PDFs
- Add watermarks
- Convert formats

**Example Prompts**:
1. "Extract pages 5-10 from this PDF"
2. "Merge these three PDFs into one"
3. "Remove page 3 from this document"
4. "Add a watermark to all pages"
5. "Split this PDF into individual pages"
6. "Rotate page 2 by 90 degrees"
7. "Compress this PDF to reduce file size"
8. "Extract all images from this PDF"
9. "Add page numbers to this document"
10. "Convert this PDF to images"
11. "Encrypt this PDF with a password"
12. "Remove the password from this PDF"
13. "Combine the first page of each PDF in this folder"

---

## 16. obsidian

**Description**: Manage Obsidian vault - create, edit, search, and link notes.

**Cost**: FREE
**API Key**: None (local file access)
**Platform**: All (Obsidian must be installed, vault accessible)

**Use Cases**:
- Note-taking automation
- Knowledge base management
- Daily notes
- Research organization

**Example Prompts**:
1. "Create a new note about today's meeting"
2. "Search my vault for notes about Python"
3. "Add a link to this note from my project page"
4. "What did I write about React last month?"
5. "Create a daily note for today"
6. "List all notes tagged #project"
7. "Find notes that mention 'machine learning'"
8. "Update my reading list note"
9. "Create a new folder for this project"
10. "Show me recent notes I've edited"
11. "Add this quote to my quotes collection"
12. "Find orphan notes with no backlinks"
13. "Generate a summary of my weekly notes"

---

## 17. openai-whisper

**Description**: Audio transcription using OpenAI Whisper (local or API).

**Cost**: FREE (local) or PAID (OpenAI API)
**API Key**: `OPENAI_API_KEY` for API version; none for local
**Platform**: All (local requires GPU for speed)

**Use Cases**:
- Meeting transcription
- Podcast transcripts
- Voice memos to text
- Video subtitles

**Example Prompts**:
1. "Transcribe this audio file"
2. "Convert this voice memo to text"
3. "Generate subtitles for this video"
4. "Transcribe my meeting recording"
5. "What did they say in this podcast episode?"
6. "Transcribe and translate this Spanish audio"
7. "Create a transcript with timestamps"
8. "Transcribe only the first 5 minutes"
9. "Who are the speakers in this recording?"
10. "Convert this interview to text"
11. "Transcribe and summarize this lecture"
12. "Extract action items from this meeting audio"

---

## 18. openhue

**Description**: Control Philips Hue smart lights - colors, scenes, schedules.

**Cost**: FREE (requires Philips Hue bridge + lights)
**API Key**: Hue Bridge API key (auto-discovered)
**Platform**: All (must be on same network as bridge)

**Use Cases**:
- Smart lighting control
- Mood/scene setting
- Automation routines
- Wake-up lights

**Example Prompts**:
1. "Turn on the living room lights"
2. "Set bedroom lights to 50% brightness"
3. "Change office lights to blue"
4. "Activate the 'Movie Night' scene"
5. "Turn off all lights in the house"
6. "Dim the dining room lights"
7. "Set lights to warm white"
8. "Blink the lights three times"
9. "What lights are currently on?"
10. "Schedule lights to turn on at sunset"
11. "Set up a wake-up routine for 7am"
12. "Create a new scene called 'Focus Mode'"

---

## 19. oracle

**Description**: Query Oracle databases and run SQL commands.

**Cost**: FREE
**API Key**: Oracle database connection string
**Platform**: All (requires Oracle client)

**Use Cases**:
- Database queries
- Data analysis
- Report generation
- Database administration

**Example Prompts**:
1. "Show me the top 10 customers by revenue"
2. "How many orders were placed today?"
3. "Run this SQL query on the production database"
4. "List all tables in the schema"
5. "Export this query result to CSV"
6. "What's the average order value this month?"
7. "Find duplicate entries in the users table"
8. "Show database connection status"
9. "Describe the structure of the orders table"
10. "Count active subscriptions by plan type"
11. "Find records modified in the last hour"
12. "Generate a monthly sales report"

---

## 20. ordercli

**Description**: Food delivery ordering automation (various platforms).

**Cost**: FREE (requires accounts on delivery platforms)
**API Key**: Platform-specific authentication
**Platform**: Limited platform support

**Use Cases**:
- Quick food ordering
- Reorder favorites
- Track deliveries
- Compare prices

**Example Prompts**:
1. "Order my usual from Chipotle"
2. "Reorder my last Uber Eats order"
3. "What's the delivery time for pizza from Domino's?"
4. "Find the cheapest option for Thai food delivery"
5. "Track my current food order"
6. "Order coffee from Starbucks for pickup"
7. "What are today's deals on DoorDash?"
8. "Cancel my pending order"
9. "Add extra napkins to my order"
10. "Schedule lunch delivery for 12:30pm"
11. "What restaurants deliver to my location?"
12. "Show my order history"

---

## 21. sag

**Description**: Semantic search and retrieval over local files using embeddings.

**Cost**: FREE (local) or PAID (if using external embedding API)
**API Key**: Optional (OpenAI for better embeddings)
**Platform**: All

**Use Cases**:
- Search across documents
- Find related content
- Knowledge retrieval
- Research assistance

**Example Prompts**:
1. "Find documents related to 'machine learning deployment'"
2. "Search my notes for anything about AWS Lambda"
3. "What did I write about authentication?"
4. "Find similar documents to this one"
5. "Index this folder for semantic search"
6. "Search across all my markdown files"
7. "Find code examples for API integration"
8. "What documents mention this project?"
9. "Search for meeting notes about budget"
10. "Find relevant context for this topic"
11. "Re-index my documents after changes"
12. "Search with natural language: 'how to configure nginx'"

---

## 22. songsee

**Description**: Identify songs playing nearby or from audio files (like Shazam).

**Cost**: FREE
**API Key**: Optional (ACRCloud for better accuracy)
**Platform**: macOS primarily (needs microphone access)

**Use Cases**:
- Identify playing songs
- Music discovery
- Create playlists from identified songs
- Tag audio files

**Example Prompts**:
1. "What song is playing right now?"
2. "Identify this audio file"
3. "Shazam this song"
4. "What's the name of this track?"
5. "Listen and tell me what's playing"
6. "Identify the background music in this video"
7. "What song was that?"
8. "Find the artist for this song"
9. "Add this song to my Spotify playlist"
10. "Get lyrics for the song that's playing"
11. "What album is this song from?"
12. "Identify songs in this podcast episode"

---

## 23. sonoscli

**Description**: Control Sonos speakers - playback, volume, grouping, playlists.

**Cost**: FREE (requires Sonos speakers)
**API Key**: None (auto-discovered on network)
**Platform**: All (must be on same network)

**Use Cases**:
- Music playback control
- Multi-room audio
- Speaker grouping
- Playlist management

**Example Prompts**:
1. "Play music in the living room"
2. "Set volume to 50% on all speakers"
3. "Pause playback"
4. "Skip to the next track"
5. "Group all speakers together"
6. "Play my morning playlist"
7. "What's currently playing?"
8. "Ungroup the bedroom speaker"
9. "Play this podcast episode"
10. "Set a sleep timer for 30 minutes"
11. "List all Sonos speakers"
12. "Play jazz in the kitchen at low volume"

---

## 24. summarize

**Description**: Summarize text, documents, articles, and web pages.

**Cost**: FREE
**API Key**: None (uses current LLM)
**Platform**: All

**Use Cases**:
- Document summarization
- Article digests
- Meeting notes
- Research summaries

**Example Prompts**:
1. "Summarize this article"
2. "Give me the key points from this document"
3. "TL;DR this email thread"
4. "Summarize this PDF in 3 bullet points"
5. "What's the main argument of this paper?"
6. "Create an executive summary of this report"
7. "Summarize today's news about AI"
8. "Condense this meeting transcript"
9. "What are the action items from this document?"
10. "Summarize this book chapter"
11. "Give me a one-paragraph summary"
12. "Summarize and highlight key decisions"

---

## 25. video-frames

**Description**: Extract frames from videos for analysis or processing.

**Cost**: FREE
**API Key**: None
**Platform**: macOS primarily (requires ffmpeg)

**Use Cases**:
- Video analysis
- Thumbnail generation
- Frame extraction
- Motion detection

**Example Prompts**:
1. "Extract a frame at 1:30 from this video"
2. "Get 10 evenly-spaced frames from this video"
3. "Create a thumbnail from this video"
4. "Extract frames where there's motion"
5. "Get all frames from seconds 10-15"
6. "Create a contact sheet of this video"
7. "Extract the best frame for a thumbnail"
8. "Get frames at 1 FPS for the whole video"
9. "Find frames with faces in this video"
10. "Extract the first and last frame"
11. "Create a GIF from these frames"
12. "Analyze frames for scene changes"

---

## 26. wacli

**Description**: WhatsApp automation - search messages, manage conversations, sync history.

**Cost**: FREE
**API Key**: None (WhatsApp Web authentication)
**Platform**: All

**Security Note**: Full access to WhatsApp message history. Different from the `message` tool which only sends.

**Use Cases**:
- Search chat history
- Export conversations
- Contact management
- Message analytics

**Example Prompts**:
1. "Search my WhatsApp for messages about the meeting"
2. "What did John say last week?"
3. "Export my conversation with Mom"
4. "Find all messages with links"
5. "When did I last message this person?"
6. "Search for photos shared in this group"
7. "List my most active chats"
8. "Find messages from this date range"
9. "What voice notes did I receive?"
10. "Search for messages containing 'payment'"
11. "Show unread message count per chat"
12. "Find all forwarded messages"

---

## 27. xurl

**Description**: Advanced web fetching - extract content, handle JavaScript, bypass blocks.

**Cost**: FREE
**API Key**: Optional (proxy services for better access)
**Platform**: All

**Use Cases**:
- Web scraping
- Content extraction
- Research automation
- Data collection

**Example Prompts**:
1. "Fetch the main content from this URL"
2. "Extract all links from this page"
3. "Get the article text without ads"
4. "Download this webpage as markdown"
5. "Fetch this JavaScript-rendered page"
6. "Extract product info from this Amazon page"
7. "Get all images from this article"
8. "Fetch and parse this JSON API"
9. "Download the table data from this page"
10. "Extract the author and date from this article"
11. "Fetch multiple pages from this site"
12. "Get the raw HTML of this page"

---

## Windows Compatibility Guide [VERIFIED]

### Problem: Many Skills Need macOS/Linux Tools

Most bundled skills rely on CLI tools installed via:
- **Homebrew** (macOS/Linux only): gog, gemini, goplaces, openai-whisper, video-frames, nano-banana-pro
- **Go**: wacli, blogwatcher

These won't work on native Windows.

### Solutions for Windows Users

**Option 1: Use WSL2** (Recommended)
Install skills in WSL2 Ubuntu where Homebrew/Go work. OpenClaw gateway runs in WSL, accessible from Windows.

**Option 2: Community Skills via ClawHub**
Several community skills work on Windows using pure Node.js or PowerShell.

**Option 3: Direct API Integration**
Use built-in tools (`web_fetch`, `exec`) to call APIs directly without skill dependencies.

### Windows-Compatible Skills for Enterprise Services

#### Microsoft 365 / Outlook

**outlook** (Community Skill)
- **Source**: `clawhub install jotamed/outlook`
- **Platform**: Windows, macOS, Linux
- **Requirements**: Azure CLI, Azure App Registration
- **Features**: Mail, Calendar via Microsoft Graph API
- **Setup**: Automated script creates Azure app registration

```powershell
# Install
clawhub install jotamed/outlook
# Setup (requires Azure CLI)
./scripts/outlook-setup.sh
```

**Example Prompts**:
1. "Check my Outlook inbox for unread messages"
2. "Send an email to john@company.com about the meeting"
3. "What's on my Outlook calendar today?"
4. "Create a meeting for tomorrow at 2pm"
5. "Search my emails for invoices"
6. "Reply to the latest email from my boss"
7. "Show my calendar for next week"
8. "Flag this email as important"
9. "Delete all emails from this newsletter"
10. "Schedule a Teams meeting for Friday"

**Status**: Native M365 skill (like gog for Google) is a requested feature (#30023) but not yet available.

#### Azure

**agent-framework-azure-ai-py** (Community)
- **Source**: `clawhub install thegovind/agent-framework-azure-ai-py`
- **Platform**: Windows, macOS, Linux
- **Requirements**: Azure subscription, Python
- **Features**: Build Azure AI Foundry agents

**agentic-devops** (Community)
- **Source**: `clawhub install tkuehnl/agentic-devops`
- **Platform**: Windows, macOS, Linux
- **Features**: Docker, process management, log analysis, health monitoring

#### Google Services (Windows Workarounds)

**Without gog skill, use built-in tools:**

```
# Use web_fetch for Google APIs directly
"Fetch my Google Calendar events using the Calendar API"
"Use web_fetch to check Gmail via API"
```

**Or install Go on Windows:**
```powershell
winget install GoLang.Go
# Then install gog CLI manually
go install github.com/openclaw/gog@latest
```

**Gemini on Windows:**
Configure as model provider in `openclaw.json` instead of using the skill:
```json
{
  "models": {
    "providers": {
      "google": {
        "apiKey": "${GEMINI_API_KEY}"
      }
    }
  },
  "agent": {
    "model": "google/gemini-2.0-flash"
  }
}
```

### Windows-Native Skills Summary

| Skill | Windows | Requires | Purpose |
|-------|---------|----------|---------|
| clawhub | ✅ | npm | Skill marketplace |
| github | ✅ | gh CLI | GitHub operations |
| summarize | ✅ | None | Text summarization |
| xurl | ✅ | None | Web fetching |
| nano-pdf | ✅ | nano-pdf CLI | PDF editing |
| outlook | ✅ | Azure CLI | M365 email/calendar |
| 1password | ✅ | op CLI | Password vault |
| obsidian | ✅ | Obsidian | Note-taking |
| oracle | ✅ | Oracle client | Database |
| mcporter | ✅ | None | MCP integration |
| sag | ✅ | None | Semantic search |

### Skills That Need WSL2 on Windows

| Skill | Reason | Alternative |
|-------|--------|-------------|
| gog | Needs Homebrew | Install Go, build manually |
| gemini | Needs Homebrew | Configure as model provider |
| goplaces | Needs Homebrew | Use web_fetch + Google Places API |
| openai-whisper | Needs Homebrew | Use OpenAI Whisper API directly |
| video-frames | Needs ffmpeg via brew | Install ffmpeg via winget |
| wacli | Needs Go | Install Go on Windows |
| blogwatcher | Needs Go | Install Go on Windows |

### Installing Go on Windows (for wacli, blogwatcher)

```powershell
winget install GoLang.Go
# Restart terminal, then:
go install github.com/openclaw/wacli@latest
go install github.com/openclaw/blogwatcher@latest
```

### Installing ffmpeg on Windows (for video-frames)

```powershell
winget install Gyan.FFmpeg
# Restart terminal, video-frames should work
```

**Sources**:
- [VERIFIED] (OCLAW-SC-GHUB-M365 | https://github.com/openclaw/openclaw/issues/30023)
- [VERIFIED] (OCLAW-SC-LOBE-OUTL | https://lobehub.com/skills/openclaw-skills-outlook)
- [VERIFIED] (OCLAW-SC-GHUB-AWSK | https://github.com/VoltAgent/awesome-openclaw-skills)

## Recommendations by Use Case

### Essential for Everyone
- **clawhub** - Manage skills
- **summarize** - Universal utility
- **xurl** - Web content fetching

### For Google Users
- **gog** - Full Google Workspace
- **gemini** - Google AI models
- **goplaces** - Location search

### For Developers
- **github** - Repository management
- **sag** - Code search
- **mcporter** - MCP integration

### For Content Creators
- **openai-whisper** - Transcription
- **nano-pdf** - PDF editing
- **video-frames** - Video processing

### For Smart Home
- **openhue** - Philips Hue
- **sonoscli** - Sonos speakers
- **eightctl** - Eight Sleep

### For Productivity
- **obsidian** - Note-taking
- **blogwatcher** - Feed monitoring
- **himalaya** - Email (non-Google)

---

## Sources

- [VERIFIED] (OCLAW-SC-YUWH-GUIDE | https://yu-wenhao.com/en/blog/openclaw-tools-skills-tutorial/)
- [VERIFIED] (OCLAW-SC-DOCS-SKILLS | https://docs.openclaw.ai/skills)
- [VERIFIED] (OCLAW-SC-CLWHB-MAIN | https://clawhub.ai/skills)
- [COMMUNITY] (OCLAW-SC-GHUB-AWSKL | https://github.com/VoltAgent/awesome-openclaw-skills)

## Document History

**[2026-03-01 15:50]**
- Initial document created with 27 skills
- Each skill includes description, cost, API requirements, use cases, and 10+ example prompts
