#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Validate Python 3.14.0 installation and repository compatibility.

.DESCRIPTION
    Comprehensive validation of Python 3.14.0 installation including:
    - Python version check
    - PATH configuration
    - pip functionality
    - Required packages installation
    - Repository scripts compatibility

.EXAMPLE
    .\validate-python.ps1 -Verbose

.NOTES
    Part of scripts reorganization (SRP/DRY principles)
    Ensures full compatibility between Python and repository
#>

[CmdletBinding()]
param(
    [switch]$InstallDependencies,
    [switch]$RunTests
)

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

function Test-PythonCommand {
    Write-Header "Testing Python Command"
    
    try {
        $version = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ python --version: $version" -Color Green
            
            if ($version -like "*3.14.*") {
                Write-ColorOutput "  ✓ Python 3.14.x detected" -Color Green
                return $true
            }
            else {
                Write-ColorOutput "  ✗ Wrong version: Expected 3.14.x, got $version" -Color Red
                return $false
            }
        }
        else {
            Write-ColorOutput "  ✗ python command failed" -Color Red
            return $false
        }
    }
    catch {
        Write-ColorOutput "  ✗ python command not found: $_" -Color Red
        return $false
    }
}

function Test-PythonPath {
    Write-Header "Testing Python PATH"
    
    try {
        $pythonPath = where.exe python 2>&1 | Select-Object -First 1
        
        if ($pythonPath -and $LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ python.exe location: $pythonPath" -Color Green
            
            if ($pythonPath -like "*Python314*") {
                Write-ColorOutput "  ✓ Correct Python 3.14 path" -Color Green
                return $true
            }
            elseif ($pythonPath -like "*WindowsApps*") {
                Write-ColorOutput "  ✗ Windows App Alias still active!" -Color Red
                Write-ColorOutput "    Please disable in Settings → Apps → App execution aliases" -Color Yellow
                return $false
            }
            else {
                Write-ColorOutput "  ⚠ Unexpected path (not Python314)" -Color Yellow
                return $true
            }
        }
        else {
            Write-ColorOutput "  ✗ python.exe not in PATH" -Color Red
            return $false
        }
    }
    catch {
        Write-ColorOutput "  ✗ PATH test failed: $_" -Color Red
        return $false
    }
}

function Test-PipCommand {
    Write-Header "Testing Pip Command"
    
    try {
        $pipVersion = pip --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ pip --version: $($pipVersion -split "`n" | Select-Object -First 1)" -Color Green
            return $true
        }
        else {
            Write-ColorOutput "  ✗ pip command failed" -Color Red
            return $false
        }
    }
    catch {
        Write-ColorOutput "  ✗ pip command not found: $_" -Color Red
        return $false
    }
}

function Test-RequiredPackages {
    Write-Header "Checking Required Packages"
    
    $requiredPackages = @("uv", "black", "ruff", "mypy", "yamllint", "pytest")
    
    try {
        $installedPackages = pip list --format=freeze 2>&1
        
        $missing = @()
        foreach ($package in $requiredPackages) {
            if ($installedPackages -match "^$package==") {
                $version = ($installedPackages | Select-String "^$package==").ToString().Split("==")[1]
                Write-ColorOutput "  ✓ $package ($version)" -Color Green
            }
            else {
                Write-ColorOutput "  ✗ $package (not installed)" -Color Red
                $missing += $package
            }
        }
        
        if ($missing.Count -gt 0) {
            Write-ColorOutput "`n  Missing $($missing.Count) package(s)" -Color Yellow
            
            if ($InstallDependencies) {
                Write-ColorOutput "  Installing missing packages..." -Color Cyan
                pip install -r requirements.txt --quiet
                Write-ColorOutput "  ✓ Dependencies installed" -Color Green
                return $true
            }
            else {
                Write-ColorOutput "  Run with -InstallDependencies to install" -Color Yellow
                return $false
            }
        }
        
        return $true
    }
    catch {
        Write-ColorOutput "  ✗ Package check failed: $_" -Color Red
        return $false
    }
}

function Test-RepositoryScripts {
    Write-Header "Testing Repository Scripts"
    
    $scripts = @(
        "scripts\python\validation\validate_env.py",
        "scripts\python\validation\validate_configs.py"
    )
    
    $allPassed = $true
    foreach ($script in $scripts) {
        $scriptPath = Join-Path $PSScriptRoot "..\..\..\$script"
        
        if (Test-Path $scriptPath) {
            Write-ColorOutput "  Testing: $script" -Color Cyan
            
            try {
                python $scriptPath --help 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 2) {
                    Write-ColorOutput "    ✓ Script executable" -Color Green
                }
                else {
                    Write-ColorOutput "    ✗ Script execution failed (exit code: $LASTEXITCODE)" -Color Red
                    $allPassed = $false
                }
            }
            catch {
                Write-ColorOutput "    ✗ Script error: $_" -Color Red
                $allPassed = $false
            }
        }
        else {
            Write-ColorOutput "  ✗ Script not found: $script" -Color Red
            $allPassed = $false
        }
    }
    
    return $allPassed
}

function Test-Orchestrators {
    Write-Header "Testing Orchestrators"
    
    $orchestrators = @(
        @{Path = "scripts\orchestrator.ps1"; Command = "powershell"; Args = @("-File") }
        @{Path = "scripts\orchestrator.py"; Command = "python"; Args = @() }
    )
    
    $allPassed = $true
    foreach ($orch in $orchestrators) {
        $orchPath = Join-Path $PSScriptRoot "..\..\..\$($orch.Path)"
        
        if (Test-Path $orchPath) {
            Write-ColorOutput "  Testing: $($orch.Path)" -Color Cyan
            
            try {
                if ($orch.Args.Count -gt 0) {
                    $null = & $orch.Command $orch.Args $orchPath help 2>&1
                }
                else {
                    $null = & $orch.Command $orchPath help 2>&1
                }

                if ($LASTEXITCODE -eq 0) {
                    Write-ColorOutput "    ✓ Orchestrator working" -Color Green
                }
                else {
                    Write-ColorOutput "    ✗ Orchestrator failed (exit code: $LASTEXITCODE)" -Color Red
                    $allPassed = $false
                }
            }
            catch {
                Write-ColorOutput "    ✗ Orchestrator error: $_" -Color Red
                $allPassed = $false
            }
        }
        else {
            Write-ColorOutput "  ✗ Orchestrator not found: $($orch.Path)" -Color Red
            $allPassed = $false
        }
    }
    
    return $allPassed
}

function Get-ValidationSummary {
    param(
        [bool]$PythonCmd,
        [bool]$PythonPath,
        [bool]$PipCmd,
        [bool]$Packages,
        [bool]$Scripts,
        [bool]$Orchestrators
    )
    
    Write-Header "Validation Summary"
    
    $results = @(
        @{Name = "Python Command"; Status = $PythonCmd },
        @{Name = "Python PATH"; Status = $PythonPath },
        @{Name = "Pip Command"; Status = $PipCmd },
        @{Name = "Required Packages"; Status = $Packages },
        @{Name = "Repository Scripts"; Status = $Scripts },
        @{Name = "Orchestrators"; Status = $Orchestrators }
    )
    
    $passed = 0
    $failed = 0
    
    foreach ($result in $results) {
        if ($result.Status) {
            Write-ColorOutput "  ✓ $($result.Name)" -Color Green
            $passed++
        }
        else {
            Write-ColorOutput "  ✗ $($result.Name)" -Color Red
            $failed++
        }
    }
    
    Write-ColorOutput "`nResults: $passed passed, $failed failed" -Color $(if ($failed -eq 0) { "Green" } else { "Yellow" })
    
    return $failed -eq 0
}

# Main execution
Write-ColorOutput "`n╔══════════════════════════════════════════════════════════╗" -Color Cyan
Write-ColorOutput "║      Python 3.14.0 Validation Script                   ║" -Color Cyan
Write-ColorOutput "╚══════════════════════════════════════════════════════════╝" -Color Cyan

# Run all tests
$pythonCmdOk = Test-PythonCommand
$pythonPathOk = Test-PythonPath
$pipCmdOk = Test-PipCommand
$packagesOk = Test-RequiredPackages
$scriptsOk = Test-RepositoryScripts
$orchestratorsOk = Test-Orchestrators

# Show summary
$allValid = Get-ValidationSummary -PythonCmd $pythonCmdOk -PythonPath $pythonPathOk -PipCmd $pipCmdOk -Packages $packagesOk -Scripts $scriptsOk -Orchestrators $orchestratorsOk

if ($allValid) {
    Write-ColorOutput "`n✓ ALL VALIDATIONS PASSED!" -Color Green
    Write-ColorOutput "  Python 3.14.0 is properly configured" -Color Green
    Write-ColorOutput "  Repository is fully compatible" -Color Green
    exit 0
}
else {
    Write-ColorOutput "`n✗ VALIDATION FAILED" -Color Red
    Write-ColorOutput "  Please review errors above" -Color Yellow
    
    if (-not $InstallDependencies -and -not $packagesOk) {
        Write-ColorOutput "`n  Tip: Run with -InstallDependencies to install missing packages" -Color Cyan
    }
    
    exit 1
}
