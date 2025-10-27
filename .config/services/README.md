---
date_created: '2025-10-27T02:35:56Z'
last_updated: '2025-10-27T02:35:56Z'
tags: [services, pgadmin, localstack, configuration]
description: 'Service-specific configuration files'
---

# Services Configuration

Individual service configuration files.

## 📁 Files

### `pgadmin-servers.json`
**pgAdmin server connection definitions**.

**Servers Configured**:
1. **PostgreSQL Cluster**
   - Host: `cluster-postgres`
   - Port: 5432
   - Database: `clusterdb`
   - User: `cluster_user`
   - Network: `cluster-data`

2. **MariaDB Cluster** (MySQL protocol)
   - Host: `cluster-mariadb`
   - Port: 3306
   - Database: `clusterdb`
   - User: `cluster_user`
   - Network: `cluster-data`

**Usage**: Auto-imported when pgAdmin starts.

---

### `localstack-init.sh`
**LocalStack initialization script**.

Configures AWS services on startup:
- S3 buckets
- DynamoDB tables
- SQS queues
- SNS topics
- Lambda functions
- API Gateway endpoints

---

## �� Quick Start

### pgAdmin Access

```powershell
# Open pgAdmin
Start-Process http://localhost:5050

# Default credentials
# Email: admin@example.com
# Password: See .secrets/pgadmin_password.txt
```

### LocalStack Services

```powershell
# Check LocalStack health
curl http://localhost:4566/_localstack/health

# List S3 buckets
aws --endpoint-url=http://localhost:4566 s3 ls

# Access LocalStack console
Start-Process http://localhost:4571
```

---

## 📚 References

- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [LocalStack Documentation](https://docs.localstack.cloud/)
