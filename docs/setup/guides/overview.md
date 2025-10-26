---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["setup", "installation", "overview", "quickstart"]
description: "Project setup and installation overview"
---
# Setup Overview

Complete setup guide for Modern Data Platform local development environment.

## Prerequisites

- Docker 24.0+ with Docker Compose v2
- Python 3.14+ (via UV package manager)
- Node.js 22+ LTS
- Git 2.40+
- 8GB RAM minimum, 16GB recommended
- 20GB free disk space

## Quick Start (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/DeanLuus22021994/docker_dotfiles.git
cd docker_dotfiles

# 2. Copy environment file
cp .env.example .env

# 3. Start services
docker-compose up -d

# 4. Verify services
docker-compose ps
```

## Setup Steps

1. **Prerequisites** - Install required software
2. **Clone Repository** - Get project code
3. **Environment Configuration** - Set up .env file
4. **Python Setup** - Configure Python environment
5. **Docker Setup** - Start container stack
6. **Verification** - Confirm all services running

See `guides/` subdocs for detailed step-by-step instructions.
