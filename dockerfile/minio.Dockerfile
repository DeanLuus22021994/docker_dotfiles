# MinIO Dockerfile - S3-compatible object storage
# Production-ready configuration

FROM minio/minio:latest

# Install curl for health checks
RUN microdnf install -y curl && microdnf clean all

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:9000/minio/health/live || exit 1

VOLUME ["/data"]

EXPOSE 9000 9001

# Start MinIO server with console
ENTRYPOINT ["/usr/bin/minio"]
CMD ["server", "/data", "--console-address", ":9001"]
