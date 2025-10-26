---
date_created: "2025-10-26T18:32:25.946717+00:00"
last_updated: "2025-10-26T18:32:25.946717+00:00"
tags: ["documentation", "production", "deployment"]
description: "Documentation for authentication"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- production
- authentication
- jwt
- security
  description: Authentication setup and user management for production
  ---\n# Authentication Setup

## Enable JWT Authentication

**Environment variables:**

```bash
AUTH_ENABLED=true
JWT_SECRET=$(openssl rand -hex 32)  # 64 characters
JWT_EXPIRES_IN=8h
JWT_REFRESH_EXPIRES_IN=7d
```

## Create Admin User

```bash
# Register first user (becomes admin)
curl -X POST https://your-domain.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_secure_password",
    "email": "admin@your-domain.com"
  }'
```

## Login Flow

**1. Login:**

```bash
curl -X POST https://your-domain.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Returns: { "accessToken": "...", "refreshToken": "..." }
```

**2. Use Access Token:**

```bash
curl https://your-domain.com/api/containers \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**3. Refresh Token (when expired):**

```bash
curl -X POST https://your-domain.com/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refreshToken": "YOUR_REFRESH_TOKEN"}'
```

## User Management

See `api/README.md` for full user management API.
