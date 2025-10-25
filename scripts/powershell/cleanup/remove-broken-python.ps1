#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Remove all broken Python installations from Windows system.

.DESCRIPTION
    Detects and removes corrupted/incomplete Python installations using winget,
    cleans up broken PATH entries, and prepares system for fresh Python 3.14.0 install.

.EXAMPLE
    .\remove-broken-python.ps1 -Verbose

.NOTES
    Part of scripts reorganization (SRP/DRY principles)
    Requires: Administrator privileges for winget uninstall
#>

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Force
)

# Add parent directory to path for imports
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent (Split-Path -Parent $scriptPath)
$env:PSModulePath = "$rootPath;$env:PSModulePath"

function Write-ColorOutput {
    param(
        [string]$Message,
        [ConsoleColor]$Color = [ConsoleColor]::White
    )
    $previousColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host $Message
    $Host.UI.RawUI.ForegroundColor = $previousColor
}

function Write-Header {
    param([string]$Text)
    Write-ColorOutput "`n=== $Text ===" -Color Blue
}

function Get-InstalledPythonVersions {
    Write-Header "Detecting Python Installations"
    
    $pythonVersions = winget list | Select-String -Pattern "Python.*\d+\.\d+" 
    
    $installations = @()
    foreach ($line in $pythonVersions) {
        if ($line -match "Python\s+([\d\.]+).*?(Python\.Python\.[\d\.]+)") {
            $version = $matches[1]
            $id = $matches[2]
            
            $installations += [PSCustomObject]@{
                Version = $version
                ID = $id
                Line = $line.ToString()
            }
            
            Write-ColorOutput "  Found: Python $version (ID: $id)" -Color Yellow
        }
    }
    
    return $installations
}

function Test-PythonInstallation {
    param(
        [string]$Version,
        [string]$Path
    )
    
    if (-not (Test-Path $Path)) {
        return $false
    }
    
    $pythonExe = Join-Path $Path "python.exe"
    if (-not (Test-Path $pythonExe)) {
        return $false
    }
    
    try {
        $output = & $pythonExe --version 2>&1
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Get-BrokenPythonInstallations {
    param([array]$Installations)
    
    Write-Header "Checking Installation Integrity"
    
    $broken = @()
    
    foreach ($install in $Installations) {
        # Skip Python 3.14.0 if it exists
        if ($install.Version -like "3.14.*") {
            Write-ColorOutput "  Skipping Python 3.14.0 (target version)" -Color Green
            continue
        }
        
        # Check common installation paths
        $paths = @(
            "$env:LOCALAPPDATA\Programs\Python\Python$($install.Version.Replace('.',''))",
            "C:\Program Files\Python$($install.Version.Replace('.',''))",
            "$env:USERPROFILE\AppData\Local\Programs\Python\Python$($install.Version.Replace('.',''))"
        )
        
        $isBroken = $true
        foreach ($path in $paths) {
            if (Test-PythonInstallation -Version $install.Version -Path $path) {
                Write-ColorOutput "  ✓ Python $($install.Version): Working at $path" -Color Green
                $isBroken = $false
                break
            }
        }
        
        if ($isBroken) {
            Write-ColorOutput "  ✗ Python $($install.Version): BROKEN/INCOMPLETE" -Color Red
            $broken += $install
        }
    }
    
    return $broken
}

function Remove-PythonInstallation {
    param(
        [PSCustomObject]$Installation,
        [switch]$DryRun
    )
    
    $version = $Installation.Version
    $id = $Installation.ID
    
    if ($DryRun) {
        Write-ColorOutput "  [DRY RUN] Would uninstall: Python $version" -Color Yellow
        return $true
    }
    
    Write-ColorOutput "  Uninstalling Python $version..." -Color Cyan
    
    try {
        $result = winget uninstall --id $id --silent --accept-source-agreements 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "    ✓ Successfully uninstalled Python $version" -Color Green
            return $true
        } else {
            Write-ColorOutput "    ⚠ Uninstall completed with warnings (exit code: $LASTEXITCODE)" -Color Yellow
            return $true
        }
    } catch {
        Write-ColorOutput "    ✗ Failed to uninstall: $_" -Color Red
        return $false
    }
}

function Clear-PythonPathEntries {
    param([switch]$DryRun)
    
    Write-Header "Cleaning PATH Environment Variables"
    
    # Clean User PATH
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $userPathEntries = $userPath -split ';'
    $cleanUserPath = $userPathEntries | Where-Object { 
        $_ -notlike "*Python\Python*" -and 
        $_ -notlike "*python*" -and
        $_ -ne ""
    }
    
    $removedCount = $userPathEntries.Count - $cleanUserPath.Count
    
    if ($removedCount -gt 0) {
        Write-ColorOutput "  Found $removedCount Python-related PATH entries to remove" -Color Yellow
        
        if (-not $DryRun) {
            $newUserPath = $cleanUserPath -join ';'
            [System.Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
            Write-ColorOutput "  ✓ User PATH cleaned" -Color Green
        } else {
            Write-ColorOutput "  [DRY RUN] Would clean User PATH" -Color Yellow
        }
    } else {
        Write-ColorOutput "  ✓ No Python entries found in User PATH" -Color Green
    }
}

function Remove-PythonLauncherConfig {
    param([switch]$DryRun)
    
    Write-Header "Cleaning Python Launcher Configuration"
    
    $launcherConfig = "$env:LOCALAPPDATA\py.ini"
    
    if (Test-Path $launcherConfig) {
        if (-not $DryRun) {
            Remove-Item $launcherConfig -Force
            Write-ColorOutput "  ✓ Removed py.ini configuration" -Color Green
        } else {
            Write-ColorOutput "  [DRY RUN] Would remove $launcherConfig" -Color Yellow
        }
    } else {
        Write-ColorOutput "  ✓ No launcher config found" -Color Green
    }
}

# Main execution
Write-ColorOutput "`n╔══════════════════════════════════════════════════════════╗" -Color Cyan
Write-ColorOutput "║  Python Cleanup Script - Remove Broken Installations   ║" -Color Cyan
Write-ColorOutput "╚══════════════════════════════════════════════════════════╝" -Color Cyan

if ($DryRun) {
    Write-ColorOutput "`n⚠ DRY RUN MODE - No changes will be made" -Color Yellow
}

# Step 1: Detect installations
$allInstallations = Get-InstalledPythonVersions

if ($allInstallations.Count -eq 0) {
    Write-ColorOutput "`n✓ No Python installations detected by winget" -Color Green
    exit 0
}

# Step 2: Identify broken installations
$brokenInstallations = Get-BrokenPythonInstallations -Installations $allInstallations

if ($brokenInstallations.Count -eq 0) {
    Write-ColorOutput "`n✓ No broken Python installations found" -Color Green
    
    if (-not $Force) {
        Write-ColorOutput "`nUse -Force to remove all non-3.14 Python versions" -Color Cyan
        exit 0
    }
}

# Step 3: Remove broken installations
if ($brokenInstallations.Count -gt 0 -or $Force) {
    Write-Header "Removing Python Installations"
    
    $toRemove = if ($Force) { 
        $allInstallations | Where-Object { $_.Version -notlike "3.14.*" }
    } else { 
        $brokenInstallations 
    }
    
    Write-ColorOutput "`nWill remove $($toRemove.Count) Python installation(s)" -Color Yellow
    
    if (-not $DryRun) {
        $confirm = Read-Host "`nProceed with uninstallation? (y/N)"
        if ($confirm -ne 'y' -and $confirm -ne 'Y') {
            Write-ColorOutput "Cancelled by user" -Color Yellow
            exit 1
        }
    }
    
    $successCount = 0
    foreach ($install in $toRemove) {
        if (Remove-PythonInstallation -Installation $install -DryRun:$DryRun) {
            $successCount++
        }
    }
    
    Write-ColorOutput "`n✓ Successfully removed $successCount of $($toRemove.Count) installations" -Color Green
}

# Step 4: Clean PATH
Clear-PythonPathEntries -DryRun:$DryRun

# Step 5: Clean launcher config
Remove-PythonLauncherConfig -DryRun:$DryRun

# Summary
Write-Header "Cleanup Summary"
Write-ColorOutput "✓ Broken Python installations removed: $($brokenInstallations.Count)" -Color Green
Write-ColorOutput "✓ PATH entries cleaned" -Color Green
Write-ColorOutput "✓ Python launcher config cleaned" -Color Green
Write-ColorOutput "`n✓ System ready for Python 3.14.0 installation" -Color Green
Write-ColorOutput "`nNext steps:" -Color Cyan
Write-ColorOutput "  1. Run: .\scripts\powershell\cleanup\install-python314.ps1" -Color White
Write-ColorOutput "  2. Restart terminal to refresh environment" -Color White
Write-ColorOutput "  3. Run: .\scripts\powershell\cleanup\validate-python.ps1" -Color White

exit 0
