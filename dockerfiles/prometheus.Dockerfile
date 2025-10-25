# Prometheus Dockerfile - Metrics collection and monitoring
# Production-ready configuration

FROM prom/prometheus:latest

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:9090/-/healthy || exit 1

USER nobody

EXPOSE 9090

VOLUME ["/prometheus"]

# Start Prometheus
ENTRYPOINT ["/bin/prometheus"]
CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.console.libraries=/usr/share/prometheus/console_libraries", \
     "--web.console.templates=/usr/share/prometheus/consoles"]
