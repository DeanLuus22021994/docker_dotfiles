---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["scripts", "overview", "documentation"]
description: "Documentation for overview in scripts"
---
# Scripts Directory

Automation scripts for the Docker infrastructure, organized by language and task (SRP/DRY principles).

## Structure

```
scripts/
├── README.md                    # This file
├── orchestrator.ps1             # PowerShell orchestrator
├── orchestrator.sh              # Bash orchestrator
├── orchestrator.py              # Python orchestrator
├── powershell/                  # PowerShell scripts by task
│   ├── README.md
│   ├── config/                  # Configuration management
│   ├── docker/                  # Docker operations
│   ├── docs/                    # Documentation tasks
│   ├── audit/                   # Auditing scripts
│   └── cleanup/                 # Cleanup operations
├── python/                      # Python scripts by task
│   ├── README.md
│   ├── validation/              # Configuration validation
│   ├── audit/                   # Code audit scripts
│   └── utils/                   # Shared utilities (DRY)
└── bash/                        # Bash scripts by task
    ├── README.md
    ├── docker/                  # Docker operations
    └── docs/                    # Documentation tasks
```

## Quick Start

### Using Orchestrators

**PowerShell:**
```powershell
# Display help
.\orchestrator.ps1 help

# Validate environment
.\orchestrator.ps1 validate env

# Apply settings
.\orchestrator.ps1 config apply-settings

# Start devcontainer
.\orchestrator.ps1 docker start-devcontainer
```

**Bash:**
```bash
# Display help
./orchestrator.sh help

# Validate environment
./orchestrator.sh validate env

# Serve documentation
./orchestrator.sh docs serve
```

**Python:**
```bash
# Display help
python orchestrator.py help

# Validate configs
python orchestrator.py validate configs
```

### Direct Script Execution

You can also run scripts directly:

```powershell
# PowerShell
python .\python\validation\validate_env.py
.\powershell\config\apply-settings.ps1

# Bash
python python/validation/validate_env.py
bash bash/docs/serve-docs.sh
```

## Design Principles

### SRP (Single Responsibility Principle)
- Each script does ONE thing well
- Organized by task domain (config, docker, docs, audit, cleanup)
- Clear naming: `[task]-[action].ps1/sh/py`

### DRY (Don't Repeat Yourself)
- Shared utilities in `python/utils/`
  - `colors.py`: ANSI terminal colors
  - `file_utils.py`: File operations
  - `logging_utils.py`: Logging configuration
- PowerShell functions extracted to modules (planned)
- No code duplication across scripts

### Configuration-Driven
- All behavior controlled by `.config/` directory
- No hardcoded values in scripts
- Environment variables for secrets (`DOCKER_*` prefix)

## Available Tasks

### PowerShell Tasks

| Task | Action | Description |
|------|--------|-------------|
| config | apply-settings | Apply VSCode settings |
| config | setup-secrets | Setup environment secrets |
| docker | start-devcontainer | Start development container |
| docs | serve | Serve documentation |
| audit | test-integration | Run integration tests |
| validate | env | Validate environment (Python) |
| validate | configs | Validate configs (Python) |
| mcp | new-profiles | Generate MCP profiles (core, fullstack, testing, data) |
| mcp | set-profile | Switch to a specific MCP profile |
| mcp | get-profile | Display current active MCP profile |
| mcp | test-servers | Health check all MCP servers |
| mcp | compare-profiles | Compare tool counts and token usage across profiles |
| mcp | test-profiles | Run comprehensive profile generation and validation tests |

### Bash Tasks

| Task | Action | Description |
|------|--------|-------------|
| docker | start-devcontainer | Start development container |
| docs | serve | Serve documentation |
| validate | env | Validate environment (Python) |
| validate | configs | Validate configs (Python) |

### Python Tasks

| Task | Action | Description |
|------|--------|-------------|
| validate | env | Validate environment variables |
| validate | configs | Validate configuration files |
| audit | code | Code quality audit (planned) |
| mcp | validate | Validate MCP configuration schema |
| mcp | analyze | Analyze MCP token usage (supports --json, --compare) |

## Python Utilities (Shared)

### colors.py
```python
from python.utils.colors import Colors, success, error, warning, info

print(success("Operation completed!"))
print(error("Something went wrong"))
print(warning("Please review this"))
```

### file_utils.py
```python
from python.utils.file_utils import read_json, write_json, get_files_by_extension

data = read_json('.env.json')
py_files = get_files_by_extension('.', '.py')
```

### logging_utils.py
```python
from python.utils.logging_utils import setup_logger

logger = setup_logger('my_script', use_colors=True)
logger.info("Starting validation...")
```

## Migration from Old Structure

| Old Path | New Path |
|----------|----------|
| `validate_env.py` | `python/validation/validate_env.py` |
| `validate_configs.py` | `python/validation/validate_configs.py` |
| `apply-settings.ps1` | `powershell/config/apply-settings.ps1` |
| `setup_secrets.ps1` | `powershell/config/setup-secrets.ps1` |
| `start_devcontainer.ps1` | `powershell/docker/start-devcontainer.ps1` |
| `start_devcontainer.sh` | `bash/docker/start-devcontainer.sh` |
| `serve_docs.ps1` | `powershell/docs/serve-docs.ps1` |
| `serve_docs.sh` | `bash/docs/serve-docs.sh` |
| `test_integration.ps1` | `powershell/audit/test-integration.ps1` |

**Old scripts remain in root for backward compatibility** (deprecated, will be removed after full migration).

## Adding New Scripts

### PowerShell Script

1. Identify task category: config, docker, docs, audit, cleanup
2. Create script in `powershell/[category]/[name].ps1`
3. Add to orchestrator switch statement
4. Update README.md

### Python Script

1. Identify task category: validation, audit
2. Create script in `python/[category]/[name].py`
3. Import shared utilities: `from python.utils.colors import success`
4. Add to orchestrator if needed
5. Update README.md

### Bash Script

1. Identify task category: docker, docs
2. Create script in `bash/[category]/[name].sh`
3. Use `set -euo pipefail` for safety
4. Add to orchestrator if needed
5. Update README.md

## Testing

```powershell
# Test orchestrators
.\orchestrator.ps1 help
.\orchestrator.sh help
python orchestrator.py help

# Test validation
.\orchestrator.ps1 validate env
python python\validation\validate_env.py

# Test config scripts
.\orchestrator.ps1 config apply-settings
```

## Troubleshooting

### Python Import Errors

If you get `ModuleNotFoundError: No module named 'python'`:

```python
# Add this at the top of your script:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

### PowerShell Execution Policy

If scripts won't run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Bash Permission Denied

If bash scripts aren't executable:

```bash
chmod +x orchestrator.sh
chmod +x bash/**/*.sh
```

## Documentation

- [PowerShell Scripts](powershell/README.md) - PowerShell-specific documentation
- [Python Scripts](python/README.md) - Python-specific documentation
- [Bash Scripts](bash/README.md) - Bash-specific documentation
- [MCP Configuration](.vscode/configs/mcp/README.md) - MCP profile management (VS Code Insiders)
- [Python Setup Guide](../docs/python-setup-troubleshooting.md) - Python installation help

## MCP Management (VS Code Insiders)

The MCP (Model Context Protocol) system provides tool integration for AI agents in VS Code Insiders. Use profiles to optimize token usage.

### Quick Start

```powershell
# Generate all profiles (core, fullstack, testing, data)
.\orchestrator.ps1 mcp new-profiles

# Switch to core profile (53 tools, ~50% token reduction)
.\orchestrator.ps1 mcp set-profile -Profile core

# Restart VS Code for changes to take effect

# Check active profile
.\orchestrator.ps1 mcp get-profile

# Test server health
.\orchestrator.ps1 mcp test-servers

# Compare profiles
.\orchestrator.ps1 mcp compare-profiles
```

### Python Validation

```bash
# Validate MCP configuration
python orchestrator.py mcp validate

# Analyze token usage
python orchestrator.py mcp analyze

# Compare profiles with JSON output
python orchestrator.py mcp analyze --compare --json
```

### Profile System

| Profile | Tools | Servers | Tokens | Use Case |
|---------|-------|---------|--------|----------|
| core | 53 | github, filesystem, git, fetch | 8-10k | Daily development (50% reduction) |
| fullstack | 80 | github, filesystem + 6 more | 11-14k | Web development + testing |
| testing | 87 | github, filesystem, playwright, git, fetch, postgres | 12-15k | Browser automation + QA |
| data | 47 | github, filesystem, postgres, sqlite, memory, git, fetch | 7-9k | Database/analytics work |
| all | 107 | All 9 servers | 15-20k | Full toolset (baseline) |

**Token Optimization:**
- Tools loaded at VS Code startup (not per-request)
- Each tool schema: ~180 tokens + 50 tokens per server
- core profile: 50% startup reduction vs all
- Profile switch requires VS Code restart

**See:** [.vscode/configs/mcp/README.md](../.vscode/configs/mcp/README.md) for detailed configuration docs.

## Contributing

When adding new scripts:

1. Follow SRP: One script, one responsibility
2. Use shared utilities (DRY principle)
3. Add to appropriate orchestrator
4. Update relevant README.md
5. Test with orchestrator and direct execution
6. Commit with descriptive message

---

**Status:** v3.0 - Refactored with SRP/DRY principles (2025-10-25)
