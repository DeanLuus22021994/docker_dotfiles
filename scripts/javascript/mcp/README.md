# MCP JavaScript Tools

Node.js utilities for managing MCP (Model Context Protocol) servers in VS Code Copilot.

## Scripts

### Tool Discovery

Queries all configured MCP servers to extract complete tool lists, schemas, and detect overlaps.

```bash
# Run discovery
node discover-tools.js

# Via npm
npm run discover
```

**Output:** `../../mcp_tools_report.json` (3500+ lines with complete tool schemas)

**Discovered Tools:**

- 107 total tools across 9 servers
- No name overlaps detected
- Full JSON schemas with input parameters

### Health Check

Lightweight ping to verify MCP servers are responding.

```bash
# Console output
node health-check.js

# JSON output (for programmatic use)
node health-check.js --json
npm run health:json
```

**Example Output:**

```
======================================================================
MCP SERVER HEALTH CHECK
======================================================================

✓ github              healthy    (856ms)
✓ filesystem          healthy    (742ms)
✗ postgres            failed     (123ms)
  └─ Connection refused
✓ git                 healthy    (1024ms)

======================================================================
Health: 3/4 servers responding
======================================================================
```

**Exit Codes:**

- `0` - All servers healthy
- `1` - One or more servers failed/timeout

## Usage in PowerShell

```powershell
# Check server health
$health = node scripts\javascript\mcp\health-check.js --json | ConvertFrom-Json
if ($health.github.status -eq 'healthy') {
    Write-Host "✓ GitHub MCP server is up"
}

# Discover tools
node scripts\javascript\mcp\discover-tools.js
```

## Usage in Python

```python
import subprocess
import json

# Run health check
result = subprocess.run(
    ['node', 'scripts/javascript/mcp/health-check.js', '--json'],
    capture_output=True,
    text=True
)
health = json.loads(result.stdout)

for server, status in health.items():
    print(f"{server}: {status['status']} ({status['duration']}ms)")
```

## Requirements

- **Node.js:** >= 18.0.0 (v25.0.0 installed)
- **MCP Config:** `.vscode/mcp.json` must exist
- **Servers:** npm/npx for Node.js servers, uvx for Python servers

## Technical Details

### Protocol Communication

Both scripts use the MCP JSON-RPC protocol over stdio:

1. **Initialize:** `{ method: 'initialize', protocolVersion: '2024-11-05' }`
2. **Tools List:** `{ method: 'tools/list' }` (discover-tools only)
3. **Parse Response:** Handle `result` or `error` in JSON-RPC response

### Timeouts

- **Health Check:** 5 seconds per server (configurable)
- **Tool Discovery:** 15 seconds per server

### Environment Resolution

Automatically resolves:

- `${workspaceFolder}` → Current working directory
- `${env:VAR_NAME}` → Environment variable value

## Related Files

- **Profiles:** `.vscode/configs/mcp/profiles/` - Server configurations
- **Reports:** `../../mcp_tools_report.json` - Complete tool inventory
- **Documentation:** `.vscode/configs/mcp/documentation/` - Reference docs

## Integration

These tools are called by:

- `scripts/powershell/mcp/Test-Servers.ps1` - Health check wrapper
- `scripts/python/mcp/health_check.py` - Python wrapper
- `scripts/orchestrator.ps1` - MCP management commands

---

**Last Updated:** 2025-10-25
