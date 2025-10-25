#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Integration test for environment variables and devcontainer setup.

.DESCRIPTION
    Tests that all environment variables are properly configured and
    the devcontainer can be started with the full stack.

.EXAMPLE
    .\scripts\test_integration.ps1
#>

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $PSCommandPath
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  Integration Test Suite" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$TestResults = @{
    Passed = 0
    Failed = 0
    Tests = @()
}

function Test-Step {
    param(
        [string]$Name,
        [scriptblock]$Test
    )
    
    Write-Host "`n[TEST] $Name..." -ForegroundColor Yellow
    try {
        & $Test
        Write-Host "[PASS] $Name" -ForegroundColor Green
        $TestResults.Passed++
        $TestResults.Tests += @{ Name = $Name; Result = "PASS" }
        return $true
    } catch {
        Write-Host "[FAIL] $Name : $_" -ForegroundColor Red
        $TestResults.Failed++
        $TestResults.Tests += @{ Name = $Name; Result = "FAIL"; Error = $_ }
        return $false
    }
}

Set-Location $ProjectRoot

# Test 1: Environment Variables
Test-Step "Environment Variables Validation" {
    $validateScript = Join-Path $ScriptDir "validate_env.ps1"
    & $validateScript
    if ($LASTEXITCODE -ne 0) {
        throw "Environment validation failed"
    }
}

# Test 2: Docker Compose Configuration
Test-Step "Docker Compose Configuration" {
    $output = docker-compose config -q 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose config validation failed: $output"
    }
}

# Test 3: Required Files Exist
Test-Step "Required Files Exist" {
    $requiredFiles = @(
        "docker-compose.yml",
        ".devcontainer/devcontainer.json",
        ".github/workflows/ci.yml",
        "scripts/validate_env.py",
        "scripts/validate_env.ps1",
        "scripts/start_devcontainer.sh",
        "scripts/start_devcontainer.ps1",
        ".env.example"
    )
    
    foreach ($file in $requiredFiles) {
        $filePath = Join-Path $ProjectRoot $file
        if (-not (Test-Path $filePath)) {
            throw "Required file not found: $file"
        }
    }
}

# Test 4: DevContainer Configuration
Test-Step "DevContainer Configuration" {
    $devcontainerPath = Join-Path $ProjectRoot ".devcontainer/devcontainer.json"
    $config = Get-Content $devcontainerPath | ConvertFrom-Json
    
    if ($config.service -ne "devcontainer") {
        throw "DevContainer service name mismatch"
    }
    
    if ($config.dockerComposeFile -ne "../docker-compose.yml") {
        throw "DevContainer docker-compose file path incorrect"
    }
    
    # Check runServices includes key services
    $requiredServices = @(
        "cluster-postgres",
        "cluster-redis",
        "cluster-grafana",
        "cluster-prometheus",
        "cluster-docker-api"
    )
    
    foreach ($service in $requiredServices) {
        if ($config.runServices -notcontains $service) {
            throw "DevContainer missing required service: $service"
        }
    }
}

# Test 5: Docker Compose Services
Test-Step "Docker Compose Services Configuration" {
    # Check devcontainer service is defined
    $composeContent = Get-Content (Join-Path $ProjectRoot "docker-compose.yml") -Raw
    
    if ($composeContent -notmatch 'devcontainer:') {
        throw "DevContainer service not found in docker-compose.yml"
    }
    
    # Check devcontainer has profile
    if ($composeContent -notmatch 'profiles:\s*\[\s*"dev"\s*\]') {
        throw "DevContainer dev profile not configured"
    }
    
    # Check environment variables are passed
    if ($composeContent -notmatch 'GITHUB_OWNER') {
        throw "DevContainer environment variables not configured"
    }
}

# Test 6: CI/CD Workflow
Test-Step "CI/CD Workflow Configuration" {
    $workflowPath = Join-Path $ProjectRoot ".github/workflows/ci.yml"
    $workflow = Get-Content $workflowPath -Raw
    
    # Check environment variables are defined
    if ($workflow -notmatch 'GITHUB_OWNER') {
        throw "CI/CD workflow missing GITHUB_OWNER"
    }
    
    if ($workflow -notmatch 'GH_PAT') {
        throw "CI/CD workflow missing GH_PAT"
    }
    
    if ($workflow -notmatch 'DOCKER_ACCESS_TOKEN') {
        throw "CI/CD workflow missing DOCKER_ACCESS_TOKEN"
    }
}

# Test 7: Volume Mounts
Test-Step "Volume Mount Configuration" {
    $dockerComposeContent = Get-Content (Join-Path $ProjectRoot "docker-compose.yml") -Raw
    
    # Check devcontainer has workspace mount
    if ($dockerComposeContent -notmatch '/workspaces/docker') {
        throw "DevContainer workspace mount not configured"
    }
    
    # Check Docker socket mount
    if ($dockerComposeContent -notmatch '/var/run/docker.sock') {
        throw "Docker socket mount not configured"
    }
}

# Test 8: Network Configuration
Test-Step "Network Configuration" {
    $dockerComposeContent = Get-Content (Join-Path $ProjectRoot "docker-compose.yml") -Raw
    
    if ($dockerComposeContent -notmatch 'cluster-network') {
        throw "Cluster network not defined"
    }
}

# Print Summary
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  Test Summary" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "`nTotal Tests: $($TestResults.Passed + $TestResults.Failed)" -ForegroundColor White
Write-Host "Passed: $($TestResults.Passed)" -ForegroundColor Green
Write-Host "Failed: $($TestResults.Failed)" -ForegroundColor Red

if ($TestResults.Failed -gt 0) {
    Write-Host "`nFailed Tests:" -ForegroundColor Red
    foreach ($test in $TestResults.Tests | Where-Object { $_.Result -eq "FAIL" }) {
        Write-Host "  ✗ $($test.Name)" -ForegroundColor Red
        if ($test.Error) {
            Write-Host "    Error: $($test.Error)" -ForegroundColor DarkRed
        }
    }
}

Write-Host "`n=========================================" -ForegroundColor Cyan

if ($TestResults.Failed -eq 0) {
    Write-Host "✅ All tests passed!" -ForegroundColor Green
    Write-Host "`nYou can now:" -ForegroundColor Cyan
    Write-Host "  1. Start the stack: docker-compose --profile dev up -d"
    Write-Host "  2. Or use: .\scripts\start_devcontainer.ps1"
    Write-Host "  3. Attach to devcontainer in VS Code"
    exit 0
} else {
    Write-Host "❌ Some tests failed. Please fix the issues above." -ForegroundColor Red
    exit 1
}
