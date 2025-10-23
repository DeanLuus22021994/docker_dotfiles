# Docker Compose Examples - Copilot Instructions

## Stack
- Python 3.14 + UV | Node.js 22 + Vite | PostgreSQL/MariaDB
- Hidden dirs: `.docker-compose/`, `.devcontainer/`, `.github/`

## Standards
- **NO** `version:` in docker-compose.yml (deprecated)
- Volumes: `docker_examples_<service>_<type>`
- Health checks: `interval:30s timeout:10s retries:3 start_period:40s`
- Secrets: Never hardcode passwords
- Python: py314, UV, Black, Ruff, mypy strict
- Node: npm install --legacy-peer-deps

## Commands
```bash
python .docker-compose/validate_stacks.py
docker-compose -f .docker-compose/basic-stack/docker-compose.yml build
```

## TODO
Check TODO.md for active tasks