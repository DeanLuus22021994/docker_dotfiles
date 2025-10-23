# Custom Dockerfiles for Swarm Stack

This directory contains optimized Dockerfiles for the swarm-stack Docker Compose setup. These custom Dockerfiles provide Docker Swarm-specific optimizations with resource constraints, placement strategies, and orchestration-aware configurations.

## Benefits

### 🚀 **Swarm-Optimized Performance**

- **Resource-aware builds** with memory and CPU constraints
- **Manager placement** for critical services (PostgreSQL)
- **Overlay network optimization** for service discovery
- **Health checks tuned** for Swarm orchestration

### 🔒 **Security Enhancements**

- **Non-root users** for all services
- **Minimal attack surfaces** with essential packages only
- **Swarm-aware security** with service isolation
- **Resource limits** preventing resource exhaustion

### 📦 **Orchestration Features**

- **Swarm deployment constraints** and placement rules
- **Rolling updates** with health check integration
- **Service scaling** with resource reservations
- **Failure recovery** with restart policies

### 🏥 **Reliability Improvements**

- **Swarm-aware health checks** with appropriate intervals
- **Resource monitoring** and limits enforcement
- **Graceful shutdown** handling for Swarm
- **Persistent volumes** optimized for Swarm

## Services

### Node.js Service (`node.Dockerfile`)

- **Base image**: Node.js 20 Alpine
- **Multi-stage build**: base → deps → dev-deps → builder → runner
- **Swarm optimizations**:
  - Resource limits: 1G memory, 256M reservation
  - Health checks: 30s interval for Swarm efficiency
  - Non-root user execution
  - Production-ready configuration

### Python Service (`python.Dockerfile`)

- **Base image**: Python 3.14 slim
- **Multi-stage build**: base → deps → runner
- **Swarm optimizations**:
  - Resource limits: 512M memory, 128M reservation
  - Conservative health checks for resource constraints
  - Virtual environment isolation
  - Non-root user execution

### PostgreSQL Database (`postgres.Dockerfile`)

- **Base image**: PostgreSQL 13 Alpine
- **Swarm optimizations**:
  - Manager node placement constraint
  - Resource limits: 1G memory, 1 CPU, 512M/0.5 CPU reservations
  - Lightweight configuration for constrained resources
  - Performance monitoring with pg_stat_statements

## Architecture

```text
Docker Swarm Cluster
├── Manager Node
│   └── PostgreSQL (constrained placement)
├── Worker Nodes
│   ├── Node.js Service (replicated)
│   └── Python Service (replicated)
└── Overlay Network (swarm-network)
```

## Usage

### Swarm Deployment

```bash
# Initialize Swarm (if not already done)
docker swarm init

# Build custom images
docker-compose build

# Deploy to Swarm
docker stack deploy -c docker-compose.yml react-scuba

# Check service status
docker stack services react-scuba

# Scale services
docker service scale react-scuba_node=3
docker service scale react-scuba_python=2
```

### Local Development

```bash
# Run locally with Swarm-like constraints
docker-compose up

# Or run in background
docker-compose up -d
```

## Swarm-Specific Features

### Placement Constraints

- **PostgreSQL**: Runs only on manager nodes for data safety
- **Application services**: Can run on any available nodes
- **Resource reservations**: Ensure minimum resources available

### Resource Management

- **Memory limits**: Prevent memory exhaustion
- **CPU limits**: Fair CPU sharing across services
- **Reservations**: Guaranteed minimum resources
- **Monitoring**: Built-in resource tracking

### Health Checks & Recovery

- **Swarm-aware intervals**: Less frequent checks for orchestration efficiency
- **Automatic restarts**: Failed containers restart automatically
- **Rolling updates**: Zero-downtime updates with health checks
- **Service discovery**: Automatic service registration

## Configuration

### Resource Limits

```yaml
# Node.js service limits
limits:
  memory: 1G
reservations:
  memory: 256M

# Python service limits
limits:
  memory: 512M
reservations:
  memory: 128M

# PostgreSQL limits (manager only)
limits:
  memory: 1G
  cpus: "1.0"
reservations:
  memory: 512M
  cpus: "0.5"
```

### PostgreSQL Configuration

Custom configuration in `postgresql.conf` includes:

- Resource-constrained memory settings
- Lightweight performance monitoring
- Swarm-optimized connection limits
- Conservative autovacuum settings

### Environment Variables

All environment variables remain the same as the original configuration.

## Scaling & Management

### Horizontal Scaling

```bash
# Scale Node.js service
docker service scale react-scuba_node=5

# Scale Python service
docker service scale react-scuba_python=3

# Check scaling status
docker stack services react-scuba
```

### Rolling Updates

```bash
# Update with zero downtime
docker stack deploy -c docker-compose.yml react-scuba

# Monitor update progress
docker stack services react-scuba
```

### Resource Monitoring

```bash
# Check resource usage
docker stats

# Service-specific stats
docker service ps react-scuba_node

# Swarm node status
docker node ls
```

## Troubleshooting

### Swarm Issues

- Verify Swarm mode: `docker info | grep Swarm`
- Check node status: `docker node ls`
- Service logs: `docker service logs react-scuba_node`

### Resource Issues

- Check resource limits: `docker service inspect react-scuba_node`
- Monitor usage: `docker stats`
- Adjust limits in docker-compose.yml if needed

### Placement Issues

- Check manager constraints: `docker node inspect self`
- Verify placement: `docker service ps react-scuba_db`
- Update constraints if manager unavailable

### Network Issues

- Check overlay network: `docker network ls`
- Service discovery: `docker service inspect react-scuba_node`
- DNS resolution: Check service names in docker-compose.yml

## Migration from Default Images

The custom Dockerfiles are drop-in replacements for the default images. The Swarm stack provides enhanced orchestration capabilities and resource management compared to basic Docker Compose deployments.
