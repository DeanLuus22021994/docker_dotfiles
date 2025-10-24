# Docker Compose - Copilot Instructions

## Stack
- Python 3.14 + UV | Node.js 22 + Vite | PostgreSQL/MariaDB
- Hidden dirs: `.docker-compose/`, `.devcontainer/`, `.github/`

## Standards
- **NO** `version:` in docker-compose.yml (deprecated)
- Volumes: `docker_<service>_<type>`
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
- Integrates with GitHub tokens for enhanced repository analysis

### semantic_search Tool
**Purpose**: Run a natural language search for relevant code or documentation comments from the user's current workspace
**Usage**: Returns relevant code snippets from the user's current workspace if it is large, or the full contents if small
**Important Notes**:
- Use natural language queries that might appear in code, function names, variable names, or comments
- Particularly effective for agent development when searching for patterns, implementations, or API usage
- Combines well with environment variables like GITHUB_TOKEN for enhanced context
- Supports complex queries for finding agent frameworks, MCP implementations, and AI model integrations
- Returns full workspace contents for small projects, snippets for large codebases

### Environment Variable Integration
**Available Environment Variables for Agent Development**:
- `GITHUB_TOKEN` / `GH_TOKEN`: For GitHub API access and enhanced repository operations
- `AZURE_CLIENT_ID/SECRET/TENANT_ID`: For Azure AI and cloud service integrations
- `DOCKER_*`: For containerized agent deployments and testing
- `PYTHON_*`: For Python environment configuration and virtual environments
- `HUGGINGFACE_ACCESS_TOKEN`: For accessing AI models and datasets

### When to Use Tools
- Use `get_changed_files` to review current changes before validation/testing
- Use `semantic_search` for finding code patterns, agent implementations, or API usage
- Use `run_in_terminal` for git operations like `git status`, `git diff`, `git add`, etc.
- Combine tools when needed: check changes first, then run git commands
- For agent development: Always check changes before running tests or validation
- Leverage environment variables for enhanced tool capabilities and integrations

## TODO
Check TODO.md for active tasks