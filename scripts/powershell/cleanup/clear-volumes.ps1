<#
.SYNOPSIS
    Clear unused Docker volumes safely.

.DESCRIPTION
    Identifies and removes Docker volumes not attached to any containers.
    Provides size reporting and interactive prompts for safety.

.PARAMETER UnusedOnly
    Only remove volumes not attached to containers (default: true)

.PARAMETER Force
    Skip confirmation prompts

.PARAMETER ExcludePattern
    Exclude volumes matching this pattern (regex)

.PARAMETER WhatIf
    Preview deletions without actually removing volumes

.EXAMPLE
    .\clear-volumes.ps1
    Interactive mode removing unused volumes only

.EXAMPLE
    .\clear-volumes.ps1 -Force -ExcludePattern "production|backup"
    Remove unused volumes except those matching pattern

.NOTES
    Version: 1.0
    Author: Cluster Dashboard Team
    Last Modified: 2025-10-26
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter()]
    [switch]$UnusedOnly = $true,

    [Parameter()]
    [switch]$Force,

    [Parameter()]
    [string]$ExcludePattern = "",

    [Parameter()]
    [switch]$WhatIf
)

# Color functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Docker Volume Cleanup Utility" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verify Docker
try {
    $null = docker ps 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Docker not running" }
} catch {
    Write-Error "ERROR: Docker is not running"
    exit 1
}

# Get all volumes
$AllVolumes = docker volume ls --format "{{.Name}}" | ForEach-Object {
    $name = $_
    $inspect = docker volume inspect $name | ConvertFrom-Json
    [PSCustomObject]@{
        Name = $name
        Mountpoint = $inspect[0].Mountpoint
        Driver = $inspect[0].Driver
        Labels = $inspect[0].Labels
        InUse = $false
        Size = 0
    }
}

# Get volumes in use
$VolumesInUse = docker ps -a --format "{{.Mounts}}" | ForEach-Object {
    $_ -split ',' | ForEach-Object { $_.Trim() }
} | Select-Object -Unique

foreach ($vol in $AllVolumes) {
    if ($VolumesInUse -contains $vol.Name) {
        $vol.InUse = $true
    }
    
    # Get size (Windows: du equivalent)
    if (Test-Path $vol.Mountpoint) {
        $size = (Get-ChildItem -Path $vol.Mountpoint -Recurse -Force -ErrorAction SilentlyContinue |
            Measure-Object -Property Length -Sum).Sum
        $vol.Size = if ($size) { $size } else { 0 }
    }
}

# Filter volumes to delete
$VolumesToDelete = $AllVolumes | Where-Object {
    $vol = $_
    
    # Skip if in use (when UnusedOnly is true)
    if ($UnusedOnly -and $vol.InUse) { return $false }
    
    # Skip if matches exclude pattern
    if ($ExcludePattern -and $vol.Name -match $ExcludePattern) { return $false }
    
    # Skip if has production/backup labels
    if ($vol.Labels -and ($vol.Labels.production -or $vol.Labels.backup)) { return $false }
    
    return $true
}

# Summary
$TotalSize = ($VolumesToDelete | Measure-Object -Property Size -Sum).Sum
Write-Info "Total volumes: $($AllVolumes.Count)"
Write-Info "In use: $($AllVolumes | Where-Object InUse | Measure-Object).Count"
Write-Warning "To delete: $($VolumesToDelete.Count)"
Write-Warning "Space to reclaim: $([math]::Round($TotalSize / 1GB, 2)) GB`n"

if ($VolumesToDelete.Count -eq 0) {
    Write-Success "No volumes to delete!"
    exit 0
}

# Display volumes
$VolumesToDelete | Format-Table Name, @{L='Size';E={"{0:N2} MB" -f ($_.Size / 1MB)}}, InUse

if ($WhatIf) {
    Write-Info "WhatIf mode: No volumes deleted"
    exit 0
}

if (-not $Force) {
    $conf = Read-Host "Delete $($VolumesToDelete.Count) volumes? (y/N)"
    if ($conf -ne 'y') { Write-Info "Cancelled"; exit 0 }
}

# Delete
$deleted = 0
foreach ($vol in $VolumesToDelete) {
    Write-Host "Deleting: $($vol.Name)..." -NoNewline
    docker volume rm $vol.Name 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { Write-Success " ✓"; $deleted++ }
    else { Write-Error " ✗" }
}

Write-Success "`nDeleted: $deleted volumes"
Write-Success "Space reclaimed: $([math]::Round($TotalSize / 1GB, 2)) GB`n"
