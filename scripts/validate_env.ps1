#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Validates and loads environment variables for the Docker cluster stack.

.DESCRIPTION
    This script validates that all required environment variables are set
    and provides helpful instructions for fixing any missing variables.

.EXAMPLE
    .\scripts\validate_env.ps1
#>

# Color definitions
$Colors = @{
    Green  = [ConsoleColor]::Green
    Yellow = [ConsoleColor]::Yellow
    Red    = [ConsoleColor]::Red
    Blue   = [ConsoleColor]::Blue
    Reset  = [ConsoleColor]::White
}

function Write-ColorOutput {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [ConsoleColor]$Color = [ConsoleColor]::White
    )
    $previousColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host $Message
    $Host.UI.RawUI.ForegroundColor = $previousColor
}

function Test-EnvironmentVariables {
    # Required environment variables
    $requiredVars = @{
        'GITHUB_OWNER' = 'GitHub organization/username for API access'
        'GH_PAT' = 'GitHub Personal Access Token for authentication'
    }
    
    # Optional but recommended environment variables
    $optionalVars = @{
        'DOCKER_ACCESS_TOKEN' = 'Docker Hub access token for increased pull limits'
        'CODECOV_TOKEN' = 'Codecov token for coverage reporting'
    }
    
    $missingRequired = @()
    $missingOptional = @()
    
    Write-Host "`n=== Environment Variables Validation ===`n" -ForegroundColor Blue
    
    # Check required variables
    Write-Host "Required Variables:" -ForegroundColor White
    foreach ($var in $requiredVars.Keys) {
        $value = [Environment]::GetEnvironmentVariable($var)
        if ($value) {
            $maskedValue = if ($value.Length -gt 8) { "$($value.Substring(0, 8))..." } else { "***" }
            Write-ColorOutput "  ✓ ${var}: $maskedValue" -Color $Colors.Green
        } else {
            Write-ColorOutput "  ✗ ${var}: NOT SET - $($requiredVars[$var])" -Color $Colors.Red
            $missingRequired += $var
        }
    }
    
    # Check optional variables
    Write-Host "`nOptional Variables:" -ForegroundColor White
    foreach ($var in $optionalVars.Keys) {
        $value = [Environment]::GetEnvironmentVariable($var)
        if ($value) {
            $maskedValue = if ($value.Length -gt 8) { "$($value.Substring(0, 8))..." } else { "***" }
            Write-ColorOutput "  ✓ ${var}: $maskedValue" -Color $Colors.Green
        } else {
            Write-ColorOutput "  ⚠ ${var}: NOT SET - $($optionalVars[$var])" -Color $Colors.Yellow
            $missingOptional += $var
        }
    }
    
    $allValid = $missingRequired.Count -eq 0
    
    return @{
        AllValid = $allValid
        MissingRequired = $missingRequired
        MissingOptional = $missingOptional
    }
}

function Show-Summary {
    param($result)
    
    Write-Host "`n$('='*60)" -ForegroundColor White
    
    if ($result.AllValid) {
        Write-ColorOutput "✓ All required environment variables are set!" -Color $Colors.Green
        
        if ($result.MissingOptional.Count -gt 0) {
            Write-Host "`n⚠ Optional variables missing:" -ForegroundColor Yellow
            foreach ($var in $result.MissingOptional) {
                Write-Host "  - $var" -ForegroundColor Yellow
            }
            Write-Host "`nConsider setting these for full functionality." -ForegroundColor Yellow
        }
        
        Write-Host "`nYou can now start the stack:" -ForegroundColor Green
        Write-Host "  docker-compose up -d"
        Write-Host "  docker-compose --profile dev up -d  # Include devcontainer"
        
    } else {
        Write-ColorOutput "✗ Missing required environment variables!" -Color $Colors.Red
        Write-Host "`nRequired variables missing:" -ForegroundColor Red
        foreach ($var in $result.MissingRequired) {
            Write-Host "  - $var" -ForegroundColor Red
        }
        
        Write-Host "`nTo fix this:" -ForegroundColor Blue
        Write-Host "  1. Copy .env.example to .env:"
        Write-Host "     Copy-Item .env.example .env"
        Write-Host "  2. Edit .env and fill in your values"
        Write-Host "  3. Load the .env file:"
        Write-Host "     Get-Content .env | ForEach-Object {"
        Write-Host "       if ($_ -match '^([^#][^=]+)=(.*)$') {"
        Write-Host "         [Environment]::SetEnvironmentVariable(`$matches[1].Trim(), `$matches[2].Trim(), 'Process')"
        Write-Host "       }"
        Write-Host "     }"
        Write-Host "  4. Run this script again to verify"
    }
    
    Write-Host "$('='*60)`n" -ForegroundColor White
}

# Main execution
$result = Test-EnvironmentVariables
Show-Summary -result $result

# Return exit code
if ($result.AllValid) {
    exit 0
} else {
    exit 1
}
