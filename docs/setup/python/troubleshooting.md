---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["python", "troubleshooting", "setup", "errors"]
description: "Python setup troubleshooting guide overview"
---
# Python Setup Troubleshooting

Common Python 3.14 setup issues and solutions.

## Common Issues

**1. Python 3.14 not found**
- Install via UV: `uv python install 3.14`
- Verify: `python --version`

**2. UV installation fails**
- Try alternative: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows: Download from astral.sh/uv

**3. Package installation errors**
- Clear cache: `uv cache clean`
- Reinstall: `uv pip install -e ".[dev]" --reinstall`

**4. Import errors**
- Check Python path: `python -c "import sys; print(sys.path)"`
- Add parent directory to path in scripts

**5. Type checking failures**
- Update mypy: `uv pip install --upgrade mypy`
- Use Python 3.14 type hints (PEP 585)

## Quick Fixes

```bash
# Reinstall Python environment
rm -rf .venv
uv venv
uv pip install -e ".[dev]"

# Verify installation
python --version
pytest --version
```

See subdocs for detailed troubleshooting steps and platform-specific issues.
