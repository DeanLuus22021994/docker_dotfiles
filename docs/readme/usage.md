---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["usage", "commands", "makefile", "docker-compose"]
description: "Common commands and usage patterns for managing the cluster"
---

# Usage

## Makefile Commands

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

## Docker Compose Commands

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

See [service access](service-access.md) for endpoint URLs.
