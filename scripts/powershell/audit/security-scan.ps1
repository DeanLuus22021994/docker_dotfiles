<#
.SYNOPSIS
    Security vulnerability scan for Docker images and dependencies.

.DESCRIPTION
    Scans Docker images (Trivy), Python dependencies (pip-audit),
    Node.js dependencies (npm audit), and secrets (gitleaks).

.PARAMETER Target
    What to scan: All, Docker, Python, Node, Secrets

.PARAMETER OutputFormat
    Report format: Console, JSON, HTML

.PARAMETER OutputPath
    Path to save report (default: ./security-report)

.PARAMETER FailOnCritical
    Exit with error code if critical vulnerabilities found

.EXAMPLE
    .\security-scan.ps1
    Scan everything and display in console

.EXAMPLE
    .\security-scan.ps1 -Target Docker -OutputFormat HTML -OutputPath ./reports

.NOTES
    Version: 1.0
    Author: Cluster Dashboard Team
    Last Modified: 2025-10-26
    Requires: Trivy, Python 3.14, Node.js 22, gitleaks
#>

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet('All', 'Docker', 'Python', 'Node', 'Secrets')]
    [string]$Target = 'All',

    [Parameter()]
    [ValidateSet('Console', 'JSON', 'HTML')]
    [string]$OutputFormat = 'Console',

    [Parameter()]
    [string]$OutputPath = ".\security-report",

    [Parameter()]
    [switch]$FailOnCritical
)

$ErrorActionPreference = 'Continue'

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Security Vulnerability Scanner" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$reportDir = Join-Path $OutputPath $timestamp
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null

$criticalFound = $false
$results = @{
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Target = $Target
    Scans = @()
}

# Docker Image Scanning with Trivy
if ($Target -in 'All', 'Docker') {
    Write-Host "Scanning Docker images with Trivy..." -ForegroundColor Cyan
    
    # Check if Trivy is installed
    $trivyInstalled = Get-Command trivy -ErrorAction SilentlyContinue
    if (-not $trivyInstalled) {
        Write-Warning "Trivy not installed. Install: https://github.com/aquasecurity/trivy"
    } else {
        $images = docker images --format "{{.Repository}}:{{.Tag}}" | Where-Object { $_ -notmatch '<none>' }
        
        foreach ($image in $images) {
            Write-Host "  Scanning: $image" -ForegroundColor Gray
            $trivyOutput = trivy image --severity CRITICAL,HIGH --format json $image 2>&1 | ConvertFrom-Json
            
            $vulnCount = ($trivyOutput.Results | ForEach-Object { $_.Vulnerabilities } | Measure-Object).Count
            if ($vulnCount -gt 0) {
                $criticalCount = ($trivyOutput.Results | ForEach-Object { $_.Vulnerabilities | Where-Object { $_.Severity -eq 'CRITICAL' } } | Measure-Object).Count
                
                if ($criticalCount -gt 0) {
                    $criticalFound = $true
                    Write-Host "    ✗ CRITICAL vulnerabilities found: $criticalCount" -ForegroundColor Red
                } else {
                    Write-Host "    ⚠ HIGH vulnerabilities found: $vulnCount" -ForegroundColor Yellow
                }
                
                $results.Scans += @{
                    Type = "Docker"
                    Target = $image
                    Critical = $criticalCount
                    High = $vulnCount - $criticalCount
                    Details = $trivyOutput
                }
            } else {
                Write-Host "    ✓ No vulnerabilities" -ForegroundColor Green
            }
        }
        
        # Save Trivy report
        trivy image --severity CRITICAL,HIGH --format table --output (Join-Path $reportDir "trivy-report.txt") $images[0]
    }
}

# Python Dependencies with pip-audit
if ($Target -in 'All', 'Python') {
    Write-Host "`nScanning Python dependencies with pip-audit..." -ForegroundColor Cyan
    
    try {
        $pipAudit = pip-audit --format json 2>&1 | ConvertFrom-Json
        $vulnCount = ($pipAudit.dependencies | Measure-Object).Count
        
        if ($vulnCount -gt 0) {
            Write-Host "  ✗ Vulnerabilities found: $vulnCount" -ForegroundColor Red
            $criticalFound = $true
            $results.Scans += @{
                Type = "Python"
                Target = "pyproject.toml"
                Count = $vulnCount
                Details = $pipAudit
            }
        } else {
            Write-Host "  ✓ No vulnerabilities" -ForegroundColor Green
        }
        
        pip-audit --format json --output (Join-Path $reportDir "pip-audit.json")
    } catch {
        Write-Warning "pip-audit failed: $($_.Exception.Message)"
    }
}

# Node.js Dependencies with npm audit
if ($Target -in 'All', 'Node') {
    Write-Host "`nScanning Node.js dependencies..." -ForegroundColor Cyan
    
    $npmDirs = @(".\api", ".\web-content")
    foreach ($dir in $npmDirs) {
        if (Test-Path (Join-Path $dir "package.json")) {
            Write-Host "  Scanning: $dir" -ForegroundColor Gray
            Push-Location $dir
            
            try {
                $npmAudit = npm audit --json 2>&1 | ConvertFrom-Json
                $criticalCount = $npmAudit.metadata.vulnerabilities.critical
                $highCount = $npmAudit.metadata.vulnerabilities.high
                
                if ($criticalCount -gt 0) {
                    Write-Host "    ✗ CRITICAL: $criticalCount" -ForegroundColor Red
                    $criticalFound = $true
                }
                if ($highCount -gt 0) {
                    Write-Host "    ⚠ HIGH: $highCount" -ForegroundColor Yellow
                }
                if ($criticalCount -eq 0 -and $highCount -eq 0) {
                    Write-Host "    ✓ No high/critical vulnerabilities" -ForegroundColor Green
                }
                
                $results.Scans += @{
                    Type = "Node"
                    Target = $dir
                    Critical = $criticalCount
                    High = $highCount
                    Details = $npmAudit
                }
                
                npm audit --json | Out-File (Join-Path $reportDir "npm-audit-$($dir -replace '\\|/', '-').json")
            } catch {
                Write-Warning "npm audit failed for $dir"
            }
            
            Pop-Location
        }
    }
}

# Secret Scanning with gitleaks
if ($Target -in 'All', 'Secrets') {
    Write-Host "`nScanning for exposed secrets with gitleaks..." -ForegroundColor Cyan
    
    $gitleaksInstalled = Get-Command gitleaks -ErrorAction SilentlyContinue
    if (-not $gitleaksInstalled) {
        Write-Warning "gitleaks not installed. Install: https://github.com/gitleaks/gitleaks"
    } else {
        try {
            gitleaks detect --no-git --report-path (Join-Path $reportDir "gitleaks-report.json") --report-format json
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ No secrets found" -ForegroundColor Green
            } else {
                Write-Host "  ✗ Secrets detected! Review report." -ForegroundColor Red
                $criticalFound = $true
            }
        } catch {
            Write-Warning "gitleaks scan failed"
        }
    }
}

# Generate summary report
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Scan Complete" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($OutputFormat -eq 'JSON') {
    $results | ConvertTo-Json -Depth 10 | Out-File (Join-Path $reportDir "summary.json")
    Write-Host "Report saved: $(Join-Path $reportDir 'summary.json')" -ForegroundColor Cyan
}

if ($OutputFormat -eq 'HTML') {
    $html = @"
<!DOCTYPE html>
<html><head><title>Security Scan Report</title>
<style>body{font-family:Arial;margin:20px}h1{color:#333}.critical{color:red}.high{color:orange}.ok{color:green}</style>
</head><body><h1>Security Scan Report</h1><p>Timestamp: $($results.Timestamp)</p>
<h2>Results</h2><ul>
$(($results.Scans | ForEach-Object { "<li>$($_.Type): $($_.Target) - Critical: $($_.Critical), High: $($_.High)</li>" }) -join "`n")
</ul></body></html>
"@
    $html | Out-File (Join-Path $reportDir "summary.html")
    Write-Host "Report saved: $(Join-Path $reportDir 'summary.html')" -ForegroundColor Cyan
}

Write-Host "Reports directory: $reportDir`n" -ForegroundColor Cyan

if ($criticalFound -and $FailOnCritical) {
    Write-Error "Critical vulnerabilities found!"
    exit 1
}

Write-Host "Security scan complete ✓`n" -ForegroundColor Green
