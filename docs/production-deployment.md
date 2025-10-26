# Production Deployment Guide

**Version:** 2.0  
**Last Updated:** 2025-10-26  
**Status:** Complete ✅

---

## Overview

This guide covers deploying the Modern Data Platform to production with HTTPS, authentication, and security hardening. Follow these steps carefully to ensure a secure deployment.

---

## Prerequisites

### Domain & DNS

- **Domain name:** Register a domain (e.g., `your-domain.com`)
- **DNS records:** Point A/AAAA records to your server's IP
- **Wildcard (optional):** For `*.your-domain.com` subdomains

```dns
A       your-domain.com         -> 192.168.1.100
A       *.your-domain.com       -> 192.168.1.100
AAAA    your-domain.com         -> 2001:db8::1
AAAA    *.your-domain.com       -> 2001:db8::1
```

### Server Requirements

- **OS:** Linux (Ubuntu 22.04+ recommended)
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 50GB minimum, 100GB+ recommended (for logs, databases)
- **Docker:** 24.0+ with Docker Compose v2
- **Ports:** 80 (HTTP), 443 (HTTPS) open in firewall

---

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/docker_dotfiles.git
cd docker_dotfiles
```

---

## Step 2: Configure Environment Variables

### Create Production .env

```bash
cp .env.example .env
nano .env  # Or use your preferred editor
```

### Required Changes

```bash
# =============================================================================
# PRODUCTION SECURITY
# =============================================================================

# Domain configuration
DOMAIN=your-domain.com
ACME_EMAIL=admin@your-domain.com

# Enable authentication
AUTH_ENABLED=true

# Generate secure JWT secret (64 characters)
# Run: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
JWT_SECRET=your_64_character_random_hex_string_here

# JWT expiration (8 hours for access, 7 days for refresh)
JWT_EXPIRES_IN=8h
JWT_REFRESH_EXPIRES_IN=7d

# CORS allowed origins (your production domains)
CORS_ORIGIN=https://your-domain.com,https://www.your-domain.com

# Node environment
NODE_ENV=production

# =============================================================================
# DATABASE PASSWORDS (CHANGE ALL!)
# =============================================================================

# PostgreSQL
DOCKER_POSTGRES_PASSWORD=$(openssl rand -base64 32)

# MariaDB
DOCKER_MARIADB_ROOT_PASSWORD=$(openssl rand -base64 32)
DOCKER_MARIADB_PASSWORD=$(openssl rand -base64 32)

# Redis
DOCKER_REDIS_PASSWORD=$(openssl rand -base64 32)

# MinIO
DOCKER_MINIO_ROOT_USER=admin
DOCKER_MINIO_ROOT_PASSWORD=$(openssl rand -base64 32)

# Grafana
DOCKER_GRAFANA_ADMIN_PASSWORD=$(openssl rand -base64 32)

# Jupyter
DOCKER_JUPYTER_TOKEN=$(openssl rand -base64 32)

# pgAdmin
DOCKER_PGADMIN_PASSWORD=$(openssl rand -base64 32)

# =============================================================================
# GITHUB INTEGRATION
# =============================================================================
GITHUB_OWNER=your-github-username
GH_PAT=ghp_your_github_personal_access_token
```

### Generate All Passwords Automatically

```bash
# Run this script to generate secure passwords
python scripts/powershell/config/setup-secrets.ps1
```

---

## Step 3: Configure Traefik

### Update Traefik Configuration

Edit `.config/traefik/traefik.yml`:

```yaml
certificatesResolvers:
  letsencrypt:
    acme:
      email: "admin@your-domain.com"  # ← Change this
      storage: "/letsencrypt/acme.json"
      caServer: "https://acme-v02.api.letsencrypt.org/directory"  # Production
      httpChallenge:
        entryPoint: web
```

### Update Domain in Dynamic Config

Edit `.config/traefik/traefik.yml`:

```yaml
entryPoints:
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: letsencrypt
        domains:
          - main: "your-domain.com"  # ← Change this
            sans:
              - "*.your-domain.com"   # ← Change this
```

---

## Step 4: Update Docker Compose

### Add Traefik Service

Edit `docker-compose.yml` and add Traefik service:

```yaml
services:
  traefik:
    build:
      context: .
      dockerfile: dockerfile/traefik.Dockerfile
    container_name: traefik
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    ports:
      - "80:80"     # HTTP (redirects to HTTPS)
      - "443:443"   # HTTPS
      - "8080:8080" # Dashboard (secure in production!)
    environment:
      - CF_API_EMAIL=${CF_API_EMAIL}  # If using Cloudflare DNS
      - CF_API_KEY=${CF_API_KEY}      # If using Cloudflare DNS
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./config/traefik/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./config/traefik/dynamic:/etc/traefik/dynamic:ro
      - traefik-letsencrypt:/letsencrypt
      - traefik-logs:/var/log/traefik
    networks:
      - traefik-public
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik-dashboard.rule=Host(`traefik.your-domain.com`)"
      - "traefik.http.routers.traefik-dashboard.entrypoints=websecure"
      - "traefik.http.routers.traefik-dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.routers.traefik-dashboard.service=api@internal"
      - "traefik.http.routers.traefik-dashboard.middlewares=dashboard-auth@file"
    healthcheck:
      test: ["CMD", "traefik", "healthcheck", "--ping"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  traefik-letsencrypt:
    driver: local
  traefik-logs:
    driver: local

networks:
  traefik-public:
    external: true
```

### Update Service Labels

For each service you want to expose via HTTPS, add Traefik labels:

**Web Dashboard:**

```yaml
services:
  web:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`your-domain.com`)"
      - "traefik.http.routers.dashboard.entrypoints=websecure"
      - "traefik.http.routers.dashboard.tls.certresolver=letsencrypt"
      - "traefik.http.services.dashboard.loadbalancer.server.port=80"
      - "traefik.http.routers.dashboard.middlewares=security-headers@file,compression@file"
    networks:
      - traefik-public
```

**API Server:**

```yaml
services:
  api:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.your-domain.com`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=letsencrypt"
      - "traefik.http.services.api.loadbalancer.server.port=3001"
      - "traefik.http.routers.api.middlewares=security-headers@file,rate-limit-api@file"
    networks:
      - traefik-public
```

**Grafana:**

```yaml
services:
  grafana:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.grafana.rule=Host(`grafana.your-domain.com`)"
      - "traefik.http.routers.grafana.entrypoints=websecure"
      - "traefik.http.routers.grafana.tls.certresolver=letsencrypt"
      - "traefik.http.services.grafana.loadbalancer.server.port=3000"
    networks:
      - traefik-public
```

---

## Step 5: Change Default Credentials

### API Authentication

Edit `api/auth.js`:

```javascript
// Generate password hash:
// node -e "console.log(require('bcryptjs').hashSync('your_secure_password', 10))"

const DEFAULT_USERS = {
  admin: {
    username: 'admin',
    passwordHash: '$2a$10$your_generated_hash_here',  // ← Change this
    role: 'admin',
  },
};
```

### Traefik Dashboard

Edit `.config/traefik/dynamic/middlewares.yml`:

```yaml
# Generate with: echo $(htpasswd -nb admin your_password) | sed -e s/\\$/\\$\\$/g
dashboard-auth:
  basicAuth:
    users:
      - "admin:$apr1$your_generated_hash_here"  # ← Change this
```

---

## Step 6: Create Docker Network

```bash
docker network create traefik-public
```

---

## Step 7: Build and Deploy

### Build Images

```bash
# Build all images
docker-compose build

# Or build specific services
docker-compose build traefik api web
```

### Start Services

```bash
# Start Traefik first
docker-compose up -d traefik

# Verify Traefik is running and certificates are obtained
docker-compose logs -f traefik

# Once Traefik is healthy, start other services
docker-compose up -d
```

### Verify Deployment

```bash
# Check all services are running
docker-compose ps

# Check Traefik logs
docker-compose logs traefik | grep -i "certificate"

# Check API logs
docker-compose logs api

# Test HTTPS
curl -I https://your-domain.com
```

---

## Step 8: Post-Deployment Verification

### SSL/TLS Check

```bash
# Check SSL certificate
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Verify SSL Labs rating (aim for A+)
# https://www.ssllabs.com/ssltest/analyze.html?d=your-domain.com
```

### Security Headers Check

```bash
# Check security headers
curl -I https://your-domain.com | grep -i "strict-transport"

# Expected headers:
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# Content-Security-Policy: ...
```

### Authentication Check

```bash
# Test login endpoint
curl -X POST https://api.your-domain.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'

# Should return:
# {"success":true,"accessToken":"eyJ...","refreshToken":"eyJ...","expiresIn":"8h"}
```

### Rate Limiting Check

```bash
# Test rate limits (should get 429 after limit)
for i in {1..110}; do
  curl -s -o /dev/null -w "%{http_code}\n" https://api.your-domain.com/health
done
```

---

## Step 9: Monitoring & Maintenance

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api

# Traefik access logs
docker-compose exec traefik tail -f /var/log/traefik/access.log

# Traefik error logs
docker-compose exec traefik tail -f /var/log/traefik/traefik.log
```

### Certificate Renewal

Let's Encrypt certificates auto-renew. Verify renewal:

```bash
# Check certificate expiry
docker-compose exec traefik cat /letsencrypt/acme.json | jq '.letsencrypt.Certificates[].certificate' | openssl x509 -text -noout | grep "Not After"

# Force renewal (if needed)
docker-compose restart traefik
```

### Backup Critical Data

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Backup .env (encrypted)
gpg -c .env -o "$BACKUP_DIR/env.gpg"

# Backup Let's Encrypt certificates
docker cp $(docker-compose ps -q traefik):/letsencrypt/acme.json "$BACKUP_DIR/"

# Backup databases
docker-compose exec -T postgres pg_dumpall -U postgres > "$BACKUP_DIR/postgres.sql"
docker-compose exec -T mariadb mysqldump -u root -p${DOCKER_MARIADB_ROOT_PASSWORD} --all-databases > "$BACKUP_DIR/mariadb.sql"
```

---

## Troubleshooting

### Traefik Not Getting Certificates

**Problem:** Let's Encrypt challenge fails

**Solutions:**

1. Check DNS records:
   ```bash
   dig your-domain.com
   nslookup your-domain.com
   ```

2. Check firewall allows port 80:
   ```bash
   sudo ufw status
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

3. Check Traefik logs:
   ```bash
   docker-compose logs traefik | grep -i "acme"
   docker-compose logs traefik | grep -i "error"
   ```

4. Use Let's Encrypt staging server first (change in `traefik.yml`):
   ```yaml
   caServer: "https://acme-staging-v02.api.letsencrypt.org/directory"
   ```

### Rate Limit Too Restrictive

**Problem:** Legitimate users getting rate limited

**Solutions:**

1. Increase limits in `api/middleware.js`:
   ```javascript
   const apiLimiter = rateLimit({
     windowMs: 15 * 60 * 1000,
     max: 200,  // Increase from 100
   });
   ```

2. Implement IP whitelisting:
   ```javascript
   const apiLimiter = rateLimit({
     skip: (req) => {
       const whitelist = ['192.168.1.100', '10.0.0.1'];
       return whitelist.includes(req.ip);
     },
   });
   ```

### Authentication Not Working

**Problem:** Always getting 401 Unauthorized

**Solutions:**

1. Check `AUTH_ENABLED` is set to `true`
2. Verify JWT_SECRET is configured
3. Check token format in Authorization header:
   ```bash
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. Check API logs:
   ```bash
   docker-compose logs api | grep -i "auth"
   ```

---

## Security Checklist

Before going live, verify:

- [ ] All default passwords changed
- [ ] JWT_SECRET is 64+ random characters
- [ ] AUTH_ENABLED=true in production
- [ ] CORS_ORIGIN restricted to your domains
- [ ] Traefik dashboard secured with strong password
- [ ] Let's Encrypt production server configured
- [ ] Firewall configured (only 80, 443, 22 open)
- [ ] SSH key-based authentication only
- [ ] Regular backups configured
- [ ] Monitoring/alerting setup
- [ ] Log retention policy defined
- [ ] SSL Labs rating A or A+
- [ ] Security headers verified
- [ ] Rate limits tested
- [ ] Documentation reviewed

---

## References

- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

---

**Last Updated:** 2025-10-26  
**Next Review:** 2025-11-26
