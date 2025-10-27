<#
.SYNOPSIS
    Rotate a Docker Secret
.DESCRIPTION
    Safely rotates a Docker secret with automatic backup and new secure value generation.
.PARAMETER SecretName
    The name of the secret to rotate (e.g., postgres_password, redis_password)
.EXAMPLE
    .\Update-DockerSecret.ps1 -SecretName postgres_password
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(
        'postgres_user',
        'postgres_password',
        'redis_password',
        'mariadb_root_password',
        'mariadb_password',
        'mariadb_user'
    )]
    [string]$SecretName
)

$file = ".secrets/$SecretName.txt"

Write-Host "Rotating secret: $SecretName" -ForegroundColor Cyan
Write-Host ''

if (!(Test-Path $file)) {
    Write-Host "❌ Secret file not found: $file" -ForegroundColor Red
    exit 1
}

# Create backup
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backup = "$file.bak.$timestamp"
Copy-Item $file $backup
Write-Host "✅ Backup created: $backup" -ForegroundColor Green
Write-Host ''

# Generate new value
if ($SecretName -like '*_user') {
    $value = Read-Host "Enter new username for $SecretName"
} else {
    $random = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
    Write-Host "Generated new secure password (32 characters)" -ForegroundColor Green
    $value = $random
}

# Write new value
$value | Out-File -FilePath $file -Encoding utf8 -NoNewline
Write-Host "✅ Secret rotated: $SecretName" -ForegroundColor Green
Write-Host ''

# Provide restart instructions
Write-Host '⚠️  IMPORTANT: Restart affected services to apply changes' -ForegroundColor Yellow
Write-Host ''
Write-Host 'Run one of the following commands:' -ForegroundColor Gray
Write-Host '  docker-compose restart cluster-postgres cluster-redis cluster-mariadb' -ForegroundColor Cyan
Write-Host '  OR' -ForegroundColor Gray
Write-Host '  docker-compose down && docker-compose up -d' -ForegroundColor Cyan
Write-Host ''
