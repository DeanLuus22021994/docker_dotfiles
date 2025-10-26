---
date_created: "2025-10-26T18:32:25.940943+00:00"
last_updated: "2025-10-26T18:32:25.940943+00:00"
tags: ["documentation", "agent", "development"]
description: "Documentation for security"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- security
- authentication
- secrets
- best-practices
  description: Security guidelines and credential management procedures
  ---\n# Security Guidelines

## Never Commit

- `.env` file (contains credentials)
- `.vscode/*.local.json` (personal preferences)
- Any file with actual passwords or tokens

## Always Use

- Environment variables with `DOCKER_` prefix
- `.env.example` as template (no real credentials)
- GitHub Secrets for CI/CD
- Strong passwords (16+ chars, mixed characters)

## Password Rotation

- Not automated (manual process)
- Update `.env` file locally
- Update GitHub Secrets in repository settings
- Restart affected services: `docker-compose restart [service]`

## Best Practices

- Use password manager to generate and store credentials
- Rotate credentials periodically
- Never hardcode secrets in configs or code
- Use read-only mounts for sensitive configs
- Regular security updates via base images

See [AI workflow guide](agent-workflow.md) for development process.
