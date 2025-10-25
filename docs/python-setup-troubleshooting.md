# Python Setup Troubleshooting Guide

## Current System Diagnosis (2025-10-25)

### Findings

**Problem:** `python` command not accessible on Windows host  
**Root Cause:** Windows App Execution Aliases redirect `python` to Microsoft Store

### Detailed Analysis

1. **Python Command Resolution:**
   ```powershell
   where.exe python
   # Result: C:\Users\deanl.MSI\AppData\Local\Microsoft\WindowsApps\python.exe
   ```
   - This is a Windows App Execution Alias (AppX package redirect)
   - Not an actual Python installation

2. **Execution Test:**
   ```powershell
   python --version
   # Result: "Python was not found; run without arguments to install from the Microsoft Store"
   # Exit Code: 9009
   ```

3. **Python Launcher (py) Test:**
   ```powershell
   py --version
   # Result: 'py' is not recognized
   ```
   - Python launcher not installed

4. **PATH Analysis:**
   ```powershell
   $env:PATH -split ';' | Select-String -Pattern 'python'
   # Result:
   # - C:\Users\deanl.MSI\AppData\Local\Programs\Python\Python38\Scripts\
   # - C:\Users\deanl.MSI\AppData\Local\Programs\Python\Python38\
   # - c:\Users\deanl.MSI\.vscode-insiders\extensions\ms-python.debugpy-2025.14.1\bundled\scripts\noConfigScripts
   ```

5. **Python 3.8 Verification:**
   ```powershell
   Test-Path "C:\Users\deanl.MSI\AppData\Local\Programs\Python\Python38\python.exe"
   # Result: False
   ```
   - **Conclusion:** Python 3.8 paths are in PATH but executable doesn't exist (stale entry)

### Impact

- ❌ Cannot run `scripts/validate_env.py`
- ❌ Cannot run `scripts/validate_configs.py`
- ❌ Cannot use Python formatting tools (Black, Ruff, mypy)
- ❌ Cannot use UV package manager
- ❌ Blocks Phase 1 Task 1.3 (Code formatting)
- ❌ Blocks Phase 3 implementation (scripts reorganization)

---

## Solution: Install Python 3.14.0 Standalone

### Step 1: Download Python

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.14.0** (latest stable)
3. Choose **Windows installer (64-bit)**

### Step 2: Install Python

**Critical Installation Options:**

1. ✅ **Check "Add Python to PATH"** (bottom of installer)
2. Click **"Customize installation"**
3. Optional Features:
   - ✅ Documentation
   - ✅ pip
   - ✅ tcl/tk and IDLE
   - ✅ Python test suite
   - ✅ py launcher (for all users)
4. Advanced Options:
   - ✅ Install for all users
   - ✅ Add Python to environment variables
   - ✅ Precompile standard library
   - ✅ Download debugging symbols
   - Install location: `C:\Program Files\Python313` (recommended)

5. Click **"Install"** (requires admin privileges)

### Step 3: Disable Windows App Execution Aliases

**Why?** Windows redirects `python` command to Microsoft Store, overriding actual installation.

**Steps:**

1. Open **Settings** (Win + I)
2. Navigate to: **Apps** → **Advanced app settings** → **App execution aliases**
3. Find and **disable**:
   - ❌ App Installer: `python.exe`
   - ❌ App Installer: `python3.exe`

### Step 4: Verify Installation

Open **new** PowerShell window (important - PATH changes require new session):

```powershell
# Check Python version
python --version
# Expected: Python 3.14.0

# Check Python path
where.exe python
# Expected: C:\Program Files\Python313\python.exe

# Check pip
pip --version
# Expected: pip 24.x from C:\Program Files\Python313\Lib\site-packages\pip

# Check Python launcher
py --version
# Expected: Python 3.14.0
```

### Step 5: Clean Up Stale PATH Entries

Remove old Python 3.8 entries from PATH:

```powershell
# View current PATH
$env:PATH -split ';' | Select-String -Pattern 'python'

# Remove stale entries (System PATH - requires admin)
# 1. Open "Edit the system environment variables"
# 2. Click "Environment Variables"
# 3. Under "User variables" or "System variables", edit PATH
# 4. Remove entries containing:
#    - C:\Users\deanl.MSI\AppData\Local\Programs\Python\Python38\Scripts\
#    - C:\Users\deanl.MSI\AppData\Local\Programs\Python\Python38\
```

### Step 6: Install UV Package Manager

UV is a fast Rust-based Python package manager (recommended over pip):

```powershell
# Install UV
pip install uv

# Verify
uv --version
```

### Step 7: Install Project Dependencies

```powershell
# Navigate to project root
cd c:\global\docker

# Install dependencies using UV (fast)
uv pip install -r requirements.txt

# Or using pip (slower)
pip install -r requirements.txt
```

### Step 8: Test Validation Scripts

```powershell
# Test environment validation
python scripts/validate_env.py

# Test configuration validation
python scripts/validate_configs.py

# Both should execute without "Python was not found" error
```

---

## Alternative: Use Python from WSL2

If you have WSL2 installed, you can use Python from Linux:

```bash
# Install Python in WSL2 (Ubuntu)
sudo apt update
sudo apt install python3.14 python3-pip

# Run scripts from WSL2
python3 scripts/validate_env.py
```

**Note:** This requires mounting Windows filesystem in WSL2 and may have performance implications.

---

## Common Errors & Solutions

### Error: "Python was not found"

**Cause:** Windows App Execution Aliases enabled  
**Solution:** Follow Step 3 to disable aliases

### Error: "'python' is not recognized"

**Cause:** Python not in PATH  
**Solution:** Reinstall Python with "Add to PATH" checked

### Error: "ImportError: No module named 'xyz'"

**Cause:** Dependencies not installed  
**Solution:** Run `uv pip install -r requirements.txt`

### Error: "Permission denied" during installation

**Cause:** Insufficient privileges  
**Solution:** Run installer as administrator

### Error: "pip is not recognized"

**Cause:** pip not installed or not in PATH  
**Solution:** Reinstall Python with "pip" option checked

---

## Verification Checklist

- [ ] `python --version` shows Python 3.14.0
- [ ] `where.exe python` shows `C:\Program Files\Python313\python.exe` (NOT `WindowsApps`)
- [ ] `pip --version` shows pip 24.x
- [ ] `py --version` shows Python 3.14.0
- [ ] `uv --version` shows uv version (if installed)
- [ ] `python scripts/validate_env.py` runs without errors
- [ ] No stale Python 3.8 entries in PATH
- [ ] Windows App Execution Aliases disabled for python.exe

---

## Next Steps After Installation

1. ✅ **Phase 1 Task 1.3**: Run Black, Ruff, mypy on Python files
2. ✅ **Phase 3**: Implement scripts reorganization
3. ✅ **Phase 4**: Run integration tests

**Status:** Phase 2 Task 2.1 Complete - Documented diagnosis and solution
