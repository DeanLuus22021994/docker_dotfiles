---
date_created: '2025-10-27T02:35:55Z'
last_updated: '2025-10-27T02:35:55Z'
tags: [monitoring, prometheus, grafana, alertmanager, observability]
description: 'Observability stack configuration for Prometheus, Grafana, and Alertmanager'
---

# Monitoring & Observability Configuration

Production-grade monitoring stack with Prometheus, Grafana, Alertmanager, and exporters.

## 📁 Files Overview

### `prometheus.yml`
**Prometheus scrape configuration** - Defines all metric collection targets.

**Scrape Targets** (9 total):
1. Prometheus (self-monitoring, port 9090)
2. Grafana (port 3000)
3. cAdvisor (container metrics, port 8080)
4. PostgreSQL exporter (port 9187)
5. Redis exporter (port 9121)
6. Node exporter (host metrics, port 9100)

**Key Settings**:
- Scrape interval: 15s (default)
- Evaluation interval: 15s
- External labels: `cluster=docker-cluster`, `environment=development`

**Network**: All exporters on `cluster-observability`

---

### `alertmanager.yml`
**Alert routing and notification configuration**.

**Receivers**:
- `default` - Team email notifications
- `critical-alerts` - Oncall email (5m repeat interval)
- `warning-alerts` - Team email (1h repeat interval)

**SMTP**: Uses `cluster-mailhog:1025` for development

**Inhibition Rules**:
- Critical alerts suppress warnings for same alert
- HostDown suppresses container alerts

---

### `alerts/` Directory
**Prometheus alert rule definitions**.

Contains `.yml` files with alerting rules for:
- Service availability
- Resource utilization
- Performance degradation
- Database health

---

### `dashboards/` Directory
**Grafana dashboard JSON definitions**.

Pre-configured dashboards for:
- Cluster overview
- Container metrics (cAdvisor)
- Database performance (PostgreSQL, Redis)
- Host system metrics

---

### `grafana/` Directory
**Grafana provisioning configuration**.

Auto-configures:
- Data sources (Prometheus)
- Dashboards
- Notification channels
- Users and organizations

---

## 🚀 Quick Start

### Verify Prometheus Targets

```powershell
# Check Prometheus targets status
curl http://localhost:9090/api/v1/targets | ConvertFrom-Json

# View Prometheus config
docker exec cluster-prometheus cat /etc/prometheus/prometheus.yml
```

### Access Dashboards

```powershell
# Prometheus UI
Start-Process http://localhost:9090

# Grafana UI
Start-Process http://localhost:3002
# Default credentials: admin/admin

# Alertmanager UI
Start-Process http://localhost:9093
```

### Test Alerting

```powershell
# Trigger a test alert
curl -X POST http://localhost:9093/api/v1/alerts -d '[{\"labels\":{\"alertname\":\"TestAlert\",\"severity\":\"warning\"}}]' -H \"Content-Type: application/json\"

# Check MailHog for alert email
Start-Process http://localhost:8025
```

---

## 📊 Monitoring Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    cluster-observability                    │
│                     (172.20.3.0/24)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐       ┌──────────────┐                   │
│  │  Prometheus  │◄──────│   Grafana    │                   │
│  │   :9090      │       │    :3002     │                   │
│  └──────┬───────┘       └──────────────┘                   │
│         │                                                   │
│         │ Scrapes metrics from:                             │
│         ├─► cAdvisor (container metrics)                    │
│         ├─► PostgreSQL Exporter                             │
│         ├─► Redis Exporter                                  │
│         ├─► Node Exporter (host metrics)                    │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                           │
│  │ Alertmanager │──────► MailHog (SMTP)                     │
│  │   :9093      │         :1025                             │
│  └──────────────┘                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Best Practices

### Prometheus Configuration

✅ **Scrape intervals** - Balance data granularity with resource usage  
✅ **Retention period** - Default 15 days, increase for production  
✅ **Label management** - Use consistent labels (service, tier, environment)  
✅ **Query optimization** - Use recording rules for complex queries  

### Grafana Dashboards

✅ **Variable templates** - Use variables for dynamic filtering  
✅ **Alert annotations** - Show alerts on time-series charts  
✅ **Dashboard folders** - Organize by service/tier  
✅ **Permissions** - Restrict edit access in production  

### Alerting

✅ **Alert thresholds** - Tune to reduce false positives  
✅ **Notification channels** - Use Slack/Teams/PagerDuty in production  
✅ **Runbook links** - Include remediation steps in alerts  
✅ **Alert grouping** - Group related alerts to reduce noise  

---

## 📚 References

- [Prometheus Configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Alertmanager Configuration](https://prometheus.io/docs/alerting/latest/configuration/)
