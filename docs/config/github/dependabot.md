---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["github", "dependabot", "automation", "dependencies"]
description: "Dependabot configuration for automated dependency updates"
---
# Dependabot Configuration

Automated dependency updates for Docker images, Python packages, Node.js modules, and GitHub Actions.

## Update Schedule

```yaml
Updates:
- Docker images: Weekly Monday 9:00 AM
- Python (pip): Weekly Monday 9:00 AM  
- Node.js (npm): Weekly Monday 9:00 AM
- GitHub Actions: Monthly
```

## Features

- Max 5 open PRs per ecosystem (3 for Actions)
- Auto-labeling by dependency type
- Conventional commit messages (`chore(deps)`)
- Auto-assigns to @DeanLuus22021994

## Workflow

1. Dependabot scans dependencies on schedule
2. Creates PRs for available updates
3. Applies semantic versioning strategy
4. Requires manual review and merge

## Setup

```bash
# Verify configuration
cat .config/github/dependabot.yml

# Enable in GitHub settings
# Settings → Security & analysis → Enable Dependabot
```

## PR Management

```powershell
# Review Dependabot PR
gh pr view 123

# Check tests
gh pr checks 123

# Approve and merge
gh pr review 123 --approve
gh pr merge 123 --squash
```

**Cost:** FREE
