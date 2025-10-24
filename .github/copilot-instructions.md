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

## Tool Usage Guidelines

### get_changed_files Tool
**Purpose**: Retrieve git diffs of current file changes in the repository for comprehensive change analysis
**Usage**: Use this tool to see what files have been modified, added, or deleted in the current git working directory
**Important Notes**:
- Returns git diff output showing changes between working directory and last commit
- Useful for understanding what changes have been made before committing
- Can be used with `run_in_terminal` for additional git commands if needed
- Does NOT modify files - only shows differences
- Essential for agent development workflows to track codebase evolution
- Helps identify files that need testing or validation after changes

### When to Use Tools
- Use `get_changed_files` to review current changes before validation/testing
- Use `run_in_terminal` for git operations like `git status`, `git diff`, `git add`, etc.
- Combine tools when needed: check changes first, then run git commands
- For agent development: Always check changes before running tests or validation
- Use semantic_search for finding code patterns across the codebase
- Use grep_search for exact string matching within files

## TODO
Check TODO.md for active tasks