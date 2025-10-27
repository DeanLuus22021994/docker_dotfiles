---
date_created: '2025-10-27T02:27:50Z'
last_updated: '2025-10-27T02:27:50Z'
tags: [docker, configuration, buildkit, beta-features, gpu]
description: 'Docker configuration files for local development and production'
---

# Docker Configuration

This directory contains Docker daemon and BuildKit configuration files optimized for local development with cutting-edge beta features.

## 📁 Files Overview

### daemon.json

**Docker Engine daemon configuration** - Reference file for system-level Docker settings.

**Apply Location:**
- **Windows (WSL2)**: %USERPROFILE%\.docker\daemon.json
- **Linux**: /etc/docker/daemon.json
- **macOS**: ~/.docker/daemon.json

**Key Features:**
- ✅ **BuildKit v0.25.1** enabled by default
- ✅ **250GB build cache** (20.4 GB used, 5.2 GB shared)
- ✅ **Experimental features** enabled
- ✅ **Multi-platform support**: amd64, arm64, riscv64, ppc64le, s390x, arm/v7, arm/v6
- ✅ **NVIDIA GPU runtime** configured for ML/AI workloads
- ✅ **DNS servers**: Google (8.8.8.8, 8.8.4.4) + Cloudflare (1.1.1.1)
- ✅ **50 concurrent downloads/uploads** for faster operations
- ✅ **Custom network pools** (172.20.0.0/16) to avoid conflicts

**Beta Features Enabled:**
- 🤖 **Docker AI** - "Ask Gordon" CLI assistant and Desktop integration
- 🔗 **Docker MCP Toolkit** - Model Context Protocol for AI agents
- 🌐 **Wasm Support** - WebAssembly workloads with containerd image store
- 🚀 **Docker Model Runner** - GPU-accelerated inference engines
  - Endpoints: model-runner.docker.internal:80, localhost:12434
  - GPU: RTX consumer-grade with NVIDIA runtime
  - Components: ~/.docker/bin/inference
- 🧩 **Docker Extensions** - Marketplace distribution enabled

**Apply Changes:**
```powershell
# Windows - Restart Docker Desktop from system tray

# Linux
sudo systemctl restart docker

# macOS
# Restart Docker Desktop
```

---

### uildkitd.toml

**BuildKit daemon configuration** for the cluster-buildkit service.

**Mounted via**: docker-compose.yml → /etc/buildkit/buildkitd.toml

**Key Features:**
- �� **250GB cache** with 7-day retention (aligned with daemon.json)
- 🌍 **Multi-platform builds**: amd64, arm64, riscv64, ppc64le, s390x, arm variants
- 🧹 **Advanced garbage collection**:
  - Primary policy: Keep 200GB for 3 days
  - Secondary policy: Keep 50GB for 2 days
- ⚡ **50 max parallelism** (aligned with concurrent operations)
- 📊 **Build history**: 500 entries, 7-day retention

**Cache Policies:**
```toml
[[worker.oci.gcpolicy]]
  keepBytes = 214748364800  # 200GB
  keepDuration = 259200     # 3 days
  filters = ["type==source.local,type==exec.cachemount,type==source.git.checkout"]

[[worker.oci.gcpolicy]]
  all = true
  keepBytes = 53687091200  # 50GB
  keepDuration = 172800     # 2 days
```

**Validation:**
```powershell
# Check if mounted correctly
docker exec cluster-buildkit cat /etc/buildkit/buildkitd.toml

# View cache usage
docker exec cluster-buildkit buildctl debug workers
```

---

### compose.override.example.yml

**Local development overrides template** - Copy and customize for your environment.

**Setup:**
```powershell
# Copy to project root (automatically gitignored)
Copy-Item .config/docker/compose.override.example.yml docker-compose.override.yml

# Edit for local environment
code docker-compose.override.yml
```

**Usage:**
- Automatically loaded by docker-compose commands
- Overrides/extends main docker-compose.yml
- **Never committed** (in .gitignore)

**Example Use Cases:**
- 🔧 Port conflict resolution
- 🔥 Hot-reload volume mounts
- 🐛 Debug mode enablement
- 💪 Resource limit adjustments
- 🖥️ **GPU workload configuration** (new)
- 🌐 **WebAssembly runtime** examples (new)
- 🤖 **AI inference** with Model Runner (new)

**New Examples Added:**
```yaml
# GPU-accelerated ML workload
cluster-ml-model:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: all
            capabilities: [gpu]

# WebAssembly workload
cluster-wasm-app:
  runtime: io.containerd.wasmedge.v1
  platform: wasi/wasm

# Local AI inference
local-inference:
  image: ollama/ollama:latest
  ports:
    - "11434:11434"
```

---

## 🚀 Quick Start

### 1. Apply Daemon Configuration

```powershell
# Windows (PowerShell as Administrator)
Copy-Item .config/docker/daemon.json C:\Users\deanl.MSI\.docker\daemon.json
# Restart Docker Desktop from system tray

# Linux
sudo cp .config/docker/daemon.json /etc/docker/daemon.json
sudo systemctl restart docker

# Verify
docker info | Select-String -Pattern "BuildKit|Experimental|GPU"
```

### 2. Verify BuildKit Service

```powershell
# BuildKit is pre-configured in cluster-buildkit service
docker-compose ps cluster-buildkit

# Check cache usage
docker exec cluster-buildkit buildctl debug workers

# View build history
docker exec cluster-buildkit buildctl debug history
```

### 3. Create Local Overrides

```powershell
# Copy template
Copy-Item .config/docker/compose.override.example.yml docker-compose.override.yml

# Customize for your needs
# Examples: Change ports, add debug volumes, enable GPU
```

### 4. Test Beta Features

```powershell
# Test Docker AI
docker ai "How do I optimize my Dockerfile?"

# Test GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# Test Model Runner
curl http://model-runner.docker.internal:80/health
curl http://localhost:12434/health

# Test Wasm support
docker info | Select-String -Pattern "containerd"
```

---

## 🎯 Best Practices

### For Local Development

✅ **Use overrides file** - Keep local changes in docker-compose.override.yml  
✅ **Leverage BuildKit cache** - 250GB available for fast rebuilds  
✅ **Multi-platform builds** - Test ARM compatibility early  
✅ **GPU workloads** - Use deploy.resources.reservations.devices  
✅ **AI features** - Leverage Model Runner for ML inference  
✅ **Wasm workloads** - Use containerd image store for WebAssembly  
✅ **Port management** - Override ports in local overrides file  

### For Production

✅ **Apply daemon.json** - Consistent logging and resource limits  
✅ **Enable BuildKit** - Faster builds with advanced caching  
✅ **No overrides** - Use only main docker-compose.yml  
✅ **Secrets management** - Always use Docker secrets, never env vars  
✅ **Health checks** - Verify all services before deployment  
✅ **Disable beta features** - Only use stable features in production  
❌ **No GPU in prod** - Unless specifically architected for ML workloads  

---

## 🔧 Troubleshooting

### BuildKit Cache Not Working

```powershell
# Check cache size
docker exec cluster-buildkit buildctl du

# Clear cache if needed
docker exec cluster-buildkit buildctl prune --all

# Verify cache retention policy
docker exec cluster-buildkit cat /etc/buildkit/buildkitd.toml
```

### GPU Not Available

```powershell
# Verify NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# Check daemon.json includes runtime
Get-Content C:\Users\deanl.MSI\.docker\daemon.json | Select-String -Pattern "nvidia"

# Restart Docker Desktop after changes
```

### Model Runner Not Working

```powershell
# Check inference engine
Test-Path C:\Users\deanl.MSI\.docker\bin\inference

# Test endpoints
curl http://model-runner.docker.internal:80/health
curl http://localhost:12434/health

# Check logs (if running as service)
docker logs <model-runner-container-name>
```

### Wasm Workloads Failing

```powershell
# Verify containerd image store
docker info | Select-String -Pattern "Storage Driver"

# Check Wasm runtime
docker buildx ls
```

### Port Conflicts

```powershell
# Check what's using ports
netstat -ano | Select-String ":5432"

# Override in docker-compose.override.yml
# services:
#   cluster-postgres:
#     ports:
#       - "5433:5432"
```

---

## 📚 References

- [Docker Daemon Configuration Docs](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)
- [BuildKit Configuration Guide](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md)
- [Docker Compose Override](https://docs.docker.com/compose/extends/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- [Docker Desktop Beta Features](https://docs.docker.com/desktop/beta/)
- [WebAssembly on Docker](https://docs.docker.com/desktop/wasm/)

---

## 📝 Maintenance

**Update Schedule:**
- Review cache usage monthly
- Update BuildKit version quarterly
- Test beta features before enabling
- Document breaking changes in this README

**Cache Monitoring:**
```powershell
# Check current usage
docker exec cluster-buildkit buildctl du

# View detailed cache breakdown
docker system df -v

# Clean up if needed (>200GB used)
docker builder prune --filter "until=72h"
```

**Version Tracking:**
- **BuildKit**: v0.25.1 (as of 2025-01-26)
- **Docker Desktop**: Latest with beta features enabled
- **NVIDIA Runtime**: Latest from Container Toolkit
