---
date_created: "2025-10-26T18:32:25.972355+00:00"
last_updated: "2025-10-26T18:32:25.972355+00:00"
tags: ['documentation', 'setup', 'installation', 'python']
description: "Documentation for python 314 install"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- python
- installation
- troubleshooting
description: Python 3.14 installation issues and fixes
---\n# Python 3.14 Installation Issues

## Windows Installation

**Issue:** Python 3.14 not available in official installer

**Solution:** Use UV to install Python 3.14

```powershell
# Install UV first
irm https://astral.sh/uv/install.ps1 | iex

# Install Python 3.14
uv python install 3.14

# Verify
uv python list
python --version
```

## Linux Installation

**Issue:** Python 3.14 not in apt/yum repositories

**Solution:** Build from source or use UV

```bash
# Option 1: UV (recommended)
uv python install 3.14

# Option 2: Build from source
wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tgz
tar -xf Python-3.14.0.tgz
cd Python-3.14.0
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
```

## macOS Installation

**Issue:** Homebrew doesn't have Python 3.14 yet

**Solution:** Use UV or pyenv

```bash
# Option 1: UV
uv python install 3.14

# Option 2: pyenv
brew install pyenv
pyenv install 3.14.0
pyenv global 3.14.0
```

## Common Errors

**SSL certificate errors:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org package
```

**Permission denied:**
```bash
# Use virtual environment instead of system Python
uv venv
source .venv/bin/activate
```
