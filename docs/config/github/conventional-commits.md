---
date_created: "2025-10-26T18:32:25.996132+00:00"
last_updated: "2025-10-26T18:32:25.996132+00:00"
tags: ["documentation", "configuration", "setup"]
description: "Documentation for conventional commits"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- documentation
  description: Conventional commits standard for semantic commit messages
  ---\n# Conventional Commits

Semantic commit message format for automatic changelog generation.

## Commit Types

```bash
# Features
git commit -m "feat(api): add health check endpoint"

# Bug fixes
git commit -m "fix(docker): correct volume mount path"

# Documentation
git commit -m "docs: update deployment guide"

# Refactoring
git commit -m "refactor(monitoring): restructure alert rules"

# Performance
git commit -m "perf(postgres): optimize query indexes"

# Tests
git commit -m "test(api): add integration tests"

# CI/CD
git commit -m "ci: add automated deployment"

# Dependencies
git commit -m "chore(deps): update prometheus to v2.45"

# Breaking changes
git commit -m "feat(api)!: change response format

BREAKING CHANGE: API now returns JSON instead of XML"
```

## Format Structure

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Type:** feat, fix, docs, refactor, perf, test, ci, chore
**Scope:** Component affected (api, docker, monitoring, etc.)
**Subject:** Short description (imperative, lowercase, no period)

## Benefits

- Auto-generate changelogs
- Semantic versioning automation
- Clear git history
- Easy to filter by type

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
