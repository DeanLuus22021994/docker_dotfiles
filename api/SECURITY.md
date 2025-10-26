# API Security Documentation

**Version:** 2.0  
**Last Updated:** 2025-10-26  
**Status:** Production-Ready ✅

---

## Overview

The Docker API Proxy implements multiple layers of security to protect against common web vulnerabilities and unauthorized access. This document details all security features, configuration options, and best practices.

---

## Security Features

### 1. JWT Authentication

**Status:** ✅ Implemented  
**Optional:** Yes (controlled by `AUTH_ENABLED` environment variable)

#### How It Works

- **Access Tokens:** Short-lived tokens (default: 8 hours) for API access
- **Refresh Tokens:** Long-lived tokens (default: 7 days) to obtain new access tokens
- **Token Storage:** Clients should store tokens in httpOnly cookies or secure localStorage

#### Configuration

```bash
# .env
AUTH_ENABLED=true
JWT_SECRET=your_64_character_random_hex_string
JWT_EXPIRES_IN=8h
JWT_REFRESH_EXPIRES_IN=7d
```

#### Default Credentials

**⚠️ SECURITY WARNING:** Change these immediately in production!

```
Username: admin
Password: admin
```

#### Endpoints

**Login:**
```bash
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}

Response:
{
  "success": true,
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": "8h",
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

**Refresh Token:**
```bash
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response:
{
  "success": true,
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": "8h"
}
```

**Logout:**
```bash
POST /auth/logout

Response:
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### Using Authentication

Include the access token in all API requests:

```bash
# Authorization Header (Recommended)
GET /api/containers
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Cookie (Alternative)
GET /api/containers
Cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### 2. Rate Limiting

**Status:** ✅ Implemented  
**Library:** express-rate-limit v7.1.5

#### Rate Limits

| Endpoint Category | Limit | Window | Purpose |
|------------------|-------|--------|---------|
| General API (`/api/*`) | 100 requests | 15 minutes | Prevent API abuse |
| Stats Endpoints (`/api/containers/:id/stats`) | 10 requests | 15 minutes | Protect resource-intensive ops |
| Authentication (`/auth/login`, `/auth/refresh`) | 5 requests | 15 minutes | Prevent brute force attacks |

#### Response Headers

Rate limit information is included in response headers:

```
RateLimit-Limit: 100
RateLimit-Remaining: 95
RateLimit-Reset: 1698765432
```

#### Rate Limit Exceeded Response

```json
HTTP/1.1 429 Too Many Requests

{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please try again later.",
  "retryAfter": 1698765432
}
```

---

### 3. Input Validation

**Status:** ✅ Implemented  
**Library:** express-validator v7.0.1

#### Validation Rules

**Container ID:**
- Format: 12-64 character hexadecimal string
- Pattern: `/^[a-f0-9]{12,64}$/`
- Applied to: `/api/containers/:id/stats`

**Login Credentials:**
- Username: 3-50 alphanumeric characters (plus `_` and `-`)
- Password: Minimum 4 characters (8+ recommended)

**Refresh Token:**
- Format: Valid JWT token
- Applied to: `/auth/refresh`

#### Validation Error Response

```json
HTTP/1.1 400 Bad Request

{
  "error": "Validation Error",
  "message": "Invalid request data",
  "details": [
    {
      "field": "id",
      "message": "Invalid container ID format. Must be 12-64 character hex string.",
      "value": "invalid_id"
    }
  ]
}
```

---

### 4. CORS (Cross-Origin Resource Sharing)

**Status:** ✅ Implemented  
**Library:** cors v2.8.5

#### Configuration

```bash
# .env
CORS_ORIGIN=http://localhost:3000,http://localhost:5173,https://your-domain.com
```

#### Default Allowed Origins

- `http://localhost:3000` (React development)
- `http://localhost:5173` (Vite development)

#### CORS Settings

```javascript
{
  origin: (origin, callback) => {
    // Whitelist check against CORS_ORIGIN env var
    if (allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,  // Allow cookies and auth headers
  optionsSuccessStatus: 200
}
```

#### CORS Error Response

```json
HTTP/1.1 403 Forbidden

{
  "error": "CORS Error",
  "message": "Not allowed by CORS"
}
```

---

### 5. Helmet Security Headers

**Status:** ✅ Implemented  
**Library:** helmet v7.1.0

#### Security Headers Applied

```
Content-Security-Policy: default-src 'self';base-uri 'self';font-src 'self' https: data:;...
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
X-Content-Type-Options: nosniff
X-DNS-Prefetch-Control: off
X-Download-Options: noopen
X-Frame-Options: SAMEORIGIN
X-Permitted-Cross-Domain-Policies: none
X-XSS-Protection: 0
Origin-Agent-Cluster: ?1
Referrer-Policy: no-referrer
Strict-Transport-Security: max-age=15552000; includeSubDomains
```

---

### 6. Docker Socket Security

**Status:** ✅ Implemented (Read-Only)  
**Audit:** Documented below

#### Current Configuration

```yaml
# docker-compose.yml
services:
  api:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro  # Read-only mount
```

#### Security Considerations

**✅ Good:**
- Socket mounted read-only (`:ro` flag)
- API only performs read operations (list, inspect, stats)
- No container creation, deletion, or modification
- No image operations

**⚠️ Cautions:**
- Read access still exposes sensitive information (environment variables, volumes)
- Socket access could reveal network topology
- Consider using Docker socket proxy for additional isolation

#### Recommended: Docker Socket Proxy

For production environments, consider using [tecnativa/docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy):

```yaml
services:
  docker-proxy:
    image: tecnativa/docker-socket-proxy
    container_name: docker-proxy
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - CONTAINERS=1
      - INFO=1
      - VERSION=1
      - NETWORKS=0
      - VOLUMES=0
      - IMAGES=0
    ports:
      - 2375:2375

  api:
    environment:
      - DOCKER_HOST=tcp://docker-proxy:2375
    depends_on:
      - docker-proxy
```

**Benefits:**
- Whitelist allowed API endpoints only
- No direct socket access required
- Better audit trail
- Defense in depth

---

## Production Deployment Checklist

### Required Changes

- [ ] **Change default credentials**
  ```bash
  # Generate strong password hash
  node -e "console.log(require('bcryptjs').hashSync('your_strong_password', 10))"
  
  # Update auth.js DEFAULT_USERS with new hash
  ```

- [ ] **Generate secure JWT secret**
  ```bash
  node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
  
  # Add to .env
  JWT_SECRET=<generated_secret>
  ```

- [ ] **Enable authentication**
  ```bash
  AUTH_ENABLED=true
  ```

- [ ] **Configure CORS origins**
  ```bash
  CORS_ORIGIN=https://your-production-domain.com,https://www.your-production-domain.com
  ```

- [ ] **Set NODE_ENV to production**
  ```bash
  NODE_ENV=production
  ```

- [ ] **Review Docker socket security**
  - Consider implementing Docker socket proxy
  - Document socket permissions in security policy
  - Audit what data is exposed via read-only access

### Optional Enhancements

- [ ] **HTTPS/TLS termination**
  - Use Traefik or nginx reverse proxy
  - Configure Let's Encrypt for automatic certificates
  - Force HTTPS redirects

- [ ] **Database-backed authentication**
  - Replace DEFAULT_USERS with database lookup
  - Support multiple users with different roles
  - Implement user management API

- [ ] **Logging and monitoring**
  - Log all authentication attempts
  - Monitor rate limit violations
  - Alert on suspicious activity

- [ ] **API key authentication (alternative)**
  - For service-to-service communication
  - Simpler than JWT for automated clients
  - Store hashed API keys in database

---

## Security Best Practices

### For Developers

1. **Never commit secrets**
   - Use `.env` for sensitive configuration
   - Add `.env` to `.gitignore` (already configured)
   - Use environment-specific `.env.development` and `.env.production`

2. **Keep dependencies updated**
   ```bash
   npm audit
   npm audit fix
   ```

3. **Review security advisories**
   - Monitor GitHub Security Advisories
   - Subscribe to security mailing lists for dependencies

4. **Principle of least privilege**
   - Grant minimum required Docker permissions
   - Use read-only mounts when possible
   - Limit API surface area

### For Operators

1. **Regular password rotation**
   - Change admin password every 90 days
   - Rotate JWT secret periodically
   - Use password manager for strong credentials

2. **Monitor logs**
   ```bash
   # View API logs
   docker-compose logs -f api
   
   # Monitor authentication attempts
   docker-compose logs api | grep "Login"
   ```

3. **Network isolation**
   - Use Docker networks to isolate services
   - Don't expose API directly to internet
   - Use reverse proxy with TLS termination

4. **Backup and recovery**
   - Backup `.env` file securely
   - Document recovery procedures
   - Test disaster recovery plan

---

## Vulnerability Reporting

If you discover a security vulnerability, please email: **security@your-domain.com**

**Do NOT create public GitHub issues for security vulnerabilities.**

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

### Response Timeline

- **Initial response:** Within 48 hours
- **Triage and assessment:** Within 1 week
- **Fix development:** Within 2 weeks (depending on severity)
- **Public disclosure:** After fix is deployed and users notified

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Express Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Node.js Security Checklist](https://github.com/goldbergyoni/nodebestpractices#6-security-best-practices)

---

**Last Reviewed:** 2025-10-26  
**Next Review:** 2025-11-26
