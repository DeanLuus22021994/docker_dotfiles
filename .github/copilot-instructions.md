# GitHub Copilot Instructions

## Stack & Environment

**Languages & Runtimes:**

- Python 3.14 + UV package manager
- Node.js 22 + Vite + React 18 + TypeScript
- PostgreSQL 17 + MariaDB 11

**Infrastructure:**

- Docker Compose (no `version:` key - deprecated)
- Docker BuildKit for optimized builds
- Nginx reverse proxy

**Key Directories:**

- `.github/` - CI/CD workflows, project docs
- `scripts/` - Python/PowerShell/Bash automation
- `dockerfile/` - All Dockerfiles
- `web-content/` - React dashboard (Vite + TypeScript)
- `api/` - Express.js backend (Node 22)

---

## Coding Standards

### Docker Compose

```yaml
# ❌ NEVER include version (deprecated in Compose v2)
# version: "3.8"  # REMOVE THIS

services:
  postgres:
    image: postgres:17
    volumes:
      - docker_examples_postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Volume Naming:** `docker_examples_<service>_<type>`  
**Secrets:** Use `.env` files, never hardcode

### Python

**Version:** 3.14 (strict)  
**Package Manager:** UV (not pip)  
**Formatting:** Black (line-length=100)  
**Linting:** Ruff (strict mode)  
**Type Checking:** mypy (strict mode)

**Type Hints (PEP 585):**

```python
# ✅ Modern built-in generics (Python 3.14)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ❌ Old typing module (deprecated)
from typing import List, Dict
def process_items(items: List[str]) -> Dict[str, int]:  # DON'T USE
```

### Node.js

**Version:** 22 (LTS)  
**Package Manager:** npm  
**Install Command:** `npm install --legacy-peer-deps`

### Scripts Organization

```
scripts/
├── orchestrator.py|ps1|sh    # Main entry points
├── python/
│   ├── validation/           # Config validation
│   ├── audit/                # Code quality checks
│   └── utils/                # Shared utilities
├── powershell/
│   ├── config/               # Settings management
│   ├── docker/               # Container ops
│   └── cleanup/              # Maintenance
└── bash/
    ├── docker/               # Container ops
    └── docs/                 # Documentation builds
```

---

## Common Commands

**Validation:**

```bash
# Python scripts
python scripts/orchestrator.py validate env
python scripts/orchestrator.py validate configs
python scripts/orchestrator.py audit code

# Docker stacks
python .docker-compose/validate_stacks.py
```

**Docker Compose:**

```bash
# Build & start
docker-compose build
docker-compose up -d

# Specific stack
docker-compose -f .docker-compose/basic-stack/docker-compose.yml up -d
```

**Development:**

```bash
# Web dashboard
cd web-content && npm run dev

# API server
cd api && npm start
```

---

## Critical Guidelines

**DO:**

- ✅ Check `.github/TODO.md` for current tasks
- ✅ Use UV for Python package management
- ✅ Use modern type hints (PEP 585 built-ins)
- ✅ Follow Black formatting (100 char lines)
- ✅ Include health checks in all services
- ✅ Use volume names with `docker_examples_` prefix

**DON'T:**

- ❌ Add `version:` to docker-compose.yml
- ❌ Use deprecated `typing.List/Dict/Tuple`
- ❌ Hardcode secrets or passwords
- ❌ Use `pip` instead of `uv`
- ❌ Skip health checks on services

---

## Documentation

**Project Status:** `.github/TODO.md`  
**Security Policy:** `SECURITY.md`  
**Setup Guide:** `SETUP.md`  
**Architecture:** `web-content/ARCHITECTURE.md`  
**Scripts Guide:** `scripts/README.md`

---

**Last Updated:** 2025-10-25
