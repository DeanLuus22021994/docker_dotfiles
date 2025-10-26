---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["docker", "security", "checklist", "compliance"]
description: "Docker socket security checklist for all environments"
---
# Security Checklist

## Development Environment

- [ ] Socket mounted read-only (`:ro`)
- [ ] Input validation implemented
- [ ] Error messages sanitized
- [ ] Rate limiting configured
- [ ] Authentication available (can be disabled)
- [ ] Security scanning in pre-commit hooks
- [ ] Dependencies updated regularly

## Staging Environment

- [ ] Socket proxy implemented
- [ ] Authentication enabled
- [ ] Rate limiting enforced
- [ ] HTTPS/TLS configured
- [ ] Network segmentation in place
- [ ] Audit logging enabled
- [ ] Security scans automated (Trivy, npm audit)
- [ ] Secrets stored in vault (not environment)

## Production Environment

- [ ] Socket proxy with whitelisted endpoints
- [ ] Authentication enforced (JWT with strong secret)
- [ ] Rate limiting (aggressive limits)
- [ ] HTTPS with HSTS headers
- [ ] WAF protecting API (Cloudflare, AWS WAF)
- [ ] IP whitelisting for API access
- [ ] Network segmentation (internal network only)
- [ ] Audit logging to external system (Splunk, ELK)
- [ ] Runtime security monitoring (Falco, Sysdig)
- [ ] Incident response plan documented
- [ ] Regular security audits scheduled
- [ ] Disaster recovery tested

## References

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/)
