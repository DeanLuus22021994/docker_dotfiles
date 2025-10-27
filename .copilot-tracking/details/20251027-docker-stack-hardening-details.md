<!-- markdownlint-disable-file -->

# Task Details: Docker Stack Hardening

## Research Reference

**Source Research**: Template: `../research/20251027-docker-stack-hardening-research.md`

## Phase 1: Security Hardening

### Task 1.1: Segment networks and proxy Docker socket

Implement tiered Docker networks (frontend, backend, data, observability) and introduce a `docker-socket-proxy` service so dependent containers access Docker API with least privilege.

- **Files**:
  - `docker-compose.yml` — define new networks, update `services.*.networks`, add proxy service entries
  - `.config/docker/compose.override.example.yml` — propagate network/proxy guidance for local overrides
  - `.github/workflows/` (relevant workflows) — ensure networking changes validated in CI
- **Success**:
  - Dedicated networks created and assigned without breaking existing connectivity
  - Docker socket mounts removed from application containers and replaced with proxy endpoint
  - CI passes `docker-compose config` validation with new topology
- **Research References**:
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 032-036) — socket exposure and single-network risk
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 059-066) — network segmentation and proxy recommendation
- **Dependencies**:
  - Baseline compose file available
  - Security review alignment (SECURITY.md guidance)

### Task 1.2: Enforce secrets management and container hardening flags

Adopt Docker secrets (or Vault integration) for sensitive credentials and add security options (`read_only`, `tmpfs`, `security_opt`, non-root users) across hardenable services.

- **Files**:
  - `docker-compose.yml` — add `secrets:` definitions, mount points, security flags per service
  - `.config/docker/README.md` — document new secrets workflow and security expectations
  - `SECURITY.md` — update controls to reflect hardened posture
- **Success**:
  - Secrets no longer exposed as plain environment variables
  - Containers run with non-root users where possible and `no-new-privileges` enforced
  - Documentation updated with rollout and developer guidance
- **Research References**:
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 032-035) — environment secret issues and missing security opts
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 069-074) — recommended hardening flags and secret handling
- **Dependencies**:
  - Task 1.1 networking updates completed (impacts service definitions)

## Phase 2: Reliability & Disaster Recovery

### Task 2.1: Standardize health-aware startup and restart strategy

Introduce health-gated startup (e.g., `condition: service_healthy`, wait scripts) and align restart policies across services for consistent recovery behavior.

- **Files**:
  - `docker-compose.yml` — add health condition dependencies, integrate wait scripts, normalize restart settings
  - `scripts/` — optionally add helper scripts (e.g., `wait-for-it.sh`) under version control
  - `Makefile` — ensure validation/test targets cover new scripts
- **Success**:
  - Dependent services wait for upstream health before starting
  - Restart policies documented and consistent across stateful/stateless services
  - End-to-end `make up` followed by health checks succeeds without manual intervention
- **Research References**:
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 040-044) — dependency coordination and restart inconsistencies
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 095-097) — resilience script recommendation
- **Dependencies**:
  - Phase 1 changes merged to avoid merge conflicts in compose file

### Task 2.2: Add automated backups and evaluate high-availability patterns

Create scheduled backup jobs for PostgreSQL, MariaDB, Redis, and outline HA roadmap (replication, sentinel, clustering) with optional compose profiles.

- **Files**:
  - `docker-compose.yml` — add backup service containers/profile definitions
  - `backups/` (new directory) — scripts/configs for dump scheduling
  - `docs/production/` — document backup procedures and HA roadmap
- **Success**:
  - Automated backup workflow runs successfully and stores artifacts with retention policy
  - Documentation includes restore instructions and HA evaluation
  - Optional HA profiles stubbed for future implementation (disabled by default)
- **Research References**:
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 041-043) — redundancy gaps and missing backups
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 075-082) — HA and backup recommendations
- **Dependencies**:
  - Task 2.1 restart alignment ensures backup services integrate cleanly

## Phase 3: Observability & Build Quality

### Task 3.1: Deploy logging/tracing stack and define SLO instrumentation

Add Loki + Promtail + Jaeger (or OpenTelemetry collector) services, wire alerts/dashboards, and codify SLO/SLA targets.

- **Files**:
  - `docker-compose.yml` — add observability services and network bindings
  - `.config/monitoring/` — provisioning for Grafana, Prometheus scrape configs, dashboard updates
  - `docs/production/monitoring.md` (new or existing) — document SLOs, alert policies
- **Success**:
  - Centralized logs and tracing accessible via Grafana/Jaeger UIs
  - Prometheus scrapes new exporters/receivers without errors
  - Documented SLOs linked to dashboards and alert rules
- **Research References**:
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 045-050) — observability gaps
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 087-090) — logging/tracing recommendations
- **Dependencies**:
  - Phase 1 networking segmentation available for observability tier

### Task 3.2: Standardize Dockerfiles and extend CI security scanning

Refactor remaining Dockerfiles to multi-stage, non-root builds with pinned versions and integrate Hadolint/Trivy plus compose linting into CI workflows.

- **Files**:
  - `dockerfile/**/*.Dockerfile` — refactor to multi-stage patterns, add `tini`, drop root usage where feasible
  - `.github/workflows/*.yml` — add linting/scanning jobs, enforce build validation
  - `Makefile` — new targets for Dockerfile linting and image scanning
- **Success**:
  - Docker images rebuild successfully with reduced footprint and non-root defaults
  - CI pipeline fails on Dockerfile lint or vulnerability findings
  - Documentation (README/SECURITY) reflects new quality gates
- **Research References**:
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 053-056, 091-094) — Dockerfile variance and standardization guidance
  - Template: `../research/20251027-docker-stack-hardening-research.md` (Lines 083-086) — CI enhancement recommendations
- **Dependencies**:
  - Observability services (Task 3.1) may introduce new Dockerfiles requiring consistent patterns
