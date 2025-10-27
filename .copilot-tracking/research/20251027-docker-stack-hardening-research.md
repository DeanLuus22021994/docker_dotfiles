<!-- markdownlint-disable-file -->

# Docker Stack Hardening Research (2025-10-27)

## Repository Context

- **Stack Definition**: `docker-compose.yml` (Lines 1-1214) — 31 services covering ingress, app, data, monitoring, tooling
- **Service Images**: 23 custom Dockerfiles under `dockerfile/` (Lines vary, e.g., `dockerfile/nginx.Dockerfile` Lines 1-63)
- **Operational Tooling**: `Makefile` (Lines 1-216) orchestrates build, validation, testing
- **Security Guidance**: `SECURITY.md` (Lines 94-146) details current container security posture
- **Configuration Source of Truth**: `.config/` (e.g., `.config/docker/README.md` Lines 127-170)

## Current Strengths (Verified)

1. **Health Coverage** — 27 services implement Docker `HEALTHCHECK`

   - Example: `loadbalancer` command `curl -f -4 http://localhost:80` (`docker-compose.yml` Lines 44-76)
   - Monitoring stack (`cluster-grafana`, `cluster-prometheus`, exporters) all expose health endpoints (Lines 330-420)

2. **Resource Governance** — CPU/memory limits + reservations defined per service (e.g., `cluster-postgres` Lines 210-236)

3. **Observability Baseline** — Prometheus, Alertmanager, Grafana, multiple exporters configured with persistent volumes (`cluster_prometheus_data`, `cluster_grafana_data`)

4. **Development Ergonomics** — `devcontainer`, `cluster-pre-commit`, BuildKit service, MkDocs tooling accessible via Makefile targets (`Makefile` Lines 20-120)

5. **Documentation & Validation** — MkDocs strict mode hook (`.config/mkdocs/hooks/validate_frontmatter.py` Lines 1-557) and config validation scripts (`scripts/python/validation/validate_configs.py` Lines 1-420)

## Identified Gaps & Risks

### Security

- **Privileged Containers** — `cluster-buildkit`, `cluster-cadvisor`, `cluster-gpu-node` require `privileged: true` (`docker-compose.yml` Lines 720-840)
- **Docker Socket Exposure** — `cluster-docker-api` mounts `/var/run/docker.sock` read-only but runs as root (Lines 860-930) — risk of container breakout
- **Secrets in Env Vars** — Database and Redis credentials passed via environment variables (e.g., Lines 188-328) instead of Docker secrets
- **Uniform Networking** — Single `cluster-network` bridge for all tiers (Lines 1080-1100); lacks isolation between ingress, data, observability zones
- **Missing Security Opts** — No `security_opt` or `read_only` flags across services (entire file)

### Reliability

- **Dependency Coordination** — `depends_on` lacks health-aware gating; services may start before dependencies become healthy (e.g., `cluster-dashboard` Lines 150-190)
- **Stateful Service Redundancy** — PostgreSQL, MariaDB, Redis operate as single instances with no replicas or sentinel configuration
- **Backups** — No automated backup/restore jobs defined for persistent volumes (`cluster_postgres_data`, `cluster_mariadb_data`, `cluster_redis_data`)
- **Restart Policies** — Mix of `unless-stopped` (e.g., `cluster-postgres` Lines 200-240) and `"no"` (`cluster-pre-commit` Lines 10-40) leads to inconsistent recovery semantics

### Observability & Operations

- **Centralized Logging** — All services use the `json-file` driver with rotation (`max-size: 10m`, `max-file: 3`) but no aggregation layer (e.g., Loki/ELK)
- **Tracing** — No Jaeger/Zipkin/OpenTelemetry collector defined for distributed tracing across services
- **SLO Monitoring** — Grafana dashboards exist, yet repo lacks documented SLO/SLA definitions or alert thresholds

### Performance & Build

- **Dockerfile Variance** — Only select Dockerfiles use multi-stage builds (e.g., `dockerfile/web-dashboard.Dockerfile` Lines 1-40); others run single-stage as root users (`dockerfile/docker-api.Dockerfile` Lines 1-45)
- **Cache Utilization** — BuildKit cache mounts leveraged in `dockerfile/devcontainer.Dockerfile` but absent elsewhere
- **Image Footprint** — Several services pin `latest` tags (e.g., `jupyter/tensorflow-notebook:latest`, `grafana/grafana:latest`), impacting reproducibility and size control

## Opportunities & Recommendations

1. **Segment Networks**

   - Create dedicated `frontend`, `backend`, `data`, `observability` networks (`docker-compose.yml` modifications around Lines 1080-1150)

2. **Introduce Socket Proxy**

   - Replace direct Docker socket mounts with `tecnativa/docker-socket-proxy`; grant least privilege to dependent containers

3. **Secrets Management**

   - Adopt Docker secrets or Vault integration for credentials (`POSTGRES_PASSWORD`, `MYSQL_ROOT_PASSWORD`, `DOCKER_REDIS_PASSWORD`)

4. **Hardening Flags**

   - Add `read_only: true`, `tmpfs`, `security_opt: ["no-new-privileges:true"]`, and non-root `user` directives across services/Dockerfiles

5. **High Availability**

   - Evaluate PostgreSQL replication (primary/replica), Redis Sentinel, and MariaDB Galera cluster via new services or compose profiles

6. **Backups & DR**

   - Add scheduled backup containers (`pg_dump`, `mysqldump`, `redis-cli save`, MinIO mirror) with retention policies stored under `backups/`

7. **CI Enhancements**

   - Extend `.github/workflows/` to run Hadolint, Trivy scans, Docker Compose config linting, and CIS benchmark scripts

8. **Logging & Tracing Stack**

   - Add Loki + Promtail + Jaeger services; update Grafana dashboards in `.config/monitoring/`

9. **Dockerfile Standardization**

   - Convert remaining Dockerfiles to multi-stage builds, enforce non-root execution, pin base image versions, and adopt `tini` for init handling

10. **Resilience Scripts**
    - Integrate `wait-for-it.sh` or `dockerize` for health-aware startup; ensure `depends_on` uses `condition: service_healthy`

## Dependencies & External Considerations

- **GPU Support** — `devcontainer` and `cluster-gpu-node` rely on NVIDIA runtime (`docker-compose.yml` Lines 120-180, 780-820)
- **Documentation Stack** — Documentation services (`cluster-docs`, `cluster-mkdocs`) must remain compatible with network/security changes
- **Compliance Alignment** — `SECURITY.md` emphasizes secret scanning, Dependabot, CodeQL; future controls should align with SOC 2-style requirements

## Next Steps for Planning

1. Define phased enhancements (Security, Reliability, Observability, Performance)
2. Inventory impacted assets per phase (compose file, Dockerfiles, GitHub workflows, Makefile targets)
3. Ensure automation (Makefile/CI) validates new hardening controls end-to-end
