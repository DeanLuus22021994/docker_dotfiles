<#
.SYNOPSIS
    Docker Secrets Setup Wizard
.DESCRIPTION
    Interactive wizard to generate and configure Docker secrets for the Modern Data Platform stack.
.EXAMPLE
    .\Initialize-DockerSecrets.ps1
#>

[CmdletBinding()]
param()

Write-Host 'Docker Secrets Setup Wizard' -ForegroundColor Cyan
Write-Host '================================' -ForegroundColor Cyan
Write-Host ''

# Ensure secrets directory exists
if (!(Test-Path '.secrets')) {
    New-Item -Path '.secrets' -ItemType Directory -Force | Out-Null
    Write-Host '✅ Created .secrets directory' -ForegroundColor Green
}

# Define all required secrets
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
    
    if (Test-Path $file) {
        $current = Get-Content $file -Raw
        
        if ($current -match 'CHANGEME' -or $current.Length -lt 8) {
            Write-Host "⚠️  $secret needs update" -ForegroundColor Yellow
            
            if ($secret -like '*_user') {
                $value = Read-Host "Enter username for $secret"
            } else {
                $random = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
                Write-Host "Generated secure password for $secret" -ForegroundColor Green
                $value = $random
            }
            
            $value | Out-File -FilePath $file -Encoding utf8 -NoNewline
            Write-Host "✅ Updated $secret" -ForegroundColor Green
        } else {
            Write-Host "✅ $secret already configured" -ForegroundColor Green
        }
    } else {
        Write-Host "Creating $file..." -ForegroundColor Yellow
        
        if ($secret -like '*_user') {
            'cluster_user' | Out-File -FilePath $file -Encoding utf8 -NoNewline
        } else {
            $random = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
            $random | Out-File -FilePath $file -Encoding utf8 -NoNewline
        }
        
        Write-Host "✅ Created $secret" -ForegroundColor Green
    }
}

Write-Host ''
Write-Host '================================' -ForegroundColor Cyan
Write-Host 'Secrets setup complete!' -ForegroundColor Green
Write-Host 'Files created in .secrets/ directory' -ForegroundColor Gray
Write-Host ''
Write-Host '⚠️  IMPORTANT: Never commit these files to version control!' -ForegroundColor Red
Write-Host ''
