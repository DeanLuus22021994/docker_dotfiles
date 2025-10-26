# Lightweight NVIDIA Kubernetes Device Plugin for GPU support
# Official NVIDIA container for GPU orchestration in k8s clusters
FROM nvcr.io/nvidia/k8s-device-plugin:v0.14.5

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

WORKDIR /workspace

# Health check - verify nvidia-device-plugin is available
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=10s \
    CMD ps aux | grep nvidia-device-plugin || exit 1

# Default command inherited from base image

