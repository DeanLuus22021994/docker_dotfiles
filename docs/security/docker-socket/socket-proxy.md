---
date_created: "2025-10-26T18:32:25.979116+00:00"
last_updated: "2025-10-26T18:32:25.979116+00:00"
tags: ['documentation', 'security', 'docker']
description: "Documentation for socket proxy"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- docker
- security
- reference
description: Docker socket proxy implementation guide
---\n# Docker Socket Proxy Implementation

## Recommended: tecnativa/docker-socket-proxy

Whitelists specific API endpoints and denies dangerous operations by default.

## Configuration

```yaml
# docker-compose.yml
services:
  docker-socket-proxy:
    image: tecnativa/docker-socket-proxy:latest
    environment:
      CONTAINERS: 1  # Allow container listing
      IMAGES: 1      # Allow image listing
      INFO: 1        # Allow system info
      VOLUMES: 0     # Deny volume operations
      NETWORKS: 0    # Deny network operations
      BUILD: 0       # Deny image building
      COMMIT: 0      # Deny container commits
      EXEC: 0        # Deny exec operations
      POST: 0        # Deny all POST operations
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - docker-proxy

  api:
    environment:
      DOCKER_HOST: tcp://docker-socket-proxy:2375
    depends_on:
      - docker-socket-proxy
    networks:
      - docker-proxy

networks:
  docker-proxy:
    internal: true
```

## Security Benefits

- API cannot perform dangerous operations
- Socket access audited and restricted
- Clear security boundary
- Defense in depth

## Alternative: Docker API over TLS

Mutual TLS authentication without socket mounting. See `alternatives.md` for full setup.
