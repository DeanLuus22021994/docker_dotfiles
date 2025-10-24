-- PostgreSQL initialization script
-- This script runs on the first startup of the container

-- Create application database and user
CREATE DATABASE app;
CREATE USER app WITH ENCRYPTED PASSWORD 'app';
GRANT ALL PRIVILEGES ON DATABASE app TO app;

-- Create test database for development
CREATE DATABASE app_test;
GRANT ALL PRIVILEGES ON DATABASE app_test TO app;

-- Enable necessary extensions
\c app
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

\c app_test
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";