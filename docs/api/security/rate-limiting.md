---
date_created: "2025-10-26T18:32:26.002342+00:00"
last_updated: "2025-10-26T18:32:26.002342+00:00"
tags: ['documentation', 'api', 'reference']
description: "Documentation for rate limiting"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- api
- security
description: Rate limiting configuration and DoS protection
---\n# Rate Limiting

## Configuration

**General API** - 100 requests per 15 minutes

```javascript
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // Max requests per window
  message: 'Too many requests, please try again later'
});
```

**Container Stats** - 10 requests per 15 minutes (expensive operation)

```javascript
const statsLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  message: 'Too many stats requests, please try again later'
});
```

## Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1698765432
```

## Error Response

**429 Too Many Requests:**

```json
{
  "error": "Too many requests, please try again later",
  "retryAfter": 900  // seconds
}
```

## Bypass (Production)

Consider IP whitelisting for trusted services:

```javascript
const limiter = rateLimit({
  skip: (req) => trustedIPs.includes(req.ip),
  ...
});
```

## Monitoring

Track rate limit hits in Prometheus:

```
http_requests_rate_limited_total{endpoint="/api/containers/stats"}
```
