---
date_created: '2025-10-27T02:38:28Z'
last_updated: '2025-10-27T02:38:28Z'
tags: [github, ci-cd, automation, security]
description: 'GitHub repository configuration and automation'
---

# GitHub Configuration

GitHub repository settings, workflows, and automation configuration.

## 📁 Files Overview

### `repository.yml`
**Repository settings and features**.

**Configured**:
- Repository visibility (public/private)
- Features (Issues, Projects, Wiki, Discussions)
- Security settings
- Branch protection defaults
- Merge strategies

---

### `branch-protection.yml`
**Branch protection rules**.

**Main Branch Protection**:
- Require pull request reviews (1+ approvals)
- Require status checks (CI/CD must pass)
- Enforce linear history
- Require signed commits (recommended)
- Dismiss stale reviews on new commits

---

### `code-security.yml`
**Security scanning and policies**.

**Features**:
- Dependabot security updates
- Code scanning (CodeQL)
- Secret scanning
- Vulnerability alerts
- Security policy (SECURITY.md)

---

### `dependabot.yml`
**Automated dependency updates**.

**Package Ecosystems**:
- Docker (Dockerfiles in `dockerfile/`)
- npm (`package.json` files)
- pip (`requirements.txt`, `pyproject.toml`)
- GitHub Actions (workflow files)

**Schedule**: Weekly updates on Mondays

---

### `labeler.yml`
**Automatic PR labeling**.

**Label Categories**:
- `documentation` - Markdown, docs changes
- `docker` - Dockerfile, docker-compose changes
- `python` - Python code changes
- `javascript` - JS/TS code changes
- `ci-cd` - GitHub Actions workflows
- `config` - Configuration file changes

---

### `actions.yml`
**GitHub Actions workflow configuration**.

**Workflows** (see `workflows/` directory):
- CI validation
- Docker image builds
- Test execution
- Documentation deployment
- Security scanning

---

### `secrets.yml`
**Repository secrets inventory** (documentation only).

**Required Secrets**:
- `DOCKER_ACCESS_TOKEN` - Docker Hub authentication
- `GH_PAT` - GitHub Personal Access Token
- `CODECOV_TOKEN` - Code coverage reporting
- `GITHUB_OWNER` - Repository owner

**Note**: Actual secrets stored in GitHub Settings, not committed.

---

### `project-v4.0.yml`
**GitHub Projects configuration**.

**Project Board Setup**:
- Columns (To Do, In Progress, Done)
- Automation rules
- Issue templates
- Field definitions

---

### `workflows/` Directory
**GitHub Actions workflow definitions**.

Contains `.yml` files for:
- `validate.yml` - CI validation (linting, tests)
- `docker-build.yml` - Docker image builds
- `docs-deploy.yml` - Documentation deployment
- `security-scan.yml` - CodeQL analysis

---

## 🚀 Quick Start

### View Repository Settings

```powershell
# Using GitHub CLI
gh repo view --json name,visibility,hasIssuesEnabled,hasWikiEnabled

# View branch protection
gh api repos/OWNER/REPO/branches/main/protection
```

### Manage Secrets

```powershell
# List secrets
gh secret list

# Set a secret
gh secret set DOCKER_ACCESS_TOKEN

# Delete a secret
gh secret delete DOCKER_ACCESS_TOKEN
```

### Trigger Workflows

```powershell
# List workflows
gh workflow list

# Run a workflow
gh workflow run validate.yml

# View workflow runs
gh run list
```

---

## 🎯 Best Practices

### Repository Security

✅ **Enable all security features** - Dependabot, code scanning, secret scanning  
✅ **Require signed commits** - Verify commit authenticity  
✅ **Branch protection** - Prevent direct pushes to main  
✅ **Require reviews** - At least 1 approval for PRs  
✅ **Status checks** - All CI checks must pass  

### Workflow Automation

✅ **Fail fast** - Run quick checks first (linting, validation)  
✅ **Cache dependencies** - Speed up workflow execution  
✅ **Matrix testing** - Test multiple Python/Node versions  
✅ **Conditional workflows** - Run only when relevant files change  
✅ **Secrets management** - Use GitHub Secrets, never commit  

### Dependabot Configuration

✅ **Group related updates** - Reduce PR noise  
✅ **Auto-merge minor/patch** - Speed up maintenance  
✅ **Review major updates** - Breaking changes need attention  
✅ **Schedule appropriately** - Weekly for most projects  

---

## 🔧 Troubleshooting

### Workflow Failures

```powershell
# View failed workflow
gh run view <run-id>

# Download logs
gh run download <run-id>

# Re-run failed jobs
gh run rerun <run-id> --failed
```

### Dependabot Issues

```powershell
# View Dependabot alerts
gh api repos/OWNER/REPO/dependabot/alerts

# Check Dependabot logs
gh api repos/OWNER/REPO/dependabot/updates
```

### Secret Scanning Alerts

```powershell
# List secret scanning alerts
gh api repos/OWNER/REPO/secret-scanning/alerts

# Resolve an alert (after rotation)
gh api repos/OWNER/REPO/secret-scanning/alerts/<alert-id> -X PATCH -f state=resolved
```

---

## 📚 References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Code Scanning with CodeQL](https://docs.github.com/en/code-security/code-scanning)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

---

## 📝 Configuration Checklist

When setting up a new repository:

- [ ] Apply `repository.yml` settings via GitHub API or UI
- [ ] Configure branch protection from `branch-protection.yml`
- [ ] Enable security features from `code-security.yml`
- [ ] Set up Dependabot with `dependabot.yml`
- [ ] Configure auto-labeling from `labeler.yml`
- [ ] Add required secrets from `secrets.yml` inventory
- [ ] Set up GitHub Projects from `project-v4.0.yml`
- [ ] Deploy workflows from `workflows/` directory
- [ ] Test all workflows execute successfully
- [ ] Verify Dependabot creates PRs as expected
