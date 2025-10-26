---
date_created: "2025-10-26T18:32:25.980244+00:00"
last_updated: "2025-10-26T18:32:25.980244+00:00"
tags: ["documentation", "security", "docker"]
description: "Documentation for authentication"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- security
- authentication
- api
  description: API authentication and authorization policies
  ---\n# Authentication & Authorization

## JWT Authentication

**Production:** `AUTH_ENABLED=true` (required)
**Development:** `AUTH_ENABLED=false` (optional)

**Token Configuration:**

```bash
JWT_SECRET=$(openssl rand -hex 32)  # 64 characters
JWT_EXPIRES_IN=8h
JWT_REFRESH_EXPIRES_IN=7d
```

## User Roles

- **Admin** - Full access to all endpoints
- **User** - Read-only access to monitoring data
- **Service** - Limited access for service-to-service communication

## Protected Endpoints

All `/api/*` endpoints require authentication when `AUTH_ENABLED=true`:

- `GET /api/containers` - List containers
- `GET /api/containers/:id` - Container details
- `GET /api/containers/:id/stats` - Container statistics
- `GET /api/health` - Health check (public)

## API Keys

For service-to-service communication, use API keys in headers:

```http
Authorization: Bearer <JWT_TOKEN>
X-API-Key: <SERVICE_API_KEY>
```

## Session Management

- Access tokens expire after 8 hours
- Refresh tokens expire after 7 days
- Implement token rotation on refresh
- Blacklist tokens on logout

## Password Requirements

- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols
- No common passwords
- Password hashing with bcrypt (10 rounds)
