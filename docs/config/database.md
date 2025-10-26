---
date_created: "2025-10-26T00:00:00Z"
last_updated: "2025-10-26T00:00:00Z"
tags: ["config", "database", "documentation"]
description: "Documentation for database in config"
---
# Database Configuration

This directory contains database server configurations for PostgreSQL and MariaDB.

## Files

### `postgresql.conf`
**Purpose:** PostgreSQL server configuration optimized for cluster workloads  
**Used by:** `cluster-postgres` service in docker-compose.yml  
**Mounts to:** `/etc/postgresql/postgresql.conf` in postgres container  
**Key settings:**
- Max connections: 200
- Shared buffers: 256MB
- Logging: DDL statements, slow queries >1s
- Performance monitoring: pg_stat_statements enabled
- Replication: Prepared for HA with WAL settings

### `mariadb.conf`
**Purpose:** MariaDB server configuration with InnoDB optimizations  
**Used by:** `cluster-mariadb` service in docker-compose.yml  
**Mounts to:** `/etc/mysql/conf.d/custom.cnf` in mariadb container  
**Key settings:**
- Character set: utf8mb4
- InnoDB buffer pool: 256MB
- Binary logging enabled for replication
- Slow query log: queries >2s
- Performance schema enabled

## Usage

Configs are mounted as read-only volumes in docker-compose.yml:
```yaml
volumes:
  - ./.config/database/postgresql.conf:/etc/postgresql/postgresql.conf:ro
  - ./.config/database/mariadb.conf:/etc/mysql/conf.d/custom.cnf:ro
```

## Tuning Guidelines

### PostgreSQL
- Adjust `shared_buffers` to 25% of available RAM
- Set `effective_cache_size` to 50-75% of available RAM
- Increase `max_connections` based on application needs

### MariaDB
- Set `innodb_buffer_pool_size` to 70-80% of available RAM
- Adjust `max_connections` based on concurrent client count
- Monitor slow query log to optimize long-running queries

## Validation

Test configuration syntax:
```bash
# PostgreSQL
docker run --rm -v "$(pwd)/.config/database/postgresql.conf:/tmp/postgresql.conf:ro" postgres:16-alpine postgres --config-file=/tmp/postgresql.conf --version

# MariaDB
docker run --rm -v "$(pwd)/.config/database/mariadb.conf:/etc/mysql/conf.d/custom.cnf:ro" mariadb:11 mysqld --help --verbose
```
