<#
.SYNOPSIS
    Validate Docker Secrets Configuration
.DESCRIPTION
    Validates all Docker secret files for security compliance and proper configuration.
.EXAMPLE
    .\Test-DockerSecrets.ps1
#>

[CmdletBinding()]
param()

Write-Host 'Docker Secrets Validation' -ForegroundColor Cyan
Write-Host '=========================' -ForegroundColor Cyan
Write-Host ''

$valid = $true
$secrets = @(
    'postgres_user',
    'postgres_password',
    'redis_password',
    'mariadb_root_password',
    'mariadb_password',
    'mariadb_user'
)

foreach ($secret in $secrets) {
    $file = ".secrets/$secret.txt"
    
    if (!(Test-Path $file)) {
        Write-Host "❌ Missing: $secret" -ForegroundColor Red
        $valid = $false
    } else {
        $content = Get-Content $file -Raw
        
        if ($content -match 'CHANGEME') {
            Write-Host "⚠️  Placeholder detected: $secret" -ForegroundColor Yellow
            $valid = $false
        } elseif ($secret -notlike '*_user' -and $content.Length -lt 16) {
            Write-Host "⚠️  Weak password: $secret (length: $($content.Length))" -ForegroundColor Yellow
            $valid = $false
        } elseif ($content -match '[\r\n]') {
            Write-Host "⚠️  Contains newlines: $secret" -ForegroundColor Yellow
            $valid = $false
        } else {
            Write-Host "✅ Valid: $secret" -ForegroundColor Green
        }
    }
}

Write-Host ''

if ($valid) {
    Write-Host '✅ All secrets are valid and secure!' -ForegroundColor Green
    Write-Host ''
    exit 0
} else {
    Write-Host '❌ Secrets validation failed.' -ForegroundColor Red
    Write-Host 'Run "Initialize-DockerSecrets.ps1" to fix issues.' -ForegroundColor Yellow
    Write-Host ''
    exit 1
}
