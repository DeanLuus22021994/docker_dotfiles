---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["api", "security", "overview"]
description: "API security overview and threat mitigation"
---
# API Security Overview

Express.js API with JWT authentication, rate limiting, and Docker socket access controls.

## Security Features

- **JWT Authentication** - Token-based auth (optional, \AUTH_ENABLED\)
- **Rate Limiting** - 100 req/15min general, 10 req/15min stats  
- **CORS** - Configurable allowed origins
- **Input Validation** - Container ID format validation
- **Error Sanitization** - No sensitive data in error messages
- **Docker Socket** - Read-only mount with proxy recommended

## Attack Surface

1. Docker socket access (high risk)
2. API endpoints (medium risk)
3. Authentication bypass (low risk with JWT)
4. DoS attacks (mitigated by rate limiting)

## Security Layers

1. Network layer (Traefik HTTPS, IP whitelisting)
2. Application layer (JWT, rate limiting, validation)
3. Docker layer (socket proxy, read-only mount)
4. Monitoring layer (Prometheus alerts, audit logs)

## Compliance

- OWASP Top 10 coverage
- CIS Docker Benchmark alignment
- Secure by default configuration

See subdocs for implementation details.
