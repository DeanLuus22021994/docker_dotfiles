# GitHub Copilot Instructions - Docker Compose Development Environment

## Project Context
This is a Docker Compose development environment with Python 3.14, Node.js 22, and PostgreSQL/MariaDB support. It includes AI agent capabilities, MCP (Model Context Protocol) integration, and comprehensive testing infrastructure.

## Technology Stack
- **Python**: 3.14 with UV package manager, Black formatter, Ruff linter, mypy type checker
- **Node.js**: 22 with Vite, legacy peer deps support
- **Databases**: PostgreSQL/MariaDB with proper health checks
- **Docker**: Docker Compose (no `version:` field - deprecated)
- **Testing**: pytest with coverage, async support
- **AI/Agent**: agent_app.py with MCP server integration

## Critical Standards

### Docker Compose
- ❌ NEVER use `version:` field in docker-compose.yml (deprecated in modern Docker)
- ✅ Volume naming: `docker_<service>_<type>` (e.g., `docker_postgres_data`)
- ✅ Health checks: `interval:30s timeout:10s retries:3 start_period:40s`
- ❌ NEVER hardcode passwords - use environment variables or secrets
- ✅ Use `.docker-compose/` directory for stack files

### Python Development
- Python version: `py314`
- Package manager: `uv` (fast Rust-based pip replacement)
- Formatter: `black` (line-length: 88)
- Linter: `ruff` (replaces flake8, isort, etc.)
- Type checker: `mypy --strict`
- Testing: `pytest` with async support

### Node.js Development
- Always use `npm install --legacy-peer-deps` for compatibility
- Use Vite for modern build tooling
- Node 22 LTS features available

### Code Quality Commands
```bash
# Python
uv sync                                    # Install dependencies
uv run python -m pytest                    # Run tests
uv run python -m pytest --cov=. --cov-report=html  # Coverage
ruff check .                               # Lint
black .                                    # Format
mypy .                                     # Type check

# Docker
python .docker-compose/validate_stacks.py  # Validate compose files
docker-compose -f .docker-compose/basic-stack/docker-compose.yml build
```

## Project Structure
```
/workspaces/docker/
├── .copilot/                 # Copilot configuration (THIS FOLDER)
├── .devcontainer/            # Dev container configuration
├── .docker-compose/          # Docker compose stacks
├── .github/                  # GitHub workflows and instructions
├── agent/                    # Agent configuration
├── agent_app.py              # Main AI agent application
├── docs/                     # Documentation
├── tests/                    # Test suites (unit/integration/e2e)
├── pyproject.toml            # Python project configuration
└── package.json              # Node.js configuration
```

## Important Files to Reference

### Configuration Files
- `.github/copilot-instructions.md` - Main Copilot instructions
- `.github/instructions/agent.instructions.md` - Agent-specific rules
- `pyproject.toml` - Python dependencies and tool configs
- `agent/config.py` - Agent configuration dataclass

### Key Implementation Files
- `agent_app.py` - Main AI agent with FastAPI server
- `agent/config.py` - Configuration management
- `.docker-compose/validate_stacks.py` - Compose validation script

## AI Agent Development

### Agent Framework
- Uses async/await patterns extensively
- FastAPI for HTTP endpoints
- MCP (Model Context Protocol) for tool calling
- GitHub CLI integration for repository operations

### Available Tools
1. **GitHub CLI** - Repository operations via `gh` command
2. **File Operations** - Read/write/list file operations
3. **Docker Operations** - Container management with auto-auth
4. **Config Management** - Configuration file handling

### Environment Variables
```bash
GITHUB_TOKEN / GH_TOKEN           # GitHub API access
AZURE_CLIENT_ID/SECRET/TENANT_ID  # Azure AI services
DOCKER_*                          # Docker configuration
HUGGINGFACE_ACCESS_TOKEN          # AI model access
```

## Code Style Guidelines

### Type Hints
- ✅ Use modern syntax: `dict[str, Any]` not `Dict[str, Any]`
- ✅ Use `X | None` not `Optional[X]`
- ✅ Use `list[str]` not `List[str]`
- ✅ Import from `collections.abc` for `Callable`, `Iterable`, etc.

### Python Best Practices
- Always use f-strings for formatting
- Use dataclasses for configuration objects
- Implement proper error handling with try/except
- Add type hints to all function signatures
- Write docstrings for public functions
- Use async/await for I/O operations

### Docker Best Practices
- Use multi-stage builds for optimization
- Leverage BuildKit features (buildx)
- Implement proper health checks
- Use .dockerignore files
- Cache layer optimization

## Testing Guidelines
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- E2E tests: `tests/e2e/`
- Use pytest fixtures for setup/teardown
- Mock external dependencies
- Aim for >80% coverage

## Common Tasks

### Running Tests
```bash
# Quick test
uv run python -m pytest

# With coverage
uv run python -m pytest --cov=. --cov-report=html

# Specific test file
uv run python -m pytest tests/unit/test_config.py
```

### Docker Operations
```bash
# Validate compose files
python .docker-compose/validate_stacks.py

# Build a stack
docker-compose -f .docker-compose/basic-stack/docker-compose.yml build

# Start with logs
docker-compose -f .docker-compose/basic-stack/docker-compose.yml up

# Clean up
docker-compose -f .docker-compose/basic-stack/docker-compose.yml down -v
```

### Agent Development
```bash
# Run agent
uv run python agent_app.py

# Test agent tools
uv run python -c "import agent_framework; print('Agent framework ready')"

# Run MCP server
uv run python -m mcp.server
```

## Performance Optimization

### Copilot Performance Tips
1. The `.copilot/ignore` file excludes large/irrelevant files
2. Focus on source code, not generated artifacts
3. Use semantic search for large codebases
4. Reference specific files when possible

### Build Performance
- Use Docker BuildKit caching
- Optimize Dockerfile layer ordering
- Use `.dockerignore` files
- Leverage multi-stage builds

## Troubleshooting

### Common Issues
1. **Import errors**: Run `uv sync` to install dependencies
2. **Docker permission issues**: Check `DOCKER_HOST` env var
3. **GitHub CLI not working**: Verify `GITHUB_TOKEN` or `GH_TOKEN`
4. **Type checking failures**: Update type hints to modern syntax

### Debug Commands
```bash
# Check Python environment
uv run python -c "import sys; print(sys.version)"

# Check agent dependencies
uv run python -c "import agent_framework, openai, anthropic; print('OK')"

# Test GitHub CLI
gh auth status

# Check Docker
docker version
docker-compose version
```

## Deprecated/Avoid

### Extensions
- ❌ GitHub Copilot Workspace (obsolete)
- ❌ Third-party extensions without >10M downloads

### Docker Compose
- ❌ `version:` field
- ❌ Hardcoded passwords
- ❌ Missing health checks

### Python
- ❌ Old typing imports (`Dict`, `List`, `Optional`)
- ❌ Using `pip` instead of `uv`
- ❌ Missing type hints

## Additional Resources
- Main instructions: `.github/copilot-instructions.md`
- Agent instructions: `.github/instructions/agent.instructions.md`
- TODO list: `docs/TODO.md`
- Architecture: `docs/architecture.md`
