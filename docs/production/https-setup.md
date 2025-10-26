---
date_created: "2025-10-26T18:32:25.948254+00:00"
last_updated: "2025-10-26T18:32:25.948254+00:00"
tags: ["documentation", "production", "deployment"]
description: "Documentation for https setup"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- production
- https
- traefik
- letsencrypt
  description: HTTPS setup with Traefik and Let's Encrypt certificates
  ---\n# HTTPS Configuration

## Traefik Configuration

Edit `.config/traefik/traefik.yml`:

```yaml
certificatesResolvers:
  letsencrypt:
    acme:
      email: "admin@your-domain.com"
      storage: "/letsencrypt/acme.json"
      caServer: "https://acme-v02.api.letsencrypt.org/directory"
      httpChallenge:
        entryPoint: web
```

## Domain Configuration

```yaml
entryPoints:
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: letsencrypt
        domains:
          - main: "your-domain.com"
            sans:
              - "*.your-domain.com"
```

## Docker Compose Traefik Service

```yaml
services:
  traefik:
    image: traefik:v2.10
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./config/traefik:/etc/traefik:ro
      - traefik-letsencrypt:/letsencrypt
    networks:
      - traefik-public
```

## Verify HTTPS

```bash
curl -I https://your-domain.com
# Should return HTTP/2 200
```

**Certificate auto-renewal:** Let's Encrypt certs renew automatically every 60 days.
