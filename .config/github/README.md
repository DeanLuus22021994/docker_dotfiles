# GitHub Configuration

This directory contains GitHub-specific configuration files for repository automation, CI/CD, and development workflows.

## Files

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

## Setup Instructions

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

### 4. Add GitHub Secrets

Required secrets for CI/CD:

```bash
# Add via GitHub CLI
gh secret set CODECOV_TOKEN --body "your-codecov-token"
gh secret set DOCKER_ACCESS_TOKEN --body "your-docker-hub-token"

# Or via GitHub UI
# Settings → Secrets and variables → Actions → New repository secret
```

**Required secrets:**
- `CODECOV_TOKEN` - For code coverage reporting
- `DOCKER_ACCESS_TOKEN` - For pushing Docker images
- `GH_PAT` - Personal access token (fine-grained)

## New Developer Onboarding

### Quick Setup
```bash
# 1. Clone repository
git clone https://github.com/DeanLuus22021994/docker_dotfiles.git
cd docker_dotfiles

# 2. Install GitHub CLI (if not installed)
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: See https://cli.github.com/

# 3. Authenticate with GitHub
gh auth login

# 4. Install dependencies
make install

# 5. Verify GitHub Actions
gh workflow list
gh run list --limit 5

# 6. Create feature branch
git checkout -b feature/your-feature

# 7. Make changes and push
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature

# 8. Create PR
gh pr create --title "feat: your feature" --body "Description of changes"

# 9. Watch auto-labeling happen!
gh pr view --web
```

## Workflow Examples

### Dependabot PR Workflow
```bash
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
