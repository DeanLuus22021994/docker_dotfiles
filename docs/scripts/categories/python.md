---
date_created: "2025-10-26T18:32:25.984785+00:00"
last_updated: "2025-10-26T18:32:25.984785+00:00"
tags: ['documentation', 'scripts', 'automation', 'python']
description: "Documentation for python"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- scripts
- python
description: Python scripts organization and modules
---\n# Python Scripts

## Modules

**`python/validation/`** - Environment and configuration validation
- `validate_env.py` - Check required environment variables
- `validate_configs.py` - Validate YAML/JSON configs

**`python/audit/`** - Code quality and dependency auditing
- `code_quality.py` - Black, Ruff, mypy checks
- `dependencies.py` - Package vulnerability scanning

**`python/utils/`** - Shared utilities (DRY)
- `colors.py` - Terminal colors for output
- `file_utils.py` - File operations (read/write JSON, ensure dir)
- `logging_utils.py` - Structured logging setup

## Usage

**Direct execution:**

```bash
python scripts/python/validation/validate_env.py
python scripts/python/audit/code_quality.py
```

**Via orchestrator (recommended):**

```bash
python scripts/orchestrator.py validate env
python scripts/orchestrator.py audit code
```

## Python Requirements

- Python 3.14+ required
- Modern type hints (PEP 585 built-in generics)
- Black formatting, Ruff linting, mypy type checking

See module-specific READMEs: `python/{validation,audit,utils}/README.md`
