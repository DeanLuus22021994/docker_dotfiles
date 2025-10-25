# Docker Configuration Migration - TODO

## Completed ✅

### Phase 1: Config Organization
- [x] Created `.config/` directory structure
  - [x] `.config/nginx/` - nginx configurations
  - [x] `.config/database/` - database configurations
  - [x] `.config/services/` - service-specific configurations
- [x] Migrated 7 config files from scattered locations to `.config/`
  - [x] `nginx.conf` (root) → `.config/nginx/loadbalancer.conf`
  - [x] `dockerfile/configs/nginx.conf` → `.config/nginx/main.conf`
  - [x] `dockerfile/configs/default.conf` → `.config/nginx/default.conf`
  - [x] `dockerfile/configs/postgresql.conf` → `.config/database/postgresql.conf`
  - [x] `dockerfile/configs/mariadb.conf` → `.config/database/mariadb.conf`
  - [x] `dockerfile/configs/pgadmin-servers.json` → `.config/services/pgadmin-servers.json`
  - [x] `dockerfile/configs/localstack-init.sh` → `.config/services/localstack-init.sh`
  - [x] `dockerfile/configs/buildkitd.toml` → `.config/docker/buildkitd.toml`
- [x] Created comprehensive README.md files for each config subdirectory
  - [x] `.config/nginx/README.md`
  - [x] `.config/database/README.md`
  - [x] `.config/services/README.md`

### Phase 2: Secrets to Environment Variables
- [x] Removed `secrets:` block from docker-compose.yml (lines 1-18)
- [x] Replaced all `*_PASSWORD_FILE` with `*_PASSWORD: ${DOCKER_*}` pattern
  - [x] PostgreSQL: `DOCKER_POSTGRES_PASSWORD`
  - [x] MariaDB: `DOCKER_MARIADB_ROOT_PASSWORD`, `DOCKER_MARIADB_PASSWORD`
  - [x] Redis: `DOCKER_REDIS_PASSWORD`
  - [x] MinIO: `DOCKER_MINIO_ROOT_USER`, `DOCKER_MINIO_ROOT_PASSWORD`
  - [x] Grafana: `DOCKER_GRAFANA_ADMIN_PASSWORD`
  - [x] Jupyter: `DOCKER_JUPYTER_TOKEN`
  - [x] pgAdmin: `DOCKER_PGADMIN_PASSWORD`
- [x] Updated `scripts/validate_env.py` to check all 11 required variables
- [x] Updated `.env.example` with DOCKER_ prefixed variables and security guidelines
- [x] Updated `.gitignore` to exclude `.env.local` and `.vscode/*.local.json`

### Phase 3: Docker Configuration Updates
- [x] Updated docker-compose.yml volume mounts
  - [x] Loadbalancer: Uses `.config/nginx/loadbalancer.conf`
- [x] Updated all Dockerfiles to use new config paths
  - [x] `dockerfile/mariadb.Dockerfile`
  - [x] `dockerfile/postgres.Dockerfile`
  - [x] `dockerfile/pgadmin.Dockerfile`
  - [x] `dockerfile/nginx.Dockerfile`
  - [x] `dockerfile/localstack.Dockerfile`
  - [x] `dockerfile/buildkit.Dockerfile`
- [x] Validated docker-compose.yml syntax (no errors)

## Pending 🔄

### Phase 4: Cleanup
- [ ] Delete `secrets/` directory and all contained files
- [ ] Delete `dockerfile/configs/` directory and all contained files
- [ ] Delete root-level `nginx.conf` (migrated to `.config/nginx/loadbalancer.conf`)
- [ ] Remove `.config/docker/buildkit.toml` (replaced by `buildkitd.toml`)

### Phase 5: Pre-commit Automation
- [ ] Create `dockerfile/pre-commit.Dockerfile`
  - [ ] Base: Python 3.13-slim
  - [ ] Install: pre-commit, yamllint, detect-secrets, Black, Ruff
  - [ ] Configure entry point for hook installation
- [ ] Create `.pre-commit-config.yaml` with strict error-enforcing hooks
  - [ ] YAML/JSON validation
  - [ ] Secrets detection (detect-secrets)
  - [ ] docker-compose syntax validation
  - [ ] Python formatting (Black, Ruff)
  - [ ] Trailing whitespace, end-of-file fixer
- [ ] Add `cluster-pre-commit` service to docker-compose.yml
  - [ ] Use `profiles: ["dev"]`
  - [ ] Mount workspace and `.git/` directory
  - [ ] Auto-install hooks on startup
  - [ ] Command: `pre-commit install && pre-commit run --all-files`
- [ ] Make `devcontainer` depend on `cluster-pre-commit`

### Phase 6: VSCode Settings Split
- [ ] Split `.vscode/settings.json` into team/personal configs
  - [ ] Keep in tracked `settings.json`:
    - [ ] YAML schemas
    - [ ] File associations
    - [ ] `github.copilot.chat.codeGeneration.useInstructionFiles: true`
    - [ ] `github.copilot.chat.testGeneration.enabled: true`
  - [ ] Move to gitignored `settings.local.json`:
    - [ ] `github.copilot.advanced.debug.overrideEngine`
    - [ ] `github.copilot.chat.localeOverride`
    - [ ] `github.copilot.chat.terminalChatLocation`
    - [ ] `github.copilot.chat.anthropic.thinking.maxTokens`
- [ ] Create `.vscode/settings.local.example.json` as template
- [ ] Update `.vscode/settings.json` with comment directing to local settings

### Phase 7: Config Validation Pipeline
- [ ] Create `scripts/validate_configs.py`
  - [ ] Validate YAML files (yamllint)
  - [ ] Validate JSON files (jsonlint)
  - [ ] Validate nginx configs (`nginx -t`)
  - [ ] Validate PostgreSQL configs (syntax check)
  - [ ] Validate MariaDB configs (syntax check)
  - [ ] Return exit code (0=success, 1=failure)
- [ ] Create `.github/workflows/validate.yml`
  - [ ] Trigger on: push, pull_request
  - [ ] Jobs:
    - [ ] Environment validation (scripts/validate_env.py)
    - [ ] Config validation (scripts/validate_configs.py)
    - [ ] docker-compose syntax (docker-compose config)
    - [ ] Pre-commit hooks (pre-commit run --all-files)
- [ ] Add `validate-configs` target to Makefile
  - [ ] Run all validation scripts
  - [ ] Report errors clearly
  - [ ] Exit with proper code

### Phase 8: Documentation
- [ ] Create root `AGENT.md` with development guidelines
  - [ ] Brief: TDD, SRP, SSoT, Config-driven principles
  - [ ] Explicit: File references, relative paths
  - [ ] Unambiguous: Clear examples and validation commands
  - [ ] AI-optimized: Human-in-the-loop workflow
- [ ] Update root `README.md` with new config structure
  - [ ] Environment variable setup instructions
  - [ ] Config validation commands
  - [ ] Pre-commit hook usage
- [ ] Update `.config/docker/README.md` (if exists) with buildkitd.toml info

## Environment Setup Instructions

### Required Before Stack Startup

1. **Copy and configure environment file:**
   ```powershell
   Copy-Item .env.example .env
   # Edit .env with your actual credentials
   ```

2. **Load environment variables:**
   ```powershell
   Get-Content .env | ForEach-Object {
     $var = $_.Split('=')
     [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process')
   }
   ```

3. **Validate environment:**
   ```powershell
   python scripts/validate_env.py
   ```

4. **Start the stack:**
   ```powershell
   docker-compose up -d                # Production services
   docker-compose --profile dev up -d  # Include devcontainer
   ```

## File Migration Summary

### Migrated Files
| Original Path | New Path | Status |
|--------------|----------|--------|
| `nginx.conf` | `.config/nginx/loadbalancer.conf` | ✅ Migrated |
| `dockerfile/configs/nginx.conf` | `.config/nginx/main.conf` | ✅ Migrated |
| `dockerfile/configs/default.conf` | `.config/nginx/default.conf` | ✅ Migrated |
| `dockerfile/configs/postgresql.conf` | `.config/database/postgresql.conf` | ✅ Migrated |
| `dockerfile/configs/mariadb.conf` | `.config/database/mariadb.conf` | ✅ Migrated |
| `dockerfile/configs/pgadmin-servers.json` | `.config/services/pgadmin-servers.json` | ✅ Migrated |
| `dockerfile/configs/localstack-init.sh` | `.config/services/localstack-init.sh` | ✅ Migrated |
| `dockerfile/configs/buildkitd.toml` | `.config/docker/buildkitd.toml` | ✅ Migrated |

### Files to Delete (After Validation)
- `secrets/` directory (entire directory)
- `dockerfile/configs/` directory (entire directory)
- `nginx.conf` (root level)
- `.config/docker/buildkit.toml` (replaced by buildkitd.toml)

## Validation Commands

```powershell
# Validate docker-compose syntax
docker-compose config --quiet

# Validate environment variables
python scripts/validate_env.py

# Validate nginx configs
docker run --rm -v "${PWD}/.config/nginx:/etc/nginx:ro" nginx:alpine nginx -t

# Test stack startup (dry-run)
docker-compose --profile dev config

# Full integration test (after all phases complete)
docker-compose --profile dev up -d
docker-compose ps
docker-compose logs --tail=50
```

## Notes

- **Security**: Never commit `.env` file - contains sensitive credentials
- **DOCKER_ Prefix**: All service passwords use `DOCKER_` prefix for consistency
- **Native Formats**: Configs preserved in native format (.conf, .json, .sh) not YAML
- **Pre-commit**: Will be automated as container service, not manual install
- **Human-in-Loop**: All validations provide clear error messages for manual fixes
