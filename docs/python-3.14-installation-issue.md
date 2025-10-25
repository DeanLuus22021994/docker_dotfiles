# Python 3.14.0 Installation Issue - Resolution

## Problem Summary

Windows Installer error 1603 preventing Python 3.14.0 installation on Windows host.

## Root Cause

1. **Windows Installer Database Corruption**: Multiple broken Python installations (3.8-3.13) left residual registry entries
2. **Exit Code 1603**: Fatal error during installation - indicates:
   - Registry conflicts from previous installations
   - Windows Installer cache corruption
   - Component already registered with different version

## Investigation Details

### Registry Analysis
- Found 58 Python-related MSI components in Windows registry
- Python 3.14.0 registry entries present but executable missing
- Python 3.13.9, 3.12.9, 3.10.11, 3.9.13, 3.8.10 components partially installed

### Installation Attempts (All Failed with 1603)
1. ✗ winget install Python.Python.3.14
2. ✗ Python.org installer (/quiet mode)
3. ✗ Python.org installer (/passive mode)
4. ✗ Chocolatey (choco install python314)
5. ✗ Chocolatey with verbose logging
6. ✗ Manual MSI extraction and installation

### Tools Used
- winget package manager
- Chocolatey package manager (with admin privileges)
- PowerShell scripts for registry cleanup
- Windows Installer logging (/l*v flag)

## Recommended Solutions

### Option 1: Use Python 3.13 (Stable - RECOMMENDED)

Python 3.13.1 is stable and widely supported:

```powershell
# Uninstall all Python versions first
.\scripts\powershell\cleanup\remove-broken-python.ps1 -Verbose

# Install Python 3.13.1 via winget
winget install --id Python.Python.3.13 --exact --accept-package-agreements

# Verify installation
python --version  # Should show Python 3.13.x
pip --version
```

Then update repository references from 3.14.0 → 3.13.1

### Option 2: Use Miniconda (Already Installed)

Miniconda3 with Python 3.13.5 is already installed at:
`C:\Users\deanl.MSI\miniconda3`

```powershell
# Update conda
conda update conda -y

# Create project environment
conda create -n docker_project python=3.13 -y
conda activate docker_project

# Install dependencies
pip install uv black ruff mypy yamllint pytest
```

### Option 3: Portable Python (No Admin Required)

Download portable Python that doesn't require Windows Installer:

```powershell
# Download Python Embedded
$url = "https://www.python.org/ftp/python/3.14.0/python-3.14.0-embed-amd64.zip"
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\python-3.14-embed.zip"

# Extract to C:\Python314-Portable
Expand-Archive "$env:TEMP\python-3.14-embed.zip" -DestinationPath "C:\Python314-Portable"

# Download get-pip.py
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "C:\Python314-Portable\get-pip.py"

# Install pip
& "C:\Python314-Portable\python.exe" "C:\Python314-Portable\get-pip.py"
```

### Option 4: Complete Windows Installer Repair (Nuclear Option)

**WARNING**: This requires system restart and may affect other applications.

```powershell
# 1. Uninstall ALL Python versions via Programs & Features
Get-WmiObject -Class Win32_Product | Where-Object { $_.Name -like "*Python*" } | ForEach-Object { $_.Uninstall() }

# 2. Clean Windows Installer cache
Stop-Service msiserver
Remove-Item "$env:WINDIR\Installer\*.msi" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:WINDIR\Installer\*.msp" -Force -ErrorAction SilentlyContinue
Start-Service msiserver

# 3. Clean Python registry entries
Remove-Item "HKCU:\Software\Python" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKLM:\Software\Python" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKLM:\Software\WOW6432Node\Python" -Recurse -Force -ErrorAction SilentlyContinue

# 4. Restart computer
Restart-Computer

# 5. After restart, install Python 3.14.0
winget install --id Python.Python.3.14 --exact
```

## Impact on Repository

If moving to Python 3.13 instead of 3.14:

### Files to Update (37 references):
- `.github/workflows/validate.yml` (3 references)
- `pyproject.toml` (2 references)
- `.devcontainer/devcontainer.dockerfile` (6 references)
- `README.md` (7 references)
- `AGENT.md` (4 references)
- `docs/python-setup-troubleshooting.md` (6 references)
- `TODO.md` (3 references)
- `.pre-commit-config.yaml` (1 reference)
- `.docker-compose/cluster.config.yml` (1 reference)
- Scripts documentation

### Command to Update:
```powershell
# Find all references
rg "3\.14\.0|Python 3\.14|python-3\.14|py314|Python314" --type-add 'config:*.{yml,yaml,toml,md,txt}' -t config

# Replace 3.14.0 → 3.13.1 (manual review recommended)
```

## Decision Matrix

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Python 3.13 | Stable, tested, easy install | Not latest version | ⭐⭐⭐⭐⭐ Best |
| Miniconda | Already installed, isolated | Conda overhead, GIL issues | ⭐⭐⭐⭐ Good |
| Portable | No admin, no installer | Manual pip setup, no launcher | ⭐⭐⭐ OK |
| Full Repair | Clean slate for 3.14 | Requires restart, risky | ⭐⭐ Last resort |

## Recommended Action

**Use Python 3.13.1 via winget:**

1. Run `.\scripts\powershell\cleanup\remove-broken-python.ps1`
2. Install Python 3.13.1: `winget install Python.Python.3.13`
3. Update repository references: 3.14.0 → 3.13.1
4. Run `.\scripts\powershell\cleanup\validate-python.ps1 -InstallDependencies`
5. Test all scripts and orchestrators

This provides a stable, supported Python environment without the Windows Installer issues affecting 3.14.0.

## Technical Notes

- Python 3.14.0 is relatively new (released Oct 2024)
- Some Windows Installer databases have compatibility issues with newest Python versions
- The free-threaded GIL changes in 3.14 may cause additional compatibility issues
- Python 3.13.x is battle-tested and widely deployed

## Related Files

- `scripts/powershell/cleanup/remove-broken-python.ps1`
- `scripts/powershell/cleanup/install-python314.ps1` (needs update for 3.13 fallback)
- `scripts/powershell/cleanup/validate-python.ps1`
- `docs/python-setup-troubleshooting.md`
