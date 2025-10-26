---
date_created: "2025-10-26T18:32:25.988592+00:00"
last_updated: "2025-10-26T18:32:25.988592+00:00"
tags: ["documentation", "scripts", "automation"]
description: "Documentation for troubleshooting"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- scripts
- migration
- troubleshooting
  description: Common migration issues and solutions
  ---\n# Migration Troubleshooting

## Issue: "Module not found" errors

**Cause:** Python can't find new package structure

**Solution:** Add parent directory to Python path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
```

## Issue: "File not found" errors

**Cause:** Using old script paths

**Solution:** Update paths to new locations. See `path-mapping.md` for complete mapping.

## Issue: Import errors in Python scripts

**Cause:** Using old import patterns

**Solution:** Use package imports:

```python
# Old
from validate_env import Colors

# New
from python.utils.colors import Colors
```

## Issue: GitHub Actions failing

**Cause:** Workflow using old paths

**Solution:** Update workflow YAML:

```yaml
# Old
run: python scripts/validate_env.py

# New
run: python scripts/python/validation/validate_env.py
```

## Issue: Orchestrator not found

**Cause:** Running from wrong directory

**Solution:** Run from project root or use full path:

```powershell
cd C:\global\docker
python scripts/orchestrator.py validate env
```

## Need Help?

1. Check `scripts/python/*/README.md` for module docs
2. Review `scripts/README.md` for orchestrator usage
3. See `docs/python-setup-troubleshooting.md` for environment issues
4. Check git history for specific file migrations
