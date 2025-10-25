# Grafana Configuration

Automated provisioning for Grafana dashboards and datasources.

## Structure

```
grafana/
├── README.md
└── provisioning/
    ├── dashboards/
    │   └── dashboards.yml      # Dashboard provider config
    └── datasources/
        └── prometheus.yml       # Prometheus datasource
```

## Provisioning

All configurations auto-load on Grafana startup via volume mounts in `docker-compose.yml`:

```yaml
volumes:
  - ./.config/monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
  - ./.config/monitoring/dashboards:/etc/grafana/dashboards:ro
```

## Quick Start

1. **Start Grafana**: `docker-compose up -d cluster-grafana`
2. **Access**: http://localhost:3002
3. **Login**: admin / (check secrets/grafana_admin_password.txt)
4. **Dashboards**: Auto-loaded from `../dashboards/`

## Datasource

Prometheus auto-configured:
- **URL**: http://cluster-prometheus:9090
- **Access**: Proxy
- **Default**: Yes
- **Scrape interval**: 15s

## Dashboards

Four dashboards auto-provisioned:
- **Containers**: CPU, memory, network per container
- **Host**: System-level metrics
- **PostgreSQL**: Database performance
- **Redis**: Cache metrics

## Customization

Edit provisioning configs, restart Grafana:
```bash
docker-compose restart cluster-grafana
```
