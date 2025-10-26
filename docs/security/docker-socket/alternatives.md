---
date_created: "2025-10-26T18:32:25.976176+00:00"
last_updated: "2025-10-26T18:32:25.976176+00:00"
tags: ["documentation", "security", "docker"]
description: "Documentation for alternatives"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- docker
- security
- reference
  description: Alternative approaches to Docker socket security
  ---\n# Docker Socket Alternatives

## 1. Docker API over TCP with TLS

**Benefits:** No socket mounting, mutual TLS authentication, network-level access control

**Setup:**

```bash
# Generate CA and certificates
openssl genrsa -aes256 -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
# ... (full cert generation in detailed docs)
```

**Daemon config:**

```json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"],
  "tls": true,
  "tlsverify": true,
  "tlscacert": "/root/.docker/ca.pem",
  "tlscert": "/root/.docker/server-cert.pem",
  "tlskey": "/root/.docker/server-key.pem"
}
```

## 2. Rootless Docker

**Benefits:** Docker daemon runs as non-root user, reduced attack surface, container escape has limited impact

**Limitations:** Some features unavailable (overlay networks, cgroup v1), performance overhead

```bash
curl -fsSL https://get.docker.com/rootless | sh
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
```

## 3. Read-Only Operations Only

**Use Case:** Monitoring dashboards, metrics collection

**Limitation:** Cannot stop/start containers or create/delete resources
