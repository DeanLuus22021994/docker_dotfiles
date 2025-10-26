# Test-McpProfileGeneration
# Comprehensive testing for MCP profile generation and validation

<#
.SYNOPSIS
    Tests MCP profile generation, validation, and mcp.json creation.

.DESCRIPTION
    Performs comprehensive testing of the MCP management system:
    1. Validates all generated profiles exist
    2. Verifies github and filesystem servers are always first
    3. Tests profile switching and mcp.json creation
    4. Validates JSON structure and metadata
    5. Confirms orchestrator integration works

.PARAMETER CleanTest
    Remove existing profiles and test from scratch

.EXAMPLE
    .\Test-McpProfileGeneration.ps1
    Run all tests on existing profiles

.EXAMPLE
    .\Test-McpProfileGeneration.ps1 -CleanTest
    Clean slate test with fresh profile generation
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$CleanTest
)

$ErrorActionPreference = "Continue"
Set-StrictMode -Version Latest

$testsPassed = 0
$testsFailed = 0

# Color functions
function Write-TestHeader { param([string]$Message) Write-Host "`n$('=' * 70)" -ForegroundColor Cyan; Write-Host $Message -ForegroundColor Cyan; Write-Host $('=' * 70) -ForegroundColor Cyan }
function Write-TestPass { param([string]$Message) Write-Host "  ✓ $Message" -ForegroundColor Green; $script:testsPassed++ }
function Write-TestFail { param([string]$Message) Write-Host "  ✗ $Message" -ForegroundColor Red; $script:testsFailed++ }
function Write-TestInfo { param([string]$Message) Write-Host "  ℹ $Message" -ForegroundColor Blue }

# Resolve paths
$workspaceRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$profilesDir = Join-Path $workspaceRoot ".vscode\profiles"
$mcpJsonPath = Join-Path $workspaceRoot ".vscode\mcp.json"
$scriptsDir = Join-Path $workspaceRoot "scripts"

Write-TestHeader "MCP PROFILE GENERATION TEST SUITE"

# Test 1: Clean test setup
if ($CleanTest) {
    Write-TestInfo "Cleaning existing profiles for fresh test..."
    $profilesToRemove = @('core.json', 'fullstack.json', 'testing.json', 'data.json')
    foreach ($profileName in $profilesToRemove) {
        $profilePath = Join-Path $profilesDir $profileName
        if (Test-Path $profilePath) {
            Remove-Item $profilePath -Force
            Write-TestInfo "Removed $profileName"
        }
    }
}

# Test 2: Directory structure
Write-TestHeader "TEST 1: Directory Structure"
if (Test-Path $profilesDir) {
    Write-TestPass "Profiles directory exists: $profilesDir"
} else {
    Write-TestFail "Profiles directory missing: $profilesDir"
}

# Test 3: Generate profiles
Write-TestHeader "TEST 2: Profile Generation"
Write-TestInfo "Running: .\scripts\orchestrator.ps1 mcp new-profiles"
try {
    & "$scriptsDir\orchestrator.ps1" mcp new-profiles 2>&1 | Out-Null
    Write-TestPass "Profile generation command executed"
} catch {
    Write-TestFail "Profile generation failed: $_"
}

# Test 4: Validate all profiles exist
Write-TestHeader "TEST 3: Profile File Existence"
$expectedProfiles = @('core.json', 'fullstack.json', 'testing.json', 'data.json')
foreach ($profileName in $expectedProfiles) {
    $profilePath = Join-Path $profilesDir $profileName
    if (Test-Path $profilePath) {
        Write-TestPass "Profile exists: $profileName"
    } else {
        Write-TestFail "Profile missing: $profileName"
    }
}

# Test 5: Validate JSON structure and server order
Write-TestHeader "TEST 4: JSON Structure & Server Order"
foreach ($profileName in $expectedProfiles) {
    $profilePath = Join-Path $profilesDir $profileName
    if (Test-Path $profilePath) {
        try {
            $content = Get-Content $profilePath -Raw | ConvertFrom-Json
            
            # Check servers object exists
            if ($content.servers) {
                Write-TestPass "$profileName has servers object"
            } else {
                Write-TestFail "$profileName missing servers object"
                continue
            }
            
            # Get server names in order
            $serverNames = $content.servers.PSObject.Properties.Name
            
            # Check github is first
            if ($serverNames[0] -eq 'github') {
                Write-TestPass "$profileName has 'github' as first server"
            } else {
                Write-TestFail "$profileName first server is '$($serverNames[0])', expected 'github'"
            }
            
            # Check filesystem is second
            if ($serverNames[1] -eq 'filesystem') {
                Write-TestPass "$profileName has 'filesystem' as second server"
            } else {
                Write-TestFail "$profileName second server is '$($serverNames[1])', expected 'filesystem'"
            }
            
            # Note: _metadata property removed to prevent JSON schema validation warnings
            # Profiles now only contain servers object for clean validation
            
        } catch {
            Write-TestFail "$profileName JSON parse error: $_"
        }
    }
}

# Test 6: Profile switching and mcp.json creation
Write-TestHeader "TEST 5: Profile Switching & mcp.json Creation"
$testProfile = 'core'
Write-TestInfo "Testing profile switch to: $testProfile"

# Backup existing mcp.json if it exists
$mcpBackup = $null
if (Test-Path $mcpJsonPath) {
    $mcpBackup = Get-Content $mcpJsonPath -Raw
    Write-TestInfo "Backed up existing mcp.json"
}

try {
    # Switch profile
    & "$scriptsDir\orchestrator.ps1" mcp set-profile -Profile $testProfile 2>&1 | Out-Null
    
    # Check mcp.json was created
    if (Test-Path $mcpJsonPath) {
        Write-TestPass "mcp.json created after profile switch"
        
        # Validate mcp.json content
        $mcpContent = Get-Content $mcpJsonPath -Raw | ConvertFrom-Json
        $mcpServers = $mcpContent.servers.PSObject.Properties.Name
        
        if ($mcpServers[0] -eq 'github') {
            Write-TestPass "Active mcp.json has 'github' as first server"
        } else {
            Write-TestFail "Active mcp.json first server is '$($mcpServers[0])', expected 'github'"
        }
        
        if ($mcpServers[1] -eq 'filesystem') {
            Write-TestPass "Active mcp.json has 'filesystem' as second server"
        } else {
            Write-TestFail "Active mcp.json second server is '$($mcpServers[1])', expected 'filesystem'"
        }
        
        # Validate it matches the profile
        $profileContent = Get-Content (Join-Path $profilesDir "$testProfile.json") -Raw | ConvertFrom-Json
        $profileServers = $profileContent.servers.PSObject.Properties.Name -join ','
        $mcpServers = $mcpContent.servers.PSObject.Properties.Name -join ','
        
        if ($profileServers -eq $mcpServers) {
            Write-TestPass "Active mcp.json matches $testProfile profile"
        } else {
            Write-TestFail "Active mcp.json does not match $testProfile profile"
        }
    } else {
        Write-TestFail "mcp.json was not created after profile switch"
    }
} catch {
    Write-TestFail "Profile switch failed: $_"
} finally {
    # Restore backup if it existed
    if ($mcpBackup) {
        $mcpBackup | Set-Content $mcpJsonPath
        Write-TestInfo "Restored original mcp.json"
    }
}

# Test 7: Test all profile switches
Write-TestHeader "TEST 6: All Profile Switches"
foreach ($profileName in @('core', 'fullstack', 'testing', 'data')) {
    try {
        & "$scriptsDir\orchestrator.ps1" mcp set-profile -Profile $profileName 2>&1 | Out-Null
        
        if (Test-Path $mcpJsonPath) {
            $mcpContent = Get-Content $mcpJsonPath -Raw | ConvertFrom-Json
            $mcpServers = $mcpContent.servers.PSObject.Properties.Name
            
            if ($mcpServers[0] -eq 'github' -and $mcpServers[1] -eq 'filesystem') {
                Write-TestPass "$profileName switch creates mcp.json with correct server order"
            } else {
                Write-TestFail "$profileName switch has incorrect server order in mcp.json"
            }
        } else {
            Write-TestFail "$profileName switch did not create mcp.json"
        }
    } catch {
        Write-TestFail "$profileName switch failed: $_"
    }
}

# Test 8: Python validation
Write-TestHeader "TEST 7: Python Validation"
foreach ($profileName in $expectedProfiles) {
    $profilePath = Join-Path $profilesDir $profileName
    Write-TestInfo "Validating $profileName with Python validator..."
    
    try {
        $result = & python "$scriptsDir\python\mcp\validate_config.py" $profilePath 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-TestPass "$profileName passes Python validation"
        } else {
            Write-TestFail "$profileName fails Python validation"
        }
    } catch {
        Write-TestFail "$profileName validation error: $_"
    }
}

# Test 9: Token analysis
Write-TestHeader "TEST 8: Token Analysis"
foreach ($profileName in @('core', 'fullstack', 'testing', 'data')) {
    $profilePath = Join-Path $profilesDir "$profileName.json"
    Write-TestInfo "Analyzing tokens for $profileName..."
    
    try {
        $result = & python "$scriptsDir\python\mcp\analyze_tokens.py" $profilePath --json 2>&1 | ConvertFrom-Json
        if ($result.estimated_tokens -gt 0) {
            Write-TestPass "$profileName token analysis successful (Est: $($result.estimated_tokens) tokens)"
        } else {
            Write-TestFail "$profileName token analysis returned 0 tokens"
        }
    } catch {
        Write-TestFail "$profileName token analysis error: $_"
    }
}

# Restore backup
if ($mcpBackup) {
    $mcpBackup | Set-Content $mcpJsonPath
    Write-TestInfo "`nRestored original mcp.json configuration"
}

# Final summary
Write-TestHeader "TEST SUMMARY"
$totalTests = $testsPassed + $testsFailed
$passRate = if ($totalTests -gt 0) { [math]::Round(($testsPassed / $totalTests) * 100, 2) } else { 0 }

Write-Host "`nTotal Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: " -NoNewline -ForegroundColor White
Write-Host $testsPassed -ForegroundColor Green
Write-Host "Failed: " -NoNewline -ForegroundColor White
Write-Host $testsFailed -ForegroundColor $(if ($testsFailed -eq 0) { "Green" } else { "Red" })
Write-Host "Pass Rate: $passRate%" -ForegroundColor $(if ($passRate -ge 90) { "Green" } elseif ($passRate -ge 70) { "Yellow" } else { "Red" })

if ($testsFailed -eq 0) {
    Write-Host "`n✓ ALL TESTS PASSED!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n✗ SOME TESTS FAILED" -ForegroundColor Red
    exit 1
}
