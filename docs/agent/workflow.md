---
date_created: "2025-10-26T18:32:25.941427+00:00"
last_updated: "2025-10-26T18:32:25.941427+00:00"
tags: ["documentation", "agent", "development"]
description: "Documentation for workflow"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- automation
- development
  description: AI-optimized development workflow and human-in-the-loop procedures
  ---\n# AI-Optimized Workflow

## Human-in-the-Loop

1. **Agent proposes changes** - Clear file paths, specific edits
2. **Human reviews** - Validation scripts provide clear errors
3. **Manual approval** - Developer commits after verification
4. **Pre-commit validates** - Automated checks before commit
5. **CI/CD validates** - GitHub Actions on push

## Example Workflow

```powershell
# 1. Agent makes changes (via Copilot)
# ... file edits happen ...

# 2. Validate changes
python scripts/validate_env.py
docker-compose config --quiet

# 3. Test locally
docker-compose --profile dev up -d
docker-compose ps

# 4. Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: migrate configs to .config/ structure"

# 5. Push (CI/CD validates)
git push origin main
```

See [quick reference](agent-reference.md) for common commands and file paths.
