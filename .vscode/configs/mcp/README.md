# MCP Configuration Management

This directory contains organized MCP (Model Context Protocol) server configurations for VS Code Copilot integration.

## Directory Structure

```
.vscode/configs/mcp/
├── profiles/           # MCP server profile configurations
│   ├── core.json      # Core development (53 tools)
│   ├── fullstack.json # Full-stack development (80 tools)
│   ├── testing.json   # Testing & automation (87 tools)
│   └── data.json      # Data & analytics (47 tools)
├── documentation/      # Tool inventories and reports
│   └── toolset.json   # Complete tool catalog
└── README.md          # This file
```

## Profile Overview

| Profile | Tool Count | Servers | Use Case |
|---------|-----------|---------|----------|
| **core** | 53 | github, filesystem, git, fetch | Daily development, version control |
| **fullstack** | 80 | github, filesystem + playwright, postgres, sqlite, memory, git, fetch | Backend + frontend + database work |
| **testing** | 87 | github, filesystem, playwright, git, fetch, postgres | E2E testing, browser automation |
| **data** | 47 | github, filesystem, postgres, sqlite, memory, git, fetch | Database ops, analytics, knowledge graphs |
| **all** | 107 | All 9 servers enabled | Complete toolset (main mcp.json) |

## Metadata Structure

Each profile includes metadata for tracking:

```json
{
  "_metadata": {
    "profile_name": "core",
    "tool_count": 53,
    "estimated_tokens": "8-10k",
    "last_generated": "2025-10-25T00:00:00Z",
    "servers_enabled": ["git", "github", "filesystem", "fetch"]
  },
  "servers": { ... }
}
```

## Active Configuration

The active MCP configuration is at `.vscode/mcp.json` (parent directory).

**To switch profiles:**
```powershell
# Using PowerShell orchestrator
.\scripts\orchestrator.ps1 mcp set-profile -Profile core

# Direct execution
.\scripts\powershell\mcp\Set-Profile.ps1 -Profile core
```

**Restart VS Code Insiders after switching profiles.**

## Token Optimization

Token usage estimates (tool definitions sent at startup):

- **core**: ~8-10k tokens (50% reduction vs all)
- **data**: ~7-9k tokens (55% reduction vs all)
- **fullstack**: ~11-14k tokens (25-30% reduction vs all)
- **testing**: ~12-15k tokens (15-20% reduction vs all)
- **all**: ~15-20k tokens (baseline)

**Recommendation:** Use the most specific profile for your current task.

## Version Control

- ✅ **Tracked in git**: All profile files in `profiles/`
- ✅ **Tracked in git**: Documentation in `documentation/`
- ❌ **Ignored in git**: Active `.vscode/mcp.json` (contains local customizations)

## Management Commands

See `scripts/README.md` for complete MCP management commands:

```powershell
# Create/regenerate profiles
.\scripts\orchestrator.ps1 mcp new-profiles

# Switch active profile
.\scripts\orchestrator.ps1 mcp set-profile -Profile core

# View current profile
.\scripts\orchestrator.ps1 mcp get-profile

# Health check servers
.\scripts\orchestrator.ps1 mcp test-servers

# Compare profiles
.\scripts\orchestrator.ps1 mcp compare-profiles
```

## Technical Details

- **Protocol**: MCP (Model Context Protocol) over JSON-RPC stdio
- **Runtimes**: npx (Node.js) and uvx (Python/UV)
- **Startup**: Servers spawn as child processes when VS Code launches
- **Tool Discovery**: `initialize` → `tools/list` sequence at startup
- **Caching**: Tool schemas cached in memory for session lifetime
- **Restart Required**: Configuration changes require VS Code restart

## Server Requirements

### Node.js Servers (npx)
- github, filesystem, postgres, memory, puppeteer, playwright, sqlite
- Requires: Node.js >= 18.0.0 (v25.0.0 installed)

### Python Servers (uvx)
- git, fetch
- Requires: UV Python package manager
  ```powershell
  irm https://astral.sh/uv/install.ps1 | iex
  ```

### Environment Variables
- `GITHUB_TOKEN` - Required for github server
- `DOCKER_POSTGRES_PASSWORD` - Required for postgres server

---

**Last Updated:** 2025-10-25
