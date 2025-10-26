---
date_created: "2025-10-26T18:32:25.950320+00:00"
last_updated: "2025-10-26T18:32:25.950320+00:00"
tags: ['documentation', 'production', 'deployment']
description: "Documentation for troubleshooting"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- production
- troubleshooting
- debugging
- support
description: Common production issues and troubleshooting steps
---\n# Production Troubleshooting

## Certificate Issues

**Problem:** HTTPS not working

**Solutions:**

```bash
# Check certificate status
docker exec traefik cat /letsencrypt/acme.json

# Verify DNS records
dig your-domain.com +short

# Check Traefik logs
docker-compose logs traefik | grep -i certificate
```

## Authentication Failures

**Problem:** JWT tokens not working

**Solutions:**

- Verify JWT_SECRET is set in .env
- Check token expiration (JWT_EXPIRES_IN)
- Confirm AUTH_ENABLED=true
- Review API logs for auth errors

## Service Not Accessible

**Problem:** Can't reach service through Traefik

**Solutions:**

```bash
# Check service labels
docker inspect <container> | grep traefik.http

# Verify network connectivity
docker network inspect traefik-public

# Test internal access
docker exec traefik wget -O- http://api:3000/health
```

## High Resource Usage

**Problem:** Container using too much CPU/memory

**Solutions:**

```bash
# Check resource usage
docker stats

# Set resource limits in docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

## Database Connection Errors

**Problem:** Services can't connect to databases

**Solutions:**

- Verify database passwords in .env match docker-compose
- Check database container health: `docker-compose ps`
- Review database logs: `docker-compose logs postgres`

**Need Help?** Check GitHub issues or contact support.
