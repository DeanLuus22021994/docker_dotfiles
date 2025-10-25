# k9s Dockerfile - Kubernetes CLI UI
# Lightweight Alpine-based image

FROM alpine:latest AS base

# Install runtime dependencies
RUN apk add --no-cache \
    ca-certificates \
    curl \
    bash \
    git

# Install k9s
FROM base AS production

ARG K9S_VERSION=v0.32.4
ARG TARGETARCH=amd64

RUN curl -sL https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TARGETARCH}.tar.gz | \
    tar xvz -C /usr/local/bin k9s && \
    chmod +x /usr/local/bin/k9s

# Create k9s config directory
RUN mkdir -p /root/.config/k9s

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD k9s version || exit 1

WORKDIR /root

# Start k9s in headless mode
CMD ["k9s", "version"]
