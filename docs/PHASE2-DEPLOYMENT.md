# Phase 2 Deployment Guide

## Overview

Phase 2 implements production-grade security, resource management, and observability across the entire Docker Compose stack.

## ✅ What Was Implemented

### 1. Docker Secrets (Security Layer)
- **9 secret files** created with placeholder values
- **2 example files** for documentation
- **secrets/.gitignore** prevents accidental commits
- **secrets/README.md** with comprehensive setup instructions

### 2. Resource Limits (Stability Layer)
All 20 services now have CPU and memory limits:

| Service Category | CPU Limit | Memory Limit | Reservation |
|-----------------|-----------|--------------|-------------|
| PostgreSQL      | 4 CPUs    | 4GB          | 2 CPU / 2GB |
| MariaDB         | 4 CPUs    | 4GB          | 2 CPU / 2GB |
| Jupyter         | 8 CPUs    | 8GB          | 4 CPU / 4GB |
| Redis           | 2 CPUs    | 2GB          | 1 CPU / 1GB |
| MinIO           | 2 CPUs    | 2GB          | 1 CPU / 1GB |
| Prometheus      | 2 CPUs    | 2GB          | 1 CPU / 1GB |
| Grafana         | 2 CPUs    | 1GB          | 1 CPU / 512MB |
| BuildKit        | 4 CPUs    | 4GB          | 2 CPU / 2GB |
| LocalStack      | 2 CPUs    | 2GB          | 1 CPU / 1GB |
| Web servers (×3)| 0.5 CPU   | 128MB        | 0.25 CPU / 64MB |
| Load balancer   | 1 CPU     | 256MB        | 0.5 CPU / 128MB |
| Dashboard       | 1 CPU     | 256MB        | 0.5 CPU / 128MB |

**Total Allocation:**
- **Max CPUs:** ~35 CPUs (with limits)
- **Max RAM:** ~30GB (with limits)
- **Min CPUs:** ~20 CPUs (reservations)
- **Min RAM:** ~18GB (reservations)

### 3. Logging Configuration (Observability Layer)
- **Driver:** json-file (structured logging)
- **Max size:** 10MB per log file
- **Rotation:** 3 files (30MB total per service)
- **Total cap:** 600MB (20 services × 30MB)

## 🚀 Deployment Steps

### Step 1: Generate Secure Passwords

**For Development (Quick Start):**
```powershell
# Use provided placeholder values
# Secrets are already created with 'changeme_secure_*' values
# Good enough for local testing
```

**For Production (Recommended):**
```powershell
# Generate random 32-character passwords
function New-SecurePassword {
    param([int]$Length = 32)
    -join ((65..90) + (97..122) + (48..57) + (33,35,37,38,42,43,45,61,63,64) | Get-Random -Count $Length | ForEach-Object {[char]$_})
}

# Generate and save passwords
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\postgres_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\mariadb_root_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\mariadb_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\redis_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\minio_root_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\grafana_admin_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\jupyter_token.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\pgadmin_password.txt
"minioadmin" | Out-File -Encoding ASCII -NoNewline secrets\minio_root_user.txt

# IMPORTANT: Save passwords to password manager!
Write-Host "`n⚠️  SAVE THESE PASSWORDS TO YOUR PASSWORD MANAGER:" -ForegroundColor Yellow
Get-Content secrets\postgres_password.txt | Write-Host "PostgreSQL: " -NoNewline; $_
Get-Content secrets\mariadb_root_password.txt | Write-Host "MariaDB Root: " -NoNewline; $_
Get-Content secrets\grafana_admin_password.txt | Write-Host "Grafana Admin: " -NoNewline; $_
```

### Step 2: Validate Configuration

```powershell
# Validate docker-compose.yml syntax
docker-compose config > $null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ docker-compose.yml is valid" -ForegroundColor Green
} else {
    Write-Host "✗ docker-compose.yml has errors" -ForegroundColor Red
    exit 1
}

# Verify all secret files exist
$required_secrets = @(
    "postgres_password.txt",
    "mariadb_root_password.txt",
    "mariadb_password.txt",
    "redis_password.txt",
    "minio_root_user.txt",
    "minio_root_password.txt",
    "grafana_admin_password.txt",
    "jupyter_token.txt",
    "pgadmin_password.txt"
)

$missing = @()
foreach ($secret in $required_secrets) {
    if (-not (Test-Path "secrets\$secret")) {
        $missing += $secret
    }
}

if ($missing.Count -eq 0) {
    Write-Host "✓ All 9 secret files found" -ForegroundColor Green
} else {
    Write-Host "✗ Missing secret files:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}
```

### Step 3: Restart Stack with New Configuration

```powershell
# Stop all services
Write-Host "`n1. Stopping current stack..." -ForegroundColor Cyan
docker-compose down

# Remove old containers (optional, if secrets were changed)
Write-Host "`n2. Removing old containers..." -ForegroundColor Cyan
docker-compose rm -f

# Pull latest images (optional)
Write-Host "`n3. Pulling latest images..." -ForegroundColor Cyan
docker-compose pull

# Start with new configuration
Write-Host "`n4. Starting stack with new configuration..." -ForegroundColor Cyan
docker-compose up -d

# Wait for services to initialize
Write-Host "`n5. Waiting for services to initialize (60s)..." -ForegroundColor Cyan
Start-Sleep -Seconds 60

# Check service health
Write-Host "`n6. Checking service health..." -ForegroundColor Cyan
docker-compose ps
```

### Step 4: Verify Secrets Mounting

```powershell
# Test secret mounting in PostgreSQL
Write-Host "`n7. Verifying secrets mounting..." -ForegroundColor Cyan

# Check if secret files exist in containers
docker exec cluster-postgres ls -la /run/secrets/ 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PostgreSQL secrets mounted" -ForegroundColor Green
}

docker exec cluster-mariadb ls -la /run/secrets/ 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ MariaDB secrets mounted" -ForegroundColor Green
}

docker exec cluster-grafana ls -la /run/secrets/ 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Grafana secrets mounted" -ForegroundColor Green
}

# DEVELOPMENT ONLY: Read secret values (DO NOT DO IN PRODUCTION!)
if ($env:ENVIRONMENT -eq "development") {
    Write-Host "`n⚠️  Development Mode - Reading secrets:" -ForegroundColor Yellow
    docker exec cluster-postgres cat /run/secrets/postgres_password
}
```

### Step 5: Monitor Resource Usage

```powershell
# Check resource usage with limits
Write-Host "`n8. Monitoring resource usage..." -ForegroundColor Cyan
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Check if any containers are being OOM killed
docker ps -a --filter "status=exited" --format "{{.Names}}: {{.Status}}"
```

### Step 6: Verify Logging Configuration

```powershell
# Check log file sizes
Write-Host "`n9. Verifying logging configuration..." -ForegroundColor Cyan
docker inspect cluster-postgres | ConvertFrom-Json | Select-Object -ExpandProperty HostConfig | Select-Object -ExpandProperty LogConfig

# Check actual log files (Linux/WSL only)
# docker exec cluster-postgres ls -lh /var/lib/docker/containers/*/
```

## 🔍 Verification Checklist

- [ ] All 19 services running (`docker-compose ps`)
- [ ] All health checks passing (status shows "healthy")
- [ ] Secrets mounted at `/run/secrets/` in containers
- [ ] Resource limits applied (check `docker stats`)
- [ ] Logging configuration active (check `docker inspect`)
- [ ] No hardcoded passwords in `docker-compose.yml`
- [ ] Secrets directory has `.gitignore` (prevents commits)
- [ ] All 9 secret files exist with secure values

## 🚨 Troubleshooting

### Issue: Service won't start after secrets change
**Solution:**
```powershell
# Remove container and volume
docker-compose down -v
docker-compose up -d
```

### Issue: Permission denied reading secrets
**Solution:**
```powershell
# Ensure secret files have correct permissions (Linux/Mac)
chmod 600 secrets/*.txt

# On Windows, secrets are read-only by default
```

### Issue: Container OOM killed
**Solution:**
```powershell
# Check which service exceeded memory limit
docker ps -a --filter "status=exited"

# Increase memory limit in docker-compose.yml
# Or reduce service workload
```

### Issue: Health check failing
**Solution:**
```powershell
# Check logs for specific service
docker-compose logs cluster-postgres --tail=50

# Verify service is listening
docker exec cluster-postgres netstat -tlnp

# Increase start_period if service needs more time
```

## 📊 Monitoring Commands

### View all service statuses
```powershell
docker-compose ps
```

### View resource usage
```powershell
docker stats --no-stream
```

### View logs (last 100 lines)
```powershell
docker-compose logs --tail=100 -f
```

### View specific service logs
```powershell
docker-compose logs cluster-postgres --tail=50 -f
```

### Check secret files in container
```powershell
docker exec cluster-postgres ls -la /run/secrets/
```

### Read secret value (DEVELOPMENT ONLY!)
```powershell
docker exec cluster-postgres cat /run/secrets/postgres_password
```

## 🔐 Security Best Practices

1. **Never commit secret values to git**
   - `.gitignore` is configured to prevent this
   - Only example files are committed

2. **Use strong passwords in production**
   - Minimum 32 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Use password generator function provided

3. **Rotate passwords regularly**
   - Every 90 days recommended
   - Update secret files and restart services

4. **Backup secrets securely**
   - Store in password manager (1Password, LastPass, Bitwarden)
   - Encrypt backups
   - Never store in plain text files

5. **Monitor secret access**
   - Check logs for authentication failures
   - Alert on repeated failed login attempts

## 📚 References

- [Docker Secrets Documentation](https://docs.docker.com/engine/swarm/secrets/)
- [Docker Compose Resources](https://docs.docker.com/compose/compose-file/deploy/#resources)
- [Docker Logging Drivers](https://docs.docker.com/config/containers/logging/json-file/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## 🎯 Success Criteria

Phase 2 is successfully deployed when:

- ✅ All 19 services running with healthy status
- ✅ Zero hardcoded passwords in docker-compose.yml
- ✅ All services using Docker secrets
- ✅ Resource limits enforced (check docker stats)
- ✅ Logging configured with rotation
- ✅ Maximum 600MB total log storage
- ✅ Services respect CPU/memory reservations
- ✅ No secrets committed to git

## 🔄 Next Steps

After successful Phase 2 deployment:

1. **Phase 3: Real Data Integration**
   - Replace simulated metrics with Docker Engine API
   - Enable Prometheus exporters (cAdvisor, postgres-exporter, etc.)
   - Configure Grafana dashboards

2. **Phase 4: Monitoring & Alerting**
   - Set up Prometheus alerting rules
   - Configure notification channels
   - Create Grafana dashboard provisioning

3. **Phase 5: Testing & CI/CD**
   - Write unit/integration tests
   - Set up GitHub Actions workflows
   - Implement automated deployments
