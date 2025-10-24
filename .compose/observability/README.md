# Observability Stack

This directory contains the observability and monitoring infrastructure for Docker Compose, including Prometheus, Grafana, and Loki.

## Components

### Prometheus
- **Port**: 9090
- **Purpose**: Metrics collection and time-series database
- **URL**: http://localhost:9090

### Grafana
- **Port**: 3001
- **Purpose**: Metrics visualization and dashboards
- **URL**: http://localhost:3001
- **Default Credentials**: 
  - Username: `admin`
  - Password: Stored in `../../secrets/grafana_password.txt`

### Loki
- **Port**: 3100
- **Purpose**: Log aggregation system
- **URL**: http://localhost:3100

### Promtail
- **Purpose**: Log collector that ships logs to Loki
- **Scrapes**: All Docker container logs

### Node Exporter
- **Port**: 9100
- **Purpose**: Hardware and OS metrics

### cAdvisor
- **Port**: 8080
- **Purpose**: Container resource usage and performance metrics
- **URL**: http://localhost:8080

## Quick Start

### 1. Create Grafana Password Secret

```bash
# Create password file (replace with your secure password)
echo "your_secure_password_here" > ../../secrets/grafana_password.txt
```

### 2. Start the Observability Stack

```bash
# Start all services
docker compose -f .docker-compose/observability/docker-compose.yml up -d

# View logs
docker compose -f .docker-compose/observability/docker-compose.yml logs -f

# Check service status
docker compose -f .docker-compose/observability/docker-compose.yml ps
```

### 3. Access Services

- **Grafana**: http://localhost:3001
- **Prometheus**: http://localhost:9090
- **cAdvisor**: http://localhost:8080

## Grafana Setup

### First Login

1. Navigate to http://localhost:3001
2. Login with username `admin` and password from `secrets/grafana_password.txt`
3. Datasources are auto-configured (Prometheus and Loki)

### Exploring Metrics

1. Go to **Explore** in the left menu
2. Select **Prometheus** datasource
3. Try queries like:
   - `rate(container_cpu_usage_seconds_total[5m])` - CPU usage
   - `container_memory_usage_bytes` - Memory usage
   - `up` - Service availability

### Exploring Logs

1. Go to **Explore** in the left menu
2. Select **Loki** datasource
3. Filter logs by labels:
   - `{compose_project="basic-stack"}`
   - `{container="docker_python"}`
   - `{compose_service="python"} |= "error"`

## Pre-configured Dashboards

Dashboards will be available in the **Docker Compose** folder:

1. **Container Overview** - Resource usage across all containers
2. **Service Health** - Service availability and health checks
3. **Logs Dashboard** - Centralized log viewing

## Monitoring Your Services

### Expose Metrics from Your Applications

#### Python FastAPI Example

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI

app = FastAPI()

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

@app.middleware("http")
async def add_prometheus_middleware(request, call_next):
    request_count.inc()
    with request_duration.time():
        response = await call_next(request)
    return response
```

#### Node.js Express Example

```javascript
const promClient = require('prom-client');
const express = require('express');

const app = express();
const register = new promClient.Registry();

// Default metrics
promClient.collectDefaultMetrics({ register });

// Expose metrics
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

## Common Queries

### Prometheus Queries

```promql
# CPU usage by container
sum(rate(container_cpu_usage_seconds_total[5m])) by (container)

# Memory usage by container
container_memory_usage_bytes{container!=""}

# Network I/O
rate(container_network_receive_bytes_total[5m])
rate(container_network_transmit_bytes_total[5m])

# Disk I/O
rate(container_fs_reads_bytes_total[5m])
rate(container_fs_writes_bytes_total[5m])

# Service availability
up{job="python-app"}
```

### Loki Queries (LogQL)

```logql
# All logs from a service
{compose_service="python"}

# Error logs only
{compose_service="python"} |= "ERROR"

# Logs matching pattern
{container="docker_db"} |~ "connection.*failed"

# Count errors per minute
sum(count_over_time({compose_service="python"} |= "ERROR" [1m])) by (container)
```

## Configuration

### Retention Policies

**Prometheus**: 15 days (default)
- Configured in `docker-compose.yml` via `--storage.tsdb.retention.time`

**Loki**: 31 days
- Configured in `config/loki-config.yml` under `limits_config.retention_period`

### Scrape Intervals

**Prometheus**: 15 seconds
- Configured in `config/prometheus.yml` under `global.scrape_interval`

### Resource Limits

To add resource limits:

```yaml
services:
  prometheus:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker compose -f .docker-compose/observability/docker-compose.yml logs

# Verify secret file exists
ls -la ../../secrets/grafana_password.txt

# Check permissions
docker compose -f .docker-compose/observability/docker-compose.yml ps
```

### Can't Access Grafana

```bash
# Check if port 3001 is already in use
lsof -i :3001

# Verify Grafana is running
docker ps | grep grafana

# Check Grafana logs
docker logs docker_grafana
```

### No Metrics Appearing

```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Verify services are exposing metrics
curl http://localhost:8000/metrics  # Python app
curl http://localhost:3000/metrics  # Node app
```

### No Logs in Loki

```bash
# Check Promtail is running
docker ps | grep promtail

# Check Promtail logs
docker logs docker_promtail

# Verify Loki is ready
curl http://localhost:3100/ready
```

## Cleanup

```bash
# Stop services
docker compose -f .docker-compose/observability/docker-compose.yml down

# Remove volumes (deletes all metrics and logs)
docker compose -f .docker-compose/observability/docker-compose.yml down -v
```

## Integration with Main Stack

To monitor your main application stacks, ensure they're on a network that can reach the observability stack, or use Docker DNS for service discovery.

Example: Add observability network to basic-stack:

```yaml
networks:
  observability:
    external: true
    name: docker_observability
```

Then attach services to both networks:

```yaml
services:
  python:
    networks:
      - basic-stack-network
      - observability
```

## Security Considerations

1. **Change default Grafana password** immediately after first login
2. **Use strong passwords** in `secrets/grafana_password.txt`
3. **Don't expose ports** to the internet in production
4. **Use reverse proxy** with SSL/TLS in production
5. **Regularly update** container images
6. **Set resource limits** to prevent resource exhaustion

## Further Reading

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [cAdvisor GitHub](https://github.com/google/cadvisor)
