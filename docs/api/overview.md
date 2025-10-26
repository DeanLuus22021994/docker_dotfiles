---
date_created: "2025-10-26T18:32:25.941921+00:00"
last_updated: "2025-10-26T18:32:25.941921+00:00"
tags: ["documentation", "api", "reference"]
description: "Documentation for overview"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:

- api
- overview
- documentation
  description: Documentation for overview in api
  ---\n# Docker API Proxy

Secure HTTP API for accessing Docker Engine metrics and container health information.

## Features

- **Container Listing**: Get all containers with health status
- **Real-time Stats**: CPU, memory, network, and disk I/O metrics
- **System Info**: Docker version, host information, resource totals
- **Aggregated Stats**: Cluster-wide resource usage summary
- **Health Checks**: Built-in health endpoint for monitoring

## API Endpoints

### Health Check

```
GET /health
```

Returns server health status.

### Container List

```
GET /api/containers
```

Returns all containers with health status and basic info.

### Container Stats

```
GET /api/containers/:id/stats
```

Returns real-time stats for a specific container.

### System Info

```
GET /api/system/info
```

Returns Docker system information and host details.

### System Version

```
GET /api/system/version
```

Returns Docker Engine version information.

### Aggregate Stats

```
GET /api/stats/aggregate
```

Returns aggregated stats across all running containers.

## Development

```bash
npm install
npm run dev
```

## Production

```bash
npm ci --only=production
npm start
```

## Docker

```bash
docker build -t docker-api-proxy .
docker run -p 3001:3001 -v /var/run/docker.sock:/var/run/docker.sock docker-api-proxy
```

## Security Considerations

- Mount Docker socket read-only in production
- Use environment variables for configuration
- Enable rate limiting for API endpoints
- Implement authentication for production use
- Run as non-root user (nodejs)

## Environment Variables

| Variable | Default    | Description      |
| -------- | ---------- | ---------------- |
| PORT     | 3001       | Server port      |
| NODE_ENV | production | Environment mode |

## Response Examples

### Container Stats

```json
{
  "container": "abc123",
  "timestamp": "2025-10-25T10:30:00.000Z",
  "cpu": {
    "percent": "2.50",
    "usage": 1234567890,
    "system": 9876543210
  },
  "memory": {
    "usage": 134217728,
    "limit": 536870912,
    "percent": "25.00"
  },
  "network": {
    "rx_bytes": 1024000,
    "tx_bytes": 512000
  }
}
```

### Aggregate Stats

```json
{
  "timestamp": "2025-10-25T10:30:00.000Z",
  "total_containers": 20,
  "total_cpu_percent": "45.80",
  "total_memory_bytes": 8589934592,
  "containers": [...]
}
```

## License

MIT
