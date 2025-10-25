# Docker Secrets Directory

This directory contains sensitive credentials for the Docker Compose stack using Docker Secrets.

## 🔒 Security Notice

**NEVER commit actual secret values to git!** The `.gitignore` file is configured to exclude all files except examples and documentation.

## 📁 Required Secret Files

Create these files with your secure passwords (minimum 16 characters recommended):

```bash
# PostgreSQL
secrets/postgres_password.txt

# MariaDB
secrets/mariadb_root_password.txt
secrets/mariadb_password.txt

# Redis
secrets/redis_password.txt

# MinIO
secrets/minio_root_user.txt
secrets/minio_root_password.txt

# Grafana
secrets/grafana_admin_password.txt

# Jupyter
secrets/jupyter_token.txt

# pgAdmin
secrets/pgadmin_password.txt
```

## 🚀 Quick Setup

### Development (Quick Start)
```powershell
# Copy examples to create actual secrets (placeholder values)
"changeme_secure_password_here" | Out-File -Encoding ASCII -NoNewline secrets\postgres_password.txt
"changeme_secure_password_here" | Out-File -Encoding ASCII -NoNewline secrets\mariadb_root_password.txt
"changeme_secure_password_here" | Out-File -Encoding ASCII -NoNewline secrets\mariadb_password.txt
"changeme_secure_password_here" | Out-File -Encoding ASCII -NoNewline secrets\redis_password.txt
"changeme_secure_password_here" | Out-File -Encoding ASCII -NoNewline secrets\minio_root_password.txt
"changeme_secure_password_here" | Out-File -Encoding ASCII -NoNewline secrets\grafana_admin_password.txt
"changeme_secure_token_here" | Out-File -Encoding ASCII -NoNewline secrets\jupyter_token.txt
"changeme_secure_password_here" | Out-File -Encoding ASCII -NoNewline secrets\pgadmin_password.txt
"minioadmin" | Out-File -Encoding ASCII -NoNewline secrets\minio_root_user.txt
```


### Production (Secure Generation)
```powershell
# Generate random secure passwords (PowerShell 5.1+)
function New-SecurePassword {
    param([int]$Length = 32)
    -join ((65..90) + (97..122) + (48..57) + (33,35,37,38,42,43,45,61,63,64) | Get-Random -Count $Length | ForEach-Object {[char]$_})
}

# Create secrets with random passwords
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\postgres_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\mariadb_root_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\mariadb_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\redis_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\minio_root_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\grafana_admin_password.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\jupyter_token.txt
New-SecurePassword | Out-File -Encoding ASCII -NoNewline secrets\pgadmin_password.txt

# MinIO username (no special characters)
"minioadmin" | Out-File -Encoding ASCII -NoNewline secrets\minio_root_user.txt
```

## 🔄 How Docker Secrets Work

Docker Secrets are mounted as files at `/run/secrets/<secret_name>` inside containers:

```yaml
secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt

services:
  cluster-postgres:
    secrets:
      - postgres_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
```

## ⚠️ Important Notes

1. **File Format**: Secrets must be plain text files with NO newlines (use `-NoNewline` in PowerShell)
2. **Permissions**: On Linux/Mac, set `chmod 600 secrets/*.txt` to restrict access
3. **Backup**: Store production secrets in a secure password manager (1Password, LastPass, Bitwarden)
4. **Rotation**: Change production passwords every 90 days
5. **Never Log**: Ensure applications never log secret values

## 🧪 Testing Secrets

Verify secrets are properly mounted:
```powershell
# Check if secret file exists in container
docker exec cluster-postgres ls -la /run/secrets/

# Read secret value (development only!)
docker exec cluster-postgres cat /run/secrets/postgres_password
```

## 📚 References

- [Docker Secrets Documentation](https://docs.docker.com/engine/swarm/secrets/)
- [Docker Compose Secrets](https://docs.docker.com/compose/use-secrets/)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
