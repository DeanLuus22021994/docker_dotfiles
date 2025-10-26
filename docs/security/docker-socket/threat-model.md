---
date_created: "2025-10-26T18:32:25.979678+00:00"
last_updated: "2025-10-26T18:32:25.979678+00:00"
tags: ['documentation', 'security', 'docker']
description: "Documentation for threat model"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- docker
- security
description: Docker socket threat model and attack vector analysis
---\n# Docker Socket Threat Model

## Attack Vectors

### 1. Compromised API Container

**Scenario:** Attacker gains code execution in API container

**Capabilities:**
- Read all container configurations and secrets
- Stop/start any container
- Create new privileged containers
- Mount host filesystem
- Execute commands on host

**Impact:** Complete host compromise

**Mitigation:** Socket proxy, network segmentation, runtime security

### 2. API Vulnerability Exploitation

**Scenario:** Attacker exploits vulnerability in Express.js or dependencies

**Capabilities:**
- Bypass authentication/rate limiting
- Direct Docker API access
- Container manipulation

**Impact:** Service disruption, data breach

**Mitigation:** Security scanning, dependency updates, WAF

### 3. Insider Threat

**Scenario:** Malicious developer with API access

**Capabilities:**
- Same as compromised container
- Can modify codebase to create backdoors

**Impact:** Long-term persistent access

**Mitigation:** Code review, audit logging, least privilege

## Key Indicators of Compromise

- Privileged container creation (`--privileged` flag)
- Unusual container mount points (`-v /:/host`)
- High volume API calls (rate limit exceeded)
- Failed authentication attempts
