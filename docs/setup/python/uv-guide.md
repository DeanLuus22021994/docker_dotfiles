---
date_created: "2025-10-26T18:32:25.973830+00:00"
last_updated: "2025-10-26T18:32:25.973830+00:00"
tags: ["documentation", "setup", "installation", "python"]
description: "Documentation for uv guide"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- python
- installation
  description: UV package manager installation and configuration
  ---\n# UV Package Manager

Modern Python package manager for fast, reliable dependency management.

## Installation

**Linux/macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Via pip:**

```bash
pip install uv
```

## Setup Project

```bash
# Create virtual environment
uv venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

## Common Commands

```bash
# Install packages
uv pip install package-name

# Upgrade package
uv pip install --upgrade package-name

# List installed packages
uv pip list

# Show package info
uv pip show package-name

# Clear cache
uv cache clean
```

## Benefits

- **Fast** - 10-100x faster than pip
- **Reliable** - Consistent resolution
- **Compatible** - Drop-in pip replacement
- **Modern** - Built in Rust

## Troubleshooting

**Issue:** `uv: command not found`

- Add to PATH: `export PATH="$HOME/.cargo/bin:$PATH"`
- Restart shell
