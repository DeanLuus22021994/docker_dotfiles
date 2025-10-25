# GitHub Configuration

This directory contains GitHub-specific configuration files for repository automation, CI/CD, security, and development workflows.

**💰 Cost: $0/month** - All features are FREE for public repositories

## Configuration Files

### Repository Settings (`repository.yml`)
Complete repository configuration as code. Apply with: `.\scripts\apply-settings.ps1 -ApplyRepository`

**Includes:**
- Repository metadata (name, description, homepage)
- Topics/tags for discoverability (20+ tags)
- Merge strategies and branch settings
- Security features (secret scanning, Dependabot, push protection)

**Cost: FREE**

### Branch Protection (`branch-protection.yml`)
Protection rules for `main` branch. Apply with: `.\scripts\apply-settings.ps1 -ApplyBranchProtection`

**Enforces:**
- Required status checks (4 validation jobs)
- Required PR approvals (1 minimum)
- Conversation resolution before merge
- No force pushes or deletions

**Cost: FREE**

### GitHub Secrets (`secrets.yml`)
Documentation for 11 required secrets. Set with: `.\scripts\setup_secrets.ps1 -SetGitHubSecrets`

**Required Secrets:**
- `GH_PAT` - GitHub Personal Access Token
- 10× `DOCKER_*` prefixed service credentials

**Cost: FREE** - Secrets storage is unlimited and free

### Actions Configuration (`actions.yml`)
GitHub Actions permissions and self-hosted runner setup.

**Features:**
- Unlimited free minutes (self-hosted)
- Workflow permissions (read-only by default)
- Fork PR workflows with approval
- 90-day artifact retention

**Cost: $0/month** - Self-hosted runners = unlimited free

### Security Settings (`code-security.yml`)
Code scanning, secret detection, and dependency review configuration.

**Enabled Features:**
- CodeQL analysis (Python, JavaScript, TypeScript)
- Secret scanning with push protection
- Dependabot alerts and security updates
- Dependency review for PRs
- Container scanning (Trivy)

**Cost: FREE** - GitHub Advanced Security included for public repos

### `dependabot.yml`
Automated dependency updates for Docker images, Python packages, Node.js modules, and GitHub Actions.

**Configuration:**
```yaml
Updates:
- Docker images: Weekly on Monday 9:00 AM
- Python (pip): Weekly on Monday 9:00 AM  
- Node.js (npm): Weekly on Monday 9:00 AM
- GitHub Actions: Monthly
```

**Features:**
- Max 5 open PRs per ecosystem (3 for Actions)
- Auto-labeling by dependency type
- Conventional commit messages (`chore(deps)`)
- Auto-assigns to @DeanLuus22021994

**How it works:**
1. Dependabot scans dependencies on schedule
2. Creates PRs for available updates
3. Applies semantic versioning strategy
4. Requires manual review and merge

### `labeler.yml`
Automatic PR labeling based on changed files.

**Labels applied:**
- `documentation` - Markdown files, docs/ folder
- `config` - Configuration files (.yml, .env)
- `docker` - Dockerfiles, compose files
- `monitoring` - Prometheus, Grafana configs
- `ci-cd` - Workflow files, Makefile
- `python` - Python files, requirements
- `nodejs` - Node.js files, package.json
- `scripts` - Shell scripts, PowerShell
- `tests` - Test files
- `security` - Secrets, passwords, .env

**Workflow:** `.github/workflows/labeler.yml`

### `workflows/labeler.yml`
GitHub Action workflow to run the PR labeler.

**Triggers:** Every pull request (target branch)

**Permissions:**
- Read: repository contents
- Write: pull requests (to add labels)

## Quick Start

### Apply All Repository Settings

```powershell
# 1. Review configuration files
Get-ChildItem .config\github\*.yml

# 2. Apply repository settings (dry-run first)
.\scripts\apply-settings.ps1 -DryRun

# 3. Apply all settings
.\scripts\apply-settings.ps1 -ApplyAll

# 4. Set GitHub secrets
.\scripts\setup_secrets.ps1 -SetGitHubSecrets

# 5. Verify settings applied
gh api repos/DeanLuus22021994/docker_dotfiles
gh secret list --repo DeanLuus22021994/docker_dotfiles
```

**Total Setup Time:** ~5 minutes  
**Total Cost:** $0/month

## Detailed Setup Instructions

### 1. Enable Dependabot

Dependabot is automatically enabled from `.config/github/dependabot.yml`:

```bash
# Verify configuration
cat .config/github/dependabot.yml

# View Dependabot dashboard
# GitHub → Repository → Insights → Dependency graph → Dependabot
```

**Manual trigger:**
1. Go to repository Settings
2. Click "Security & analysis"
3. Enable "Dependabot alerts" and "Dependabot security updates"

### 2. Enable PR Labeler

The labeler workflow is in `.config/github/workflows/labeler.yml`:

```bash
# Copy to correct location for GitHub Actions
mkdir -p .github/workflows
cp .config/github/workflows/labeler.yml .github/workflows/

# Commit and push
git add .github/workflows/labeler.yml
git commit -m "chore(ci): enable automatic PR labeling"
git push
```

**Verify:**
1. Create a test PR with changes
2. Check PR labels are auto-applied
3. View workflow runs in Actions tab

### 3. Configure Branch Protection

Recommended settings for `main` branch:

```bash
# Via GitHub CLI
gh api repos/DeanLuus22021994/docker_dotfiles/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["validate"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

**Or via GitHub UI:**
1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass
   - ✅ Require conversation resolution
   - ✅ Include administrators

### 4. Set GitHub Secrets

**Automated via script:**

```powershell
# Edit .env file with actual credentials (replace placeholders)
notepad .env

# Set all 11 required secrets automatically
.\scripts\setup_secrets.ps1 -SetGitHubSecrets

# Verify all secrets created
gh secret list --repo DeanLuus22021994/docker_dotfiles
```

**Required Secrets** (documented in `.config/github/secrets.yml`):
- `GH_PAT` - GitHub Personal Access Token
- `DOCKER_POSTGRES_PASSWORD` - PostgreSQL password
- `DOCKER_MARIADB_ROOT_PASSWORD` - MariaDB root password
- `DOCKER_MARIADB_PASSWORD` - MariaDB user password
- `DOCKER_REDIS_PASSWORD` - Redis password
- `DOCKER_MINIO_ROOT_USER` - MinIO root username
- `DOCKER_MINIO_ROOT_PASSWORD` - MinIO root password
- `DOCKER_GRAFANA_ADMIN_PASSWORD` - Grafana admin password
- `DOCKER_JUPYTER_TOKEN` - Jupyter notebook token
- `DOCKER_PGADMIN_PASSWORD` - pgAdmin password

**Optional Secrets:**
- `DOCKER_ACCESS_TOKEN` - Docker Hub token (if pushing images)
- `CODECOV_TOKEN` - Codecov token (if using code coverage)

**💰 Cost Impact:** FREE - Secrets storage unlimited, used only in self-hosted runners ($0/month)

### 5. Configure Self-Hosted Runner

Required for all workflows to maintain $0/month cost.

**Docker-Based Runner (Recommended):**

```powershell
docker run -d --restart always `
  --name github-runner `
  -e RUNNER_NAME="docker-stack-runner" `
  -e REPO_URL="https://github.com/DeanLuus22021994/docker_dotfiles" `
  -e ACCESS_TOKEN="${env:GH_PAT}" `
  -v /var/run/docker.sock:/var/run/docker.sock `
  myoung34/github-runner:latest

# Verify runner registered
gh api repos/DeanLuus22021994/docker_dotfiles/actions/runners
```

**Requirements:**
- 2 CPU cores minimum
- 4GB RAM minimum
- 20GB disk space
- Docker installed

**Cost: $0/month** - Unlimited free minutes

### 6. Enable Security Features

```powershell
# Open repository security settings
Start-Process "https://github.com/DeanLuus22021994/docker_dotfiles/settings/security_analysis"
```

Enable via GitHub UI:
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ Secret scanning
- ✅ Push protection
- ✅ Code scanning (CodeQL)

**Cost: FREE** - GitHub Advanced Security included for public repos

### 7. Apply Repository Configuration

```powershell
# Apply repository settings (metadata, features, merge strategies)
.\scripts\apply-settings.ps1 -ApplyRepository

# Apply branch protection (required checks, PR approvals)
.\scripts\apply-settings.ps1 -ApplyBranchProtection

# Or apply everything at once
.\scripts\apply-settings.ps1 -ApplyAll
```

**What Gets Applied:**
- Repository name, description, homepage, topics (20+)
- Merge strategies (squash, merge, rebase)
- Security analysis settings
- Branch protection with 4 required status checks
- PR review requirements (1 approval minimum)

### 8. Test Workflows

```powershell
# Trigger validation workflow manually
gh workflow run validate.yml

# Check workflow status
gh run list --workflow=validate.yml --limit 5

# View logs if needed
gh run view --log
```

**Expected Results:**
- 4 jobs: validate-environment, validate-configs, validate-docker-compose, validate-pre-commit
- All jobs run on self-hosted runner
- All jobs should pass after secrets configured

## Cost Breakdown ($0/month)

| Feature | GitHub-Hosted Cost | Self-Hosted Cost | This Repo |
|---------|-------------------|------------------|-----------|
| Actions Minutes | $0.008/min | FREE | **$0/month** (self-hosted) |
| Artifact Storage | $0.25/GB | FREE | **$0/month** (90-day retention) |
| Secrets Storage | FREE | FREE | **$0/month** (unlimited) |
| GitHub Advanced Security | $49/user/month private repos | FREE public repos | **$0/month** (public repo) |
| CodeQL Scanning | Included in GAS | Included in GAS | **$0/month** |
| Secret Scanning | Included in GAS | Included in GAS | **$0/month** |
| Dependabot | FREE | FREE | **$0/month** |
| Self-Hosted Runner | N/A | Hardware cost | **$0/month** (existing hardware) |

**Total: $0/month** 🎉

## Automation Tools

### `scripts/apply-settings.ps1`

Applies all repository configuration from `.config/github/*.yml` files via GitHub CLI.

**Usage:**

```powershell
# Show what would change (dry-run)
.\scripts\apply-settings.ps1 -DryRun

# Apply repository settings only
.\scripts\apply-settings.ps1 -ApplyRepository

# Apply branch protection only
.\scripts\apply-settings.ps1 -ApplyBranchProtection

# Apply all settings
.\scripts\apply-settings.ps1 -ApplyAll

# Show manual setup guidance for Actions
.\scripts\apply-settings.ps1 -ConfigureActions

# Show manual setup guidance for Security
.\scripts\apply-settings.ps1 -ConfigureSecurity
```

**Features:**
- ✅ Idempotent (safe to run multiple times)
- ✅ Color-coded status output
- ✅ Dry-run mode for safety
- ✅ Validates gh CLI authentication
- ✅ Minimal design (reads config files, no hardcoded values)

### `scripts/setup_secrets.ps1`

Sets all GitHub secrets from `.env` file.

**Usage:**

```powershell
# Set all 11 required secrets
.\scripts\setup_secrets.ps1 -SetGitHubSecrets

# Validate .env file format
.\scripts\setup_secrets.ps1 -ValidateOnly

# List current secrets (without values)
gh secret list --repo DeanLuus22021994/docker_dotfiles
```

## New Developer Onboarding

### Quick Setup (8 steps, ~10 minutes)

1. **Clone repository**
   ```powershell
   ```powershell
   git clone https://github.com/DeanLuus22021994/docker_dotfiles.git
   cd docker_dotfiles
   ```

2. **Verify GitHub CLI installed and authenticated**
   ```powershell
   # Check installation
   gh --version
   
   # Authenticate
   gh auth login
   
   # Verify access
   gh repo view DeanLuus22021994/docker_dotfiles
   ```

3. **Apply repository settings**
   ```powershell
   # Review config files
   Get-ChildItem .config\github\*.yml
   
   # Apply all settings
   .\scripts\apply-settings.ps1 -ApplyAll
   ```

4. **Set up self-hosted runner** (if not already configured)
   ```powershell
   # See section 5 above for Docker-based runner setup
   docker run -d --restart always --name github-runner ...
   ```

5. **Install dependencies**
   ```powershell
   # Python (if needed)
   uv sync
   
   # Node.js (if needed)
   npm install --legacy-peer-deps
   ```

6. **Validate environment**
   ```powershell
   # Run validation scripts
   python scripts\validate_env.py
   python scripts\validate_configs.py
   
   # Trigger workflow
   gh workflow run validate.yml
   ```

7. **Create feature branch**
   ```powershell
   git checkout -b feature/your-feature-name
   ```

8. **Make changes and create PR**
   ```powershell
   # Stage changes
   git add .
   
   # Commit (follows conventional commits)
   git commit -m "feat: your feature description"
   
   # Push
   git push origin feature/your-feature-name
   
   # Create PR
   gh pr create --title "feat: your feature" --body "Description of changes"
   
   # Watch auto-labeling and checks!
   gh pr view --web
   ```

**Expected Outcome:**
- ✅ Auto-labeling applies based on changed files
- ✅ 4 validation checks run on self-hosted runner
- ✅ CODEOWNERS automatically requests review from @DeanLuus22021994
- ✅ All checks must pass before merge

## Workflow Examples

### Dependabot PR Workflow
```powershell
# 1. Dependabot creates PR automatically
# 2. Review changes in PR
gh pr view 123

# 3. Check if tests pass
gh pr checks 123

# 4. Approve and merge
gh pr review 123 --approve
gh pr merge 123 --squash
```

### Manual PR Workflow
```bash
# 1. Create feature branch
git checkout -b feat/new-service

# 2. Make changes
# ... edit files ...

# 3. Commit with conventional commits
git add .
git commit -m "feat(docker): add new monitoring service"

# 4. Push and create PR
git push origin feat/new-service
gh pr create --fill

# 5. Labels auto-applied based on changed files
# 6. Request reviews
gh pr edit --add-reviewer DeanLuus22021994

# 7. Merge when approved
gh pr merge --squash
```

## Conventional Commits

Use semantic commit messages for automatic changelog generation:

```bash
# Features
git commit -m "feat(api): add health check endpoint"

# Bug fixes
git commit -m "fix(docker): correct volume mount path"

# Documentation
git commit -m "docs: update deployment guide"

# Refactoring
git commit -m "refactor(monitoring): restructure alert rules"

# Performance
git commit -m "perf(postgres): optimize query indexes"

# Tests
git commit -m "test(api): add integration tests"

# CI/CD
git commit -m "ci: add automated deployment"

# Dependencies
git commit -m "chore(deps): update prometheus to v2.45"

# Breaking changes
git commit -m "feat(api)!: change response format

BREAKING CHANGE: API now returns JSON instead of XML"
```

## Automation Features

### Auto-merge Dependabot (Optional)
```yaml
# Add to .github/workflows/auto-merge.yml
name: Auto-merge Dependabot PRs
on: pull_request

jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - name: Auto-merge minor/patch updates
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

### Release Automation (Future)
```yaml
# .github/workflows/release.yml
# Auto-generate releases from semantic commits
# Tag versions, create changelogs, publish artifacts
```

## Troubleshooting

### Dependabot not creating PRs
1. Check `.config/github/dependabot.yml` is valid
2. Verify Dependabot is enabled in repository settings
3. Check Dependabot logs: Repository → Insights → Dependency graph → Dependabot

### Labeler not working
1. Ensure workflow file is in `.github/workflows/` (not `.config/github/workflows/`)
2. Check workflow permissions include `pull-requests: write`
3. View workflow runs in Actions tab for errors

### Branch protection blocking merges
1. Check required status checks are passing
2. Verify you have admin/maintainer permissions
3. Temporarily disable "Include administrators" if needed

## References

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Actions Labeler](https://github.com/actions/labeler)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub CLI](https://cli.github.com/manual/)
