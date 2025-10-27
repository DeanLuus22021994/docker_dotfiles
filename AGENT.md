---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["development", "guidelines", "agent", "documentation"]
description: "Development guidelines documentation index for AI agents and developers"
---

# Development Guidelines

Comprehensive development guidelines for AI agents and developers.

## Core Principles

**TDD** · **SRP** · **SSoT** · **DRY** · **Config-Driven** · **Modular**

## Documentation

**Foundation:** [Principles](docs/agent/principles.md) | [Python Setup](docs/agent/python-setup.md) | [Configuration](docs/agent/configuration.md) | [Environment](docs/agent/environment.md)

**Quality:** [Code Quality](docs/agent/code-quality.md) | [Docker Stack](docs/agent/docker-stack.md) | [File Organization](docs/agent/file-organization.md) | [Security](docs/agent/security.md)

**Workflow:** [AI Workflow](docs/agent/workflow.md) | [Quick Reference](docs/agent/reference.md)

## File Structure

**Config:** `.config/mkdocs/` (docs), `.config/docker/` (daemon), `.config/python/` (pyright/pytest), `.config/git/` (pre-commit), `.config/markdownlint/` (linting), `.config/monitoring/` (prometheus/grafana)

**Application:** `backend/` (Express.js), `dashboard/` (React), `dockerfile/` (multi-stage builds)

**Automation:** `scripts/orchestrator.py` (CLI), `scripts/python/` (validation/audit/utils), `scripts/powershell/` (config/docker/mcp)

**Documentation:** `docs/` (MkDocs site), `.github/` (copilot instructions, TODO, commands, issue templates)

**Quality:** `pyproject.toml` (Python config), `.vscode/` (workspace settings, snippets, instructions)

## Quick Commands

**See:** [.github/commands.yml](.github/commands.yml) for complete command reference

**Golden Rule:** Config-driven, SSoT, explicit paths, validate before deploy, human approves all changes.

See [complete guide](docs/agent/principles.md) for details.
