#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Serves GitHub Pages documentation locally.

.DESCRIPTION
    This script installs Jekyll dependencies and serves the documentation
    site locally for development and preview.

.EXAMPLE
    .\scripts\serve_docs.ps1
#>

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)

Set-Location $ProjectRoot

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  GitHub Pages - Local Server" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Ruby is installed
try {
    $rubyVersion = ruby --version
    Write-Host "✓ Ruby installed: $rubyVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Ruby is not installed!" -ForegroundColor Red
    Write-Host "Please install Ruby: https://www.ruby-lang.org/en/downloads/" -ForegroundColor Yellow
    Write-Host "Or use Windows Subsystem for Linux (WSL)" -ForegroundColor Yellow
    exit 1
}

# Check if Bundler is installed
try {
    bundle --version | Out-Null
    Write-Host "✓ Bundler installed" -ForegroundColor Green
} catch {
    Write-Host "Installing Bundler..." -ForegroundColor Yellow
    gem install bundler
}

# Install dependencies
Write-Host "`nInstalling Jekyll dependencies..." -ForegroundColor Yellow
bundle install

# Serve the site
Write-Host ""
Write-Host "Starting Jekyll server..." -ForegroundColor Green
Write-Host "Site will be available at: http://localhost:4000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload
