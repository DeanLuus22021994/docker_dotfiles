# Environment Variables Setup Guide

This guide explains how to configure environment variables for the Docker cluster stack.

## Quick Start

### 1. Copy the Example File

```bash
# Linux/macOS
cp .env.example .env

# Windows PowerShell
Copy-Item .env.example .env
```

### 2. Edit the .env File

Open `.env` and configure these **required** variables:

```bash
# REQUIRED: GitHub Configuration
GITHUB_OWNER=your-actual-github-username
GH_PAT=ghp_your_actual_personal_access_token

# OPTIONAL: Docker Hub (for increased pull rate limits)
DOCKER_ACCESS_TOKEN=your_docker_access_token

# OPTIONAL: Codecov (for CI/CD coverage reporting)
CODECOV_TOKEN=your_codecov_token
```

### 3. Load Environment Variables

#### Linux/macOS (Bash/Zsh)
```bash
export $(cat .env | grep -v '^#' | xargs)
```

#### Windows PowerShell
```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}
```

### 4. Validate Configuration

```bash
# Linux/macOS
python3 scripts/validate_env.py

# Windows PowerShell
.\scripts\validate_env.ps1
```

### 5. Start the Stack

```bash
# Standard stack
docker-compose up -d

# With devcontainer (pre-production environment)
docker-compose --profile dev up -d

# Or use the helper scripts
./scripts/start_devcontainer.sh      # Linux/macOS
.\scripts\start_devcontainer.ps1    # Windows PowerShell
```

---

## Required Environment Variables

### GITHUB_OWNER
- **Required**: Yes
- **Description**: Your GitHub username or organization name
- **Used by**: GitHub MCP Server, CI/CD pipeline
- **Example**: `GITHUB_OWNER=DeanLuus22021994`

### GH_PAT (GitHub Personal Access Token)
- **Required**: Yes
- **Description**: Personal access token for GitHub API authentication
- **Used by**: GitHub MCP Server, CI/CD pipeline, container registry
- **Scopes needed**: `repo`, `read:packages`, `workflow`
- **Example**: `GH_PAT=ghp_xxxxxxxxxxxxxxxxxxxx`
- **Generate at**: https://github.com/settings/tokens

---

## Optional Environment Variables

### DOCKER_ACCESS_TOKEN
- **Required**: No
- **Description**: Docker Hub access token for increased pull rate limits
- **Used by**: CI/CD pipeline, container builds
- **Default**: Anonymous pulls (limited to 100/6hr)
- **Example**: `DOCKER_ACCESS_TOKEN=dckr_pat_xxxxxxxxxxxxxxxxxxxx`
- **Generate at**: https://hub.docker.com/settings/security

### CODECOV_TOKEN
- **Required**: No (CI/CD only)
- **Description**: Codecov token for uploading test coverage reports
- **Used by**: CI/CD pipeline
- **Example**: `CODECOV_TOKEN=xxxxxxxxxxxxxxxxxxxx`
- **Get from**: https://codecov.io/

---

## Environment Variable Validation

The validation scripts check that all required variables are set before starting services.

### Python Script (`scripts/validate_env.py`)
```bash
python3 scripts/validate_env.py
```

**Output:**
```
=== Environment Variables Validation ===

Required Variables:
  ✓ GITHUB_OWNER: DeanLuus...
  ✓ GH_PAT: ghp_XXXX...

Optional Variables:
  ✓ DOCKER_ACCESS_TOKEN: dckr_pat...
  ⚠ CODECOV_TOKEN: NOT SET - Codecov token for coverage reporting

============================================================
✓ All required environment variables are set!
⚠ Optional variables missing:
  - CODECOV_TOKEN

Consider setting these for full functionality.

You can now start the stack:
  docker-compose up -d
  docker-compose --profile dev up -d  # Include devcontainer
============================================================
```

### PowerShell Script (`scripts/validate_env.ps1`)
```powershell
.\scripts\validate_env.ps1
```

---

## DevContainer Configuration

The devcontainer automatically receives environment variables from the host:

```json
{
  "customizations": {
    "vscode": {
      "settings": {
        "terminal.integrated.env.linux": {
          "GITHUB_OWNER": "${localEnv:GITHUB_OWNER}",
          "DOCKER_ACCESS_TOKEN": "${localEnv:DOCKER_ACCESS_TOKEN}",
          "GH_PAT": "${localEnv:GH_PAT}",
          "CODECOV_TOKEN": "${localEnv:CODECOV_TOKEN}"
        }
      }
    }
  }
}
```

Environment variables are also passed via docker-compose:

```yaml
devcontainer:
  environment:
    - GITHUB_OWNER=${GITHUB_OWNER:-DeanLuus22021994}
    - DOCKER_ACCESS_TOKEN=${DOCKER_ACCESS_TOKEN}
    - GH_PAT=${GH_PAT}
    - CODECOV_TOKEN=${CODECOV_TOKEN}
```

---

## CI/CD Pipeline Integration

The GitHub Actions workflow uses repository secrets:

```yaml
env:
  GITHUB_OWNER: ${{ secrets.GITHUB_OWNER || github.repository_owner }}
  DOCKER_ACCESS_TOKEN: ${{ secrets.DOCKER_ACCESS_TOKEN }}
  GH_PAT: ${{ secrets.GH_PAT || github.token }}
```

### Setting GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:
   - `GITHUB_OWNER` (optional, defaults to repo owner)
   - `GH_PAT` (required)
   - `DOCKER_ACCESS_TOKEN` (optional)
   - `CODECOV_TOKEN` (optional)

---

## Troubleshooting

### Error: "Missing required environment variables"

**Solution**: Ensure you've loaded the .env file in your current shell session.

```bash
# Check if variables are set
echo $GITHUB_OWNER
echo $GH_PAT

# If empty, load the .env file
export $(cat .env | grep -v '^#' | xargs)
```

### Error: "Bad credentials" from GitHub API

**Solution**: Verify your GH_PAT has the correct scopes:
- Go to https://github.com/settings/tokens
- Edit your token
- Ensure these scopes are checked: `repo`, `read:packages`, `workflow`
- If you changed scopes, regenerate the token

### Error: "Docker pull rate limit exceeded"

**Solution**: Set the DOCKER_ACCESS_TOKEN:
1. Create a Docker Hub account if you don't have one
2. Generate an access token at https://hub.docker.com/settings/security
3. Add it to your .env file
4. Reload environment variables

### DevContainer doesn't start with stack

**Solution**: Ensure you're using the `dev` profile:
```bash
docker-compose --profile dev up -d
# Or
./scripts/start_devcontainer.sh
```

### Environment variables not available in devcontainer

**Solution**: 
1. Check that variables are set on the host before starting the container
2. Rebuild the devcontainer: `Dev Containers: Rebuild Container`
3. Or restart the container: `docker-compose restart devcontainer`

---

## Security Best Practices

1. **Never commit .env file**: It's already in .gitignore
2. **Use strong tokens**: Generate new tokens, don't reuse old ones
3. **Rotate tokens regularly**: Update tokens every 90 days
4. **Limit token scopes**: Only grant the minimum required permissions
5. **Use repository secrets**: For CI/CD, always use GitHub Secrets, not environment variables

---

## Additional Resources

- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [DevContainer Environment Variables](https://code.visualstudio.com/docs/devcontainers/containers#_environment-variables)
