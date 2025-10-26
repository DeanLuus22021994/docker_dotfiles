# Traefik Reverse Proxy with Automatic HTTPS
# Handles SSL/TLS termination and routing for all services

FROM traefik:v3.2

# Labels for automatic service discovery
LABEL maintainer="Cluster Dashboard Team"
LABEL description="Traefik reverse proxy with automatic HTTPS via Let's Encrypt"
LABEL version="3.2"

# Expose ports
# 80: HTTP (redirects to HTTPS)
# 443: HTTPS
# 8080: Traefik dashboard (optional, disable in production)
EXPOSE 80 443 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD traefik healthcheck --ping || exit 1

# Run Traefik
# Configuration loaded from docker-compose.yml and dynamic configs
ENTRYPOINT ["/usr/local/bin/traefik"]
CMD ["--configFile=/etc/traefik/traefik.yml"]
