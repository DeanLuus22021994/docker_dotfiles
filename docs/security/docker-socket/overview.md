---
date_created: "2025-10-26T18:32:25.978535+00:00"
last_updated: "2025-10-26T18:32:25.978535+00:00"
tags: ["documentation", "security", "docker"]
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- docker
- security
- overview
  description: Docker socket security guide overview and risk assessment
  ---\n# Docker Socket Security Overview

The Docker socket (`/var/run/docker.sock`) provides complete control over the Docker daemon. Mounting in containers grants powerful capabilities but introduces significant security risks.

## Security Risks

**High-Risk Scenarios:**

1. **Container Escape** - Privileged containers can break containment → full host compromise
2. **Arbitrary Code Execution** - Execute commands on host via Docker API
3. **Data Exfiltration** - Read volumes, secrets, environment variables from all containers
4. **Denial of Service** - Stop/remove critical containers, consume host resources

## Current Implementation

**API Server:** `backend/server.js` mounts socket read-only

```yaml
services:
  api:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

**Security Controls:**

- Read-only mount (`:ro` flag)
- JWT authentication (optional, `AUTH_ENABLED`)
- Rate limiting (100 req/15min general, 10 req/15min stats)
- Input validation (container ID format)

**Limitation:** Read-only mount does NOT restrict Docker API write operations.

## Recommended Approach

Use **socket proxy** (`tecnativa/docker-socket-proxy`) to whitelist specific endpoints and deny dangerous operations.

See subdocs for details on threat models, best practices, alternatives, and monitoring.
