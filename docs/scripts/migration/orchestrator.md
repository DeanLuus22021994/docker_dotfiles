---
date_created: "2025-10-26T18:32:25.986224+00:00"
last_updated: "2025-10-26T18:32:25.986224+00:00"
tags: ['documentation', 'scripts', 'automation']
description: "Documentation for orchestrator"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- scripts
- orchestrator
- usage
description: Orchestrator usage guide for unified script execution
---\n# Orchestrator Usage

Unified task execution across all platforms (PowerShell, Bash, Python).

## Available Orchestrators

- `scripts/orchestrator.py` - Python-based (cross-platform)
- `scripts/orchestrator.ps1` - PowerShell-specific (Windows)
- `scripts/orchestrator.sh` - Bash-specific (Linux/macOS)

## Usage Examples

**List Available Tasks:**

```powershell
scripts/orchestrator.ps1 help
python scripts/orchestrator.py help
```

**Validation Tasks:**

```powershell
# Environment validation
python scripts/orchestrator.py validate env

# Configuration validation
python scripts/orchestrator.py validate configs
```

**Audit Tasks:**

```powershell
# Code quality (Black, Ruff, mypy)
python scripts/orchestrator.py audit code

# Dependency audit
python scripts/orchestrator.py audit deps
```

## Benefits

- **Cross-platform** - Works on Windows, Linux, macOS
- **Consistent interface** - Same commands regardless of platform
- **Path abstraction** - No need to remember new paths
- **Task composition** - Can run multiple tasks in sequence

## Example Output

```
=== Running Black Format Check ===
✓ Black formatting check passed

=== Running Ruff Linter ===
✓ Ruff linting check passed

=== Running mypy Type Check ===
✓ mypy type check passed
```
