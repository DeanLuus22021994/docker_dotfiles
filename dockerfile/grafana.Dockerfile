# Grafana Dockerfile - Monitoring and visualization
# Production-ready configuration

FROM grafana/grafana:latest

# Install curl for better health checks
USER root
RUN apk add --no-cache curl

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

USER grafana

EXPOSE 3000

VOLUME ["/var/lib/grafana"]

# Start Grafana
CMD ["grafana-server", "--homepath=/usr/share/grafana", "--config=/etc/grafana/grafana.ini"]
