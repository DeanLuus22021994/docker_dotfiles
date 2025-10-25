# Validation Module

Python scripts for comprehensive validation of environment variables and configuration files before Docker stack deployment.

## Overview

The validation module ensures all required settings and configurations are valid before starting Docker services. This prevents runtime failures and provides early feedback on configuration issues.

## Scripts

### validate_env.py

**Purpose:** Validate required and optional environment variables

**Usage:**

```powershell
# Via orchestrator (recommended)
python ../orchestrator.py validate env

# Direct execution
python validate_env.py
```

**Environment Variables Checked:**

**Required (must be set):**

- `GITHUB_OWNER` - GitHub organization/username
- `GH_PAT` - GitHub Personal Access Token
- `DOCKER_POSTGRES_PASSWORD` - PostgreSQL password
- `DOCKER_MARIADB_PASSWORD` - MariaDB password
- `DOCKER_MARIADB_ROOT_PASSWORD` - MariaDB root password
- `DOCKER_REDIS_PASSWORD` - Redis password
- `POSTGRES_PASSWORD` - Alternative PostgreSQL password
- `MARIADB_PASSWORD` - Alternative MariaDB password
- `MARIADB_ROOT_PASSWORD` - Alternative MariaDB root password
- `REDIS_PASSWORD` - Alternative Redis password

**Optional (warnings only):**

- `DOCKER_ACCESS_TOKEN` - Docker Hub access token
- `CODECOV_TOKEN` - Codecov coverage reporting token

**Exit Codes:**

- `0` = All required variables set
- `1` = Missing required variables

**Example Output:**

```
============================================================
Environment Variables Validation
============================================================

✓ All required environment variables are set
⚠ Optional environment variables missing:
  - DOCKER_ACCESS_TOKEN: Docker Hub access token
  - CODECOV_TOKEN: Codecov token for coverage reporting

============================================================
✓ VALIDATION PASSED (with warnings)
============================================================
```

---

### validate_configs.py

**Purpose:** Validate configuration files (YAML, JSON, nginx, PostgreSQL, MariaDB)

**Usage:**

```powershell
# Via orchestrator (recommended)
python ../orchestrator.py validate configs

# Direct execution
python validate_configs.py
```

**Validations Performed:**

#### YAML Files

- **Tool:** `yamllint`
- **Files:** `docker-compose.yml`, `.github/workflows/*.yml`, etc.
- **Checks:** Syntax errors, formatting issues, structure problems

#### JSON Files

- **Files:** `package.json`, `*.json` (excludes `.vscode/*.json` JSONC files)
- **Checks:** Valid JSON syntax, proper structure

#### nginx Configuration

- **Tool:** Docker nginx container (`nginx -t`)
- **Files:** `web-content/nginx.conf`, `*.nginx.conf`
- **Checks:** Syntax errors, directive issues, invalid configurations

#### PostgreSQL Configuration

- **Files:** `*.postgresql.conf`, `pg_*.conf`
- **Checks:** Syntax validation, parameter format, setting validity

#### MariaDB Configuration

- **Files:** `*.mariadb.cnf`, `my.cnf`
- **Checks:** Syntax validation, section structure, option validity

**Exit Codes:**

- `0` = All configurations valid
- `1` = Validation errors found

**Example Output:**

```
=== Validating YAML Files ===
✓ docker-compose.yml is valid
✓ .github/workflows/ci.yml is valid

=== Validating JSON Files ===
✓ package.json is valid
✓ tsconfig.json is valid

=== Validating nginx Configs ===
✓ nginx configuration is valid

=== Validating PostgreSQL Config ===
✓ PostgreSQL configuration is valid

=== Validating MariaDB Config ===
✓ MariaDB configuration is valid

✓ ALL CONFIGURATION VALIDATION PASSED
```

---

## Module API

### Import Patterns

```python
# Import specific modules
from python.validation import validate_env, validate_configs

# Import all (via __all__)
from python.validation import *

# Import specific functions
from python.validation.validate_env import validate_env_vars
from python.validation.validate_configs import validate_yaml_files, validate_json_files
```

### Exports

The module exports the following via `__all__`:

- `validate_env` - Environment variable validation module
- `validate_configs` - Configuration file validation module

---

## Type Annotations

All functions use modern Python 3.14 type hints:

```python
def validate_env_vars() -> tuple[bool, list[str], list[str]]:
    """
    Validate required and optional environment variables.

    Returns:
        Tuple of (all_valid, missing_required, missing_optional)
    """
    missing_required: list[str] = []
    missing_optional: list[str] = []
    # ...
    return all_valid, missing_required, missing_optional

def validate_yaml_files() -> tuple[bool, list[str]]:
    """Validate all YAML files with yamllint."""
    errors: list[str] = []
    # ...
    return success, errors
```

---

## Dependencies

**Required:**

- `yamllint` - YAML linter
- `docker` - For nginx config validation (Docker must be running)

**Optional:**

- `jsonschema` - For JSON schema validation (if implementing)

**Installation:**

```powershell
# Using UV (recommended)
uv pip install yamllint

# Using pip
pip install yamllint
```

**Docker Requirements:**

- Docker daemon must be running for nginx validation
- nginx test uses: `docker run --rm -v $(pwd):/etc/nginx nginx:alpine nginx -t`

---

## Integration with Orchestrator

The orchestrator provides convenient access to validation scripts:

```powershell
# PowerShell
..\orchestrator.ps1 validate env
..\orchestrator.ps1 validate configs

# Bash
../orchestrator.sh validate env
../orchestrator.sh validate configs

# Python
python ..\orchestrator.py validate env
python ..\orchestrator.py validate configs
```

---

## Best Practices

### Pre-deployment Validation

Always validate before starting Docker stack:

```powershell
# 1. Validate environment
python ../orchestrator.py validate env

# 2. Validate configurations
python ../orchestrator.py validate configs

# 3. If all pass, start stack
docker-compose up -d
```

### CI/CD Integration

Add to your CI pipeline:

```yaml
# GitHub Actions example
- name: Validate Environment
  run: python scripts/orchestrator.py validate env
  env:
    GITHUB_OWNER: ${{ github.repository_owner }}
    GH_PAT: ${{ secrets.GH_PAT }}
    DOCKER_POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}

- name: Validate Configurations
  run: python scripts/orchestrator.py validate configs
```

### Pre-commit Hooks

Configure in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-env
        name: Validate Environment Variables
        entry: python scripts/orchestrator.py validate env
        language: system
        pass_filenames: false

      - id: validate-configs
        name: Validate Configuration Files
        entry: python scripts/orchestrator.py validate configs
        language: system
        pass_filenames: false
```

---

## Configuration Files

### yamllint Configuration

Create `.yamllint` in project root:

```yaml
extends: default

rules:
  line-length:
    max: 120
    level: warning
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
```

### Excluding Files

**YAML Validation:**

- Automatically skips `.github/dependabot.yml` and similar metadata files
- Add patterns to exclude list in `validate_configs.py`

**JSON Validation:**

- Automatically skips `.vscode/*.json` (JSONC with comments)
- Add patterns to exclude list in `validate_configs.py`

---

## Error Messages

### Environment Variable Errors

```
✗ VALIDATION FAILED
Missing required environment variables:
  - GH_PAT: GitHub Personal Access Token
  - DOCKER_POSTGRES_PASSWORD: PostgreSQL password

Set these in .env file or environment
```

### Configuration Errors

```
✗ Configuration validation failed:
  - docker-compose.yml:12: [error] syntax error: expected <block end>
  - nginx.conf:45: nginx: [emerg] unknown directive "invalid_option"
  - postgresql.conf:89: invalid parameter: "invalid_setting"
```

---

## Troubleshooting

### "yamllint not found"

Install yamllint:

```powershell
uv pip install yamllint
```

### Docker nginx validation fails

Ensure Docker is running:

```powershell
docker ps
```

### Environment variables not found

Check `.env` file exists and is loaded:

```powershell
# PowerShell
Get-Content .env

# Bash
cat .env
```

Load environment manually if needed:

```powershell
# PowerShell
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.+)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}
```

---

## Standards Compliance

### Python 3.14

- ✅ PEP 585: Built-in generics (`tuple[bool, list[str], list[str]]`)
- ✅ PEP 649: Deferred annotation evaluation
- ✅ PEP 484: Type hints on all functions

### Code Quality

- ✅ Black formatting (line-length=100)
- ✅ Ruff linting (strict mode)
- ✅ mypy type checking (strict mode)
- ✅ Comprehensive error handling

### Security

- ✅ No hardcoded secrets
- ✅ Environment variable validation
- ✅ Secure configuration checks

---

## Extending Validation

### Adding New Environment Variables

Edit `validate_env.py`:

```python
required_vars = {
    "NEW_VAR": "Description of new variable",
    # ... existing vars
}

optional_vars = {
    "OPTIONAL_NEW_VAR": "Description of optional variable",
    # ... existing vars
}
```

### Adding New Config Validators

Edit `validate_configs.py`:

```python
def validate_new_config() -> tuple[bool, list[str]]:
    """Validate new configuration type."""
    errors: list[str] = []

    # Validation logic

    return len(errors) == 0, errors

# Add to main()
def main():
    # ... existing validations
    passed, errors = validate_new_config()
    # ... handle results
```

---

**Last Updated:** 2025-10-25  
**Python Version:** 3.14.0+  
**Module Version:** 1.0.0
