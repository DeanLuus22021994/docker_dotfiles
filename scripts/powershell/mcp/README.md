# MCP (Model Context Protocol) Management

PowerShell utilities for managing MCP server configurations in VS Code Copilot.

## Commands

### New-McpProfiles

Generate optimized MCP profile configurations.

```powershell
.\New-McpProfiles.ps1 [-Force]
```

**Creates 4 profiles:**
- **core** (53 tools) - github, filesystem, git, fetch
- **fullstack** (80 tools) - github, filesystem + playwright, postgres, sqlite, memory, git, fetch
- **testing** (87 tools) - github, filesystem, playwright, git, fetch, postgres
- **data** (47 tools) - github, filesystem, postgres, sqlite, memory, git, fetch

**Output:** `.vscode/profiles/`

---

### Set-McpProfile

Switch active MCP profile.

```powershell
.\Set-McpProfile.ps1 -Profile <name> [-NoBackup]
```

**Profiles:** core, fullstack, testing, data, all

**Example:**
```powershell
.\Set-McpProfile.ps1 -Profile core
```

**⚠️ Requires VS Code restart after switching.**

---

### Get-McpProfile

Display current active profile.

```powershell
.\Get-McpProfile.ps1 [-Detailed]
```

**Shows:**
- Profile name
- Tool count
- Token estimate
- Enabled servers
- Last generation timestamp

---

### Test-McpServers

Health check all MCP servers.

```powershell
.\Test-McpServers.ps1 [-Json] [-Timeout <ms>]
```

**Example:**
```powershell
# Console output
.\Test-McpServers.ps1

# JSON output
.\Test-McpServers.ps1 -Json | ConvertFrom-Json
```

**Exit Codes:**
- `0` - All servers healthy
- `1` - One or more servers failed

---

### Compare-McpProfiles

Compare two profiles.

```powershell
.\Compare-McpProfiles.ps1 [-Profile1 <name>] [-Profile2 <name>] [-ShowServers]
```

**Example:**
```powershell
.\Compare-McpProfiles.ps1 -Profile1 core -Profile2 fullstack -ShowServers
```

**Shows:**
- Tool count differences
- Server inclusion/exclusion
- Token usage comparison

---

### Test-McpProfileGeneration

Comprehensive testing for profile generation and validation.

```powershell
.\Test-McpProfileGeneration.ps1 [-CleanTest]
```

**Example:**
```powershell
# Test existing profiles
.\Test-McpProfileGeneration.ps1

# Clean test from scratch
.\Test-McpProfileGeneration.ps1 -CleanTest
```

**Tests:**
- Profile file existence
- JSON structure validation
- GitHub/Filesystem server ordering
- Profile switching and mcp.json creation
- Python validation integration
- Token analysis accuracy

---

## Orchestrator Integration

Access via main orchestrator:

```powershell
# From workspace root
.\scripts\orchestrator.ps1 mcp <command> [options]

# Examples
.\scripts\orchestrator.ps1 mcp new-profiles
.\scripts\orchestrator.ps1 mcp set-profile -Profile core
.\scripts\orchestrator.ps1 mcp get-profile
.\scripts\orchestrator.ps1 mcp test-servers
.\scripts\orchestrator.ps1 mcp compare-profiles
.\scripts\orchestrator.ps1 mcp test-profiles
```

---

## Profile Structure

Each profile includes metadata:

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

---

## Token Optimization

| Profile | Tools | Tokens | Savings vs All | Priority Servers |
|---------|-------|--------|----------------|------------------|
| core | 53 | 8-10k | ~50% | github, filesystem always first |
| data | 47 | 7-9k | ~55% | github, filesystem always first |
| fullstack | 80 | 11-14k | ~25-30% | github, filesystem always first |
| testing | 87 | 12-15k | ~15-20% | github, filesystem always first |
| all | 107 | 15-20k | Baseline | N/A |

**Note:** GitHub and Filesystem MCP servers are always configured first in every profile for consistent tool availability.

**Recommendation:** Use the most specific profile for your task.

---

## Requirements

- **PowerShell:** 5.1+ or PowerShell Core 7+
- **Node.js:** >= 18.0.0 (for health checks)
- **UV:** Python package manager (for git/fetch servers)

---

## Related Files

- **Profiles:** `.vscode/configs/mcp/profiles/`
- **Documentation:** `.vscode/configs/mcp/documentation/`
- **Active Config:** `.vscode/mcp.json`
- **JS Tools:** `scripts/javascript/mcp/`
- **Python Tools:** `scripts/python/mcp/`

---

**Last Updated:** 2025-10-25
