# Documentation Index

**Modern Data Platform - Comprehensive Documentation**  
**Last Updated:** 2025-10-26  
**Version:** 4.0

---

## 🚀 Getting Started

Start here if you're new to the platform:

- **[README](../README.md)** - Project overview, features, and quick navigation
- **[SETUP](../SETUP.md)** - Complete installation and configuration guide
- **[Quickstart Guide](../web-content/QUICKSTART.md)** - Get up and running in 5 minutes
- **[Production Deployment](production-deployment.md)** - HTTPS, authentication, security hardening

---

## 🏗️ Architecture & Design

Understand how the platform is structured:

- **[Web Dashboard Architecture](../web-content/ARCHITECTURE.md)** - Frontend architecture, layers, services
- **[Cluster Design](../CLUSTER.md)** - Docker cluster architecture and networking
- **[API Documentation](../api/README.md)** - API server endpoints and usage
- **[Security Policy](../SECURITY.md)** - Security features and vulnerability reporting
- **[API Security](../api/SECURITY.md)** - Authentication, rate limiting, CORS, validation

---

## 🛠️ Development

Guides for developers and contributors:

### Scripts & Automation

- **[Scripts Overview](../scripts/README.md)** - All scripts organized by language
- **[Python Scripts](../scripts/python/README.md)** - Validation, audit, utilities
- **[PowerShell Scripts](../scripts/powershell/README.md)** - Windows automation
- **[Bash Scripts](../scripts/bash/README.md)** - Linux/macOS automation
- **[Migration Guide](../scripts/MIGRATION.md)** - Script reorganization and migration

### Web Dashboard

- **[Installation Guide](../web-content/INSTALL.md)** - Frontend setup and configuration
- **[Development Guide](../web-content/README.md)** - Local development, hot reload

### Testing

- **[Testing Guide](../tests/README.md)** - pytest configuration, running tests
- **[Test Coverage](../COVERAGE.md)** - Coverage reports and metrics

---

## 📦 Services & Components

Documentation for individual services:

### Data Layer

- **PostgreSQL** - Relational database configuration
- **MariaDB** - Alternative relational database
- **Redis** - In-memory cache and message broker
- **MinIO** - S3-compatible object storage

### Services Layer

- **API Server** - Docker Engine API proxy ([README](../api/README.md))
- **Web Dashboard** - React/Vite dashboard ([README](../web-content/README.md))

### Monitoring Layer

- **Grafana** - Metrics visualization dashboards
- **Prometheus** - Time-series metrics collection
- **[Monitoring Configuration](.config/monitoring/README.md)** - Setup guides

### Compute Layer

- **Jupyter** - Interactive Python notebooks
- **[Dev Containers](../.devcontainer/README.md)** - VS Code dev environment

### Network Layer

- **Nginx** - Reverse proxy and load balancer
- **Traefik** - HTTPS/TLS termination with Let's Encrypt

---

## 🔒 Security

Security-related documentation:

- **[Security Policy](../SECURITY.md)** - Vulnerability reporting and policies
- **[API Security](../api/SECURITY.md)** - Authentication, rate limiting, validation
- **[Production Deployment](production-deployment.md)** - Secure deployment checklist
- **[Docker Socket Security](docker-socket-security.md)** - Docker socket proxy setup

---

## 📊 Monitoring & Operations

Operational guides:

- **[Production Deployment](production-deployment.md)** - Complete production setup
- **[Backup Strategy](backup-strategy.md)** - Data backup and recovery
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Performance Tuning](performance-tuning.md)** - Optimization guides

---

## 🤖 AI & Automation

AI-powered development tools:

- **[AI Agent Development](../AGENT.md)** - GitHub Copilot integration and best practices
- **[Copilot Instructions](../.github/copilot-instructions.md)** - Coding standards for AI

---

## 📚 Reference

### Configuration Files

- **[pyproject.toml](../pyproject.toml)** - Python dependencies and tool configuration
- **[docker-compose.yml](../docker-compose.yml)** - Service orchestration
- **[.env.example](../.env.example)** - Environment variables template
- **[Traefik Config](.config/traefik/traefik.yml)** - Reverse proxy configuration

### Project Management

- **[TODO](../.github/TODO.md)** - Current tasks and roadmap (v4.0+)
- **[Archived TODOs](../.github/archive/)** - Completed version milestones
- **[Changelog](../CHANGELOG.md)** - Version history and changes

### Community

- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute
- **[Code of Conduct](../CODE_OF_CONDUCT.md)** - Community guidelines
- **[License](../LICENSE)** - Project license (MIT)

---

## 🔍 Quick Reference

### Common Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run tests
pytest

# Build documentation
bash scripts/bash/docs/build-docs.sh

# Security scan
pwsh scripts/powershell/audit/security-scan.ps1
```

### Important URLs

- **Dashboard:** http://localhost:3000
- **API:** http://localhost:3001
- **Grafana:** http://localhost:3000 (Grafana service)
- **Jupyter:** http://localhost:8888
- **Traefik Dashboard:** http://localhost:8080

### Support Channels

- **GitHub Issues:** [Create an issue](https://github.com/your-org/docker_dotfiles/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/docker_dotfiles/discussions)
- **Security:** security@your-domain.com

---

## 📖 Documentation Standards

### File Organization

```
docs/
├── INDEX.md (this file)
├── production-deployment.md
├── docker-socket-security.md
├── troubleshooting.md
└── python-setup-troubleshooting.md

.github/
├── TODO.md
├── copilot-instructions.md
└── archive/
    ├── TODO-v3.1-20251025.md
    └── CLEANUP-REPORT-v3.1-20251025.md

web-content/
├── README.md
├── ARCHITECTURE.md
├── INSTALL.md
└── QUICKSTART.md

api/
├── README.md
└── SECURITY.md

scripts/
├── README.md
├── python/README.md
├── powershell/README.md
└── bash/README.md
```

### Writing Style

- **Concise:** Get to the point quickly
- **Actionable:** Provide clear next steps
- **Searchable:** Use descriptive headers
- **Up-to-date:** Include last updated date
- **Examples:** Show, don't just tell

---

## 🚦 Status Legend

| Icon | Status | Description |
|------|--------|-------------|
| 🟢 | Complete | Fully implemented and documented |
| 🔵 | In Progress | Currently being worked on |
| 🟡 | Planned | Scheduled for future implementation |
| 🔴 | Blocked | Waiting on dependencies |
| ⚪ | Optional | Nice-to-have, not critical |

---

## 📅 Documentation Roadmap

### v4.0 (Current)

- [x] Comprehensive testing documentation
- [x] Security hardening guides
- [x] API security documentation
- [x] Production deployment guide
- [x] Centralized documentation index
- [ ] MkDocs static site
- [ ] Interactive tutorials

### v4.1 (Planned)

- [ ] Video tutorials
- [ ] Interactive API playground
- [ ] Architecture diagrams (Mermaid.js)
- [ ] Performance benchmarks
- [ ] Multi-language support

---

**Need help?** Start with the [Troubleshooting Guide](troubleshooting.md) or create an [issue](https://github.com/your-org/docker_dotfiles/issues).

**Last Updated:** 2025-10-26 | **Maintained by:** Cluster Dashboard Team
