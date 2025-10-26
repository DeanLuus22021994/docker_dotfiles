---
date_created: "2025-10-26T18:32:26.001149+00:00"
last_updated: "2025-10-26T18:32:26.001149+00:00"
tags: ["documentation", "api", "reference"]
description: "Documentation for jwt authentication"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- api
- security
- jwt
- authentication
  description: JWT authentication implementation and configuration
  ---\n# JWT Authentication

## Configuration

**Environment variables:**

```bash
AUTH_ENABLED=true  # Enable/disable authentication
JWT_SECRET=$(openssl rand -hex 32)  # 64-character secret
JWT_EXPIRES_IN=8h  # Access token expiration
JWT_REFRESH_EXPIRES_IN=7d  # Refresh token expiration
```

## Endpoints

**Register** - `POST /api/auth/register`

<!-- pragma: allowlist secret -->

```json
{
  "username": "admin",
  "password": "<secure-password>",
  "email": "admin@example.com"
}
```

**Login** - `POST /api/auth/login`

<!-- pragma: allowlist secret -->

```json
{ "username": "admin", "password": "<password>" }
```

Returns: `{"accessToken": "...", "refreshToken": "..."}`

**Refresh** - `POST /api/auth/refresh`

<!-- pragma: allowlist secret -->

```json
{ "refreshToken": "<refresh-token>" }
```

## Protected Routes

Add `Authorization: Bearer <token>` header:

```bash
# pragma: allowlist secret
curl https://api.example.com/containers \
  -H "Authorization: Bearer <jwt-token>"
```

## Token Structure

- **Access token** - Short-lived (8h), for API requests
- **Refresh token** - Long-lived (7d), to get new access tokens
- **Payload** - User ID, username, issued/expires timestamps

## Security Best Practices

- Use strong JWT_SECRET (32+ bytes)
- Rotate secrets periodically
- Implement token blacklist for logout
- Use HTTPS only
- Store tokens securely (httpOnly cookies preferred)
