# Docker Cluster Implementation

[![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-V2-blue)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready Docker cluster implementation featuring nginx load balancing, high availability with multiple web server replicas, and PostgreSQL database backend.

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
          ┌─────────┼─────────┐
          │         │         │
        Web1      Web2      Web3
       (nginx)   (nginx)   (nginx)
                     ↓
                PostgreSQL
              (Database:5432)
```

### Components

- **Load Balancer**: Nginx-based load balancer distributing traffic across web servers
- **Web Servers**: 3 nginx instances serving static content with round-robin distribution
- **Database**: PostgreSQL 16 with persistent storage and health monitoring
- **Networking**: Isolated bridge network for secure internal communication
- **Storage**: Named volumes for database persistence and nginx caching

## ✨ Features

- ✅ **High Availability**: Multiple web server replicas for redundancy
- ✅ **Load Balancing**: Nginx round-robin distribution across all replicas
- ✅ **Health Monitoring**: Comprehensive health checks for all services
- ✅ **Security**: Non-root execution, secrets management, network isolation
- ✅ **Performance**: BuildKit caching, optimized Dockerfiles
- ✅ **Scalability**: Easy horizontal scaling of web servers
- ✅ **Production Ready**: Best practices, proper logging, error handling

## 📦 Prerequisites

- Docker Engine 20.10+
- Docker Compose V2
- 2GB RAM minimum (4GB recommended)
- Ports 8080 (load balancer), 5432 (PostgreSQL)

## 📂 Project Structure

```
docker/
├── .devcontainer/          # VS Code devcontainer
├── .github/                # GitHub configuration
├── dockerfiles/            # Dockerfile definitions
│   ├── nginx.Dockerfile    # Nginx web server & load balancer
│   ├── postgres.Dockerfile # PostgreSQL database
│   ├── default.conf        # Nginx upstream config
│   ├── nginx.conf          # Nginx server config
│   └── postgresql.conf     # PostgreSQL tuning
├── docs/                   # Documentation
│   ├── architecture.md     # System architecture
│   ├── deployment.md       # Deployment guide
│   └── troubleshooting.md  # Troubleshooting guide
├── secrets/                # Secrets directory
├── web-content/            # Static web content
├── docker-compose.yml      # Main compose file
├── Makefile                # Build commands
├── nginx.conf              # Load balancer config
└── README.md               # This file
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

- **Load Balancer**: http://localhost:8080
- **PostgreSQL**: localhost:5432
  - Database: `clusterdb`
  - User: `cluster_user`
  - Password: From `secrets/db_password.txt`

## ⚙️ Configuration

### Environment Variables

Configure database in `cluster/docker-compose.yml`:

```yaml
environment:
  POSTGRES_DB: clusterdb
  POSTGRES_USER: cluster_user
  POSTGRES_PASSWORD_FILE: /run/secrets/db_password
```

### Scaling

Scale web servers dynamically:

```bash
cd cluster
docker-compose up -d --scale web1=5 --scale web2=5 --scale web3=5
```

### Custom Nginx Configuration

Edit load balancer configuration:
- `cluster/nginx.conf` - Main nginx configuration
- `cluster/dockerfiles/default.conf` - Upstream server configuration

### PostgreSQL Configuration

Customize PostgreSQL settings:
- `cluster/dockerfiles/postgresql.conf` - Database parameters

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
