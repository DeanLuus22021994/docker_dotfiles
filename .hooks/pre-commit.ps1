#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Platform-agnostic pre-commit hook using Docker
.DESCRIPTION
    Validates code quality using cluster-pre-commit container.
    No local Python/virtualenv installation required.
.NOTES
    Runs automatically on git commit
    Skip with: git commit --no-verify
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

Write-Host "Running pre-commit validation..." -ForegroundColor Cyan

# Verify Docker is available
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker not found. Please install Docker." -ForegroundColor Red
    exit 1
}

try {
    docker info 2>&1 | Out-Null
} catch {
    Write-Host "Error: Docker daemon not running. Please start Docker." -ForegroundColor Red
    exit 1
}

# Navigate to repository root
$repoRoot = git rev-parse --show-toplevel
Set-Location $repoRoot

# Build container if needed
$imageExists = docker image inspect cluster-pre-commit:latest 2>&1 | Select-String "cluster-pre-commit"
if (-not $imageExists) {
    Write-Host "Building pre-commit container..." -ForegroundColor Yellow
    docker build -q -f dockerfile/pre-commit.Dockerfile -t cluster-pre-commit . | Out-Null
}

# Get staged files
$stagedFiles = git diff --cached --name-only --diff-filter=ACM
if (-not $stagedFiles) {
    Write-Host "No staged files to validate" -ForegroundColor Yellow
    exit 0
}

# Run validation in container
$filesArg = $stagedFiles -join " "
Write-Host "Validating: $filesArg" -ForegroundColor Cyan

docker run --rm `
    -v "${repoRoot}:/workspace:rw" `
    --network none `
    cluster-pre-commit `
    bash -c "cd /workspace && git config --global --add safe.directory /workspace && pre-commit run --files $filesArg"

$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "❌ Pre-commit validation failed" -ForegroundColor Red
    Write-Host "Fix issues or skip with: git commit --no-verify" -ForegroundColor Yellow
    exit $exitCode
}

Write-Host "✓ All checks passed" -ForegroundColor Green
exit 0
