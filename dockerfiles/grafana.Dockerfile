# Grafana Dockerfile - Monitoring and visualization
# Production-ready configuration

FROM grafana/grafana:latest

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/api/health || exit 1

USER grafana

EXPOSE 3000

VOLUME ["/var/lib/grafana"]

# Start Grafana
CMD ["grafana-server", "--homepath=/usr/share/grafana", "--config=/etc/grafana/grafana.ini"]
