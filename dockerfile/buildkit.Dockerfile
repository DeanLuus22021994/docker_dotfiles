# BuildKit Dockerfile - Docker build engine with cache optimization
# Provides BuildKit daemon for faster, more efficient Docker builds

FROM moby/buildkit:buildx-stable-1

# Install additional tools for development
USER root

RUN apk add --no-cache \
    git \
    curl \
    ca-certificates \
    bash \
    openssh-client

# Create buildkit user and directories
RUN addgroup -g 1000 buildkit || true \
    && adduser -D -u 1000 -G buildkit buildkit || true \
    && mkdir -p /var/lib/buildkit \
    && mkdir -p /etc/buildkit \
    && chown -R buildkit:buildkit /var/lib/buildkit

# Copy custom buildkit configuration
COPY .config/docker/buildkitd.toml /etc/buildkit/buildkitd.toml

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD buildctl debug workers || exit 1

# Expose BuildKit port
EXPOSE 1234

# Volume for cache
VOLUME ["/var/lib/buildkit"]

USER buildkit

# Start BuildKit daemon
ENTRYPOINT ["buildkitd"]
CMD ["--addr", "tcp://0.0.0.0:1234", "--config", "/etc/buildkit/buildkitd.toml"]
