---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["api", "security", "cors", "cross-origin"]
description: "CORS configuration for cross-origin requests"
---
# CORS Configuration

## Environment Variable

```bash
CORS_ORIGIN=https://your-domain.com,https://www.your-domain.com
```

Supports comma-separated multiple origins.

## Implementation

```javascript
const cors = require('cors');

const corsOptions = {
  origin: process.env.CORS_ORIGIN?.split(',') || '*',
  credentials: true,  // Allow cookies/auth headers
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
};

app.use(cors(corsOptions));
```

## Development vs Production

**Development:** `CORS_ORIGIN=*` (allow all origins)

**Production:** Specific domains only

```bash
CORS_ORIGIN=https://dashboard.example.com,https://api.example.com
```

## Preflight Requests

CORS automatically handles OPTIONS preflight requests:

```http
OPTIONS /api/containers HTTP/1.1
Origin: https://dashboard.example.com
Access-Control-Request-Method: GET
```

Response includes allowed origins/methods/headers.

## Security Considerations

- Never use `*` in production with credentials
- Whitelist specific subdomains, not wildcards
- Validate Origin header on sensitive operations
- Consider CSRF tokens for state-changing requests

## Troubleshooting

**CORS error in browser:** Check CORS_ORIGIN includes requesting domain.
