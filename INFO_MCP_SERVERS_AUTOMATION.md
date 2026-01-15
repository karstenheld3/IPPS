# INFO: MCP (Model Context Protocol) Servers for Programming and Process Automation

**Doc ID**: MCPS-IN01
**Goal**: Comprehensive reference of MCP servers for programmers and automation engineers
**Timeline**: Created 2026-01-15, Updated 2 times (2026-01-15)

## Summary

- **Document Reading**: pdf-reader-mcp (production-ready), Pandoc MCP (format conversion), Office-Word-MCP-Server (DOCX) [VERIFIED]
- **File System**: Official @modelcontextprotocol/server-filesystem with sandboxed directory access [VERIFIED]
- **Browser - Playwright**: microsoft/playwright-mcp (accessibility tree), Playwriter (Chrome extension for logged-in sessions) [VERIFIED]
- **Browser - Alternatives**: Browserbase+Stagehand (cloud), mcp-selenium (WebDriver), Puppeteer MCP [VERIFIED]
- **Code Testing**: mcp-test-runner supports Pytest, Jest, Bats, Flutter, Go, Rust [VERIFIED]
- **Local LLMs (Large Language Models)**: ollama-mcp-bridge enables Ollama models to use MCP tools [VERIFIED]
- **Vision/AI Models**: Vision MCP Server, mcp-image-recognition, Grok Vision OCR (Optical Character Recognition) [VERIFIED]
- **Google Workspace**: google_workspace_mcp - Gmail, Drive, Docs, Sheets, Calendar, Chat [VERIFIED]
- **Microsoft 365**: ms-365-mcp-server - Outlook, OneDrive, SharePoint, Teams, Excel [VERIFIED]
- **SharePoint**: Included in ms-365-mcp-server (org-mode), dedicated mcp-onedrive-sharepoint [VERIFIED]
- **API Documentation**: Context7 (up-to-date library docs), Swagger-MCP (OpenAPI exploration) [VERIFIED]
- **RAG (Retrieval-Augmented Generation)/Memory**: rag-memory-mcp (local knowledge graph + vector search), sequential-thinking (reasoning) [VERIFIED]
- **Local Databases**: DBHub (multi-database), mcp-database-server, official SQLite MCP [VERIFIED]
- **Local Automation**: cli-mcp-server (shell/CLI - Command Line Interface), Git MCP (local repos), GitHub MCP (remote) [VERIFIED]
- **Testing Framework**: mcp-testing-framework (mocking, coverage, benchmarking) [VERIFIED]
- **SaaS Providers**: Composio (500+ toolkits), Arcade (OAuth-first), Nango (unified API auth), Cloudflare (edge hosting) [VERIFIED]
- **Enterprise Gateways**: Microsoft MCP Gateway (Kubernetes), Microsoft MCP Server for Enterprise (free M365), Azure API Management [VERIFIED]
- **Registries**: Smithery (marketplace), Docker MCP Catalog (secure), Official MCP Registry [VERIFIED]

## Table of Contents

1. [Document Reading MCPs](#1-document-reading-mcps)
2. [File System MCPs](#2-file-system-mcps)
3. [Browser Automation - Playwright](#3-browser-automation---playwright)
4. [Browser Automation - Alternatives](#4-browser-automation---alternatives)
5. [Code Testing MCPs](#5-code-testing-mcps)
6. [Local LLM/ML MCPs](#6-local-llmml-mcps)
7. [Specialized AI Model MCPs](#7-specialized-ai-model-mcps)
8. [Google Workspace MCPs](#8-google-workspace-mcps)
9. [Microsoft 365 / Outlook MCPs](#9-microsoft-365--outlook-mcps)
10. [SharePoint MCPs](#10-sharepoint-mcps)
11. [API Documentation MCPs](#11-api-documentation-mcps)
12. [RAG and Memory MCPs](#12-rag-and-memory-mcps)
13. [Local Database MCPs](#13-local-database-mcps)
14. [Local Machine Automation MCPs](#14-local-machine-automation-mcps)
15. [Testing and Quality MCPs](#15-testing-and-quality-mcps)
16. [SaaS Providers and Managed MCP Solutions](#16-saas-providers-and-managed-mcp-solutions)
17. [Sources](#17-sources)
18. [Document History](#18-document-history)

## 1. Document Reading MCPs

### 1.1 PDF Reading

**pdf-reader-mcp** (SylphxAI) - Production-ready PDF processing
- 5-10x faster parallel processing
- Y-coordinate content ordering for accurate text extraction
- 94%+ test coverage with 103 tests passing
- Supports local files and remote URLs
- Returns structured JSON data
- GitHub: `github.com/SylphxAI/pdf-reader-mcp`

**PDF Tools MCP** (Sohaib-2)
- Comprehensive PDF manipulation: merge, split, encrypt, optimize
- GitHub: `github.com/Sohaib-2/pdf-mcp-server`

**mcp_pdf_reader** (gpetraroli)
- Read and search text in local PDF files
- GitHub: `github.com/gpetraroli/mcp_pdf_reader`

### 1.2 Office Documents

**Office-Word-MCP-Server** (GongRzhe)
- Word document operations via python-docx
- Create, read, edit DOCX files
- Text formatting and color control
- GitHub: `github.com/GongRzhe/Office-Word-MCP-Server`

**Document Loader MCP Server** (AWS)
- Multi-format support: PDF, DOCX, DOC, Excel, PowerPoint, images
- Part of AWS MCP Servers collection
- Docs: `awslabs.github.io/mcp/servers/document-loader-mcp-server`

**Pandoc MCP** (vivekVells)
- Seamless document format conversion
- Supports: Markdown, HTML, PDF, DOCX, CSV, and more
- GitHub: `github.com/vivekVells/mcp-pandoc`

### 1.3 Configuration Example (PDF Reader)

```json
{
  "mcpServers": {
    "pdf-reader": {
      "command": "npx",
      "args": ["-y", "@anthropic/pdf-reader-mcp"]
    }
  }
}
```

## 2. File System MCPs

### 2.1 Official Filesystem Server

**@modelcontextprotocol/server-filesystem** (Anthropic Reference)
- Secure file operations with configurable access controls
- Sandboxed directory access - only allowed directories accessible
- Tools: `read_file`, `write_file`, `list_directory`, `create_directory`, `move_file`, `search_files`
- GitHub: `github.com/modelcontextprotocol/servers/tree/main/src/filesystem`

**Key Security Features:**
- Operations restricted to explicitly specified directories
- Configurable via args or Roots
- Read-only mode available
- Idempotent and destructive operation hints

### 2.2 Go Implementation

**mcp-filesystem-server** (mark3labs)
- Go implementation of filesystem MCP
- Same capabilities as official Node.js version
- GitHub: `github.com/mark3labs/mcp-filesystem-server`

### 2.3 Configuration Example

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory1",
        "/path/to/allowed/directory2"
      ]
    }
  }
}
```

## 3. Browser Automation - Playwright

### 3.1 Microsoft Playwright MCP

**microsoft/playwright-mcp** - Official Microsoft implementation
- Fast and lightweight - uses accessibility tree, not pixel-based input
- LLM-friendly - no vision models needed, operates on structured data
- Deterministic tool application - avoids screenshot ambiguity
- GitHub: `github.com/microsoft/playwright-mcp`

**Key Features:**
- Cross-browser: Chrome, Firefox, Safari
- Cross-platform: Windows, macOS, Linux
- Works with VS Code, Cursor, Windsurf, Claude Desktop, Goose

**Available Tools:**
- `browser_click` - Click elements with optional double-click, modifiers
- `browser_close` - Close browser session
- `browser_console_messages` - Get console logs by level
- `browser_drag` - Drag and drop between elements
- `browser_fill` - Fill form inputs
- `browser_navigate` - Go to URL
- `browser_screenshot` - Capture page/element screenshots
- `browser_select` - Select dropdown options
- `browser_snapshot` - Get accessibility tree snapshot
- `browser_type` - Type text with keyboard simulation

### 3.2 Configuration Example

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/playwright-mcp"]
    }
  }
}
```

### 3.3 Playwriter (remorses)

**playwriter** - Chrome Extension-Based MCP
- Repository: `github.com/remorses/playwriter`
- **Key Differentiator**: Connects to existing browser tabs via Chrome extension

**Advantages over Playwright MCP:**
- Uses your existing browser with logged-in sessions
- Work alongside the AI in same browser
- Reuse ad blockers, password managers, other extensions
- Bypass automation detection (can disconnect extension temporarily)
- Less resource usage - no separate Chrome instance
- Full Playwright API via single `execute` tool

**Installation:**
1. Install Chrome extension from Chrome Web Store
2. Configure MCP:
```json
{
  "mcpServers": {
    "playwriter": {
      "command": "npx",
      "args": ["playwriter@latest"]
    }
  }
}
```

### 3.4 Advantages Over Screenshot-Based Approaches

- No vision model costs
- Faster execution
- More precise element targeting
- Consistent across different screen sizes
- Works in headless mode without visual rendering overhead

## 4. Browser Automation - Alternatives

### 4.1 Browserbase + Stagehand (Cloud)

**mcp-server-browserbase** - Cloud browser automation
- AI-powered automation with natural language commands
- Multi-model support: OpenAI, Claude, Gemini
- Screenshot capture: full-page and element-specific
- Intelligent content extraction
- Enterprise proxy capabilities
- Stealth mode with anti-detection features
- Context persistence for authentication state
- GitHub: `github.com/browserbase/mcp-server-browserbase`

**Use Cases:**
- Web scraping at scale
- Automated testing in cloud
- Data extraction from JavaScript-heavy sites

### 4.2 Selenium MCP

**mcp-selenium** (angiejones)
- Browser automation via Selenium WebDriver
- Supported browsers: Chrome, Firefox, MS Edge
- Headless mode support
- GitHub: `github.com/angiejones/mcp-selenium`

**Available Tools:**
- `start_browser` - Launch browser with options (headless, arguments)
- `navigate` - Go to URL
- `find_element` - Locate by id, css, xpath, name, tag, class
- `click_element` - Click with timeout
- `send_keys` - Type text into inputs
- `get_element_text` - Extract text content
- `hover`, `drag_and_drop`, `double_click`, `right_click`
- `press_key` - Keyboard input
- `upload_file` - File upload handling
- `take_screenshot` - Capture page state
- `close_session` - Clean up resources

### 4.3 Puppeteer MCP

**puppeteer-mcp-server** (merajmehrabi)
- Chrome/Chromium automation via Puppeteer
- Similar capabilities to Playwright
- GitHub: `github.com/merajmehrabi/puppeteer-mcp-server`

### 4.4 Comparison

- **Playwright MCP**: Best for accessibility-tree based automation, no vision needed
- **Browserbase**: Best for cloud-scale scraping with stealth features
- **Selenium MCP**: Best for traditional WebDriver workflows, multi-browser
- **Puppeteer MCP**: Best for Chrome-specific automation

## 5. Code Testing MCPs

### 5.1 Test Runner MCP

**mcp-test-runner** (privsim) - Unified multi-framework test runner
- GitHub: `github.com/privsim/mcp-test-runner`

**Supported Frameworks:**
- **Bats** - Bash Automated Testing System
- **Pytest** - Python testing framework
- **Jest** - JavaScript testing framework
- **Flutter** - Flutter test framework
- **Go** - Go test framework
- **Rust** - Cargo test
- **Generic** - Arbitrary command execution

**Installation:**
```bash
npm install test-runner-mcp
```

**Prerequisites:**
- Bats: `apt-get install bats` or `brew install bats`
- Pytest: `pip install pytest`
- Jest: `npm install --save-dev jest`
- Go/Rust: Standard toolchain installation

### 5.2 Configuration Example

```json
{
  "mcpServers": {
    "test_runner": {
      "command": "node",
      "args": ["/path/to/test-runner-mcp/build/index.js"],
      "env": {
        "NODE_PATH": "/path/to/test-runner-mcp/node_modules"
      }
    }
  }
}
```

### 5.3 Use Cases for Autonomous Testing

- Run tests after code changes
- Parse and report test failures to AI agent
- Execute test suites across multiple languages
- CI/CD integration for automated quality checks

## 6. Local LLM/ML MCPs

### 6.1 Ollama MCP Bridge

**ollama-mcp-bridge** (patruff)
- Bridges local LLMs (via Ollama) to MCP servers
- Enables any Ollama-compatible model to use MCP tools
- GitHub: `github.com/patruff/ollama-mcp-bridge`

**Architecture:**
- Bridge: Manages tool registration and execution
- LLM Client: Handles Ollama interactions, formats tool calls
- MCP Client: Manages MCP server connections via JSON-RPC
- Tool Router: Routes requests to appropriate MCP

**Supported Models:**
- Qwen 2.5 (tested with qwen2.5-coder:7b-instruct)
- Any Ollama model with tool-calling capability

**Compatible MCPs:**
- Filesystem operations
- Brave web search
- GitHub interactions
- Google Drive and Gmail
- Memory/storage
- Image generation (Flux)

### 6.2 MCP Client for Ollama

**mcp-client-for-ollama** (jonigl)
- TUI (Terminal User Interface) application
- Connect local Ollama LLMs to multiple MCP servers
- Agent Mode with configurable loop limits
- GitHub: `github.com/jonigl/mcp-client-for-ollama`

### 6.3 Ollama MCP Agent

**ollama-mcp-agent** (godstale)
- Direct LLM functionality extension through MCP
- Supports models with tool-calling (e.g., qwen3:14b)
- Python-based MCP server implementation
- GitHub: `github.com/godstale/ollama-mcp-agent`

### 6.4 Benefits of Local LLM + MCP

- Complete data privacy
- Zero API costs after initial setup
- Offline capability
- Unlimited customization
- No rate limits

## 7. Specialized AI Model MCPs

### 7.1 Vision and OCR

**Vision MCP Server** (Z.AI)
- Image analysis and video understanding
- Tools: `ui_to_artifact` (UI screenshots to code/specs), `extract_text_from_screenshot` (OCR)
- Docs: `docs.z.ai/devpack/mcp/vision-mcp-server`

**Grok Vision OCR** (7etsuo)
- xAI Grok vision model + Tesseract OCR
- Image analysis and text extraction from URLs/local files
- Multiple format support

**mcp-image-recognition** (mario-andreschak)
- Supports OpenAI, OpenRouter, Anthropic Claude
- Configurable vision provider
- GitHub: `github.com/mario-andreschak/mcp-image-recognition`

**Computer Vision Tools** (omidsrezai)
- Image generation, OCR text extraction, object detection
- Containerized Docker services
- MinIO integration for image storage

### 7.2 Image Generation

**OpenAI GPT Image MCP** (SureScaleAI)
- Generate images from text prompts
- Edit images: inpainting, outpainting, compositing
- Works with Claude Desktop, Cursor, VSCode, Windsurf
- GitHub: `github.com/SureScaleAI/openai-gpt-image-mcp`

### 7.3 Multi-Model Access

**mcp-openai** (mzxrai)
- Use OpenAI models from Claude
- Seamless model switching
- GitHub: `github.com/mzxrai/mcp-openai`

**OpenRouter Vision** (Nazruden)
- Access multiple vision models via OpenRouter
- Single API key for many providers

## 8. Google Workspace MCPs

### 8.1 Comprehensive Google Workspace MCP

**google_workspace_mcp** (taylorwilsdon) - Most feature-complete
- GitHub: `github.com/taylorwilsdon/google_workspace_mcp`

**Supported Services:**
- **Gmail**: search, send, draft, label management, thread operations
- **Google Drive**: file operations, sharing, permissions, Office format support
- **Google Calendar**: events, calendars, scheduling
- **Google Docs**: create, edit, comments, export to PDF
- **Google Sheets**: read/write values, create spreadsheets
- **Google Slides**: presentations, content manipulation
- **Google Forms**: create forms, manage responses
- **Google Tasks**: task lists, hierarchy management
- **Google Chat**: spaces, messaging, search
- **Google Custom Search**: PSE (Programmable Search Engine) integration

**Authentication:**
- OAuth 2.0 and OAuth 2.1 support
- Automatic token refresh
- Multi-user bearer token authentication
- Remote OAuth2.1 for multi-user support

**Tool Tiers:**
- `core` - Essential tools only
- `extended` - Core + extras
- `complete` - All tools

### 8.2 Configuration Example

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tool-tier", "core"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "...",
        "GOOGLE_OAUTH_CLIENT_SECRET": "..."
      }
    }
  }
}
```

### 8.3 Gmail-Specific MCP

**Gmail MCP via n8n** - 20+ Gmail operations
- Search, send, reply, draft
- Label and thread management
- Mark read/unread, delete
- Workflow: `n8n.io/workflows/3605`

**Gmail MCP via Zapier**
- No-code setup with Zapier Agents
- Connect to any AI environment
- Site: `zapier.com/mcp/gmail`

## 9. Microsoft 365 / Outlook MCPs

### 9.1 ms-365-mcp-server (Softeria)

**Primary M365 MCP Server** - Comprehensive Graph API integration
- GitHub: `github.com/Softeria/ms-365-mcp-server`

**Personal Account Tools (default):**
- **Email (Outlook)**: list, get, send, delete, draft, move messages
- **Calendar**: list, create, update, delete events
- **OneDrive**: list drives, folder operations, upload, download, delete
- **Excel**: worksheets, ranges, charts, formatting, sorting
- **OneNote**: notebooks, sections, pages
- **To Do Tasks**: lists, tasks CRUD (Create, Read, Update, Delete) operations
- **Planner**: tasks, plans
- **Contacts**: Outlook contacts management
- **Search**: unified search

**Organization Tools (--org-mode):**
- **Teams & Chats**: list chats, messages, teams, channels, members
- **SharePoint Sites**: search, get sites, drives, lists, items
- **Shared Mailboxes**: list, get, send messages
- **User Management**: list users

**Features:**
- MSAL (Microsoft Authentication Library) authentication
- Read-only mode for safe operations
- Tool filtering for granular access
- Azure Key Vault integration
- Multiple cloud environments support

### 9.2 Configuration Example

```json
{
  "mcpServers": {
    "ms365": {
      "command": "npx",
      "args": ["-y", "ms-365-mcp-server", "--org-mode"],
      "env": {}
    }
  }
}
```

### 9.3 CLI Options

- `--login` - Login using device code flow
- `--logout` - Log out and clear credentials
- `--verify-login` - Verify login without starting server
- `--org-mode` - Enable organization/work mode (includes Teams, SharePoint)

### 9.4 Outlook-Specific MCP

**OutlookMCPServer** (Norcim133)
- Outlook Mail + Calendar + OneDrive
- Requires Azure admin setup
- GitHub: `github.com/Norcim133/OutlookMCPServer`

## 10. SharePoint MCPs

### 10.1 Via ms-365-mcp-server (Recommended)

SharePoint access included in ms-365-mcp-server with `--org-mode`:
- `search-sharepoint-sites` - Find sites
- `get-sharepoint-site` - Get site details
- `get-sharepoint-site-by-path` - Get by URL path
- `list-sharepoint-site-drives` - List document libraries
- `list-sharepoint-site-items` - List items in library
- `get-sharepoint-site-item` - Get specific item
- `list-sharepoint-site-lists` - List SharePoint lists
- `list-sharepoint-site-list-items` - Get list items
- `get-sharepoint-sites-delta` - Track changes

### 10.2 Dedicated SharePoint MCP

**mcp-onedrive-sharepoint** (ftaricano)
- Unified OneDrive and SharePoint access via Microsoft Graph
- Device code flow authentication
- File operations and collaboration
- GitHub: `github.com/ftaricano/mcp-onedrive-sharepoint`

**Features:**
- List files/folders in OneDrive or SharePoint
- SharePoint list management
- Excel integration
- Content search across personal and business accounts

### 10.3 Agent 365 Tooling Servers (Microsoft Official)

**Enterprise-grade MCP servers** from Microsoft
- Safe, governed access to business systems
- Supports: Outlook, Teams, SharePoint, OneDrive, Dataverse
- Tooling gateway for enterprise security
- Docs: `learn.microsoft.com/en-us/microsoft-agent-365/tooling-servers-overview`

### 10.4 CLI for Microsoft 365 MCP

**cli-microsoft365-mcp-server** (PnP)
- Natural language to CLI for M365 commands
- Handles complex prompts as command chains
- GitHub: `github.com/pnp/cli-microsoft365-mcp-server`

## 11. API Documentation MCPs

### 11.1 Context7 - Up-to-Date Library Docs

**context7** (Upstash) - Solves stale LLM training data problem
- Pulls version-specific documentation directly into prompts
- Curated database of library documentation
- GitHub: `github.com/upstash/context7`

**Tools:**
- `resolve-library-id` - Find library ID from name
- `get-library-docs` - Get documentation for specific library version

**Configuration:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### 11.2 OpenAPI/Swagger MCPs

**Swagger-MCP** (Vizioz)
- Download, cache, and explore Swagger/OpenAPI specs
- Extract endpoints, HTTP methods, models
- Generate API interfaces from documentation
- GitHub: `github.com/Vizioz/Swagger-MCP`

**Tools:**
- `getSwaggerDefinition` - Download and cache Swagger spec
- `getSwaggerEndpoints` - List all API endpoints
- `getSwaggerEndpointDetails` - Get specific endpoint details
- `getSwaggerModels` - List data models

**OpenAPI Schema Explorer** (kadykov)
- Read-only exploration of OpenAPI specs
- Supports local files and remote URLs
- Auto-converts Swagger v2.0 to OpenAPI v3
- mcpservers.org: `mcpservers.org/servers/kadykov/mcp-openapi-schema-explorer`

## 12. RAG and Memory MCPs

### 12.1 RAG Memory MCP (Recommended for Local)

**rag-memory-mcp** (ttommyth) - Local knowledge graph with vector search
- GitHub: `github.com/ttommyth/rag-memory-mcp`

**Key Features:**
- Knowledge Graph Memory: Persistent entities, relationships, observations
- Vector Search: Semantic similarity using sentence transformers
- Document Processing: RAG-enabled chunking and embedding
- Hybrid Search: Combines vector similarity with graph traversal
- SQLite Backend: Fast local storage with sqlite-vec

**Document Management Tools:**
- `storeDocument` - Store documents with metadata
- `chunkDocument` - Create text chunks with configurable parameters
- `embedChunks` - Generate vector embeddings
- `extractTerms` - Extract potential entity terms
- `linkEntitiesToDocument` - Create entity-document associations
- `deleteDocuments`, `listDocuments`

**Knowledge Graph Tools:**
- `createEntities` - Create entities with observations and types
- `createRelations` - Establish relationships between entities
- `addObservations` - Add contextual information to entities
- `deleteEntities`, `deleteRelations`, `deleteObservations`

**Search Tools:**
- `hybridSearch` - Advanced vector + graph search
- `searchNodes` - Find entities by name, type, observation
- `openNodes` - Retrieve entities and relationships
- `readGraph` - Get complete knowledge graph structure

**Configuration:**
```json
{
  "mcpServers": {
    "rag_memory": {
      "command": "npx",
      "args": ["-y", "rag-memory-mcp"],
      "env": {
        "MEMORY_DB_PATH": "/path/to/memory.db"
      }
    }
  }
}
```

### 12.2 Official Memory Server (Anthropic)

**@modelcontextprotocol/server-memory** - Knowledge graph-based persistent memory
- Part of official MCP servers
- Simpler than rag-memory-mcp but less features
- GitHub: `github.com/modelcontextprotocol/servers/tree/main/src/memory`

### 12.3 Sequential Thinking

**@modelcontextprotocol/server-sequential-thinking** - Structured reasoning
- Dynamic problem-solving through thought sequences
- Break complex problems into steps
- Revise and refine thoughts
- Branch into alternative reasoning paths
- GitHub: `github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking`

**Configuration:**
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

## 13. Local Database MCPs

### 13.1 DBHub (Multi-Database)

**dbhub** (Bytebase) - Universal database MCP
- Zero dependency, token-efficient
- Single interface for multiple databases
- GitHub: `github.com/bytebase/dbhub`

**Supported Databases:**
- PostgreSQL
- MySQL
- MariaDB
- SQL Server
- SQLite

**Features:**
- Multi-connection via TOML (Tom's Obvious Minimal Language) config
- Read-only by default (safe)
- Just two MCP tools to maximize context window

### 13.2 MCP Database Server

**mcp-database-server** (ExecuteAutomation)
- SQLite, SQL Server, PostgreSQL, MySQL support
- Natural language to SQL queries
- Schema exploration
- GitHub: `github.com/executeautomation/mcp-database-server`

**Tools:**
- `connect_database` - Connect to database
- `list_tables` - Show all tables
- `describe_table` - Get table schema
- `query_database` - Execute SQL queries
- `get_database_info` - Connection status and info

### 13.3 SQLite MCP (Official)

**@modelcontextprotocol/server-sqlite** - SQLite operations
- Schema exploration and querying
- AI-driven analysis
- Part of official MCP servers

## 14. Local Machine Automation MCPs

### 14.1 Shell Command Execution

**cli-mcp-server** (MladenSU)
- Execute whitelisted CLI commands
- Configurable allowed directories
- GitHub: `github.com/MladenSU/cli-mcp-server`

**Security Features:**
- Command whitelist (only approved commands)
- Directory restrictions
- Configurable timeout

**Shell Command Runner** (various)
- Direct shell execution
- Process management
- File operations
- PulseMCP: `pulsemcp.com/servers/shell-command-runner`

### 14.2 Git Operations (Local)

**@modelcontextprotocol/server-git** - Local Git repository operations
- Read, search, manipulate Git repos
- Part of official reference servers
- GitHub: `github.com/modelcontextprotocol/servers/tree/main/src/git`

**Tools:**
- `git_status` - Repository status
- `git_log` - Commit history
- `git_diff` - Show changes
- `git_commit` - Create commits
- `git_branch` - Branch operations

**git-mcp-server** (cyanheads) - Extended Git operations
- Secure, scalable Git MCP
- Human-readable summaries
- GitHub: `github.com/cyanheads/git-mcp-server`

### 14.3 GitHub Operations

**github-mcp-server** (GitHub Official)
- Read repositories and code
- Manage issues and PRs
- Analyze code
- Automate workflows
- GitHub: `github.com/github/github-mcp-server`

**GitMCP** (idosal) - Remote documentation hub
- Transforms any GitHub project into docs
- Zero setup, cloud-hosted
- GitHub: `github.com/idosal/git-mcp`

## 15. Testing and Quality MCPs

### 15.1 MCP Testing Framework

**mcp-testing-framework** (haakco)
- Comprehensive testing for MCP servers
- GitHub: `github.com/haakco/mcp-testing-framework`

**Features:**
- Advanced Mocking: Mock MCP servers, tools, resources
- Coverage Analysis: Track code coverage with thresholds
- Performance Benchmarking: Response times and throughput
- Integration Testing: Complete server workflows

### 15.2 MCP Hello World (Test Double)

**mcp-hello-world** (LobeHub)
- Minimal MCP server for testing
- Test Double / Mock Server
- Unit and integration testing for MCP clients
- LobeHub: `lobehub.com/mcp/lobehub-mcp-hello-world`

### 15.3 Testing Best Practices

**Unit Testing MCP Servers:**
- Test tool implementations in isolation
- Mock slow operations for speed
- Configure longer timeouts for integration tests
- Handle async operation edge cases

**Resources:**
- Guide: `mcpcat.io/guides/writing-unit-tests-mcp-servers/`
- Python SDK testing: `github.com/modelcontextprotocol/python-sdk/issues/1252`

## 16. SaaS Providers and Managed MCP Solutions

### 16.1 Managed MCP Server Platforms

**Composio** - Hosted MCP with 500+ Toolkits
- Website: `composio.dev`
- Managed authentication: OAuth, API keys, custom auth flows handled automatically
- Hosted MCP servers for all 500+ toolkits (Slack, GitHub, Notion, Salesforce, etc.)
- Tool Router: Single MCP server that searches, authenticates, and executes across all tools
- Fine-grained permissions per tool and user
- Triggers: Subscribe to external events (new Slack message, new GitHub issue)
- Framework-agnostic: Works with OpenAI, Anthropic, LangChain, Vercel AI SDK (Software Development Kit)
- **Key benefit**: No credential management needed, handles OAuth refresh automatically

**Arcade.dev** - OAuth-First MCP Framework
- Website: `arcade.dev`
- Focus: Secure authentication for AI agents
- Features:
  - OAuth tools with managed config and secrets
  - Production deployment with zero rewrites
  - Connects to identity providers (Google, Slack, Salesforce, Twitter, LinkedIn)
  - Tokens never reach the language model - handled server-side
- Open source framework: `arcade-mcp` (MIT license)
- Use case: Enterprise-ready MCP with identity provider integration

**Nango** - Unified API Auth + MCP Server
- Website: `nango.dev`
- 500+ API integrations with unified authentication
- Built-in MCP Server exposes integrations as tools
- Connect Links: Surface OAuth flows directly in chat UI
- Tool execution via Actions with prebuilt templates
- Under 100ms overhead for tool executions
- Sandboxed, elastic environments for tool code
- **Key benefit**: Handle OAuth complexity once, use everywhere

**Cloudflare Workers** - Remote MCP Server Hosting
- Deploy remote MCP servers to Cloudflare edge network
- `McpAgent` class handles remote transport (SSE - Server-Sent Events, Streamable HTTP)
- `workers-oauth-provider`: OAuth 2.1 Provider library included
- Durable Objects for persistent, stateful sessions
- WebSocket support for bidirectional communication
- **Key benefit**: Global edge deployment with built-in auth

### 16.2 Enterprise MCP Gateways

**Microsoft MCP Gateway** (Open Source)
- Repository: `github.com/microsoft/mcp-gateway`
- Reverse proxy and management layer for MCP servers
- Features:
  - Session-aware stateful routing in Kubernetes
  - Control Plane: RESTful APIs for MCP server lifecycle (deploy, update, delete)
  - Data Plane: Gateway routing with session affinity
  - Tool registration and dynamic routing
  - Entra ID (Azure AD) authentication and RBAC (Role-Based Access Control)
  - Roles: `mcp.admin`, `mcp.engineer` for access control
- Deploy to: Local Kubernetes or Azure (1-click)
- **Key benefit**: Enterprise-grade MCP management in Kubernetes

**Microsoft MCP Server for Enterprise** (Hosted)
- URL: `https://mcp.svc.cloud.microsoft/enterprise`
- Natural language queries to Microsoft Graph API
- Tools: `microsoft_graph_suggest_queries`, `microsoft_graph_get`, `microsoft_graph_list_properties`
- Use cases: IT helpdesk, admin reporting, API discovery
- **No additional cost** - uses existing Microsoft licenses
- Rate limit: 100 calls/minute per user
- **Key benefit**: Zero-config access to Microsoft 365/Entra data

**Azure API Management** - MCP Auth Gateway
- Credential manager for secure token forwarding
- Policies: `get-authorization-context`, `set-header`
- Protected Resource Metadata (PRM) support
- **Key benefit**: Centralized credential management for all MCP servers

### 16.3 MCP Server Registries and Catalogs

**Smithery** - MCP Marketplace
- Website: `smithery.ai`
- Registry of 200+ MCP servers with one-click install
- Built-in hosting infrastructure for MCP servers
- Standard installation commands and configuration
- Community-driven with publisher verification

**Docker MCP Catalog** - Secure Distribution
- URL: `hub.docker.com/mcp`
- Security features:
  - Cryptographic signatures (image verification)
  - SBOM (Software Bill of Materials) documentation
  - Complete container isolation from host
- Categories: Docker-built (full security treatment) vs Community-built
- Browse by use case: Data Integration, Development Tools, Communication, Productivity
- **Key benefit**: Secure alternative to `npx -y @untrusted/mcp-server`

**Official MCP Registry**
- Repository: `github.com/modelcontextprotocol/registry`
- Authoritative metadata for publicly-available MCP servers
- Vendor-neutral, industry security standards
- Publisher verification process

### 16.4 Specialized Cloud Browser Providers

**Browserbase** - Cloud Browser Infrastructure
- Managed browser automation with Stagehand framework
- Enterprise SSO support
- Stealth browsers to avoid detection
- MCP Server: `mcp-server-browserbase`
- **Key benefit**: No local browser management, scales automatically

**Browser-Use Cloud** - Stealth Browser API
- Cloud profiles for authenticated sessions
- Proxy rotation and fingerprint management
- CAPTCHA handling infrastructure
- **Key benefit**: Production-grade browser automation

### 16.5 Comparison: Self-Hosted vs Managed

**Self-Hosted MCP Servers:**
- Full control over data and execution
- No per-request costs
- Requires credential management
- Must handle OAuth refresh, token storage
- Infrastructure maintenance burden

**Managed MCP Solutions:**
- Credential management handled automatically
- OAuth flows pre-configured for 500+ services
- Enterprise security features (RBAC, audit logs)
- Scalable infrastructure
- Higher per-request costs
- Potential vendor lock-in

**Recommendation by Use Case:**
- **Prototype/Development**: Self-hosted with local MCP servers
- **Production with OAuth Apps**: Composio, Nango, or Arcade for credential handling
- **Enterprise/Kubernetes**: Microsoft MCP Gateway for centralized management
- **Microsoft 365 Integration**: Microsoft MCP Server for Enterprise (free)
- **Browser Automation**: Browserbase or Browser-Use Cloud for scale

## 17. Sources

**Primary Sources:**

- `MCPS-IN01-SC-GH-MCPSVRS`: https://github.com/modelcontextprotocol/servers - Official MCP servers repository [VERIFIED]
- `MCPS-IN01-SC-GH-PLYWRT`: https://github.com/microsoft/playwright-mcp - Microsoft Playwright MCP [VERIFIED]
- `MCPS-IN01-SC-GH-GWSMCP`: https://github.com/taylorwilsdon/google_workspace_mcp - Google Workspace MCP [VERIFIED]
- `MCPS-IN01-SC-GH-MS365`: https://github.com/Softeria/ms-365-mcp-server - Microsoft 365 MCP [VERIFIED]
- `MCPS-IN01-SC-GH-TSTRN`: https://github.com/privsim/mcp-test-runner - Test Runner MCP [VERIFIED]
- `MCPS-IN01-SC-GH-OLLBR`: https://github.com/patruff/ollama-mcp-bridge - Ollama MCP Bridge [VERIFIED]
- `MCPS-IN01-SC-GH-BRBSE`: https://github.com/browserbase/mcp-server-browserbase - Browserbase MCP [VERIFIED]
- `MCPS-IN01-SC-GH-SELEN`: https://github.com/angiejones/mcp-selenium - Selenium MCP [VERIFIED]
- `MCPS-IN01-SC-GH-PDFRD`: https://github.com/SylphxAI/pdf-reader-mcp - PDF Reader MCP [VERIFIED]
- `MCPS-IN01-SC-GH-ODSP`: https://github.com/ftaricano/mcp-onedrive-sharepoint - OneDrive/SharePoint MCP [VERIFIED]
- `MCPS-IN01-SC-MS-A365`: https://learn.microsoft.com/en-us/microsoft-agent-365/tooling-servers-overview - Agent 365 docs [VERIFIED]

**New Section Sources:**

- `MCPS-IN01-SC-GH-CTX7`: https://github.com/upstash/context7 - Context7 up-to-date docs for LLMs [VERIFIED]
- `MCPS-IN01-SC-GH-SWGMCP`: https://github.com/Vizioz/Swagger-MCP - Swagger/OpenAPI MCP [VERIFIED]
- `MCPS-IN01-SC-GH-RAGMEM`: https://github.com/ttommyth/rag-memory-mcp - RAG Memory with knowledge graph [VERIFIED]
- `MCPS-IN01-SC-GH-SEQTHK`: https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking - Sequential Thinking [VERIFIED]
- `MCPS-IN01-SC-GH-DBHUB`: https://github.com/bytebase/dbhub - Universal database MCP [VERIFIED]
- `MCPS-IN01-SC-GH-CLIMCP`: https://github.com/MladenSU/cli-mcp-server - CLI command execution [VERIFIED]
- `MCPS-IN01-SC-GH-GITMCP`: https://github.com/cyanheads/git-mcp-server - Extended Git operations [VERIFIED]
- `MCPS-IN01-SC-GH-GHOFF`: https://github.com/github/github-mcp-server - GitHub official MCP [VERIFIED]
- `MCPS-IN01-SC-GH-MCPTST`: https://github.com/haakco/mcp-testing-framework - MCP testing framework [VERIFIED]

**Directory Sources:**

- `MCPS-IN01-SC-MCPFND`: https://www.mcpserverfinder.com/ - MCP Server Finder directory
- `MCPS-IN01-SC-MCPORG`: https://mcpservers.org/ - Awesome MCP Servers
- `MCPS-IN01-SC-PLYBKS`: https://playbooks.com/mcp/ - Playbooks MCP directory
- `MCPS-IN01-SC-MCPCAT`: https://mcpcat.io/guides/writing-unit-tests-mcp-servers/ - MCP testing guide [VERIFIED]

**SaaS and Enterprise Sources:**

- `MCPS-IN01-SC-COMPOS`: https://docs.composio.dev/mcp/introduction - Composio MCP documentation [VERIFIED]
- `MCPS-IN01-SC-ARCADE`: https://www.arcade.dev/mcp - Arcade MCP framework [VERIFIED]
- `MCPS-IN01-SC-NANGO`: https://nango.dev/docs/guides/mcp - Nango AI tool calling [VERIFIED]
- `MCPS-IN01-SC-CFWRKR`: https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/ - Cloudflare remote MCP [VERIFIED]
- `MCPS-IN01-SC-MSGW`: https://github.com/microsoft/mcp-gateway - Microsoft MCP Gateway [VERIFIED]
- `MCPS-IN01-SC-MSENT`: https://learn.microsoft.com/en-us/graph/mcp-server/overview - Microsoft MCP Server Enterprise [VERIFIED]
- `MCPS-IN01-SC-DKRMCP`: https://www.docker.com/blog/docker-mcp-catalog-secure-way-to-discover-and-run-mcp-servers/ - Docker MCP Catalog [VERIFIED]
- `MCPS-IN01-SC-SMITH`: https://smithery.ai/ - Smithery MCP marketplace [VERIFIED]

## 18. Document History

**[2026-01-15 10:57]**
- Added: Playwriter (remorses) to Section 3 - Chrome extension-based MCP for existing browser sessions

**[2026-01-15 10:47]**
- Fixed: Additional acronyms expanded (SSE, RBAC, SDK)

**[2026-01-15 10:46]**
- Added: Section 16 - SaaS Providers and Managed MCP Solutions
- Added: Managed platforms (Composio, Arcade, Nango, Cloudflare Workers)
- Added: Enterprise gateways (Microsoft MCP Gateway, MCP Server for Enterprise, Azure API Management)
- Added: Registries (Smithery, Docker MCP Catalog, Official MCP Registry)
- Added: Cloud browser providers (Browserbase, Browser-Use Cloud)
- Added: Self-hosted vs Managed comparison with recommendations
- Added: 8 new SaaS and enterprise sources

**[2026-01-15 10:47]**
- Fixed: Acronyms expanded on first use (MCP, LLM, OCR, RAG, CLI, CRUD, MSAL, PSE, TOML)

**[2026-01-15 10:44]**
- Added: Section 11 - API Documentation MCPs (Context7, Swagger-MCP, OpenAPI Explorer)
- Added: Section 12 - RAG and Memory MCPs (rag-memory-mcp, official memory, sequential-thinking)
- Added: Section 13 - Local Database MCPs (DBHub, mcp-database-server, SQLite)
- Added: Section 14 - Local Machine Automation MCPs (CLI, Git, GitHub)
- Added: Section 15 - Testing and Quality MCPs (mcp-testing-framework, test doubles)
- Added: 9 new verified sources

**[2026-01-15 10:30]**
- Initial research document created
- Added 10 major categories covering document reading, file system, browser automation, testing, local LLMs, AI models, Google Workspace, M365, and SharePoint
- Verified primary GitHub sources for all major MCP servers
