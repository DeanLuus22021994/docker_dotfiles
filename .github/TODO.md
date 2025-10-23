# Docker Compose Standardization Todo List
Generated: October 23, 2025
Updated: October 23, 2025

## 🔴 CRITICAL PRIORITY (Do Immediately)

- [ ] **Fix Python version references (3.13 → 3.14)**
  - [ ] Open `.devcontainer/devcontainer.json` and change line 27 from `"python.defaultInterpreterPath": "/usr/bin/python3.13"` to `"/usr/bin/python3.14"`
  - [ ] Open `.docker-compose/mcp/python_utils/pyproject.toml` and change line 103 from `target-version = "py313"` to `"py314"`
  - [ ] In same file, change line 208 from `target-version = ['py313']` to `['py314']`

- [ ] **Implement Docker secrets management for sensitive credentials**
  - [ ] Create directory: `mkdir secrets` in project root
  - [ ] Add `secrets/` to `.gitignore` file (append new line: `secrets/`)
  - [ ] Create example secrets file: `secrets/.secrets.example` with placeholder values
  - [ ] In each docker-compose.yml file, locate PostgreSQL service sections
  - [ ] Replace `POSTGRES_PASSWORD: "password123"` with `POSTGRES_PASSWORD_FILE: /run/secrets/db_password`
  - [ ] Add secrets section at root level of docker-compose.yml files:
    ```yaml
    secrets:
      db_password:
        file: ./secrets/db_password.txt
    ```
  - [ ] Update PostgreSQL service to mount secrets:
    ```yaml
    services:
      postgres:
        secrets:
          - db_password
    ```

- [ ] **Standardize volume naming with consistent project prefix**
  - [ ] In `.docker-compose/basic-stack/docker-compose.yml`, find all volume definitions
  - [ ] Rename `python_cache:` to `docker_examples_python_cache:`
  - [ ] Rename `db_data:` to `docker_examples_db_data:`
  - [ ] Rename `node_modules:` to `docker_examples_node_modules:`
  - [ ] Update all volume references in service definitions to match new names
  - [ ] Repeat for all other docker-compose.yml files in the project

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

- [ ] **Create Makefile for common development tasks**
  - [ ] Create file `Makefile` in project root
  - [ ] Add target `validate:` that runs `python .docker-compose/validate_stacks.py`
  - [ ] Add target `build:` that runs `python .docker-compose/validate_stacks.py --build`
  - [ ] Add target `test:` that runs validation and build steps
  - [ ] Add target `clean:` that runs `docker system prune -f` and removes dangling images
  - [ ] Add `.PHONY` declarations for all targets
  - [ ] Document Makefile usage in README.md

- [ ] **Enhance validation script with production-ready features**
  - [ ] In `validate_stacks.py`, replace all `print()` calls with Python `logging` module
  - [ ] Add command-line flag `--format json` to output results in JSON format
  - [ ] Implement `ThreadPoolExecutor` to validate multiple stacks in parallel
  - [ ] Add `--coverage` flag to generate coverage report of validated stacks
  - [ ] Add exit codes: 0 for success, 1 for validation errors, 2 for runtime errors

- [ ] **Set up pre-commit hooks for code quality**
  - [ ] Install pre-commit: `pip install pre-commit`
  - [ ] Create `.pre-commit-config.yaml` in project root
  - [ ] Add hook: `docker-compose config --quiet` to validate syntax
  - [ ] Add hook: `grep -r "password\|secret\|key" docker-compose*.yml` to detect credentials
  - [ ] Add hook: `hadolint` for Dockerfile linting
  - [ ] Add hook to run `validate_stacks.py` before commits
  - [ ] Run `pre-commit install` to activate hooks
  - [ ] Document in README.md under "Development Setup"

- [ ] **Create GitHub Actions CI/CD workflows**
  - [ ] Create `.github/workflows/validate-stacks.yml` that runs on pull requests
  - [ ] Add job to run `validate_stacks.py --build` with caching
  - [ ] Create `.github/workflows/build-test.yml` for full integration tests
  - [ ] Create `.github/workflows/security-scan.yml` with Trivy to scan images on push
  - [ ] Add status badges to README.md showing workflow status

- [ ] **Add observability stack for monitoring**
  - [ ] Create directory: `.docker-compose/observability/`
  - [ ] Create `.docker-compose/observability/docker-compose.yml` with Prometheus, Grafana, and Loki services
  - [ ] Create `prometheus.yml` configuration file with scrape configs for all services
  - [ ] Create Grafana dashboard JSON files in `.docker-compose/observability/dashboards/`
  - [ ] Configure Loki with retention policies in `loki-config.yml`
  - [ ] Update main docker-compose files to expose metrics endpoints
  - [ ] Document how to access dashboards in `.docker-compose/observability/README.md`

## 🔵 LOW PRIORITY (Nice to Have)

- [ ] **Create comprehensive documentation**
  - [ ] Create `docs/` directory in project root
  - [ ] Write `docs/architecture.md` with Mermaid diagram showing service relationships
  - [ ] Write `docs/deployment.md` with step-by-step deployment instructions for each environment
  - [ ] Write `docs/troubleshooting.md` with common errors and solutions
  - [ ] Add Mermaid architecture diagrams to README.md showing data flow

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
  - [ ] Install Trivy: `docker run aquasec/trivy image <image-name>`
  - [ ] Add Trivy to GitHub Actions to scan all built images
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