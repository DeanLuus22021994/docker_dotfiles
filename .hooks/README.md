# Git Hooks Directory

Platform-agnostic Git hooks using Docker containers for consistent validation across all environments.

## Overview

This directory contains standardized Git hooks that use Docker containers instead of local installations, ensuring:

- **Platform Agnostic**: Works on Windows, Linux, and macOS
- **No Local Dependencies**: Uses containerized tools (no virtualenv required)
- **Consistent Validation**: Same checks run everywhere
- **Easy Installation**: Single script to set up all hooks

## Available Hooks

### pre-commit

Validates code quality before commits using the `cluster-pre-commit` container.

**Checks include:**

- YAML/JSON syntax validation
- Shell script linting (shellcheck)
- Markdown linting
- Python formatting (black, ruff, mypy)
- Docker linting (hadolint)
- Secret detection
- Documentation frontmatter validation

**Files:**

- `pre-commit` - Bash implementation (Linux/Mac primary)
- `pre-commit.ps1` - PowerShell implementation (Windows primary)

## Installation

### Quick Install

From repository root:

```bash
# Linux/Mac
./scripts/bash/git/install-git-hooks.sh

# Windows (PowerShell)
.\scripts\powershell\git\Install-GitHooks.ps1
```

### Manual Install

```bash
# Copy hooks to .git/hooks/
cp .hooks/pre-commit .git/hooks/
cp .hooks/pre-commit.ps1 .git/hooks/

# Make executable (Linux/Mac)
chmod +x .git/hooks/pre-commit
```

## Usage

Hooks run automatically on `git commit`. To skip validation:

```bash
git commit --no-verify
```

## Requirements

- Docker Desktop running
- Git repository

## Architecture

```
.hooks/
├── README.md           # This file
├── pre-commit          # Bash hook (auto-detects PowerShell)
└── pre-commit.ps1      # PowerShell implementation

Execution Flow:
1. Git triggers .git/hooks/pre-commit
2. Hook detects platform and uses appropriate implementation
3. Docker container (cluster-pre-commit) runs validation
4. Results returned to git (pass/fail)
```

## Customization

Edit `.pre-commit-config.yaml` in repository root to configure validation rules.

## Troubleshooting

**Hook not running:**

- Verify hooks installed: `ls -la .git/hooks/pre-commit`
- Check executable: `chmod +x .git/hooks/pre-commit`

**Docker errors:**

- Ensure Docker Desktop is running
- Build container manually: `docker build -f dockerfile/pre-commit.Dockerfile -t cluster-pre-commit .`

**Validation failures:**

- Review error output for specific issues
- Run manually: `docker run --rm -v $(pwd):/workspace cluster-pre-commit bash -c "cd /workspace && pre-commit run --all-files"`

## Contributing

When adding new hooks:

1. Create both bash and PowerShell versions
2. Test on Windows, Linux, and macOS
3. Update this README
4. Update installation scripts
5. Document in `.pre-commit-config.yaml`
