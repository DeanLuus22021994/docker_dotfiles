---
date_created: "2025-10-26T18:32:25.999584+00:00"
last_updated: "2025-10-26T18:32:25.999584+00:00"
tags: ['documentation', 'configuration', 'setup']
description: "Documentation for workflows"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- ci-cd
description: GitHub Actions workflows and automation configuration
---\n# GitHub Workflows

GitHub Actions workflows for CI/CD automation with self-hosted runners.

## Actions Configuration

**File:** `.config/github/actions.yml`

- Unlimited free minutes (self-hosted runners)
- Workflow permissions (read-only by default)
- Fork PR workflows with approval required
- 90-day artifact retention

## PR Labeler Workflow

**File:** `.config/github/workflows/labeler.yml`

Auto-applies labels to PRs based on changed files:

- `documentation` - Markdown, docs/ folder
- `config` - Configuration files (.yml, .env)
- `docker` - Dockerfiles, compose files
- `monitoring` - Prometheus, Grafana configs
- `ci-cd` - Workflow files, Makefile
- `python`, `nodejs` - Language-specific files
- `scripts` - Shell/PowerShell scripts
- `tests` - Test files
- `security` - Secrets, passwords

**Setup:**

```bash
# Copy to correct location
mkdir -p .github/workflows
cp .config/github/workflows/labeler.yml .github/workflows/

# Commit
git add .github/workflows/labeler.yml
git commit -m "chore(ci): enable automatic PR labeling"
git push
```

## Test Workflows

```powershell
# Trigger manually
gh workflow run validate.yml

# Check status
gh run list --workflow=validate.yml --limit 5
```

**Cost:** $0/month (self-hosted)
