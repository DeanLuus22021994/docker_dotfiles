# Docker Compose Standardization Todo List
Generated: October 23, 2025

## 🔴 CRITICAL PRIORITY (Do Immediately)

- [ ] Remove deprecated `version: "3.8"` from all docker-compose.yml files
  - [ ] `.docker-compose/basic-stack/docker-compose.yml`
  - [ ] `.docker-compose/basic-stack/docker-compose.dev.yml`
  - [ ] `.docker-compose/cluster-example/docker-compose.yml`
  - [ ] `.docker-compose/cluster-example/docker-compose.dev.yml`
  - [ ] `.docker-compose/swarm-stack/docker-compose.yml`
  - [ ] `.docker-compose/swarm-stack/docker-compose.dev.yml`
  - [ ] `.docker-compose/mcp/python_utils/docker-compose.yml`
  - [ ] `.docker-compose/github-actions-runner/docker-compose.yml`

- [ ] Fix Python version references (3.13 → 3.14)
  - [ ] `.devcontainer/devcontainer.json` line 27
  - [ ] `.docker-compose/mcp/python_utils/pyproject.toml` line 103
  - [ ] `.docker-compose/mcp/python_utils/pyproject.toml` line 208

- [ ] Implement secrets management for credentials
  - [ ] Create `secrets/` directory structure
  - [ ] Add `secrets/` to `.gitignore`
  - [ ] Convert hardcoded PostgreSQL passwords to secrets
  - [ ] Update all docker-compose files to use secrets

- [ ] Standardize volume naming with project prefix
  - [ ] Rename `python_cache` → `react_scuba_python_cache`
  - [ ] Rename `db_data` → `react_scuba_db_data`
  - [ ] Rename `node_modules` → `react_scuba_node_modules`

## 🟡 HIGH PRIORITY (Do This Week)

- [ ] Consolidate duplicate Dockerfiles
  - [ ] Remove `.docker-compose/basic-stack/dockerfiles/python.Dockerfile`
  - [ ] Remove `.docker-compose/cluster-example/dockerfiles/python.Dockerfile`
  - [ ] Ensure all stacks reference consolidated Dockerfiles

- [ ] Standardize health check configurations
  - [ ] Set consistent interval: 30s
  - [ ] Set consistent timeout: 10s
  - [ ] Set consistent retries: 3
  - [ ] Set consistent start_period: 40s

- [ ] Add environment-specific .env files
  - [ ] Create `.env.development`
  - [ ] Create `.env.production`
  - [ ] Create `.env.docker`
  - [ ] Update `.dockerignore` to exclude .env files

- [ ] Fix context path consistency
  - [ ] Standardize all build contexts to workspace root
  - [ ] Update dockerfile paths accordingly
  - [ ] Test all builds after changes

- [ ] Update all file references in codebase
  - [ ] Update `validate_stacks.py` paths
  - [ ] Update documentation references
  - [ ] Update README.md paths
  - [ ] Update `.vscode/settings.json` paths if needed

## 🟢 MEDIUM PRIORITY (Do This Month)

- [ ] Add Makefile for convenience
  - [ ] `make validate` - Validate all stacks
  - [ ] `make build` - Build all stacks
  - [ ] `make test` - Test all stacks
  - [ ] `make clean` - Cleanup all stacks

- [ ] Enhance validation script
  - [ ] Add logging instead of print statements
  - [ ] Add JSON output option for CI/CD
  - [ ] Add parallel stack validation
  - [ ] Add coverage reporting

- [ ] Implement pre-commit hooks
  - [ ] Validate docker-compose syntax
  - [ ] Check for hardcoded credentials
  - [ ] Lint Dockerfiles
  - [ ] Run validation script

- [ ] Create GitHub Actions workflows
  - [ ] `.github/workflows/validate-stacks.yml`
  - [ ] `.github/workflows/build-test.yml`
  - [ ] `.github/workflows/security-scan.yml`

- [ ] Add observability stack
  - [ ] Create `.docker-compose/observability/` directory
  - [ ] Add Prometheus configuration
  - [ ] Add Grafana dashboards
  - [ ] Add Loki for logging

## 🔵 LOW PRIORITY (Nice to Have)

- [ ] Enhance documentation
  - [ ] Create `docs/architecture.md`
  - [ ] Create `docs/deployment.md`
  - [ ] Create `docs/troubleshooting.md`
  - [ ] Add Mermaid architecture diagrams

- [ ] Add monitoring dashboards
  - [ ] Container resource usage
  - [ ] Application metrics
  - [ ] Database performance
  - [ ] Network traffic

- [ ] Implement centralized logging
  - [ ] ELK stack or Loki
  - [ ] Trace ID implementation
  - [ ] Log aggregation

- [ ] Add security scanning
  - [ ] Trivy for container scanning
  - [ ] Snyk for dependency scanning
  - [ ] SAST tools integration

## 📋 ONGOING MAINTENANCE

- [ ] Keep Python version up to date (currently 3.14)
- [ ] Update Node.js versions regularly
- [ ] Review and update security practices
- [ ] Monitor Docker best practices changes
- [ ] Update dependencies in pyproject.toml