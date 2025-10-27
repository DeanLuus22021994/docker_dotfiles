---
date_created: '2025-10-27T02:37:39Z'
last_updated: '2025-10-27T02:37:39Z'
tags: [traefik, reverse-proxy, load-balancer, https, configuration]
description: 'Traefik edge router configuration for HTTPS and service discovery'
---

# Traefik Configuration

Traefik v3.2 edge router with HTTPS, Let's Encrypt, and Docker service discovery.

## 📁 Files

### `traefik.yml`
**Main Traefik configuration** - Static configuration.

**Entry Points**:
- `web` (port 80) - Redirects to HTTPS
- `websecure` (port 443) - HTTPS with TLS
- `traefik` (port 8080) - Dashboard

**Certificate Resolver**:
- Let's Encrypt with HTTP-01 challenge
- Auto-renewal
- Storage: `/letsencrypt/acme.json`

**Providers**:
- Docker (automatic service discovery)
- File (dynamic configuration from `dynamic/`)

**Features**:
- API dashboard
- Prometheus metrics
- Access logging (JSON format)
- Health check endpoint (ping)

---

### `dynamic/` Directory
**Dynamic configuration files**.

Contains:
- `middlewares.yml` - Security headers, rate limiting, compression
- Additional routing configurations

---

## 🚀 Quick Start

### Access Dashboard

```powershell
# Traefik dashboard (requires authentication in production)
Start-Process http://localhost:8080
```

### Test HTTPS Redirect

```powershell
# HTTP should redirect to HTTPS
curl -I http://your-domain.com

# Verify TLS certificate
curl -v https://your-domain.com
```

### Check Metrics

```powershell
# Prometheus metrics
curl http://localhost:8080/metrics
```

---

## 🎯 Production Configuration

### Security Enhancements

1. **Disable insecure dashboard**:
   ```yaml
   api:
     dashboard: false
     insecure: false
   ```

2. **Enable dashboard authentication**:
   Create `dynamic/dashboard-auth.yml`:
   ```yaml
   http:
     routers:
       dashboard:
         rule: \"Host(	raefik.your-domain.com)\"
         service: api@internal
         middlewares:
           - auth
     middlewares:
       auth:
         basicAuth:
           users:
             - \"admin:utf8apr1utf8...\"  # htpasswd generated
   ```

3. **DNS-01 challenge** (for wildcard certs):
   ```yaml
   certificatesResolvers:
     letsencrypt:
       acme:
         dnsChallenge:
           provider: cloudflare
           resolvers:
             - \"1.1.1.1:53\"
   ```

---

## 📚 References

- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Let's Encrypt Integration](https://doc.traefik.io/traefik/https/acme/)
- [Docker Provider](https://doc.traefik.io/traefik/providers/docker/)
