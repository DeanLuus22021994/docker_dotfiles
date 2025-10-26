---
date_created: "2025-10-26T18:32:25.966835+00:00"
last_updated: "2025-10-26T18:32:25.966835+00:00"
tags: ['documentation', 'testing', 'pytest']
description: "Documentation for ci cd"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- testing
- ci-cd
- github-actions
- automation
description: CI/CD pipeline configuration for automated testing
---\n# CI/CD Pipeline

## GitHub Actions Workflow

**File:** `.github/workflows/test.yml`

## Test Job (Matrix Strategy)

**Platforms:** Ubuntu, Windows, macOS  
**Python:** 3.14

**Steps:**
1. Checkout code
2. Setup Python with pip cache
3. Install UV package manager
4. Install dependencies: `uv pip install -e ".[dev]"`
5. Run pytest: `pytest --cov=scripts/python --cov-report=xml`
6. Upload coverage to Codecov
7. Upload test artifacts

## Lint Job

- **Black**: Format check (line-length=100)
- **Ruff**: Linting with strict mode
- **mypy**: Type checking (strict mode)

## Validation Job

- YAML validation with yamllint
- JSON validation via Python script

## Summary Job

- Depends on: test, lint, validation
- Reports overall status
- Fails if any job fails

## Triggers

- Push to `main`, `develop` branches
- Pull requests to `main`
- Manual workflow dispatch

## Secrets Required

- `CODECOV_TOKEN` - For coverage upload
- `GH_PAT` - GitHub Personal Access Token

## Coverage Threshold

Minimum 80% coverage enforced via `--cov-fail-under=80`.
