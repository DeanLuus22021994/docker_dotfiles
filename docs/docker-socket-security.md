# Docker Socket Security Guide

**Version:** 1.0  
**Last Updated:** 2025-10-26  
**Audience:** DevOps Engineers, System Administrators

---

## Overview

The Docker socket (`/var/run/docker.sock`) provides complete control over the Docker daemon. Mounting this socket in containers grants powerful capabilities but introduces significant security risks. This guide covers best practices, threat models, and alternative approaches.

---

## Security Risks

### High-Risk Scenarios

**1. Container Escape**
- Any container with socket access can start privileged containers
- Privileged containers can break out of containerization
- Result: Full host system compromise

**2. Arbitrary Code Execution**
- Containers can execute commands on the host via Docker API
- Can manipulate other containers (stop, start, inspect, modify)
- Can access sensitive data from all containers

**3. Data Exfiltration**
- Read volumes from any container
- Access environment variables (secrets, API keys)
- Inspect network traffic and configurations

**4. Denial of Service**
- Stop or remove critical containers
- Consume host resources (CPU, memory, disk)
- Disrupt entire Docker infrastructure

---

## Current Implementation

### API Server Socket Access

**File:** `api/server.js`

```javascript
const docker = new Docker({ socketPath: '/var/run/docker.sock' });
```

**docker-compose.yml:**

```yaml
services:
  api:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Security Controls

1. **Read-Only Mount** (`ro` flag)
   - Prevents write operations to socket file
   - Does NOT restrict Docker API write operations
   - **Limitation:** API can still modify containers despite read-only mount

2. **Authentication** (Optional)
   - JWT-based authentication (`AUTH_ENABLED` env var)
   - Default: disabled for development
   - **Recommendation:** Enable in production

3. **Rate Limiting**
   - 100 requests per 15 minutes (general API)
   - 10 requests per 15 minutes (container stats)
   - Prevents API abuse and DoS attacks

4. **Input Validation**
   - Container ID format validation (`/^[a-f0-9]{12,64}$/`)
   - Prevents injection attacks
   - Sanitizes error messages

---

## Threat Model

### Attack Vectors

**1. Compromised API Container**

Scenario: Attacker gains code execution in API container

Capabilities:
- Read all container configurations and secrets
- Stop/start any container
- Create new privileged containers
- Mount host filesystem
- Execute commands on host

**Impact:** Complete host compromise

**Mitigation:** Socket proxy, network segmentation, runtime security

**2. API Vulnerability Exploitation**

Scenario: Attacker exploits vulnerability in Express.js or dependencies

Capabilities:
- Bypass authentication/rate limiting
- Direct Docker API access
- Container manipulation

**Impact:** Service disruption, data breach

**Mitigation:** Security scanning, dependency updates, WAF

**3. Insider Threat**

Scenario: Malicious developer with API access

Capabilities:
- Same as compromised container
- Can modify codebase to create backdoors

**Impact:** Long-term persistent access

**Mitigation:** Code review, audit logging, least privilege

---

## Best Practices

### ✅ DO

1. **Use Socket Proxies**
   - Whitelist allowed API endpoints
   - Restrict dangerous operations
   - Audit all socket access
   - Example: `tecnativa/docker-socket-proxy`

2. **Enable Authentication**
   - Set `AUTH_ENABLED=true` in production
   - Use strong JWT secrets (32+ characters)
   - Rotate secrets regularly
   - Implement refresh token rotation

3. **Network Segmentation**
   - Isolate API container in separate network
   - Use internal DNS for service discovery
   - Limit external exposure

4. **Audit Logging**
   - Log all Docker API calls
   - Monitor for suspicious activity
   - Alert on privileged container creation
   - Retain logs for forensics

5. **Regular Security Scans**
   - Scan containers with Trivy/Grype
   - Update dependencies weekly
   - Patch vulnerabilities promptly
   - Use Dependabot for automation

6. **Runtime Security**
   - Use Falco or Sysdig for runtime monitoring
   - Detect anomalous container behavior
   - Alert on privilege escalation attempts

### ❌ DON'T

1. **Never mount socket read-write**
   ```yaml
   # DANGEROUS - Avoid this
   volumes:
     - /var/run/docker.sock:/var/run/docker.sock:rw
   ```

2. **Don't disable authentication in production**
   ```bash
   # INSECURE - Only for development
   AUTH_ENABLED=false
   ```

3. **Don't expose API publicly without WAF**
   - Always use reverse proxy (Traefik/Nginx)
   - Enable HTTPS/TLS
   - Implement IP whitelisting

4. **Don't ignore security updates**
   - Set up Dependabot
   - Monitor CVE databases
   - Test updates in staging

---

## Alternative Approaches

### 1. Docker Socket Proxy (Recommended)

**Tool:** `tecnativa/docker-socket-proxy`

**Benefits:**
- Whitelists specific API endpoints
- Denies dangerous operations by default
- Read-only by default
- Defense in depth

**Implementation:**

```yaml
# docker-compose.yml
services:
  docker-socket-proxy:
    image: tecnativa/docker-socket-proxy:latest
    environment:
      CONTAINERS: 1  # Allow container listing
      IMAGES: 1      # Allow image listing
      INFO: 1        # Allow system info
      VOLUMES: 0     # Deny volume operations
      NETWORKS: 0    # Deny network operations
      BUILD: 0       # Deny image building
      COMMIT: 0      # Deny container commits
      EXEC: 0        # Deny exec operations
      POST: 0        # Deny all POST operations
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - docker-proxy

  api:
    environment:
      DOCKER_HOST: tcp://docker-socket-proxy:2375
    depends_on:
      - docker-socket-proxy
    networks:
      - docker-proxy

networks:
  docker-proxy:
    internal: true
```

**Security Improvement:**
- API cannot perform dangerous operations
- Socket access audited and restricted
- Clear security boundary

### 2. Docker API over TCP with TLS

**Benefits:**
- No socket mounting required
- Mutual TLS authentication
- Network-level access control
- Works across hosts

**Implementation:**

1. **Enable Docker TLS (Host)**

```bash
# Generate CA and certificates
mkdir -p ~/.docker
cd ~/.docker

# CA certificate
openssl genrsa -aes256 -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem

# Server certificate
openssl genrsa -out server-key.pem 4096
openssl req -subj "/CN=dockerhost" -sha256 -new -key server-key.pem -out server.csr
openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out server-cert.pem

# Client certificate
openssl genrsa -out key.pem 4096
openssl req -subj '/CN=client' -new -key key.pem -out client.csr
openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out cert.pem

# Set permissions
chmod 0400 ca-key.pem key.pem server-key.pem
chmod 0444 ca.pem server-cert.pem cert.pem
```

2. **Configure Docker Daemon**

```json
// /etc/docker/daemon.json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"],
  "tls": true,
  "tlsverify": true,
  "tlscacert": "/root/.docker/ca.pem",
  "tlscert": "/root/.docker/server-cert.pem",
  "tlskey": "/root/.docker/server-key.pem"
}
```

3. **Use in API Container**

```javascript
// api/server.js
const Docker = require('dockerode');

const docker = new Docker({
  host: process.env.DOCKER_HOST || 'localhost',
  port: process.env.DOCKER_PORT || 2376,
  ca: fs.readFileSync(process.env.DOCKER_CA_PATH),
  cert: fs.readFileSync(process.env.DOCKER_CERT_PATH),
  key: fs.readFileSync(process.env.DOCKER_KEY_PATH)
});
```

**Security Improvement:**
- Mutual TLS authentication
- Network-level encryption
- No socket mounting
- Can restrict by IP/network

### 3. Rootless Docker

**Benefits:**
- Docker daemon runs as non-root user
- Reduced attack surface
- Container escape has limited impact
- Better security by default

**Limitations:**
- Some features unavailable (overlay networks, cgroup v1)
- Performance overhead
- More complex setup

**Implementation:**

```bash
# Install rootless Docker
curl -fsSL https://get.docker.com/rootless | sh

# Configure
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
export PATH=$HOME/bin:$PATH
```

### 4. Read-Only Operations Only

**Benefits:**
- No dangerous write operations
- Monitoring and metrics only
- Reduced risk

**Limitations:**
- Cannot stop/start containers
- Cannot create/delete resources
- Limited functionality

**Use Case:** Monitoring dashboards, read-only metrics

---

## Monitoring & Detection

### Key Indicators of Compromise (IOCs)

1. **Privileged Container Creation**
   ```bash
   # Monitor for this in Docker logs
   "container created with --privileged flag"
   ```

2. **Unusual Container Mount Points**
   ```bash
   # Watch for host filesystem mounts
   "container created with -v /:/host"
   ```

3. **High Volume API Calls**
   ```bash
   # Monitor API rate limiting
   "rate limit exceeded on /api/containers endpoint"
   ```

4. **Failed Authentication Attempts**
   ```bash
   # Watch auth logs
   "authentication failed for user: admin"
   ```

### Monitoring Tools

**1. Falco**
- Runtime security monitoring
- Detects anomalous container behavior
- Kubernetes and Docker support

**2. Sysdig**
- Container security platform
- Network traffic analysis
- Compliance scanning

**3. Docker Bench Security**
- CIS Docker Benchmark checks
- Best practice validation
- Automated scanning

**4. Prometheus + Grafana**
- API metrics (request rates, errors)
- Container resource usage
- Custom alerts

---

## Security Checklist

### Development Environment

- [ ] Socket mounted read-only (`:ro`)
- [ ] Input validation implemented
- [ ] Error messages sanitized
- [ ] Rate limiting configured
- [ ] Authentication available (can be disabled)
- [ ] Security scanning in pre-commit hooks
- [ ] Dependencies updated regularly

### Staging Environment

- [ ] Socket proxy implemented
- [ ] Authentication enabled
- [ ] Rate limiting enforced
- [ ] HTTPS/TLS configured
- [ ] Network segmentation in place
- [ ] Audit logging enabled
- [ ] Security scans automated (Trivy, npm audit)
- [ ] Secrets stored in vault (not environment)

### Production Environment

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

---

## Incident Response

### Suspected Compromise

1. **Immediate Actions**
   - Isolate affected container (network disconnect)
   - Snapshot container state for forensics
   - Review audit logs for timeline
   - Check for persistence mechanisms

2. **Investigation**
   - Analyze Docker API logs
   - Review authentication logs
   - Check for modified containers
   - Inspect running processes

3. **Remediation**
   - Stop compromised container
   - Rebuild from known-good image
   - Rotate all secrets (JWT, API keys)
   - Patch vulnerability if identified
   - Update security policies

4. **Prevention**
   - Implement socket proxy if not present
   - Tighten rate limits
   - Enable additional monitoring
   - Conduct security training
   - Document lessons learned

---

## References

### Documentation

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

### Tools

- [tecnativa/docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy)
- [Falco Runtime Security](https://falco.org/)
- [Trivy Container Scanner](https://github.com/aquasecurity/trivy)
- [Docker Bench Security](https://github.com/docker/docker-bench-security)

### Related Guides

- [api/SECURITY.md](../api/SECURITY.md) - API security implementation
- [docs/production-deployment.md](production-deployment.md) - Production deployment guide
- [SECURITY.md](../SECURITY.md) - Project security policy

---

## Changelog

### v1.0 (2025-10-26)
- Initial release
- Documented threat model and attack vectors
- Added socket proxy implementation guide
- Included Docker TLS alternative
- Provided monitoring and incident response guidance

---

**Questions?** Review [api/SECURITY.md](../api/SECURITY.md) or contact the security team.
