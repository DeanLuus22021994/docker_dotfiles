-- MariaDB initialization script
-- This script runs on the first startup of the container

-- Create application database and user
CREATE DATABASE IF NOT EXISTS app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'app'@'%' IDENTIFIED BY 'app';
GRANT ALL PRIVILEGES ON app.* TO 'app'@'%';
FLUSH PRIVILEGES;

-- Create test database for development
CREATE DATABASE IF NOT EXISTS app_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON app_test.* TO 'app'@'%';
FLUSH PRIVILEGES;