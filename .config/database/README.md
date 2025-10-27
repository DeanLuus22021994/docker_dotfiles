---
date_created: '2025-10-27T02:33:39Z'
last_updated: '2025-10-27T02:33:39Z'
tags: [database, postgresql, mariadb, configuration]
description: 'Database configuration files for PostgreSQL and MariaDB'
---

# Database Configuration

This directory contains production-grade database configuration files for the cluster.

## 📁 Files

### `postgresql.conf`

**PostgreSQL 16+ configuration** optimized for cluster workloads.

**Key Settings:**
- ✅ **Max connections**: 200 (high-availability ready)
- ✅ **Shared buffers**: 256MB (optimized for cluster)
- ✅ **Effective cache**: 2GB
- ✅ **WAL replication**: Configured for future HA
- ✅ **Performance monitoring**: `pg_stat_statements` enabled
- ✅ **Autovacuum**: Aggressive settings for high-write workloads
- ✅ **Security**: SCRAM-SHA-256 password encryption

**Mounted in docker-compose.yml:**
```yaml
services:
  cluster-postgres:
    volumes:
      - ./.config/database/postgresql.conf:/etc/postgresql/postgresql.conf:ro
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
```

**Networks:**
- `cluster-data` (internal-only)
- `cluster-backend` (application access)

**Secrets:**
- `postgres_user` (via `POSTGRES_USER_FILE`)
- `postgres_password` (via `POSTGRES_PASSWORD_FILE`)

---

### `mariadb.conf`

**MariaDB 11+ configuration** optimized for InnoDB workloads.

**Key Settings:**
- ✅ **Character set**: UTF-8MB4 (full Unicode support)
- ✅ **InnoDB buffer pool**: 256MB
- ✅ **Max connections**: 151
- ✅ **Binary logging**: Enabled for replication
- ✅ **Performance schema**: Enabled for monitoring
- ✅ **Slow query log**: Queries >2s logged

**Mounted in docker-compose.yml:**
```yaml
services:
  cluster-mariadb:
    volumes:
      - ./.config/database/mariadb.conf:/etc/mysql/conf.d/custom.cnf:ro
```

**Networks:**
- `cluster-data` (internal-only)
- `cluster-backend` (application access)

**Secrets:**
- `mariadb_root_password` (via `MARIADB_ROOT_PASSWORD_FILE`)
- `mariadb_password` (via `MARIADB_PASSWORD_FILE`)
- `mariadb_user` (via `MARIADB_USER_FILE`)

---

## 🚀 Quick Start

### Verify Configuration

```powershell
# PostgreSQL - Check loaded config
docker exec cluster-postgres psql -U cluster_user -d clusterdb -c \"SHOW config_file;\"
docker exec cluster-postgres psql -U cluster_user -d clusterdb -c \"SHOW shared_buffers;\"

# MariaDB - Check loaded config
docker exec cluster-mariadb mariadb -u root -p -e \"SHOW VARIABLES LIKE '%buffer%';\"
docker exec cluster-mariadb mariadb -u root -p -e \"SHOW VARIABLES LIKE 'character_set%';\"
```

### Performance Monitoring

```powershell
# PostgreSQL - Check pg_stat_statements
docker exec cluster-postgres psql -U cluster_user -d clusterdb -c \"SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;\"

# MariaDB - Check slow queries
docker exec cluster-mariadb tail -n 50 /var/log/mysql/slow.log
```

---

## 🎯 Best Practices

### For PostgreSQL

✅ **Connection pooling** - Use PgBouncer or application-level pooling  
✅ **Regular vacuuming** - Autovacuum is aggressive, monitor with `pg_stat_user_tables`  
✅ **Index maintenance** - Rebuild indexes when bloat >30%  
✅ **WAL archiving** - Enable for point-in-time recovery  
✅ **Replication** - WAL level set to `replica` for future HA setup  

### For MariaDB

✅ **InnoDB tuning** - Buffer pool should be 70-80% of available RAM in production  
✅ **Binary logs** - Monitor disk usage, expire logs after 7 days  
✅ **Replication** - Server ID configured for future replication setup  
✅ **Character sets** - Always use UTF-8MB4 for full Unicode support  
✅ **Query optimization** - Monitor slow query log for queries >2s  

---

## 🔧 Troubleshooting

### PostgreSQL Connection Issues

```powershell
# Check if PostgreSQL is ready
docker exec cluster-postgres pg_isready -U cluster_user -d clusterdb

# Check connections
docker exec cluster-postgres psql -U cluster_user -d clusterdb -c \"SELECT count(*) FROM pg_stat_activity;\"

# Check locks
docker exec cluster-postgres psql -U cluster_user -d clusterdb -c \"SELECT * FROM pg_locks WHERE NOT granted;\"
```

### MariaDB Connection Issues

```powershell
# Check MariaDB status
docker exec cluster-mariadb mariadb-admin ping -h localhost

# Check connections
docker exec cluster-mariadb mariadb -u root -p -e \"SHOW PROCESSLIST;\"

# Check InnoDB status
docker exec cluster-mariadb mariadb -u root -p -e \"SHOW ENGINE INNODB STATUS\\G\"
```

### Performance Issues

```powershell
# PostgreSQL - Check table bloat
docker exec cluster-postgres psql -U cluster_user -d clusterdb -c \"SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC LIMIT 10;\"

# MariaDB - Check table sizes
docker exec cluster-mariadb mariadb -u root -p -e \"SELECT table_schema, table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)' FROM information_schema.TABLES ORDER BY (data_length + index_length) DESC LIMIT 10;\"
```

---

## 📚 References

- [PostgreSQL Configuration Documentation](https://www.postgresql.org/docs/current/runtime-config.html)
- [MariaDB Server System Variables](https://mariadb.com/kb/en/server-system-variables/)
- [PostgreSQL High Availability](https://www.postgresql.org/docs/current/high-availability.html)
- [MariaDB Replication](https://mariadb.com/kb/en/replication/)

---

## 📝 Configuration Change Log

**PostgreSQL:**
- 2025-10-27: Increased max_connections to 200 for HA readiness
- 2025-10-27: Enabled pg_stat_statements for performance monitoring
- 2025-10-27: Set WAL level to replica for future replication

**MariaDB:**
- 2025-10-27: Increased innodb_buffer_pool_size to 256MB
- 2025-10-27: Enabled performance_schema for monitoring
- 2025-10-27: Configured binary logging for replication
