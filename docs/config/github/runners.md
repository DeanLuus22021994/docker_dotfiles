---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["github", "runners", "self-hosted", "actions"]
description: "Self-hosted GitHub Actions runners configuration"
---
# Self-Hosted Runners Configuration

Self-hosted runners for unlimited free GitHub Actions minutes.

## Docker-Based Runner Setup

**Recommended approach:**

```powershell
docker run -d --restart always `
  --name github-runner `
  -e RUNNER_NAME="docker-stack-runner" `
  -e REPO_URL="https://github.com/DeanLuus22021994/docker_dotfiles" `
  -e ACCESS_TOKEN="${env:GH_PAT}" `
  -v /var/run/docker.sock:/var/run/docker.sock `
  myoung34/github-runner:latest
```

## Requirements

- 2 CPU cores minimum
- 4GB RAM minimum
- 20GB disk space
- Docker installed
- GitHub Personal Access Token (GH_PAT)

## Verify Registration

```powershell
# Check runner status
gh api repos/DeanLuus22021994/docker_dotfiles/actions/runners

# View in GitHub UI
# Settings → Actions → Runners
```

## Benefits

- **Unlimited free minutes** (vs $0.008/min GitHub-hosted)
- Access to local Docker daemon
- Custom environment configuration
- No queue times
- Control over hardware resources

## Troubleshooting

**Runner not starting:**
- Check GH_PAT token has `repo` scope
- Verify REPO_URL format correct
- Check Docker socket permissions

**Workflows not using self-hosted:**
- Ensure workflows specify `runs-on: self-hosted`
- Verify runner is online in GitHub settings

**Cost:** $0/month (unlimited free minutes)
