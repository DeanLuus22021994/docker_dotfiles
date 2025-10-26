---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["docker", "security", "best-practices", "hardening"]
description: "Docker socket security best practices and hardening guidelines"
---
# Docker Socket Best Practices

## ✅ DO

**1. Use Socket Proxies**
- Whitelist allowed API endpoints
- Restrict dangerous operations
- Audit all socket access
- Tool: `tecnativa/docker-socket-proxy`

**2. Enable Authentication**
- Set `AUTH_ENABLED=true` in production
- Use strong JWT secrets (32+ characters)
- Rotate secrets regularly
- Implement refresh token rotation

**3. Network Segmentation**
- Isolate API container in separate network
- Use internal DNS for service discovery
- Limit external exposure

**4. Audit Logging**
- Log all Docker API calls
- Monitor for suspicious activity
- Alert on privileged container creation
- Retain logs for forensics

**5. Regular Security Scans**
- Scan containers with Trivy/Grype
- Update dependencies weekly
- Patch vulnerabilities promptly
- Use Dependabot for automation

**6. Runtime Security**
- Use Falco or Sysdig for runtime monitoring
- Detect anomalous container behavior
- Alert on privilege escalation attempts

## ❌ DON'T

**1. Never mount socket read-write**
```yaml
# DANGEROUS
volumes:
  - /var/run/docker.sock:/var/run/docker.sock:rw
```

**2. Don't disable authentication in production**
```bash
AUTH_ENABLED=false  # INSECURE
```

**3. Don't expose API publicly without WAF**

**4. Don't ignore security updates**
