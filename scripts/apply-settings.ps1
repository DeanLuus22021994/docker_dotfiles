# Apply GitHub Repository Settings
# This script applies all repository configuration from .config/github/*.yml files
# Usage: .\scripts\apply-settings.ps1 [-DryRun] [-ApplyAll] [-ApplyRepository] [-ApplyBranchProtection] [-ConfigureActions] [-ConfigureSecurity]

param(
    [switch]$DryRun,
    [switch]$ApplyAll,
    [switch]$ApplyRepository,
    [switch]$ApplyBranchProtection,
    [switch]$ConfigureActions,
    [switch]$ConfigureSecurity
)

$ErrorActionPreference = "Stop"
$ConfigPath = ".config/github"
$RepoOwner = "DeanLuus22021994"
$RepoName = "docker_dotfiles"
$RepoFullName = "$RepoOwner/$RepoName"

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $colors = @{ "Info" = "Cyan"; "Success" = "Green"; "Warning" = "Yellow"; "Error" = "Red" }
    Write-Host "[$Type] $Message" -ForegroundColor $colors[$Type]
}

function Test-GitHubCLI {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Write-Status "GitHub CLI (gh) not found. Install from: https://cli.github.com/" "Error"
        exit 1
    }
    
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Status "GitHub CLI not authenticated. Run: gh auth login" "Error"
        exit 1
    }
    
    Write-Status "✓ GitHub CLI authenticated" "Success"
}

function Apply-RepositorySettings {
    Write-Status "Applying repository settings..." "Info"
    
    $configFile = Join-Path $ConfigPath "repository.yml"
    if (-not (Test-Path $configFile)) {
        Write-Status "Config file not found: $configFile" "Error"
        return $false
    }
    
    if ($DryRun) {
        Write-Status "[DRY RUN] Would apply repository settings from: $configFile" "Warning"
        Get-Content $configFile | Select-Object -First 10
        return $true
    }
    
    try {
        $config = Get-Content $configFile -Raw | ConvertFrom-Yaml
        
        $payload = @{
            name = $config.name
            description = $config.description
            homepage = $config.homepage
            private = $config.private
            has_issues = $config.has_issues
            has_projects = $config.has_projects
            has_wiki = $config.has_wiki
            default_branch = $config.default_branch
            allow_squash_merge = $config.allow_squash_merge
            allow_merge_commit = $config.allow_merge_commit
            allow_rebase_merge = $config.allow_rebase_merge
            allow_auto_merge = $config.allow_auto_merge
            delete_branch_on_merge = $config.delete_branch_on_merge
        } | ConvertTo-Json -Depth 10
        
        $payload | gh api repos/$RepoFullName --method PATCH --input -
        Write-Status "✓ Repository settings applied" "Success"
        
        # Apply topics separately (gh API requires array format)
        $topicsJson = @{ names = $config.topics } | ConvertTo-Json
        $topicsJson | gh api repos/$RepoFullName/topics --method PUT --input -
        Write-Status "✓ Repository topics updated" "Success"
        
        return $true
    }
    catch {
        Write-Status "✗ Failed to apply repository settings: $_" "Error"
        return $false
    }
}

function Apply-BranchProtection {
    Write-Status "Applying branch protection rules..." "Info"
    
    $configFile = Join-Path $ConfigPath "branch-protection.yml"
    if (-not (Test-Path $configFile)) {
        Write-Status "Config file not found: $configFile" "Error"
        return $false
    }
    
    if ($DryRun) {
        Write-Status "[DRY RUN] Would apply branch protection from: $configFile" "Warning"
        Get-Content $configFile | Select-Object -First 10
        return $true
    }
    
    try {
        gh api repos/$RepoFullName/branches/main/protection --method PUT --input $configFile
        Write-Status "✓ Branch protection rules applied to main" "Success"
        return $true
    }
    catch {
        Write-Status "✗ Failed to apply branch protection: $_" "Error"
        return $false
    }
}

function Show-ActionsGuidance {
    Write-Status "GitHub Actions configuration requires manual setup via UI" "Warning"
    Write-Status "Go to: https://github.com/$RepoFullName/settings/actions" "Info"
    Write-Status "Reference: $ConfigPath/actions.yml" "Info"
    Write-Status "Key settings:" "Info"
    Write-Host "  - Allow all actions"
    Write-Host "  - Default permissions: read"
    Write-Host "  - Allow pull requests from forks (with approval)"
    Write-Host "  - Artifact retention: 90 days"
}

function Show-SecurityGuidance {
    Write-Status "Security configuration requires manual setup via UI" "Warning"
    Write-Status "Go to: https://github.com/$RepoFullName/settings/security_analysis" "Info"
    Write-Status "Reference: $ConfigPath/code-security.yml" "Info"
    Write-Status "Enable:" "Info"
    Write-Host "  - Dependabot alerts"
    Write-Host "  - Dependabot security updates"
    Write-Host "  - Secret scanning"
    Write-Host "  - Push protection"
    Write-Host "  - Code scanning (CodeQL)"
}

function Show-Summary {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  GitHub Repository Configuration Summary" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Status "Configuration Files:" "Info"
    Write-Host "  ✓ repository.yml - Repository metadata and settings"
    Write-Host "  ✓ branch-protection.yml - Main branch protection rules"
    Write-Host "  ✓ secrets.yml - Required GitHub secrets documentation"
    Write-Host "  ✓ actions.yml - GitHub Actions configuration"
    Write-Host "  ✓ code-security.yml - Security scanning settings"
    Write-Host ""
    Write-Status "Cost Implications: `$0/month (ALL FREE)" "Success"
    Write-Host "  - Self-hosted runners: Unlimited free minutes"
    Write-Host "  - GitHub Advanced Security: Free for public repos"
    Write-Host "  - Secret scanning: Free"
    Write-Host "  - Dependabot: Free"
    Write-Host "  - Code scanning: Free"
    Write-Host ""
    Write-Status "Next Steps:" "Info"
    Write-Host "  1. Review configuration files in .config/github/"
    Write-Host "  2. Run with -ApplyAll to apply all settings"
    Write-Host "  3. Set GitHub secrets: .\scripts\setup_secrets.ps1 -SetGitHubSecrets"
    Write-Host "  4. Configure security features via GitHub UI"
    Write-Host "  5. Set up self-hosted runner (see .config/github/actions.yml)"
    Write-Host ""
}

# Main execution
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  GitHub Repository Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Test-GitHubCLI

if ($DryRun) {
    Write-Status "Running in DRY RUN mode - no changes will be made" "Warning"
    Write-Host ""
}

$results = @{
    Repository = $false
    BranchProtection = $false
}

if ($ApplyAll -or $ApplyRepository) {
    $results.Repository = Apply-RepositorySettings
}

if ($ApplyAll -or $ApplyBranchProtection) {
    $results.BranchProtection = Apply-BranchProtection
}

if ($ApplyAll -or $ConfigureActions) {
    Show-ActionsGuidance
}

if ($ApplyAll -or $ConfigureSecurity) {
    Show-SecurityGuidance
}

if (-not ($ApplyAll -or $ApplyRepository -or $ApplyBranchProtection -or $ConfigureActions -or $ConfigureSecurity)) {
    Show-Summary
}
else {
    Write-Host ""
    Write-Status "Configuration Summary:" "Info"
    Write-Host "  Repository Settings: $(if ($results.Repository) { '✓ Applied' } else { '- Skipped' })"
    Write-Host "  Branch Protection: $(if ($results.BranchProtection) { '✓ Applied' } else { '- Skipped' })"
    Write-Host ""
}
