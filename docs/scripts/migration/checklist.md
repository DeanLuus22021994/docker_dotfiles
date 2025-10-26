---
date_created: "2025-10-26T18:32:25.985633+00:00"
last_updated: "2025-10-26T18:32:25.985633+00:00"
tags: ["documentation", "scripts", "automation"]
description: "Documentation for checklist"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- scripts
- migration
- ci-cd
  description: Migration checklist for developers and CI/CD pipelines
  ---\n# Migration Checklist

## For Developers

- [ ] Update local scripts to use new paths
- [ ] Replace direct imports with package imports
- [ ] Use shared utilities instead of duplicating code
- [ ] Update documentation references
- [ ] Test scripts with new structure

## For CI/CD Pipelines

- [ ] Update GitHub Actions workflow paths
- [ ] Update GitLab CI/CD script paths
- [ ] Update Jenkins pipeline scripts
- [ ] Update Azure DevOps pipeline tasks
- [ ] Update any automation scripts

## For Documentation

- [ ] Update README.md references
- [ ] Update setup guides
- [ ] Update troubleshooting docs
- [ ] Update API documentation
- [ ] Update contribution guidelines

## For Build Scripts

- [ ] Update Makefile targets (✅ Done)
- [ ] Update package.json scripts
- [ ] Update build automation
- [ ] Update deployment scripts

## Common Updates

**Makefile:**

```makefile
# Old: python scripts/validate_env.py
# New: python scripts/python/validation/validate_env.py
```

**GitHub Actions:**

```yaml
# Old: run: python scripts/validate_env.py
# New: run: python scripts/python/validation/validate_env.py
```

**Python Imports:**

```python
# Old: from validate_env import Colors
# New: from python.utils.colors import Colors
```
