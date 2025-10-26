---
date_created: "2025-10-26T18:32:25.981516+00:00"
last_updated: "2025-10-26T18:32:25.981516+00:00"
tags: ['documentation', 'security', 'docker']
description: "Documentation for docker"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- security
- docker
description: Docker container security policies and best practices
---\n# Docker Security

## Container Isolation

- **User namespaces** - Run containers as non-root
- **Read-only filesystem** - Prevent unauthorized writes
- **No privileged containers** - Never use `--privileged` flag
- **Resource limits** - Set CPU/memory limits

## Image Security

```yaml
services:
  api:
    image: api:latest
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

## Docker Socket Access

- Mount as read-only: `/var/run/docker.sock:/var/run/docker.sock:ro`
- Use socket proxy (`tecnativa/docker-socket-proxy`)
- Whitelist allowed API endpoints
- Monitor socket access in logs

## Network Security

- Internal networks for service communication
- Traefik reverse proxy for external access
- No direct container port exposure
- TLS for all external communication

## Secrets Management

- Use Docker secrets (Swarm) or environment variables
- Never hardcode secrets in Dockerfiles
- Rotate secrets regularly
- Use `.env` file excluded from git

## Image Scanning

```bash
# Scan with Trivy
trivy image api:latest

# Scan with Grype
grype api:latest
```

Run scans in CI/CD pipeline before deployment.
