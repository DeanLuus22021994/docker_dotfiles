---
date_created: "2025-10-26T18:32:25.949272+00:00"
last_updated: "2025-10-26T18:32:25.949272+00:00"
tags: ["documentation", "production", "deployment", "monitoring"]
description: "Documentation for monitoring"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- production
- monitoring
- health-checks
- alerts
  description: Production monitoring and health check configuration
  ---\n# Monitoring & Health Checks

## Service Health Endpoints

**API Server:**

```bash
curl https://your-domain.com/api/health
# Returns: {"status": "healthy", "uptime": 12345}
```

**Prometheus:**

```bash
curl https://prometheus.your-domain.com/-/healthy
# Returns: Prometheus is Healthy.
```

**Grafana:**

```bash
curl https://grafana.your-domain.com/api/health
# Returns: {"database": "ok", "version": "10.0.0"}
```

## Monitoring Stack

**Prometheus** - Metrics collection
**Grafana** - Visualization and dashboards
**Node Exporter** - Host metrics
**cAdvisor** - Container metrics

## Key Metrics to Monitor

- API response time (p95, p99)
- API error rate (%)
- Container CPU/memory usage
- Database connections
- Disk space usage
- Certificate expiration (Let's Encrypt)

## Alerting

Configure Grafana alerts for:

- API downtime (>1 minute)
- High error rate (>5%)
- High CPU usage (>80%)
- Low disk space (<10%)
- Certificate expiring (<30 days)

**Alert destinations:** Email, Slack, PagerDuty

## Log Aggregation

```bash
# View all logs
docker-compose logs -f

# Filter by service
docker-compose logs -f api nginx

# Export logs
docker-compose logs > production.log
```
