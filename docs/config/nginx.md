---
date_created: "2025-10-26T18:32:25.943322+00:00"
last_updated: "2025-10-26T18:32:25.943322+00:00"
tags: ['documentation', 'configuration', 'setup']
description: "Documentation for nginx"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- documentation
description: Documentation for nginx in config
---\n# Nginx Configuration

This directory contains nginx configurations organized by purpose.

## Files

### `loadbalancer.conf`
**Purpose:** Load balancer configuration for routing traffic across web server replicas  
**Used by:** `loadbalancer` service in docker-compose.yml  
**Mounts to:** `/etc/nginx/nginx.conf` in loadbalancer container  
**Key features:**
- Round-robin load balancing across cluster-web1, cluster-web2, cluster-web3
- Proxy headers for client IP forwarding
- Health check endpoint at `/health`

### `main.conf`
**Purpose:** Main nginx configuration with performance optimizations  
**Used by:** Reference configuration for nginx-based services  
**Key features:**
- Auto worker processes
- Gzip compression
- Security headers (XSS, CSRF protection)
- Rate limiting zones
- Performance tuning (sendfile, tcp_nopush)

### `default.conf`
**Purpose:** Default server block for static content serving  
**Used by:** nginx.Dockerfile for static web servers  
**Mounts to:** `/etc/nginx/conf.d/default.conf` in nginx containers  
**Key features:**
- Static content caching (1 year for assets)
- Rate-limited API endpoints (/api/, /python/)
- Health check endpoint at `/health`
- Security: Blocks dotfiles
- SPA fallback to index.html

## Usage

Configs are mounted as read-only volumes in docker-compose.yml:
```yaml
volumes:
  - ./.config/nginx/loadbalancer.conf:/etc/nginx/nginx.conf:ro
```

## Validation

Test nginx config syntax before deployment:
```bash
docker run --rm -v "$(pwd)/.config/nginx:/etc/nginx:ro" nginx:alpine nginx -t
```
