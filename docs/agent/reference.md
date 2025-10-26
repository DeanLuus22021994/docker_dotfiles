---
date_created: "2025-10-26T18:32:25.940467+00:00"
last_updated: "2025-10-26T18:32:25.940467+00:00"
tags: ["documentation", "agent", "development"]
description: "Documentation for reference"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- documentation
- commands
  description: Quick reference for file paths, validation commands, and common tasks
  ---\n# Quick Reference

## Validation Commands

```powershell
python scripts/python/validation/validate_env.py          # Environment
docker-compose config --quiet                              # Compose syntax
python scripts/python/validation/validate_configs.py       # All configs
```

## Common Tasks

**Add new service**:

1. Add to docker-compose.yml
2. Add environment variables to .env.example
3. Update scripts/validate_env.py
4. Add config to .config/[category]/
5. Validate: docker-compose config --quiet

**Update config**:

1. Edit file in .config/[category]/
2. Validate syntax (category-specific command)
3. Restart service: docker-compose restart [service]

**Change password**:

1. Update .env file
2. Restart service: docker-compose restart [service]
3. Update GitHub Secrets (for CI/CD)

---

**Remember**: Config-driven, SSoT, explicit paths, validate before deploy, human approves all changes.
