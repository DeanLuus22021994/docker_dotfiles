---
date_created: "2025-10-26T18:32:25.974340+00:00"
last_updated: "2025-10-26T18:32:25.974340+00:00"
tags: ["documentation", "setup", "installation", "python"]
description: "Documentation for alternatives"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- python
- installation
- reference
  description: Alternative Python installation methods
  ---\n# Installation Alternatives

Four alternative solutions to Python 3.14.0 installation issues.

## Option 1: Python 3.13 ⭐⭐⭐⭐⭐ (RECOMMENDED)

Stable, tested, easy installation:

```powershell
.\scripts\powershell\cleanup\remove-broken-python.ps1
winget install --id Python.Python.3.13 --exact
python --version  # Verify
```

**Impact:** Update 37 repository references (3.14.0 → 3.13.1)

## Option 2: Miniconda ⭐⭐⭐⭐

Already installed at `C:\Users\deanl.MSI\miniconda3`:

```powershell
conda update conda -y
conda create -n docker_project python=3.13 -y
conda activate docker_project
pip install uv black ruff mypy yamllint pytest
```

**Pros:** Isolated, already installed
**Cons:** Conda overhead

## Option 3: Portable Python ⭐⭐⭐

No admin required, no Windows Installer:

```powershell
# Download embedded version
$url = "https://www.python.org/ftp/python/3.14.0/python-3.14.0-embed-amd64.zip"
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\python-3.14-embed.zip"

# Extract
Expand-Archive "$env:TEMP\python-3.14-embed.zip" -DestinationPath "C:\Python314-Portable"

# Install pip
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "C:\Python314-Portable\get-pip.py"
& "C:\Python314-Portable\python.exe" "C:\Python314-Portable\get-pip.py"
```

**Pros:** No installer issues
**Cons:** Manual pip setup

## Option 4: Full Repair ⭐⭐ (LAST RESORT)

Complete Windows Installer cleanup (requires restart):

```powershell
# 1. Uninstall all Python versions
Get-WmiObject -Class Win32_Product | Where-Object { $_.Name -like "*Python*" } | ForEach-Object { $_.Uninstall() }

# 2. Clean installer cache
Stop-Service msiserver
Remove-Item "$env:WINDIR\Installer\*.msi" -Force -ErrorAction SilentlyContinue
Start-Service msiserver

# 3. Clean registry
Remove-Item "HKCU:\Software\Python" -Recurse -Force -ErrorAction SilentlyContinue

# 4. Restart & install
Restart-Computer
winget install --id Python.Python.3.14 --exact
```

**Warning:** Risky, may affect other applications
