# Python Cleanup Scripts

Comprehensive PowerShell scripts for managing Python 3.14.0 installation, following SRP/DRY principles.

## Overview

These scripts ensure clean, verified Python 3.14.0 installation on Windows systems, addressing common issues like:
- Broken/incomplete Python installations
- Windows App Execution Alias conflicts
- PATH configuration problems
- Package dependency management

## Scripts

### 1. `remove-broken-python.ps1`
Detects and removes broken Python installations.

**Usage:**
```powershell
# Dry run (preview changes)
.\scripts\powershell\cleanup\remove-broken-python.ps1 -DryRun

# Remove broken installations
.\scripts\powershell\cleanup\remove-broken-python.ps1

# Force remove ALL non-3.14 versions
.\scripts\powershell\cleanup\remove-broken-python.ps1 -Force
```

**Features:**
- Detects all Python installations via winget
- Tests integrity (checks for missing executables)
- Removes broken installations
- Cleans PATH environment variables
- Resets Python launcher configuration

**Output:**
- Lists all detected Python versions
- Identifies broken installations
- Shows uninstallation progress
- Provides cleanup summary

### 2. `install-python314.ps1`
Downloads and installs Python 3.14.0 with proper configuration.

**Usage:**
```powershell
# Standard installation
.\scripts\powershell\cleanup\install-python314.ps1

# Custom path
.\scripts\powershell\cleanup\install-python314.ps1 -InstallPath "C:\Python314"

# Skip alias warning
.\scripts\powershell\cleanup\install-python314.ps1 -SkipAliasWarning
```

**Features:**
- Checks for Windows App Execution Aliases
- Downloads Python 3.14.0 from python.org (~28 MB)
- Installs with optimal settings (pip, launcher, no docs/tests)
- Configures User PATH automatically
- Verifies installation integrity

**Requirements:**
- Windows App Execution Aliases disabled
- Internet connection for download
- ~50 MB free disk space

### 3. `validate-python.ps1`
Validates Python 3.14.0 installation and repository compatibility.

**Usage:**
```powershell
# Basic validation
.\scripts\powershell\cleanup\validate-python.ps1

# Install missing dependencies
.\scripts\powershell\cleanup\validate-python.ps1 -InstallDependencies

# Run all tests
.\scripts\powershell\cleanup\validate-python.ps1 -RunTests
```

**Validation Checks:**
- ✓ Python command accessibility
- ✓ Python version (3.14.x)
- ✓ PATH configuration
- ✓ Pip functionality
- ✓ Required packages (uv, black, ruff, mypy, yamllint, pytest)
- ✓ Repository scripts execution
- ✓ Orchestrators functionality

**Exit Codes:**
- `0` - All validations passed
- `1` - Validation failures detected

## Complete Workflow

Execute in order for clean Python setup:

```powershell
# 1. Remove broken installations
.\scripts\powershell\cleanup\remove-broken-python.ps1

# 2. Install Python 3.14.0
.\scripts\powershell\cleanup\install-python314.ps1

# 3. Restart terminal (critical for PATH changes)
exit

# 4. Validate installation
.\scripts\powershell\cleanup\validate-python.ps1 -InstallDependencies
```

## Disabling Windows App Execution Aliases

**Critical**: Windows App Execution Aliases redirect `python` command to Microsoft Store, blocking proper access.

**Steps:**
1. Press `Win + I` to open Settings
2. Navigate to: **Apps → Advanced app settings → App execution aliases**
3. Disable:
   - ☐ App Installer: python.exe
   - ☐ App Installer: python3.exe

**Verification:**
```powershell
where.exe python
# Should NOT show: C:\...\WindowsApps\...
# Should show: C:\...\Python314\python.exe
```

## Troubleshooting

### Python command not found
```powershell
# Check PATH
$env:Path -split ';' | Select-String "Python314"

# Manually add to PATH
[System.Environment]::SetEnvironmentVariable("Path", "$env:LOCALAPPDATA\Programs\Python\Python314;$env:Path", "User")

# Restart terminal
```

### Installer fails (exit code 1603)
```powershell
# Uninstall all Python versions first
.\scripts\powershell\cleanup\remove-broken-python.ps1 -Force

# Then reinstall
.\scripts\powershell\cleanup\install-python314.ps1
```

### Pip not found
```powershell
# Use full path temporarily
& "$env:LOCALAPPDATA\Programs\Python\Python314\Scripts\pip.exe" install --upgrade pip

# Verify PATH includes Scripts directory
echo $env:Path
```

### Dependencies fail to install
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies individually
pip install uv
pip install black ruff mypy yamllint pytest
```

## Integration with Repository

These scripts integrate with the repository structure:

```
scripts/
├── orchestrator.ps1          # Calls cleanup scripts
├── orchestrator.py           # Python orchestrator
├── powershell/
│   ├── cleanup/
│   │   ├── remove-broken-python.ps1
│   │   ├── install-python314.ps1
│   │   └── validate-python.ps1
│   ├── config/
│   └── docker/
└── python/
    ├── validation/
    │   ├── validate_env.py   # Tested by validate-python.ps1
    │   └── validate_configs.py
    └── utils/
```

## Standards

Following repository standards:
- **Python Version**: Strictly 3.14.0 (no other versions)
- **Package Manager**: pip + UV
- **Code Quality**: Black, Ruff, mypy (strict mode)
- **Testing**: pytest
- **Configuration**: yamllint

## Related Documentation

- `docs/python-setup-troubleshooting.md` - Comprehensive Python troubleshooting
- `scripts/README.md` - Scripts organization overview
- `scripts/powershell/README.md` - PowerShell scripts documentation
- `.github/TODO.md` - Project tasks and progress

## Exit Codes

All scripts follow consistent exit code conventions:

- `0` - Success
- `1` - Failure/validation errors
- Other codes indicate specific errors

## Notes

- Scripts follow SRP (Single Responsibility Principle)
- Shared utilities should be in `scripts/python/utils/`
- Color output for better readability
- Dry-run mode available for safety
- Comprehensive error handling and reporting
