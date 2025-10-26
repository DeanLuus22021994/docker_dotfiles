---
date_created: "2025-10-26T18:32:25.995652+00:00"
last_updated: "2025-10-26T18:32:25.995652+00:00"
tags: ["documentation", "configuration", "setup"]
description: "Documentation for branch protection"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- documentation
  description: Branch protection rules configuration for main branch
  ---\n# Branch Protection Configuration

Protection rules for `main` branch to ensure code quality and review process.

## Configuration

**File:** `.config/github/branch-protection.yml`

**Enforces:**

- Required status checks (4 validation jobs)
- Required PR approvals (1 minimum)
- Conversation resolution before merge
- No force pushes or deletions
- Administrator enforcement

## Apply Protection Rules

**Via Script:**

```powershell
.\scripts\apply-settings.ps1 -ApplyBranchProtection
```

**Via GitHub CLI:**

```bash
gh api repos/DeanLuus22021994/docker_dotfiles/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["validate"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

**Via GitHub UI:**

1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass
   - ✅ Require conversation resolution
   - ✅ Include administrators

## Validation Jobs

4 required status checks before merge:

1. `validate-environment` - Environment configuration validation
2. `validate-configs` - Configuration files validation
3. `validate-docker-compose` - Docker Compose syntax validation
4. `validate-pre-commit` - Pre-commit hooks validation

**Cost:** FREE
