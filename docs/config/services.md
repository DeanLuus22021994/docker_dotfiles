---
date_created: "2025-10-26T18:32:25.944469+00:00"
last_updated: "2025-10-26T18:32:25.944469+00:00"
tags: ['documentation', 'configuration', 'setup']
description: "Documentation for services"
---

---\ndate_created: '2025-10-26T00:00:00Z'
last_updated: '2025-10-26T00:00:00Z'
tags:
- docker-compose
- documentation
description: Documentation for services in config
---\n# Services Configuration

This directory contains configuration files for various service integrations.

## Files

### `pgadmin-servers.json`
**Purpose:** Pre-configured server connections for pgAdmin  
**Used by:** `cluster-pgadmin` service in docker-compose.yml  
**Mounts to:** `/pgadmin4/servers.json` in pgadmin container  
**Servers defined:**
- PostgreSQL Cluster (cluster-postgres:5432)
- MariaDB Cluster (cluster-mariadb:3306)

**Note:** Password authentication uses PassFile mounted separately.

### `localstack-init.sh`
**Purpose:** LocalStack initialization script for AWS service mocking  
**Used by:** `cluster-localstack` service (if enabled)  
**Creates:**
- S3 buckets: local-dev-bucket, local-test-bucket
- DynamoDB table: local-dev-table
- SQS queue: local-dev-queue
- SNS topic: local-dev-topic

**Requirements:**
- LocalStack must be running and healthy
- awslocal CLI available in container

## Usage

Configs are mounted in docker-compose.yml:
```yaml
volumes:
  - ./.config/services/pgadmin-servers.json:/pgadmin4/servers.json:ro
  - ./.config/services/localstack-init.sh:/docker-entrypoint-initaws.d/init.sh:ro
```

## Adding New Services

1. Create config file in this directory
2. Add volume mount in docker-compose.yml
3. Document in this README
4. Add validation in scripts/validate_configs.py

## Validation

Test JSON syntax:
```bash
python -m json.tool .config/services/pgadmin-servers.json
```

Test shell script syntax:
```bash
bash -n .config/services/localstack-init.sh
```
