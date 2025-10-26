# k9s Dockerfile - Kubernetes CLI UI
# Lightweight Alpine-based image

FROM alpine:3.20.3 AS base

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# Install runtime dependencies
RUN apk add --no-cache \
    ca-certificates=20250911-r0 \
    curl=8.14.1-r2 \
    bash=5.2.26-r0 \
    git=2.45.4-r0

# Install k9s
FROM base AS production

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ARG K9S_VERSION=v0.32.4
ARG TARGETARCH=amd64

RUN curl -sL https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${TARGETARCH}.tar.gz | \
    tar xvz -C /usr/local/bin k9s && \
    chmod +x /usr/local/bin/k9s

# Create k9s config directory with proper permissions
RUN mkdir -p /root/.config/k9s \
    && mkdir -p /root/.kube

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD k9s version || exit 1

WORKDIR /root

# Entrypoint for k9s
ENTRYPOINT ["k9s"]
CMD ["version"]
