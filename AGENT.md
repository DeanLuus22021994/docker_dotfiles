# AGENT.md - Development Guidelines

## Development Principles

**TDD** (Test-Driven Development): Write tests before implementation  
**SRP** (Single Responsibility Principle): One concern per module/file  
**SSoT** (Single Source of Truth): No duplication, one authoritative source  
**DRY** (Don't Repeat Yourself): Extract shared utilities, no code duplication  
**Config-Driven**: Behavior controlled by configuration, not code  
**Modular**: Loosely coupled, highly cohesive components

## Python Environment

### Required Version
- **Python 3.13+** for all scripts
- **UV package manager** for dependency management (faster than pip)
- **NOT** Microsoft Store Python (causes PATH issues on Windows)

### Setup (Windows)
```powershell
# 1. Install Python 3.13 from python.org
# 2. Disable Windows App Execution Aliases:
#    Settings → Apps → Advanced app settings → App execution aliases
#    Disable: "App Installer python.exe" and "python3.exe"

# 3. Verify installation
python --version  # Should show Python 3.13.x
where.exe python  # Should show actual Python path (not AppData\Local\Microsoft)

# 4. Install UV
pip install uv

# 5. Install dependencies
uv pip install -r requirements.txt
```

### Scripts Organization (SRP/DRY)
```
scripts/
├── README.md
├── orchestrator.ps1       # PowerShell orchestrator
├── orchestrator.sh        # Bash orchestrator
├── orchestrator.py        # Python orchestrator
├── powershell/            # PowerShell scripts by task
│   ├── config/            # Configuration management
│   ├── docker/            # Docker operations
│   ├── docs/              # Documentation tasks
│   ├── audit/             # Auditing scripts
│   └── cleanup/           # Cleanup operations
├── python/                # Python scripts by task
│   ├── validation/        # validate_env.py, validate_configs.py
│   ├── audit/             # Code audit scripts
│   └── utils/             # Shared utilities (colors.py, logging.py)
└── bash/                  # Bash scripts by task
    ├── docker/            # Docker operations
    └── docs/              # Documentation tasks
```

### Shared Utilities (DRY Principle)
- **`python/utils/colors.py`**: ANSI color codes for terminal output
- **`python/utils/file_utils.py`**: File operations helpers
- **`python/utils/logging_utils.py`**: Logging configuration

All Python scripts import from `scripts.python.utils` instead of duplicating code.

## Configuration Management

### Structure
```
.config/
├── nginx/          # Web server configs
├── database/       # Database server configs
├── services/       # Service-specific configs
├── docker/         # Docker daemon configs
├── github/         # GitHub Actions workflows
└── monitoring/     # Prometheus, Grafana configs
```

### Rules
1. **All configs in `.config/`** - No scattered configs
2. **Native formats** - Preserve .conf, .json, .sh (not YAML conversion)
3. **Read-only mounts** - Configs mounted with `:ro` flag
4. **Validated before use** - Run validation scripts before deployment

## Environment Variables

### Naming Convention
- **Prefix**: All service secrets use `DOCKER_` prefix
- **Examples**: `DOCKER_POSTGRES_PASSWORD`, `DOCKER_MARIADB_ROOT_PASSWORD`
- **Source**: GitHub Secrets (CI/CD) or host environment (local dev)

### Setup
```powershell
# Copy template
Copy-Item .env.example .env

# Edit with credentials
code .env

# Load variables
Get-Content .env | ForEach-Object {
  $var = $_.Split('=')
  [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process')
}

# Validate
python scripts/validate_env.py
```

### Required Variables
- `GITHUB_OWNER`, `GH_PAT`
- `DOCKER_POSTGRES_PASSWORD`
- `DOCKER_MARIADB_ROOT_PASSWORD`, `DOCKER_MARIADB_PASSWORD`
- `DOCKER_REDIS_PASSWORD`
- `DOCKER_MINIO_ROOT_USER`, `DOCKER_MINIO_ROOT_PASSWORD`
- `DOCKER_GRAFANA_ADMIN_PASSWORD`
- `DOCKER_JUPYTER_TOKEN`
- `DOCKER_PGADMIN_PASSWORD`

## Code Quality

### Pre-commit Hooks (Automated)
- Runs as `cluster-pre-commit` container service (dev profile)
- Auto-installs hooks on devcontainer startup
- Blocks commits on errors (no warnings)
- Checks: YAML/JSON syntax, secrets detection, docker-compose validation

### Manual Validation
```powershell
# Environment variables
python scripts/validate_env.py

# Docker Compose syntax
docker-compose config --quiet

# Nginx configs
docker run --rm -v "${PWD}/.config/nginx:/etc/nginx:ro" nginx:alpine nginx -t

# All configs
python scripts/validate_configs.py
```

## Docker Stack

### Services (25+)
- **Databases**: PostgreSQL, MariaDB, Redis
- **Storage**: MinIO (S3-compatible)
- **Monitoring**: Prometheus, Grafana, Alertmanager
- **Development**: Jupyter, pgAdmin, Redis Commander
- **Infrastructure**: nginx loadbalancer, BuildKit, LocalStack
- **DevContainer**: Python 3.13 + Node 22

### Profiles
- **Default**: Production services (databases, monitoring, web servers)
- **dev**: Includes devcontainer, pre-commit, docs server
- **docs**: GitHub Pages Jekyll server

### Commands
```powershell
# Production stack
docker-compose up -d

# Development stack (includes devcontainer and pre-commit)
docker-compose --profile dev up -d

# Documentation server
docker-compose --profile docs up -d

# View logs
docker-compose logs -f [service]

# Restart service
docker-compose restart [service]

# Stop all
docker-compose down
```

## File Organization

### Config Locations
| Type | Path | Purpose |
|------|------|---------|
| Nginx | `.config/nginx/` | loadbalancer.conf, main.conf, default.conf |
| Database | `.config/database/` | postgresql.conf, mariadb.conf |
| Services | `.config/services/` | pgadmin-servers.json, localstack-init.sh |
| Docker | `.config/docker/` | buildkitd.toml, daemon.json |
| Monitoring | `.config/monitoring/` | prometheus.yml, grafana/ |
| CI/CD | `.config/github/` | workflows/, dependabot.yml |

### Volume Mounts
```yaml
# Example: nginx loadbalancer
volumes:
  - ./.config/nginx/loadbalancer.conf:/etc/nginx/nginx.conf:ro

# Example: PostgreSQL
volumes:
  - ./.config/database/postgresql.conf:/etc/postgresql/postgresql.conf:ro
```

### Dockerfile COPY
```dockerfile
# Example: MariaDB
COPY --chown=mysql:mysql .config/database/mariadb.conf /etc/mysql/conf.d/custom.cnf

# Example: nginx
COPY --chown=nginx:nginx .config/nginx/main.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx .config/nginx/default.conf /etc/nginx/conf.d/default.conf
```

## VSCode Configuration

### Team Settings (Tracked)
- `.vscode/settings.json` - YAML schemas, file associations, Copilot code gen enabled
- Shared across team, committed to repo

### Personal Settings (Gitignored)
- `.vscode/settings.local.json` - AI model preferences, locale overrides
- Local only, added to `.gitignore`

### Usage
```json
// .vscode/settings.json (tracked)
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "github.copilot.chat.testGeneration.enabled": true
}

// .vscode/settings.local.json (gitignored)
{
  "github.copilot.advanced.debug.overrideEngine": "gpt-4o",
  "github.copilot.chat.localeOverride": "en"
}
```

## Security Guidelines

### Never Commit
- `.env` file (contains credentials)
- `.vscode/*.local.json` (personal preferences)
- Any file with actual passwords or tokens

### Always Use
- Environment variables with `DOCKER_` prefix
- `.env.example` as template (no real credentials)
- GitHub Secrets for CI/CD
- Strong passwords (16+ chars, mixed characters)

### Password Rotation
- Not automated (manual process)
- Update `.env` file locally
- Update GitHub Secrets in repository settings
- Restart affected services: `docker-compose restart [service]`

## AI-Optimized Workflow

### Human-in-the-Loop
1. **Agent proposes changes** - Clear file paths, specific edits
2. **Human reviews** - Validation scripts provide clear errors
3. **Manual approval** - Developer commits after verification
4. **Pre-commit validates** - Automated checks before commit
5. **CI/CD validates** - GitHub Actions on push

### Error Messages
- **Explicit**: Show exact file path, line number
- **Actionable**: Provide fix command or example
- **Unambiguous**: No vague errors, clear root cause

### Example Workflow
```powershell
# 1. Agent makes changes (via Copilot)
# ... file edits happen ...

# 2. Validate changes
python scripts/validate_env.py
docker-compose config --quiet

# 3. Test locally
docker-compose --profile dev up -d
docker-compose ps

# 4. Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: migrate configs to .config/ structure"

# 5. Push (CI/CD validates)
git push origin main
```

## Quick Reference

### File Paths (Relative to Root)
```
.config/nginx/loadbalancer.conf       # Load balancer nginx
.config/nginx/main.conf                # Main nginx config
.config/nginx/default.conf             # Default server block
.config/database/postgresql.conf       # PostgreSQL tuning
.config/database/mariadb.conf          # MariaDB config
.config/services/pgadmin-servers.json  # pgAdmin servers
.config/services/localstack-init.sh    # LocalStack init
.config/docker/buildkitd.toml          # BuildKit daemon
docker-compose.yml                     # Main compose file
.env.example                           # Environment template
.env                                   # Local env vars (gitignored)
scripts/python/validation/validate_env.py       # Environment validator
scripts/python/validation/validate_configs.py   # Config validator
scripts/python/utils/colors.py                  # Shared ANSI colors
.github/TODO.md                        # Implementation tasks
CLEANUP-REPORT.md                      # Code quality audit results
```

### Validation Commands
```powershell
python scripts/python/validation/validate_env.py                         # Environment
docker-compose config --quiet                                             # Compose syntax
docker run --rm -v "${PWD}/.config/nginx:/etc/nginx:ro" nginx:alpine nginx -t  # Nginx
python scripts/python/validation/validate_configs.py                      # All configs
```

### Common Tasks
```powershell
# Add new service
# 1. Add to docker-compose.yml
# 2. Add environment variables to .env.example
# 3. Update scripts/validate_env.py
# 4. Add config to .config/[category]/
# 5. Validate: docker-compose config --quiet

# Update config
# 1. Edit file in .config/[category]/
# 2. Validate syntax (category-specific command)
# 3. Restart service: docker-compose restart [service]

# Change password
# 1. Update .env file
# 2. Restart service: docker-compose restart [service]
# 3. Update GitHub Secrets (for CI/CD)
```

---

**Remember**: Config-driven, SSoT, explicit paths, validate before deploy, human approves all changes.
