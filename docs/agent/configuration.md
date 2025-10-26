---
date_created: "2025-10-26T18:32:25.936902+00:00"
last_updated: "2025-10-26T18:32:25.936902+00:00"
tags: ["documentation", "agent", "development"]
description: "Documentation for configuration"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- configuration
- architecture
  description: Configuration management structure and organization guidelines
  ---\n# Configuration Management

## Structure

```
.config/
├── nginx/          # Web server configs
├── database/       # Database server configs
├── services/       # Service-specific configs
├── docker/         # Docker daemon configs
├── github/         # GitHub Actions workflows
└── monitoring/     # Prometheus, Grafana configs
```

## Rules

1. **All configs in `.config/`** - No scattered configs
2. **Native formats** - Preserve .conf, .json, .sh (not YAML conversion)
3. **Read-only mounts** - Configs mounted with `:ro` flag
4. **Validated before use** - Run validation scripts before deployment

## Config Locations

| Type       | Path                  | Purpose                                    |
| ---------- | --------------------- | ------------------------------------------ |
| Nginx      | `.config/nginx/`      | loadbalancer.conf, main.conf, default.conf |
| Database   | `.config/database/`   | postgresql.conf, mariadb.conf              |
| Services   | `.config/services/`   | pgadmin-servers.json, localstack-init.sh   |
| Docker     | `.config/docker/`     | buildkitd.toml, daemon.json                |
| Monitoring | `.config/monitoring/` | prometheus.yml, grafana/                   |

See [environment variables guide](environment.md) for credentials.
