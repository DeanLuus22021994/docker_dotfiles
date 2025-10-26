# GitHub Copilot Instructions
**Last Updated:** 2025-10-26  
**Philosophy:** Production-ready data platform. Zero backward compatibility, bleeding-edge syntax, modular architecture.

---

## Architecture Overview

**Multi-service cluster:** 20+ Docker services across 5 architectural layers (Infrastructure, Data, Compute, Monitoring, Development). Services organized by layer in `docker-compose.yml` (1037 lines). All services require health checks and follow named volume pattern `docker_examples_<service>_<type>`.

**Key entry points:**
- `scripts/orchestrator.py` - CLI for validation/audit/MCP tasks (205 lines)
- `Makefile` - Production commands (build, up, down, validate, test-health)
- `docker-compose.yml` - 20 services with GPU support, health checks, resource limits
- `web-content/src/services/layers/` - Frontend service definitions mirroring cluster layers

**Critical workflows:**
1. **Validation:** `make validate-env` → `make validate-configs` → `make validate` (Docker syntax)
2. **Build:** `make build` (BuildKit multi-stage) → `make up` (production) or `make dev` (with devcontainer)
3. **Testing:** `pytest` (143 tests, 97% coverage), `make test-health` (service health checks)

---

## Coding Standards

**Python 3.14 (strict):**
- PEP 585 built-ins: `list[str]`, `dict[str, Any]` (never `List`, `Dict`)
- Type aliases: `TaskName: TypeAlias = str` for domain semantics
- Dataclasses: `@dataclass(frozen=True, slots=True)` for 40% memory reduction
- Protocol types: Structural subtyping for interface definitions
- UV package manager only (never pip)
- Zero type suppressions - fix architecture instead

**Docker:**
- No `version:` key in docker-compose.yml (Compose v2)
- Named volumes: `docker_examples_<service>_<type>` pattern REQUIRED
- Health checks: All services MUST have `HEALTHCHECK` in Dockerfile + `healthcheck:` in compose
- Multi-stage builds: Builder → Validation → Production (see `dockerfile/*.Dockerfile`)
- Resource limits: All services have `deploy.resources.limits` (CPU/memory)

**TypeScript/React (web-content):**
- Service layer architecture: `src/services/layers/{infrastructure,data,compute,monitoring,development}.ts`
- Type imports: `import type { Service } from '../types/cluster'`
- Hooks naming: `useClusterHealth`, `useClusterMetrics` (30s, 15s polling)
- Component structure: Feature-based in `src/components/{docker,health,metrics,network,services,storage}`

**Formatting:**
- Black: 100 char lines (configured in `pyproject.toml`)
- Ruff: Strict linting, only E402 ignored (sys.path setup)
- Pre-commit: 15 hooks (Black, Ruff, mypy, yamllint, shellcheck, markdownlint, hadolint)

---

## Key Patterns

**Service layer pattern (web-content):**
```typescript
// Each cluster layer = separate module in src/services/layers/
export const DATA_SERVICES: Omit<Service, 'status' | 'metrics'>[] = [
  { id: 'postgres', name: 'PostgreSQL', category: 'database', 
    port: 5432, healthEndpoint: 'http://localhost:5432',
    description: 'PostgreSQL 13 relational database (cluster-postgres)',
    icon: '🐘' }
]
// Aggregated in clusterService.ts: SERVICES_CONFIG = [...INFRASTRUCTURE_SERVICES, ...DATA_SERVICES, ...]
```

**Orchestrator CLI pattern:**
```python
# scripts/orchestrator.py - Central CLI delegating to specialized modules
# Tasks: validate (env, configs), audit (code, deps), mcp (validate, analyze)
# Example: python orchestrator.py validate env --dry-run
def execute_task(task: TaskName, action: ActionName) -> NoReturn:
    script = SCRIPT_DIR / "python" / task / f"{action}.py"
    result = subprocess.run([sys.executable, str(script)], check=False)
    sys.exit(result.returncode)
```

**Validation pattern:**
```python
# dataclass-based validators with Protocol interfaces
@dataclass(frozen=True, slots=True)
class EnvValidator:
    required_vars: list[str]
    def validate(self) -> ValidationResult: ...
```

**Docker health checks:**
```dockerfile
# All Dockerfiles include health checks
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

---

## Common Operations

**Add new service to cluster:**
1. Determine layer (infrastructure/data/compute/monitoring/development)
2. Add to `docker-compose.yml` with health check + resource limits + named volumes
3. Create `dockerfile/<service>.Dockerfile` with multi-stage build + health check
4. Add to web dashboard: `web-content/src/services/layers/<layer>.ts`
5. Validate: `make validate` → `make validate-configs`

**Add Python validation:**
1. Create validator in `scripts/python/validation/<name>.py`
2. Use dataclass pattern with Protocol interface
3. Add CLI entry in `scripts/orchestrator.py`
4. Write tests in `tests/python/validation/test_<name>.py`
5. Run: `pytest tests/python/validation/ --cov`

**Debug service health:**
```bash
make test-health                    # Check all services
docker-compose logs <service>       # View service logs
docker inspect <container> | findstr Health  # Check health status
curl http://localhost:<port>/health  # Test health endpoint directly
```

---

## Project Structure

**See [AGENT.md](../AGENT.md) for complete paths**

**Config:** `.config/{mkdocs,docker,python,git,markdownlint,monitoring}` - SSoT for all configs  
**Scripts:** `scripts/{orchestrator.py,python/,powershell/,bash/}` - Automation (validation, audit, cleanup)  
**Application:** `api/` (Express.js Node 22), `web-content/` (React 18 + Vite 6 + TypeScript)  
**Dockerfiles:** `dockerfile/` - Multi-stage builds, health checks (20+ files)  
**Docs:** `docs/` (MkDocs site), `.github/` (TODO, commands, instructions)  
**Quality:** `pyproject.toml` (Python config), `.vscode/` (settings, snippets), `.pre-commit-config.yaml`

---

## Critical Rules

**Before any work:**
1. Check `.github/TODO.md` for current phase/tasks (v4.0: 30/30 tasks complete, ready for production)
2. Run validation: `make validate-env && make validate-configs && make validate`
3. Read relevant `.github/instructions/*.instructions.md` for file-type-specific rules

**Never:**
- ❌ Use `version:` in docker-compose.yml (Compose v2 deprecates it)
- ❌ Hardcode secrets (use env vars, see `.env.example`)
- ❌ Use type suppressions in Python (fix architecture instead)
- ❌ Use `List`, `Dict`, `Tuple` in Python (PEP 585 built-ins only)
- ❌ Skip health checks in Docker services
- ❌ Use unnamed Docker volumes

**Always:**
- ✅ PEP 585 built-ins: `list[str]`, `dict[str, Any]`
- ✅ Named volumes: `docker_examples_<service>_<type>`
- ✅ Health checks with 30s interval, 10s timeout, 3 retries
- ✅ Resource limits in docker-compose.yml `deploy.resources`
- ✅ Validate before deploy: `make validate-env && make validate-configs && make validate`
- ✅ 143 tests passing with >97% coverage before PR merge

---

**Commands:** [.github/commands.yml](commands.yml) | **File paths:** [AGENT.md](../AGENT.md) | **TODO:** [.github/TODO.md](TODO.md)
