<#
.SYNOPSIS
    Remove old and unused Docker images to reclaim disk space.

.DESCRIPTION
    This script identifies and removes Docker images based on age and usage criteria.
    It provides interactive prompts and detailed reporting of space reclaimed.

.PARAMETER DaysOld
    Remove images older than this many days (default: 30)

.PARAMETER Force
    Skip confirmation prompts

.PARAMETER WhatIf
    Preview deletions without actually removing images

.PARAMETER ExcludeTags
    Comma-separated list of tags to exclude (default: latest,production)

.EXAMPLE
    .\remove-old-images.ps1
    Interactive mode with default 30-day threshold

.EXAMPLE
    .\remove-old-images.ps1 -DaysOld 60 -Force
    Remove images older than 60 days without confirmation

.EXAMPLE
    .\remove-old-images.ps1 -WhatIf
    Preview what would be deleted

.NOTES
    Version: 1.0
    Author: Cluster Dashboard Team
    Last Modified: 2025-10-26
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter()]
    [int]$DaysOld = 30,

    [Parameter()]
    [switch]$Force,

    [Parameter()]
    [switch]$WhatIf,

    [Parameter()]
    [string]$ExcludeTags = "latest,production"
)

# Import colors utility
$ScriptRoot = Split-Path -Parent $PSScriptRoot
. "$ScriptRoot\python\utils\colors.py" 2>$null

# Color functions (fallback if colors.py not available)
function Write-Success { param([string]$Message) Write-Host $Message -ForegroundColor Green }
function Write-Error { param([string]$Message) Write-Host $Message -ForegroundColor Red }
function Write-Warning { param([string]$Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Info { param([string]$Message) Write-Host $Message -ForegroundColor Cyan }

# Banner
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Docker Image Cleanup Utility" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verify Docker is running
try {
    $null = docker ps 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker is not running"
    }
}
catch {
    Write-Error "ERROR: Docker is not running or not installed"
    exit 1
}

# Calculate cutoff date
$CutoffDate = (Get-Date).AddDays(-$DaysOld)
Write-Info "Removing images older than: $($CutoffDate.ToString('yyyy-MM-dd HH:mm:ss'))"
Write-Info "Excluded tags: $ExcludeTags`n"

# Parse excluded tags
$ExcludeList = $ExcludeTags -split ',' | ForEach-Object { $_.Trim() }

# Get all images
Write-Info "Scanning Docker images..."
$AllImages = docker images --format "{{.ID}}|{{.Repository}}|{{.Tag}}|{{.CreatedAt}}|{{.Size}}" | ForEach-Object {
    $parts = $_ -split '\|'
    [PSCustomObject]@{
        ID = $parts[0]
        Repository = $parts[1]
        Tag = $parts[2]
        CreatedAt = $parts[3]
        Size = $parts[4]
        SizeBytes = 0
        InUse = $false
        Excluded = $false
        Reason = ""
    }
}

# Get running containers and their images
$RunningImages = docker ps --format "{{.Image}}" | Select-Object -Unique

# Process each image
$ImagesToDelete = @()
$TotalSize = 0

foreach ($image in $AllImages) {
    # Check if image is in use
    $imageTag = "$($image.Repository):$($image.Tag)"
    if ($RunningImages -contains $imageTag -or $RunningImages -contains $image.ID) {
        $image.InUse = $true
        $image.Reason = "In use by running container"
        continue
    }

    # Check if tag is excluded
    if ($ExcludeList -contains $image.Tag) {
        $image.Excluded = $true
        $image.Reason = "Excluded tag: $($image.Tag)"
        continue
    }

    # Parse creation date
    try {
        $createdDate = [DateTime]::Parse($image.CreatedAt)
        if ($createdDate -lt $CutoffDate) {
            # Get image size in bytes
            $inspectJson = docker inspect $image.ID | ConvertFrom-Json
            $image.SizeBytes = $inspectJson[0].Size
            $TotalSize += $image.SizeBytes
            
            $ImagesToDelete += $image
        }
    }
    catch {
        Write-Warning "Could not parse date for image $($image.ID): $($image.CreatedAt)"
    }
}

# Display summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Scan Results" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Info "Total images found: $($AllImages.Count)"
Write-Info "Images in use: $($AllImages | Where-Object { $_.InUse }).Count)"
Write-Info "Images excluded: $($AllImages | Where-Object { $_.Excluded }).Count)"
Write-Warning "Images to delete: $($ImagesToDelete.Count)"
Write-Warning "Total space to reclaim: $([math]::Round($TotalSize / 1GB, 2)) GB`n"

if ($ImagesToDelete.Count -eq 0) {
    Write-Success "No images to delete. Your system is clean!"
    exit 0
}

# Display images to delete
Write-Host "Images scheduled for deletion:`n" -ForegroundColor Yellow

$ImagesToDelete | Format-Table -AutoSize @{
    Label = "Repository"
    Expression = { $_.Repository }
},
@{
    Label = "Tag"
    Expression = { $_.Tag }
},
@{
    Label = "Created"
    Expression = { $_.CreatedAt }
},
@{
    Label = "Size"
    Expression = { $_.Size }
}

# WhatIf mode - exit here
if ($WhatIf) {
    Write-Info "`nWhatIf mode: No images were deleted"
    exit 0
}

# Confirmation prompt (unless -Force)
if (-not $Force) {
    Write-Host "`nThis will permanently delete $($ImagesToDelete.Count) images." -ForegroundColor Yellow
    $confirmation = Read-Host "Continue? (y/N)"
    if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
        Write-Info "Operation cancelled by user"
        exit 0
    }
}

# Delete images
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Deleting Images" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$DeletedCount = 0
$FailedCount = 0
$ReclaimedSpace = 0

foreach ($image in $ImagesToDelete) {
    Write-Host "Deleting: $($image.Repository):$($image.Tag) ($($image.Size))..." -NoNewline
    
    try {
        docker rmi $image.ID 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Success " ✓"
            $DeletedCount++
            $ReclaimedSpace += $image.SizeBytes
        }
        else {
            Write-Error " ✗ (may be in use)"
            $FailedCount++
        }
    }
    catch {
        Write-Error " ✗ (error: $($_.Exception.Message))"
        $FailedCount++
    }
}

# Final summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Cleanup Complete" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Success "Successfully deleted: $DeletedCount images"
if ($FailedCount -gt 0) {
    Write-Warning "Failed to delete: $FailedCount images"
}
Write-Success "Space reclaimed: $([math]::Round($ReclaimedSpace / 1GB, 2)) GB`n"

# Run docker system prune to clean up dangling images
Write-Info "Running 'docker system prune -f' to clean up dangling resources..."
docker system prune -f | Out-Null

Write-Success "`nCleanup complete! ✓`n"
