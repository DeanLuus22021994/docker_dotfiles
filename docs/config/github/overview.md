---
date_created: "2025-10-26T18:32:25.997571+00:00"
last_updated: "2025-10-26T18:32:25.997571+00:00"
tags: ["documentation", "configuration", "setup"]
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- overview
- automation
  description: GitHub configuration overview for repository automation and CI/CD
  ---\n# GitHub Configuration Overview

Configuration files for GitHub-specific repository automation, CI/CD, security, and development workflows. All features are **FREE** for public repositories.

## Configuration Files

- `repository.yml` - Repository metadata and settings as code
- `branch-protection.yml` - Branch protection rules for main branch
- `secrets.yml` - Documentation for 11 required secrets
- `actions.yml` - GitHub Actions permissions and runner setup
- `code-security.yml` - Security scanning and dependency review
- `dependabot.yml` - Automated dependency updates
- `labeler.yml` - Automatic PR labeling rules
- `workflows/labeler.yml` - PR labeler workflow

## Cost Breakdown

**Total: $0/month** - All features free for public repos with self-hosted runners

| Feature                | Cost                    |
| ---------------------- | ----------------------- |
| Actions Minutes        | FREE (self-hosted)      |
| Artifact Storage       | FREE (90-day retention) |
| Secrets Storage        | FREE (unlimited)        |
| Advanced Security      | FREE (public repos)     |
| CodeQL/Secret Scanning | FREE                    |
| Dependabot             | FREE                    |

## Quick Start

```powershell
# Apply all settings
.\scripts\apply-settings.ps1 -ApplyAll

# Set GitHub secrets
.\scripts\setup_secrets.ps1 -SetGitHubSecrets
```

**Setup Time:** ~5 minutes
