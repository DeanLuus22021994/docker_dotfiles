---
date_created: '2025-10-27T02:37:40Z'
last_updated: '2025-10-27T02:37:40Z'
tags: [git, pre-commit, hooks, automation]
description: 'Git hooks and pre-commit automation configuration'
---

# Git Configuration

Pre-commit hooks for code quality and consistency enforcement.

## 📁 Files

### `.pre-commit-config.yaml`
**Pre-commit hooks configuration**.

**Hooks Configured**:

1. **General Quality**
   - Trailing whitespace removal
   - End-of-file fixer
   - Large file check (500KB limit)
   - Merge conflict detection

2. **Python**
   - Black (formatting)
   - Ruff (linting)
   - Pyright (type checking)
   - Mypy (strict type checking)

3. **YAML/JSON/TOML**
   - Syntax validation
   - Key sorting
   - Formatting

4. **Markdown**
   - markdownlint-cli2 (style checking)

5. **Security**
   - detect-secrets (prevent secret commits)

**Cache**: 608.4 MB persistent volume (`pre-commit-cache`)

---

## 🚀 Quick Start

### Install Pre-commit Hooks

```powershell
# In devcontainer or local environment
pip install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files
```

### Using Docker Container

```powershell
# Run pre-commit in container
docker-compose run --rm cluster-pre-commit run --all-files

# Run specific hook
docker-compose run --rm cluster-pre-commit run black
```

---

## 🎯 Best Practices

✅ **Run before push** - Catch issues locally  
✅ **Cache environment** - Persistent volume for instant restarts  
✅ **Update regularly** - `pre-commit autoupdate`  
✅ **Skip when needed** - `git commit --no-verify` (use sparingly)  

---

## 📚 References

- [Pre-commit Documentation](https://pre-commit.com/)
