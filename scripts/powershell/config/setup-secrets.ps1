# Setup GitHub Secrets and Environment Variables
# This script helps configure all required secrets for the docker_dotfiles project

param(
    [switch]$SetGitHubSecrets,
    [switch]$LoadEnvVars,
    [switch]$ValidateAll
)

$ErrorActionPreference = "Stop"

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    $colors = @{
        "Info" = "Cyan"
        "Success" = "Green"
        "Warning" = "Yellow"
        "Error" = "Red"
    }
    Write-Host "[$Type] $Message" -ForegroundColor $colors[$Type]
}

function Test-EnvFile {
    if (-not (Test-Path ".env")) {
        Write-Status "No .env file found. Creating from .env.example..." "Warning"
        Copy-Item -Path ".env.example" -Destination ".env" -Force
        Write-Status "Created .env file. Please edit it with your actual credentials." "Warning"
        return $false
    }
    return $true
}

function Get-EnvVariables {
    $envVars = @{}
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            $line = $_.Trim()
            # Skip comments and empty lines
            if ($line -and -not $line.StartsWith("#")) {
                $parts = $line.Split("=", 2)
                if ($parts.Length -eq 2) {
                    $key = $parts[0].Trim()
                    $value = $parts[1].Trim()
                    # Only add if value is not a placeholder
                    if ($value -and -not $value.StartsWith("CHANGE_ME") -and -not $value.StartsWith("your_") -and -not $value.StartsWith("your-")) {
                        $envVars[$key] = $value
                    }
                }
            }
        }
    }
    return $envVars
}

function Set-GitHubSecrets {
    Write-Status "Setting up GitHub secrets..." "Info"
    
    $envVars = Get-EnvVariables
    
    $requiredSecrets = @(
        "GH_PAT",
        "DOCKER_POSTGRES_PASSWORD",
        "DOCKER_MARIADB_ROOT_PASSWORD",
        "DOCKER_MARIADB_PASSWORD",
        "DOCKER_REDIS_PASSWORD",
        "DOCKER_MINIO_ROOT_USER",
        "DOCKER_MINIO_ROOT_PASSWORD",
        "DOCKER_GRAFANA_ADMIN_PASSWORD",
        "DOCKER_JUPYTER_TOKEN",
        "DOCKER_PGADMIN_PASSWORD"
    )
    
    $missingSecrets = @()
    $setSecrets = @()
    
    foreach ($secret in $requiredSecrets) {
        if ($envVars.ContainsKey($secret)) {
            try {
                $value = $envVars[$secret]
                Write-Status "Setting $secret..." "Info"
                $value | gh secret set $secret --repo DeanLuus22021994/docker_dotfiles
                $setSecrets += $secret
                Write-Status "✓ Set $secret" "Success"
            }
            catch {
                Write-Status "✗ Failed to set $secret`: $_" "Error"
            }
        }
        else {
            $missingSecrets += $secret
            Write-Status "✗ Missing $secret in .env file" "Warning"
        }
    }
    
    Write-Host ""
    Write-Status "Summary:" "Info"
    Write-Status "  Set: $($setSecrets.Count)/$($requiredSecrets.Count)" "Success"
    if ($missingSecrets.Count -gt 0) {
        Write-Status "  Missing: $($missingSecrets -join ', ')" "Warning"
        Write-Status "  Please edit .env file and add these values, then run again." "Warning"
    }
}

function Set-EnvironmentVariables {
    Write-Status "Loading environment variables..." "Info"
    
    $envVars = Get-EnvVariables
    $loaded = 0
    
    foreach ($key in $envVars.Keys) {
        [Environment]::SetEnvironmentVariable($key, $envVars[$key], 'Process')
        $loaded++
    }
    
    Write-Status "✓ Loaded $loaded environment variables" "Success"
}

function Invoke-Validation {
    Write-Status "Running validation..." "Info"
    
    Write-Status "Validating environment variables..." "Info"
    try {
        python scripts/validate_env.py
        Write-Status "✓ Environment validation passed" "Success"
    }
    catch {
        Write-Status "✗ Environment validation failed" "Error"
        return
    }
    
    Write-Status "Validating configurations..." "Info"
    try {
        python scripts/validate_configs.py
        Write-Status "✓ Configuration validation passed" "Success"
    }
    catch {
        Write-Status "✗ Configuration validation failed" "Error"
        return
    }
    
    Write-Status "Validating docker-compose..." "Info"
    try {
        docker-compose config --quiet
        Write-Status "✓ Docker Compose validation passed" "Success"
    }
    catch {
        Write-Status "✗ Docker Compose validation failed" "Error"
        return
    }
    
    Write-Status "All validations passed! ✓" "Success"
}

# Main execution
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Docker Stack Setup Helper" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-EnvFile)) {
    Write-Host ""
    Write-Status "Please edit .env file with your credentials and run this script again." "Warning"
    exit 1
}

if ($SetGitHubSecrets) {
    Set-GitHubSecrets
}

if ($LoadEnvVars) {
    Set-EnvironmentVariables
}

if ($ValidateAll) {
    Set-EnvironmentVariables
    Invoke-Validation
}

if (-not $SetGitHubSecrets -and -not $LoadEnvVars -and -not $ValidateAll) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup_secrets.ps1 -SetGitHubSecrets   # Set GitHub secrets from .env"
    Write-Host "  .\scripts\setup_secrets.ps1 -LoadEnvVars        # Load .env into current session"
    Write-Host "  .\scripts\setup_secrets.ps1 -ValidateAll        # Load env vars and run all validations"
    Write-Host ""
    Write-Host "You can combine flags:"
    Write-Host "  .\scripts\setup_secrets.ps1 -SetGitHubSecrets -LoadEnvVars -ValidateAll"
    Write-Host ""
}
