---
date_created: "2025-10-26T18:32:25.957069+00:00"
last_updated: "2025-10-26T18:32:25.957069+00:00"
tags: ["documentation", "readme", "guide", "python"]
description: "Documentation for python setup"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- python
- setup
- installation
- troubleshooting
  description: Python 3.14 installation guide for validation scripts
  ---\n# Python Setup

Python 3.14.0+ is required for validation scripts. **Windows users: Do NOT use Microsoft Store Python** (causes PATH issues).

## Windows Installation

1. **Download Python 3.14.0** from [python.org](https://www.python.org/downloads/)
2. **Run installer** with these options:
   - ✅ "Add Python to PATH"
   - ✅ "Install for all users"
   - Install location: `C:\Program Files\Python313` (recommended)

3. **Disable Windows App Execution Aliases**:
   - Settings → Apps → Advanced app settings → App execution aliases
   - Disable: "App Installer python.exe"
   - Disable: "App Installer python3.exe"

4. **Verify installation**:

```powershell
python --version  # Should show Python 3.14.0
where.exe python  # Should show C:\Program Files\Python313\python.exe
```

5. **Install dependencies**:

```powershell
pip install uv  # UV package manager
uv pip install -r requirements.txt
```

See [troubleshooting guide](../docs/python-setup-troubleshooting.md) for common issues.
