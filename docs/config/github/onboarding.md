---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["github", "onboarding", "setup", "quickstart"]
description: "New developer onboarding guide for GitHub configuration"
---
# Developer Onboarding Guide

Quick setup guide for new developers (~10 minutes).

## Setup Steps

**1. Clone Repository**

```powershell
git clone https://github.com/DeanLuus22021994/docker_dotfiles.git
cd docker_dotfiles
```

**2. Authenticate GitHub CLI**

```powershell
gh auth login
gh repo view DeanLuus22021994/docker_dotfiles
```

**3. Apply Repository Settings**

```powershell
.\scripts\apply-settings.ps1 -ApplyAll
```

**4. Set Up Self-Hosted Runner**

```powershell
# See docs/config/github/runners.md for full setup
docker run -d --restart always --name github-runner ...
```

**5. Install Dependencies**

```powershell
# Python
uv sync

# Node.js
npm install --legacy-peer-deps
```

**6. Validate Environment**

```powershell
python scripts\validate_env.py
gh workflow run validate.yml
```

**7. Create Feature Branch**

```powershell
git checkout -b feature/your-feature-name
```

**8. Make Changes and Create PR**

```powershell
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
gh pr create --title "feat: your feature" --body "Description"
```

## Expected Outcome

- ✅ Auto-labeling based on changed files
- ✅ 4 validation checks on self-hosted runner
- ✅ CODEOWNERS requests review
- ✅ All checks must pass before merge

**Total Time:** ~10 minutes
