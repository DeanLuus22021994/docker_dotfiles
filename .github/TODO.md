# Docker Compose Standardization Todo List
Generated: October 23, 2025
Updated: October 23, 2025

## 🔴 CRITICAL PRIORITY (Do Immediately)

- [x] **Fix Python version references (3.13 → 3.14)** ✅ COMPLETED
  - [x] Verified `.devcontainer/devcontainer.json` has `python.defaultInterpreterPath` set to `/usr/bin/python3.14`
  - [x] Verified `.docker-compose/mcp/python_utils/pyproject.toml` has `target-version = "py314"`
  - [x] No py313 references found in codebase

- [x] **Implement Docker secrets management for sensitive credentials** ✅ COMPLETED
  - [x] Created directory: `secrets/` in project root
  - [x] Added `secrets/` to `.gitignore` with exceptions for `.secrets.example` and `README.md`
  - [x] Created example secrets file: `secrets/.secrets.example` with placeholder values
  - [x] Created `secrets/README.md` with comprehensive documentation
  - [x] Created `secrets/db_password.txt` for development use
  - [x] Verified all docker-compose.yml files have proper secrets configuration
  - [x] All PostgreSQL services use `POSTGRES_PASSWORD_FILE: /run/secrets/db_password`
  - [x] All docker-compose.yml files have secrets section with `db_password` file reference

- [x] **Standardize volume naming with consistent project prefix** ✅ COMPLETED
  - [x] Fixed `.docker-compose/basic-stack/docker-compose.yml` - updated `node_modules` and `python_venv` to use `docker_examples_` prefix
  - [x] Fixed `.docker-compose/cluster-example/docker-compose.yml` - updated `node_modules` to use `docker_examples_` prefix
  - [x] Fixed `.docker-compose/github-actions-runner/docker-compose.yml` - updated `runner_data` to `docker_examples_runner_data`
  - [x] All volume definitions now have consistent `docker_examples_` prefix
  - [x] All volume references in service definitions match the new names

## 🟡 HIGH PRIORITY (Do This Week)

- [ ] **Consolidate duplicate Dockerfiles to single source of truth**
  - [ ] Delete file: `.docker-compose/basic-stack/dockerfiles/python.Dockerfile`
  - [ ] Delete file: `.docker-compose/cluster-example/dockerfiles/python.Dockerfile`
  - [ ] In `.docker-compose/basic-stack/docker-compose.yml`, update Python service build path to reference consolidated Dockerfile: `dockerfile: .docker-compose/mcp/python_utils/dockerfiles/python.Dockerfile`
  - [ ] In `.docker-compose/cluster-example/docker-compose.yml`, update Python service build path to same consolidated location
  - [ ] Test build with: `docker-compose -f .docker-compose/basic-stack/docker-compose.yml build`

- [ ] **Standardize health check configurations across all services**
  - [ ] Search all docker-compose.yml files for `healthcheck:` sections
  - [ ] Update each healthcheck block to use these exact values:
    ```yaml
    healthcheck:
      test: ["CMD-SHELL", "<appropriate-command>"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    ```
  - [ ] Keep existing test commands, only change timing values
  - [ ] Files to update: basic-stack, cluster-example, swarm-stack, mcp/python_utils, github-actions-runner

- [x] **Create environment-specific configuration files** ✅ COMPLETED
  - [x] Created `.env.development` with dev-specific values
  - [x] Created `.env.production` with production placeholder values
  - [x] Created `.env.docker` with docker-specific values
  - [x] `.dockerignore` already has proper .env exclusions
  - [x] Documentation provided in deployment.md

- [ ] **Standardize Docker build context paths to workspace root**
  - [ ] In each docker-compose.yml file, locate all `build:` sections
  - [ ] Change all `context: ../..` or `context: ../../..` to `context: .` (workspace root)
  - [ ] Update corresponding `dockerfile:` paths to be relative to workspace root
  - [ ] Example: Change `dockerfile: dockerfiles/node.Dockerfile` to `dockerfile: .docker-compose/basic-stack/dockerfiles/node.Dockerfile`
  - [ ] After changes, test each stack: `docker-compose -f <path> build --no-cache`

- [ ] **Update file path references throughout codebase**
  - [ ] Open `.docker-compose/validate_stacks.py` and replace all `docker-compose-examples` strings with `.docker-compose`
  - [ ] Open root `README.md` and update all file path examples from `docker-compose-examples/` to `.docker-compose/`
  - [ ] Search all `.md` files for `docker-compose-examples` and replace with `.docker-compose`
  - [ ] Check if `.vscode/settings.json` contains any hardcoded paths and update them
  - [ ] Update each healthcheck block to use these exact values:
    ```yaml
    healthcheck:
      test: ["CMD-SHELL", "<appropriate-command>"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    ```
  - [ ] Keep existing test commands, only change timing values
  - [ ] Files to update: basic-stack, cluster-example, swarm-stack, mcp/python_utils, github-actions-runner

- [ ] **Create environment-specific configuration files**
  - [ ] Copy `.env.example` to `.env.development` and populate with dev-specific values
  - [ ] Copy `.env.example` to `.env.production` and populate with production-specific values
  - [ ] Copy `.env.example` to `.env.docker` and populate with docker-specific values
  - [ ] Open `.dockerignore` and add these lines:
    ```
    .env*
    !.env.example
    ```
  - [ ] Document which file to use for each environment in README.md

- [ ] **Standardize Docker build context paths to workspace root**
  - [ ] In each docker-compose.yml file, locate all `build:` sections
  - [ ] Change all `context: ../..` or `context: ../../..` to `context: .` (workspace root)
  - [ ] Update corresponding `dockerfile:` paths to be relative to workspace root
  - [ ] Example: Change `dockerfile: dockerfiles/node.Dockerfile` to `dockerfile: .docker-compose/basic-stack/dockerfiles/node.Dockerfile`
  - [ ] After changes, test each stack: `docker-compose -f <path> build --no-cache`

- [ ] **Update file path references throughout codebase**
  - [ ] Open `.docker-compose/validate_stacks.py` and replace all `docker-compose-examples` strings with `.docker-compose`
  - [ ] Open root `README.md` and update all file path examples from `docker-compose-examples/` to `.docker-compose/`
  - [ ] Search all `.md` files for `docker-compose-examples` and replace with `.docker-compose`
  - [ ] Check if `.vscode/settings.json` contains any hardcoded paths and update them

## 🟢 MEDIUM PRIORITY (Do This Month)

- [x] **Create Makefile for common development tasks** ✅ COMPLETED
  - [x] Created `Makefile` in project root
  - [x] Added target `validate:` that runs `python .docker-compose/validate_stacks.py`
  - [x] Added target `build:` that runs `python .docker-compose/validate_stacks.py --build`
  - [x] Added target `test:` that runs validation and build steps
  - [x] Added target `clean:` that runs `docker system prune -f` and removes dangling images
  - [x] Added target `format:` for Python code formatting
  - [x] Added target `lint:` for code linting
  - [x] Added target `security:` for security scans
  - [x] Added `.PHONY` declarations for all targets
  - [x] Included help target with documentation

- [ ] **Enhance validation script with production-ready features**
  - [ ] In `validate_stacks.py`, replace all `print()` calls with Python `logging` module
  - [ ] Add command-line flag `--format json` to output results in JSON format
  - [ ] Implement `ThreadPoolExecutor` to validate multiple stacks in parallel
  - [ ] Add `--coverage` flag to generate coverage report of validated stacks
  - [ ] Add exit codes: 0 for success, 1 for validation errors, 2 for runtime errors

- [x] **Set up pre-commit hooks for code quality** ✅ COMPLETED
  - [x] Created `.pre-commit-config.yaml` in project root
  - [x] Added hook: `docker-compose config --quiet` to validate syntax
  - [x] Added hook: detect credentials in docker-compose files
  - [x] Added hook: `hadolint` for Dockerfile linting
  - [x] Added hook to run `validate_stacks.py` before commits
  - [x] Added black, isort, ruff for Python formatting
  - [x] Added general file checks (trailing whitespace, YAML validation, etc.)
  - [x] Documentation note: Run `pip install pre-commit && pre-commit install` to activate

- [x] **Create GitHub Actions CI/CD workflows** ✅ COMPLETED
  - [x] Created `.github/workflows/validate-stacks.yml` that runs on pull requests
  - [x] Added job to validate docker-compose files
  - [x] Added job to check for hardcoded secrets
  - [x] Created `.github/workflows/build-test.yml` for full integration tests
  - [x] Added Docker caching for faster builds
  - [x] Added Python test execution
  - [x] Created `.github/workflows/security-scan.yml` with Trivy to scan images
  - [x] Added dependency review for pull requests
  - [x] Added scheduled security scans (weekly)

- [x] **Add observability stack for monitoring** ✅ COMPLETED
  - [x] Created directory: `.docker-compose/observability/`
  - [x] Created `.docker-compose/observability/docker-compose.yml` with Prometheus, Grafana, and Loki services
  - [x] Created `prometheus.yml` configuration file with scrape configs for all services
  - [x] Created Grafana datasource auto-provisioning configuration
  - [x] Created Grafana dashboard provider configuration in `.docker-compose/observability/dashboards/`
  - [x] Configured Loki with retention policies in `loki-config.yml`
  - [x] Added Promtail for log collection
  - [x] Added Node Exporter and cAdvisor for system and container metrics
  - [x] Documented comprehensive setup and usage in `.docker-compose/observability/README.md`
  - [x] All services include standardized health checks
  - [x] Created Grafana password secret file

## 🔵 LOW PRIORITY (Nice to Have)

- [x] **Create comprehensive documentation** ✅ COMPLETED
  - [x] Created `docs/` directory in project root
  - [x] Written `docs/architecture.md` with Mermaid diagram showing service relationships
  - [x] Written `docs/deployment.md` with step-by-step deployment instructions for each environment
  - [x] Written `docs/troubleshooting.md` with common errors and solutions
  - [x] Included architecture diagrams showing data flow

- [ ] **Build monitoring dashboards for system metrics**
  - [ ] Create Grafana dashboard for container CPU, memory, disk, and network usage
  - [ ] Create dashboard for application-level metrics (request rates, error rates, latency)
  - [ ] Create dashboard for PostgreSQL performance (query time, connections, cache hit rate)
  - [ ] Create dashboard for network traffic patterns between services
  - [ ] Export dashboards as JSON and commit to `.docker-compose/observability/dashboards/`

- [ ] **Implement centralized logging solution**
  - [ ] Choose between ELK Stack (Elasticsearch, Logstash, Kibana) or Grafana Loki
  - [ ] Create docker-compose.yml for logging stack in `.docker-compose/logging/`
  - [ ] Configure all services to send logs to centralized system
  - [ ] Implement trace ID generation and propagation across services
  - [ ] Set up log aggregation with retention policies
  - [ ] Create Kibana/Grafana queries for common log patterns

- [ ] **Add security scanning to CI/CD pipeline**
  - [x] Trivy scanning implemented in `.github/workflows/security-scan.yml`
  - [ ] Set up Snyk account and integrate for dependency vulnerability scanning
  - [ ] Add SAST (Static Application Security Testing) tools like SonarQube
  - [ ] Configure security scan failure thresholds (critical/high vulnerabilities)
  - [ ] Add security scan results to PR comments

## 📋 ONGOING MAINTENANCE

- [ ] **Monitor and update Python version** - Currently using Python 3.14, check monthly for patches
- [ ] **Update Node.js versions** - Check quarterly for LTS updates, currently on v20
- [ ] **Review security practices** - Quarterly review of OWASP Docker security best practices
- [ ] **Stay current with Docker** - Subscribe to Docker blog and review changes to compose specification
- [ ] **Update Python dependencies** - Monthly: run `poetry update` in `.docker-compose/mcp/python_utils/` and test