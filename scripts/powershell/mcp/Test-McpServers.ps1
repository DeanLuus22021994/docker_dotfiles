# Test-McpServers
# Health check for all MCP servers in active configuration

<#
.SYNOPSIS
    Performs health checks on all configured MCP servers.

.DESCRIPTION
    Pings each MCP server using the Node.js health-check utility.
    Reports status, response time, and any errors.
    Returns exit code 0 if all servers respond, 1 if any fail.

.PARAMETER Json
    Output results in JSON format for programmatic use.

.PARAMETER Timeout
    Timeout in milliseconds for each server check (default: 5000).

.EXAMPLE
    .\Test-McpServers.ps1
    Runs health check with console output.

.EXAMPLE
    .\Test-McpServers.ps1 -Json
    Outputs results as JSON for parsing.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Json,
    
    [Parameter(Mandatory=$false)]
    [int]$Timeout = 5000
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$workspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$healthCheckScript = Join-Path $workspaceRoot "scripts\javascript\mcp\health-check.js"

# Validate health check script exists
if (-not (Test-Path $healthCheckScript)) {
    Write-Host "✗ Health check script not found: $healthCheckScript" -ForegroundColor Red
    exit 1
}

# Build command
$nodeArgs = @($healthCheckScript)
if ($Json) {
    $nodeArgs += "--json"
}

# Run health check
try {
    $result = & node $nodeArgs
    $exitCode = $LASTEXITCODE
    
    if ($Json) {
        # Parse and enhance JSON output
        $healthData = $result | ConvertFrom-Json
        $healthData | ConvertTo-Json -Depth 10
    } else {
        # Pass through console output
        $result
    }
    
    exit $exitCode
} catch {
    Write-Host "✗ Health check failed: $_" -ForegroundColor Red
    exit 1
}
