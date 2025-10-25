# Modern Data Platform - Docker Cluster

[![Docker](https://img.shields.io/badge/Docker-24.0%2B-blue)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-V2-blue)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GPU](https://img.shields.io/badge/CUDA-12.2-green)](https://developer.nvidia.com/cuda-toolkit)

A turn-key modern data platform featuring GPU-accelerated Jupyter, load-balanced web services, dual databases (PostgreSQL + MariaDB), Redis cache, S3-compatible storage (MinIO), GitHub MCP integration, production-grade monitoring with Grafana/Prometheus, and complete local development stack (BuildKit, LocalStack, MailHog, pgAdmin, Redis Commander).

## 🚀 Quick Start

```bash
# Clone and navigate
git clone <repository-url>
cd docker

# Build and start cluster
make build
make up

# Verify deployment
curl http://localhost:8080/
make ps

# For development with VS Code
make dev  # Starts cluster + devcontainer
```

## 📋 Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🏗️ Architecture

```
Internet → Load Balancer (nginx:8080)
            ↓
    ┌───────┼───────┐
   Web1   Web2   Web3
    ↓       ↓      ↓
┌─────────────────────────────┐
│   Data & Processing Layer   │
├─────────────────────────────┤
│ PostgreSQL:5432             │
│ MariaDB:3306                │
│ Redis:6379 (Cache)          │
│ MinIO:9000 (S3 Storage)     │
│ Jupyter:8888 (GPU/ML)       │
│ GitHub MCP (AI Context)     │
├─────────────────────────────┤
│   Monitoring & Ops          │
│ Grafana:3002 | Prometheus   │
│ k9s (K8s CLI)               │
└─────────────────────────────┘
```

### Components

- **Load Balancer**: Nginx-based load balancer distributing traffic across web servers
- **Web Servers**: 3 nginx instances serving static content with round-robin distribution
- **Database**: PostgreSQL 16 with persistent storage and health monitoring
- **Networking**: Isolated bridge network for secure internal communication
- **Storage**: Named volumes for database persistence and nginx caching

## ✨ Features

- ✅ **GPU-Accelerated ML**: Jupyter TensorFlow notebook with CUDA 12.2 support
- ✅ **Dual Databases**: PostgreSQL (RDBMS) + MariaDB with optimized configs
- ✅ **High Availability**: Load-balanced 3x nginx web servers with Redis cache
- ✅ **S3-Compatible Storage**: MinIO for object storage (9000/9001)
- ✅ **AI Integration**: GitHub MCP Server for Model Context Protocol
- ✅ **Production Monitoring**: Grafana dashboards + Prometheus metrics
- ✅ **K8s Management**: k9s terminal UI for Kubernetes workflows
- ✅ **DevContainer Ready**: VS Code integration with all services
- ✅ **Local Development Stack**:
  - BuildKit: Optimized Docker builds with cache
  - LocalStack: Local AWS cloud emulation (S3, DynamoDB, SQS, SNS, Lambda)
  - MailHog: Email testing and capture
  - pgAdmin: Web-based database administration
  - Redis Commander: Redis data browser and management
- ✅ **Security**: Non-root execution, secrets management, network isolation
- ✅ **Performance**: BuildKit caching, optimized Dockerfiles, health checks

## 📦 Prerequisites

- Docker Engine 24.0+ with BuildKit enabled
- Docker Compose V2
- 8GB RAM minimum (16GB recommended for Jupyter GPU workloads)
- NVIDIA GPU + drivers (optional, for Jupyter CUDA acceleration)
- Ports: 8080, 5432, 3306, 6379, 8888, 9000, 9001, 3002, 9090
- Windows: WSL2 with Docker Desktop | Linux: Docker Engine | macOS: Docker Desktop

### Environment Variables Setup

**Required before starting the stack:**

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials (use strong passwords):
   ```bash
   GITHUB_OWNER=YourUsername
   GH_PAT=ghp_xxxxxxxxxxxxxxxxxxxx

   # Database passwords (16+ chars, mixed case/numbers/symbols)
   DOCKER_POSTGRES_PASSWORD=your_secure_password
   DOCKER_MARIADB_ROOT_PASSWORD=your_secure_root_password
   DOCKER_MARIADB_PASSWORD=your_secure_password

   # Service credentials
   DOCKER_REDIS_PASSWORD=your_redis_password
   DOCKER_MINIO_ROOT_USER=minioadmin
   DOCKER_MINIO_ROOT_PASSWORD=your_minio_password
   DOCKER_GRAFANA_ADMIN_PASSWORD=your_grafana_password
   DOCKER_JUPYTER_TOKEN=your_jupyter_token
   DOCKER_PGADMIN_PASSWORD=your_pgadmin_password
   ```

3. Load environment variables (PowerShell):
   ```powershell
   Get-Content .env | ForEach-Object {
     $var = $_.Split('=')
     [Environment]::SetEnvironmentVariable($var[0], $var[1], 'Process')
   }
   ```

   Or on Linux/macOS:
   ```bash
   export $(cat .env | xargs)
   ```

4. Validate environment:
   ```bash
   python scripts/validate_env.py
   # Or use make:
   make validate-env
   ```

**Security Notes:**
- Never commit `.env` file (gitignored)
- Use GitHub Secrets for CI/CD environments
- Rotate passwords regularly (update `.env` and restart services)
- All service passwords use `DOCKER_` prefix for consistency

## 📂 Project Structure

```
docker/
├── .config/                    # Centralized configuration (SSoT)
│   ├── nginx/                  # Nginx configs (loadbalancer, main, default)
│   ├── database/               # PostgreSQL and MariaDB configs
│   ├── services/               # Service-specific configs (pgAdmin, LocalStack)
│   ├── docker/                 # Docker daemon configs (buildkitd.toml)
│   ├── github/                 # GitHub Actions workflows, Dependabot
│   └── monitoring/             # Prometheus, Grafana, Alertmanager
├── .devcontainer/              # VS Code devcontainer config
│   ├── devcontainer.json       # DevContainer settings + runServices
│   └── devcontainer.dockerfile # Python 3.13 + Node 22 + kubectl
├── .github/                    # GitHub configuration
│   ├── copilot-instructions.md # Copilot coding standards
│   ├── TODO.md                 # Implementation tracking
│   └── workflows/              # CI/CD pipelines (validation, pages)
├── .vscode/                    # VS Code team settings
│   ├── settings.json           # Team settings (tracked)
│   └── settings.local.example.json # Personal settings template (gitignored)
├── dockerfile/                 # Dockerfile definitions (SRP)
│   ├── nginx.Dockerfile        # Nginx Alpine
│   ├── postgres.Dockerfile     # PostgreSQL 13 Alpine
│   ├── mariadb.Dockerfile      # MariaDB 11 Jammy
│   ├── redis.Dockerfile        # Redis 7 Alpine
│   ├── jupyter.Dockerfile      # TensorFlow GPU notebook
│   ├── minio.Dockerfile        # S3-compatible storage
│   ├── grafana.Dockerfile      # Monitoring dashboards
│   ├── prometheus.Dockerfile   # Metrics collection
│   ├── github-mcp.Dockerfile   # MCP server for GitHub
│   ├── k9s.Dockerfile          # Kubernetes CLI UI
│   └── pre-commit.Dockerfile   # Pre-commit hooks automation
├── scripts/                    # Automation scripts
│   ├── validate_env.py         # Environment variable validation
│   ├── validate_configs.py     # Configuration file validation
│   └── serve_docs.ps1          # Documentation server
├── web-content/                # Static web content
│   └── index.html              # Cluster landing page
├── docker-compose.yml          # 26-service orchestration
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── .env.example                # Environment variables template
├── Makefile                    # Build + test + validate commands
├── AGENT.md                    # Development guidelines
└── README.md                   # This file
```

## 🔧 Installation

### Production Deployment

```bash
# Clone repository
git clone <repository-url>
cd docker

# Build and start
make build
make up

# Verify
make ps
curl http://localhost:8080/
```

### Development with VS Code

1. **Open in VS Code**:
```bash
code .
```

2. **Open in DevContainer**:
   - Press `F1` or `Ctrl+Shift+P`
   - Select "Dev Containers: Reopen in Container"
   - Wait for container build and initialization

3. **Development environment includes**:
   - Full cluster access (load balancer, web servers, database)
   - Python 3.13 with UV package manager
   - Node.js 22 with npm
   - Docker-in-Docker for managing cluster
   - VS Code extensions pre-installed

## 📖 Usage

### Makefile Commands

```bash
make help       # Show all available commands
make build      # Build Docker images
make up         # Start the cluster
make down       # Stop the cluster
make logs       # View logs
make ps         # Show running services
make restart    # Restart the cluster
make validate   # Validate configuration
make clean      # Clean up resources
```

### Docker Compose Commands

```bash
# Start production cluster
docker-compose up -d loadbalancer web1 web2 web3 db

# Start with devcontainer
docker-compose --profile dev up -d

# View logs
docker-compose logs -f [service_name]

# Check status
docker-compose ps

# Scale web servers
make scale N=5

# Stop services
docker-compose down

# Clean up (including volumes)
docker-compose down -v
```

### Service Access

- **Load Balancer**: http://localhost:8080 (Web UI)
- **PostgreSQL**: localhost:5432 (User: cluster_user, DB: clusterdb)
- **MariaDB**: localhost:3306 (User: cluster_user, DB: clusterdb)
- **Redis**: localhost:6379 (Password: changeme)
- **Jupyter Lab**: http://localhost:8888 (Token: changeme, GPU-enabled)
- **MinIO Console**: http://localhost:9001 (Admin/Admin)
- **MinIO API**: localhost:9000 (S3-compatible)
- **Grafana**: http://localhost:3002 (Admin/Admin)
- **Prometheus**: http://localhost:9090 (Metrics)
- **GitHub MCP**: stdio-based (Node.js integration)
- **BuildKit**: localhost:1234 (Build daemon)
- **LocalStack**: http://localhost:4566 (AWS emulation)
- **MailHog**: http://localhost:8025 (Email testing UI, SMTP: 1025)
- **pgAdmin**: http://localhost:5050 (admin@cluster.local/admin)
- **Redis Commander**: http://localhost:8081 (admin/admin)

## ⚙️ Configuration

### Configuration Management (SSoT)

All configurations are centralized in `.config/` directory using native formats:

**Nginx Configs** (`.config/nginx/`):
- `loadbalancer.conf` - Load balancer routing to web1/2/3
- `main.conf` - Worker processes, gzip, security headers, rate limiting
- `default.conf` - Static content, API endpoints, health checks

**Database Configs** (`.config/database/`):
- `postgresql.conf` - max_connections: 200, shared_buffers: 256MB, WAL settings
- `mariadb.conf` - utf8mb4, innodb_buffer_pool: 256MB, binary logging

**Service Configs** (`.config/services/`):
- `pgadmin-servers.json` - Pre-configured PostgreSQL/MariaDB connections
- `localstack-init.sh` - S3 buckets, DynamoDB tables, SQS queues, SNS topics

**Docker Configs** (`.config/docker/`):
- `buildkitd.toml` - 10GB cache, 3-day retention, multi-platform support

**Validation Commands:**
```bash
# Validate all configs
make validate-configs
# Or directly:
python scripts/validate_configs.py

# Validate environment variables
make validate-env

# Validate docker-compose syntax
make validate

# Run all validations
make test-all
```

### Pre-commit Hooks (Automated Quality)

Pre-commit hooks run automatically in the `cluster-pre-commit` container service:

**Enabled Hooks:**
- YAML/JSON syntax validation
- Secrets detection (detect-secrets)
- docker-compose validation
- Python formatting (Black, Ruff)
- Trailing whitespace, end-of-file fixer

**Usage:**
```bash
# Pre-commit runs automatically in dev profile
make dev

# Manual run (if needed)
docker-compose run --rm cluster-pre-commit

# Or install locally
pre-commit install
pre-commit run --all-files
```

**Configuration:** See `.pre-commit-config.yaml`

### Environment Variables

Configure services using `DOCKER_` prefixed environment variables (see Prerequisites section above).

**No Docker Secrets** - All credentials via environment variables for consistency and CI/CD compatibility.

### Scaling

Scale web servers dynamically:

```bash
docker-compose up -d --scale cluster-web1=5 --scale cluster-web2=5 --scale cluster-web3=5
```

## 📚 Documentation

Detailed documentation available in the `docs/` directory:

- [Architecture](docs/architecture.md) - System design and component details
- [Deployment](docs/deployment.md) - Deployment strategies and best practices
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions
- [Cluster README](cluster/README.md) - Cluster-specific documentation

## 🔍 Troubleshooting

### Port Conflicts

```bash
# Check if ports are in use
netstat -ano | findstr :8080
netstat -ano | findstr :5432
```

### Service Health Issues

```bash
# Check service logs
make logs

# Inspect specific service
docker-compose -f cluster/docker-compose.yml logs [service_name]

# Check health status
docker inspect <container_id> | findstr Health
```

### Database Connection

```bash
# Test database connectivity
docker-compose -f cluster/docker-compose.yml exec db psql -U cluster_user -d clusterdb -c "SELECT 1;"
```

### Clean Restart

```bash
# Complete cleanup and fresh start
make clean
make build
make up
```

## 🛡️ Security

- Non-root user execution in all containers
- Secret management for sensitive data
- Read-only volumes where applicable
- Network isolation with bridge networking
- Regular security updates via base images
- Minimal attack surface with Alpine Linux

## 🚀 Performance

- BuildKit caching for fast builds
- Optimized multi-stage Dockerfiles
- Named volumes for persistent data
- Nginx caching for improved response times
- PostgreSQL tuning for optimal performance
- Resource limits and health checks

## 🔄 Maintenance

### Backup Database

```bash
docker-compose -f cluster/docker-compose.yml exec db pg_dump -U cluster_user clusterdb > backup.sql
```

### Restore Database

```bash
docker-compose -f cluster/docker-compose.yml exec -T db psql -U cluster_user -d clusterdb < backup.sql
```

### Update Images

```bash
make build --no-cache
make restart
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Docker and Docker Compose for containerization
- Nginx for load balancing
- PostgreSQL for database backend
- Alpine Linux for minimal base images

## 📧 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check [Troubleshooting](docs/troubleshooting.md) documentation
- Review [Architecture](docs/architecture.md) for system design

---

**Made with ❤️ for production-ready Docker deployments**
