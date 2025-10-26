---
date_created: "2025-10-26T18:32:25.982176+00:00"
last_updated: "2025-10-26T18:32:25.982176+00:00"
tags: ["documentation", "security", "docker"]
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- security
- overview
  description: Project security policy and vulnerability reporting
  ---\n# Security Policy Overview

Security policies and vulnerability reporting procedures for Modern Data Platform.

## Supported Versions

Currently supported versions for security updates:

| Version | Supported              |
| ------- | ---------------------- |
| 4.x     | ✅ Yes                 |
| 3.x     | ⚠️ Critical fixes only |
| < 3.0   | ❌ No                  |

## Reporting Vulnerabilities

**DO NOT** create public GitHub issues for security vulnerabilities.

**Email:** security@your-domain.com (or repository maintainer)

**Include:**

- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 7 days
- **Fix & Disclosure:** Within 30 days (severity dependent)

## Security Features

- JWT authentication for API
- Docker socket access controls
- HTTPS with Let's Encrypt
- Secret scanning in CI/CD
- Dependabot security updates
- Rate limiting and CORS

See `policies/` subdocs for detailed security implementation guides.
