---
date_created: '2025-10-27T02:35:56Z'
last_updated: '2025-10-27T02:35:56Z'
tags: [nginx, load-balancer, web-server, configuration]
description: 'NGINX configuration for load balancing and web servers'
---

# NGINX Configuration

NGINX configurations for load balancer and web servers in the cluster.

## 📁 Files

### `loadbalancer.conf`
**Load balancer configuration** - Round-robin distribution to 3 web servers.

**Upstream**: `web_backend`
- cluster-web1:80
- cluster-web2:80
- cluster-web3:80

**Features**:
- Round-robin load balancing (default)
- Proxy headers (X-Real-IP, X-Forwarded-For, X-Forwarded-Proto)
- Health check endpoint: `/health`
- Custom header: `X-Served-By: LoadBalancer`

**Networks**:
- `cluster-frontend` (port 8080)
- `cluster-backend` (upstream connections)

**Security**: Read-only root filesystem, no-new-privileges

---

### `default.conf`
**Default NGINX server configuration**.

Basic static file serving configuration.

---

### `main.conf`
**Main NGINX configuration**.

Global NGINX settings.

---

## 🚀 Quick Start

### Test Load Balancer

```powershell
# Test load balancer endpoint
curl http://localhost:8080

# Test health check
curl http://localhost:8080/health

# Verify round-robin (check X-Served-By header)
1..10 | ForEach-Object { curl -I http://localhost:8080 | Select-String \"X-Served-By\" }
```

### Reload Configuration

```powershell
# Test configuration syntax
docker exec loadbalancer nginx -t

# Reload configuration (zero-downtime)
docker exec loadbalancer nginx -s reload
```

---

## 🎯 Load Balancing Strategies

### Current: Round-Robin (Default)
Equal distribution across all backends.

### Alternative Strategies

**Least connections**:
```nginx
upstream web_backend {
    least_conn;
    server cluster-web1:80;
    server cluster-web2:80;
    server cluster-web3:80;
}
```

**IP hash** (session persistence):
```nginx
upstream web_backend {
    ip_hash;
    server cluster-web1:80;
    server cluster-web2:80;
    server cluster-web3:80;
}
```

**Weighted**:
```nginx
upstream web_backend {
    server cluster-web1:80 weight=3;
    server cluster-web2:80 weight=2;
    server cluster-web3:80 weight=1;
}
```

---

## 📚 References

- [NGINX Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [NGINX Proxy Module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
