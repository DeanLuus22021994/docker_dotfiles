#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Starts the Docker cluster stack with devcontainer profile.

.DESCRIPTION
    This script validates environment variables and starts all services
    including the devcontainer for pre-production testing.

.EXAMPLE
    .\scripts\start_devcontainer.ps1
#>

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $PSCommandPath
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Docker Cluster Stack - DevContainer" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Validate environment variables
Write-Host "Step 1: Validating environment variables..." -ForegroundColor Yellow
$validateScript = Join-Path $ScriptDir "validate_env.ps1"
if (Test-Path $validateScript) {
    & $validateScript
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ Environment validation failed!" -ForegroundColor Red
        Write-Host "Please fix the issues above and try again." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⚠️  Warning: validate_env.ps1 not found, skipping validation" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Starting Docker Compose stack with devcontainer profile..." -ForegroundColor Yellow
Set-Location $ProjectRoot

# Start all services including devcontainer
docker-compose --profile dev up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Failed to start stack!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Waiting for services to become healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service health
Write-Host ""
docker-compose ps

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✅ Stack started successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services accessible at:" -ForegroundColor Cyan
Write-Host "  - Load Balancer:    http://localhost:8080"
Write-Host "  - React Dashboard:  http://localhost:3000"
Write-Host "  - Docker API:       http://localhost:3001"
Write-Host "  - Grafana:          http://localhost:3002"
Write-Host "  - Prometheus:       http://localhost:9090"
Write-Host "  - Alertmanager:     http://localhost:9093"
Write-Host "  - PostgreSQL:       localhost:5432"
Write-Host "  - Redis:            localhost:6379"
Write-Host "  - Jupyter Lab:      http://localhost:8888"
Write-Host "  - MinIO Console:    http://localhost:9001"
Write-Host "  - MailHog UI:       http://localhost:8025"
Write-Host "  - pgAdmin:          http://localhost:5050"
Write-Host ""
Write-Host "To attach to devcontainer:" -ForegroundColor Cyan
Write-Host "  1. Open VS Code"
Write-Host "  2. Run: 'Dev Containers: Attach to Running Container'"
Write-Host "  3. Select: cluster-devcontainer"
Write-Host ""
