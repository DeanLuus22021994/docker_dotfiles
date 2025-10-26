---
date_created: "2025-10-26T18:32:25.939451+00:00"
last_updated: "2025-10-26T18:32:25.939451+00:00"
tags: ["documentation", "agent", "development"]
description: "Documentation for principles"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- development
- best-practices
- architecture
  description: Core development principles and guidelines for the Docker cluster project
  ---\n# Development Principles

**TDD** (Test-Driven Development): Write tests before implementation
**SRP** (Single Responsibility Principle): One concern per module/file
**SSoT** (Single Source of Truth): No duplication, one authoritative source
**DRY** (Don't Repeat Yourself): Extract shared utilities, no code duplication
**Config-Driven**: Behavior controlled by configuration, not code
**Modular**: Loosely coupled, highly cohesive components

## Python Environment

- **Python 3.14.0+** for all scripts
- **UV package manager** for dependency management (faster than pip)
- **NOT** Microsoft Store Python (causes PATH issues on Windows)

## Scripts Organization (SRP/DRY)

All scripts organized by task domain:

- `python/validation/` - validate_env.py, validate_configs.py
- `python/audit/` - Code audit scripts
- `python/utils/` - Shared utilities (colors.py, logging.py)
- `powershell/config/` - Configuration management
- `powershell/docker/` - Docker operations
- `bash/docker/` - Docker operations

See [python environment guide](agent-python-setup.md) for setup details.
