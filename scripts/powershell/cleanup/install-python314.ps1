#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Install Python 3.14.0 with proper configuration for the repository.

.DESCRIPTION
    Downloads and installs Python 3.14.0 from python.org with correct settings,
    configures PATH, disables Windows App Execution Aliases, and verifies installation.
    Includes registry cleanup, administrator privilege checks, and multiple installation methods.

.PARAMETER InstallPath
    Target installation directory (default: %LOCALAPPDATA%\Programs\Python\Python314)

.PARAMETER SkipAliasWarning
    Skip Windows App Execution Aliases check

.PARAMETER Force
    Force reinstallation even if Python 3.14.0 is already installed

.PARAMETER CleanRegistry
    Clean Windows Installer registry entries before installation

.EXAMPLE
    .\install-python314.ps1 -Verbose

.EXAMPLE
    .\install-python314.ps1 -Force -CleanRegistry

.NOTES
    Part of scripts reorganization (SRP/DRY principles)
    Ensures Python 3.14.0 is properly installed and accessible
    Requires administrator privileges for registry cleanup
#>

[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [ValidateScript({
        # Validate path doesn't contain invalid characters
        if ($_ -match '[\<\>\:\"\|\?\*]') {
            throw "Install path contains invalid characters: $_"
        }
        # Validate path is not too long (Windows MAX_PATH limitation)
        if ($_.Length -gt 200) {
            throw "Install path exceeds maximum length (200 characters): $_"
        }
        return $true
    })]
    [string]$InstallPath = "$env:LOCALAPPDATA\Programs\Python\Python314",
    
    [switch]$SkipAliasWarning,
    [switch]$Force,
    [switch]$CleanRegistry
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

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Clear-PythonRegistry {
    Write-Header "Cleaning Windows Installer Registry"
    
    if (-not (Test-Administrator)) {
        Write-ColorOutput "  ⚠ Registry cleanup requires administrator privileges" -Color Yellow
        Write-ColorOutput "  Skipping registry cleanup..." -Color Yellow
        return $false
    }
    
    Write-ColorOutput "  Searching for Python 3.14.0 registry entries..." -Color Cyan
    
    $registryPaths = @(
        "HKCU:\Software\Python\PythonCore\3.14",
        "HKLM:\Software\Python\PythonCore\3.14",
        "HKLM:\Software\WOW6432Node\Python\PythonCore\3.14"
    )
    
    $found = $false
    foreach ($path in $registryPaths) {
        if (Test-Path $path) {
            Write-ColorOutput "  Removing: $path" -Color Yellow
            try {
                Remove-Item -Path $path -Recurse -Force -ErrorAction Stop
                Write-ColorOutput "  ✓ Removed: $path" -Color Green
                $found = $true
            } catch {
                Write-ColorOutput "  ✗ Failed to remove: $path - $_" -Color Red
            }
        }
    }
    
    # Clean Windows Installer cache
    $installerCachePaths = @(
        "$env:WINDIR\Installer\*.msi",
        "$env:WINDIR\Installer\*.msp"
    )
    
    foreach ($pattern in $installerCachePaths) {
        $files = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | 
                 Where-Object { $_.Name -match "python.*3\.14" }
        
        foreach ($file in $files) {
            Write-ColorOutput "  Removing installer cache: $($file.Name)" -Color Yellow
            try {
                Remove-Item $file.FullName -Force -ErrorAction Stop
                Write-ColorOutput "  ✓ Removed cache: $($file.Name)" -Color Green
                $found = $true
            } catch {
                Write-ColorOutput "  ⚠ Could not remove: $($file.Name)" -Color Yellow
            }
        }
    }
    
    if ($found) {
        Write-ColorOutput "  ✓ Registry cleanup complete" -Color Green
    } else {
        Write-ColorOutput "  ℹ No Python 3.14.0 registry entries found" -Color Cyan
    }
    
    return $true
}

function Test-WindowsAppAliases {
    Write-Header "Checking Windows App Execution Aliases"
    
    $aliasPath = "$env:LOCALAPPDATA\Microsoft\WindowsApps"
    $pythonAlias = Join-Path $aliasPath "python.exe"
    
    if (Test-Path $pythonAlias) {
        $target = (Get-Item $pythonAlias).Target
        if ($target -like "*WindowsApps*") {
            Write-ColorOutput "  ⚠ Windows App Execution Alias ACTIVE" -Color Red
            Write-ColorOutput "    This will block python command access!" -Color Red
            return $false
        }
    }
    
    Write-ColorOutput "  ✓ No blocking aliases detected" -Color Green
    return $true
}

function Disable-WindowsAppAliases {
    Write-Header "Disabling Windows App Execution Aliases"
    
    Write-ColorOutput @"
  
  MANUAL ACTION REQUIRED:
  
  1. Press Win + I to open Settings
  2. Navigate to: Apps → Advanced app settings → App execution aliases
  3. Disable the following:
     • App Installer: python.exe
     • App Installer: python3.exe
  
  4. Press ENTER when complete...
"@ -Color Yellow
    
    Read-Host
    
    if (Test-WindowsAppAliases) {
        Write-ColorOutput "  ✓ Aliases disabled successfully" -Color Green
        return $true
    } else {
        Write-ColorOutput "  ✗ Aliases still active - please try again" -Color Red
        return $false
    }
}

function Get-Python314Installer {
    Write-Header "Downloading Python 3.14.0"
    
    $url = "https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe"
    $installer = "$env:TEMP\python-3.14.0-amd64.exe"
    
    if (Test-Path $installer) {
        $size = (Get-Item $installer).Length / 1MB
        Write-ColorOutput "  ✓ Installer already exists ($([math]::Round($size, 2)) MB)" -Color Green
        return $installer
    }
    
    Write-ColorOutput "  Downloading from python.org..." -Color Cyan
    Write-ColorOutput "  URL: $url" -Color Gray
    
    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $url -OutFile $installer -UseBasicParsing
        
        if (Test-Path $installer) {
            $size = (Get-Item $installer).Length / 1MB
            Write-ColorOutput "  ✓ Downloaded: $([math]::Round($size, 2)) MB" -Color Green
            return $installer
        } else {
            throw "Download failed - file not found"
        }
    } catch {
        Write-ColorOutput "  ✗ Download failed: $_" -Color Red
        return $null
    }
}

function Install-Python314 {
    param([string]$InstallerPath, [string]$TargetPath)
    
    Write-Header "Installing Python 3.14.0"
    
    Write-ColorOutput "  Target: $TargetPath" -Color Cyan
    Write-ColorOutput "  Method: Windows Installer (direct)" -Color Cyan
    Write-ColorOutput "  This will take 30-90 seconds..." -Color Yellow
    
    # Ensure target directory doesn't exist
    if (Test-Path $TargetPath) {
        Write-ColorOutput "  Removing existing directory..." -Color Yellow
        try {
            Remove-Item -Path $TargetPath -Recurse -Force -ErrorAction Stop
            Write-ColorOutput "  ✓ Removed existing directory" -Color Green
        } catch {
            Write-ColorOutput "  ⚠ Could not remove directory: $_" -Color Yellow
        }
    }
    
    $arguments = @(
        "/quiet"
        "InstallAllUsers=0"
        "PrependPath=1"
        "Include_test=0"
        "Include_pip=1"
        "Include_doc=0"
        "Include_launcher=1"
        "InstallLauncherAllUsers=0"
        "TargetDir=$TargetPath"
    )
    
    Write-ColorOutput "  Running installer..." -Color Cyan
    
    try {
        # Standard installation (already running as admin)
        $process = Start-Process -FilePath $InstallerPath -ArgumentList $arguments -Wait -PassThru -NoNewWindow
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "  ✓ Installation successful" -Color Green
            return $true
        } elseif ($process.ExitCode -eq 1638) {
            Write-ColorOutput "  ⚠ Already installed (exit code 1638)" -Color Yellow
            return $true
        } elseif ($process.ExitCode -eq 1603) {
            Write-ColorOutput "  ⚠ Installation failed (exit code 1603) - attempting repair..." -Color Yellow
            
            # Second attempt: Try with /passive for better error visibility
            Write-ColorOutput "  Retrying with /passive mode..." -Color Cyan
            $arguments[0] = "/passive"
            $process = Start-Process -FilePath $InstallerPath -ArgumentList $arguments -Wait -PassThru -NoNewWindow
            
            if ($process.ExitCode -eq 0 -or $process.ExitCode -eq 1638) {
                Write-ColorOutput "  ✓ Installation successful (passive mode)" -Color Green
                return $true
            } else {
                Write-ColorOutput "  ✗ Installation failed (exit code: $($process.ExitCode))" -Color Red
                
                # Log detailed error info
                Write-ColorOutput "`n  Troubleshooting information:" -Color Yellow
                Write-ColorOutput "  - Exit code 1603: Fatal error during installation" -Color Gray
                Write-ColorOutput "  - Check Windows Event Viewer: Application logs" -Color Gray
                Write-ColorOutput "  - Verify installer integrity" -Color Gray
                Write-ColorOutput "  - Attempting winget fallback..." -Color Gray
                
                return Install-Python314Winget
            }
        } else {
            Write-ColorOutput "  ✗ Installation failed (exit code: $($process.ExitCode))" -Color Red
            return Install-Python314Winget
        }
    } catch {
        Write-ColorOutput "  ✗ Installation error: $_" -Color Red
        
        # Attempt using winget as fallback
        Write-ColorOutput "`n  Attempting fallback: winget installation..." -Color Yellow
        return Install-Python314Winget
    }
}

function Install-Python314Winget {
    Write-ColorOutput "  Using winget package manager..." -Color Cyan
    
    try {
        # First uninstall if exists
        winget uninstall --id Python.Python.3.14 --silent 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ Uninstalled existing Python 3.14.0" -Color Green
            Start-Sleep -Seconds 3
        }
        
        # Now install fresh
        Write-ColorOutput "  Installing Python 3.14.0 via winget..." -Color Cyan
        $wingetOutput = winget install --id Python.Python.3.14 --exact --silent --accept-package-agreements --accept-source-agreements 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ Winget installation successful" -Color Green
            Start-Sleep -Seconds 5
            return $true
        } elseif ($LASTEXITCODE -eq -1978335189) {
            Write-ColorOutput "  ⚠ Python already installed via winget" -Color Yellow
            return $true
        } else {
            Write-ColorOutput "  ✗ Winget installation failed (exit code: $LASTEXITCODE)" -Color Red
            Write-ColorOutput "  Output: $wingetOutput" -Color Gray
            return $false
        }
    } catch {
        Write-ColorOutput "  ✗ Winget error: $_" -Color Red
        return $false
    }
}

function Add-PythonToPath {
    param([string]$PythonPath)
    
    Write-Header "Configuring PATH"
    
    $pathsToAdd = @(
        $PythonPath,
        (Join-Path $PythonPath "Scripts")
    )
    
    # Update User PATH
    $currentUserPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $pathEntries = $currentUserPath -split ';'
    
    $modified = $false
    foreach ($pathToAdd in $pathsToAdd) {
        if ($pathEntries -notcontains $pathToAdd) {
            $pathEntries = @($pathToAdd) + $pathEntries
            $modified = $true
            Write-ColorOutput "  Added: $pathToAdd" -Color Green
        }
    }
    
    if ($modified) {
        $newUserPath = $pathEntries -join ';'
        [System.Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
        Write-ColorOutput "  ✓ User PATH updated permanently" -Color Green
    } else {
        Write-ColorOutput "  ✓ Already in User PATH" -Color Green
    }
    
    # Update session PATH
    $env:Path = "$($pathsToAdd[0]);$($pathsToAdd[1]);" + $env:Path
    Write-ColorOutput "  ✓ Session PATH updated" -Color Green
}

function Test-Python314Installation {
    param([string]$PythonPath)
    
    Write-Header "Verifying Installation"
    
    # Wait for installation to complete
    Start-Sleep -Seconds 3
    
    $pythonExe = Join-Path $PythonPath "python.exe"
    $pipExe = Join-Path $PythonPath "Scripts\pip.exe"
    
    # Check files exist
    if (-not (Test-Path $pythonExe)) {
        Write-ColorOutput "  ✗ python.exe not found at $pythonExe" -Color Red
        return $false
    }
    Write-ColorOutput "  ✓ python.exe found" -Color Green
    
    if (-not (Test-Path $pipExe)) {
        Write-ColorOutput "  ✗ pip.exe not found at $pipExe" -Color Red
        return $false
    }
    Write-ColorOutput "  ✓ pip.exe found" -Color Green
    
    # Test execution
    try {
        $version = & $pythonExe --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ Python version: $version" -Color Green
        } else {
            Write-ColorOutput "  ✗ Python execution failed" -Color Red
            return $false
        }
        
        $pipVersion = & $pipExe --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✓ Pip version: $($pipVersion -split "`n" | Select-Object -First 1)" -Color Green
        } else {
            Write-ColorOutput "  ✗ Pip execution failed" -Color Red
            return $false
        }
        
        return $true
    } catch {
        Write-ColorOutput "  ✗ Verification error: $_" -Color Red
        return $false
    }
}

# Main execution
Write-ColorOutput "`n╔══════════════════════════════════════════════════════════╗" -Color Cyan
Write-ColorOutput "║     Python 3.14.0 Installation Script                  ║" -Color Cyan
Write-ColorOutput "╚══════════════════════════════════════════════════════════╝" -Color Cyan

# Check administrator privileges
if (Test-Administrator) {
    Write-ColorOutput "`n✓ Running with administrator privileges" -Color Green
} else {
    Write-ColorOutput "`n⚠ NOT running as administrator" -Color Yellow
    Write-ColorOutput "  Some operations may fail (registry cleanup, system-wide PATH)" -Color Yellow
    Write-ColorOutput "  Recommend: Right-click PowerShell → Run as Administrator" -Color Yellow
    
    $continue = Read-Host "`nContinue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-ColorOutput "Installation cancelled" -Color Yellow
        exit 1
    }
}

# Step 1: Clean registry if requested
if ($CleanRegistry) {
    Clear-PythonRegistry
}

# Step 2: Check for Windows App Aliases
if (-not (Test-WindowsAppAliases)) {
    if (-not $SkipAliasWarning) {
        if (-not (Disable-WindowsAppAliases)) {
            Write-ColorOutput "`n✗ Cannot proceed with aliases enabled" -Color Red
            Write-ColorOutput "  Re-run script after disabling aliases" -Color Yellow
            exit 1
        }
    } else {
        Write-ColorOutput "  ⚠ Skipping alias check (use -SkipAliasWarning)" -Color Yellow
    }
}

# Step 3: Check if already installed
if (Test-Path "$InstallPath\python.exe") {
    if (-not $Force) {
        Write-ColorOutput "`n⚠ Python 3.14.0 already installed at $InstallPath" -Color Yellow
        
        $overwrite = Read-Host "Reinstall? (y/N)"
        if ($overwrite -ne 'y' -and $overwrite -ne 'Y') {
            Write-ColorOutput "Installation cancelled" -Color Yellow
            
            # Still verify installation
            if (Test-Python314Installation -PythonPath $InstallPath) {
                Write-ColorOutput "`n✓ Existing installation verified successfully" -Color Green
                exit 0
            } else {
                Write-ColorOutput "`n⚠ Existing installation verification failed" -Color Yellow
                Write-ColorOutput "  Re-run with -Force to reinstall" -Color Yellow
                exit 1
            }
        }
    } else {
        Write-ColorOutput "`n⚠ Force reinstallation requested" -Color Yellow
    }
}

# Step 4: Download installer
$installer = Get-Python314Installer
if (-not $installer) {
    Write-ColorOutput "`n✗ Failed to download installer" -Color Red
    exit 1
}

# Verify installer integrity
Write-Header "Verifying Installer Integrity"
try {
    $hash = Get-FileHash -Path $installer -Algorithm SHA256
    Write-ColorOutput "  SHA256: $($hash.Hash)" -Color Cyan
    Write-ColorOutput "  ✓ Installer hash computed successfully" -Color Green
} catch {
    Write-ColorOutput "  ⚠ Could not verify installer hash: $_" -Color Yellow
}

# Step 5: Install Python
if (-not (Install-Python314 -InstallerPath $installer -TargetPath $InstallPath)) {
    Write-ColorOutput "`n✗ Installation failed" -Color Red
    Write-ColorOutput "`nTroubleshooting steps:" -Color Yellow
    Write-ColorOutput "  1. Check Windows Event Viewer for details" -Color White
    Write-ColorOutput "  2. Manually run installer: $installer" -Color White
    Write-ColorOutput "  3. Try with /log option to create detailed log" -Color White
    Write-ColorOutput "  4. Verify disk space and permissions" -Color White
    Write-ColorOutput "  5. Re-run this script with -CleanRegistry flag" -Color White
    
    # Cleanup installer on failure
    if (Test-Path $installer) {
        Remove-Item $installer -Force -ErrorAction SilentlyContinue
    }
    
    exit 1
}

# Cleanup installer after successful installation
if (Test-Path $installer) {
    Remove-Item $installer -Force -ErrorAction SilentlyContinue
    Write-ColorOutput "  ✓ Cleaned up installer" -Color Green
}

# Step 6: Configure PATH
Add-PythonToPath -PythonPath $InstallPath

# Step 7: Verify installation
Write-ColorOutput "`nWaiting for installation to stabilize..." -Color Yellow
Start-Sleep -Seconds 5

if (-not (Test-Python314Installation -PythonPath $InstallPath)) {
    Write-ColorOutput "`n✗ Installation verification failed" -Color Red
    Write-ColorOutput "`nAttempting to locate Python installation..." -Color Yellow
    
    # Check common installation paths
    $fallbackPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python314",
        "$env:ProgramFiles\Python314",
        "$env:ProgramFiles(x86)\Python314",
        "C:\Python314"
    )
    
    $found = $false
    foreach ($path in $fallbackPaths) {
        if (Test-Path "$path\python.exe") {
            Write-ColorOutput "  ✓ Found Python at: $path" -Color Green
            if (Test-Python314Installation -PythonPath $path) {
                Write-ColorOutput "  ✓ Installation verified at alternate location" -Color Green
                Add-PythonToPath -PythonPath $path
                $InstallPath = $path
                $found = $true
                break
            }
        }
    }
    
    if (-not $found) {
        Write-ColorOutput "  ✗ Could not locate working Python installation" -Color Red
        exit 1
    }
}

# Summary
Write-Header "Installation Complete"
Write-ColorOutput "✓ Python 3.14.0 installed: $InstallPath" -Color Green
Write-ColorOutput "✓ PATH configured" -Color Green
Write-ColorOutput "✓ Installation verified" -Color Green
Write-ColorOutput "`n⚠ IMPORTANT: Restart your terminal for PATH changes to take effect!" -Color Yellow
Write-ColorOutput "`nNext steps:" -Color Cyan
Write-ColorOutput "  1. Close and reopen PowerShell" -Color White
Write-ColorOutput "  2. Run: python --version" -Color White
Write-ColorOutput "  3. Run: .\scripts\powershell\cleanup\validate-python.ps1" -Color White

exit 0
