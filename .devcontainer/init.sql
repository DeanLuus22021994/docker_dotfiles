-- Init script for MariaDB in devcontainer
-- Create a sample database and table for scuba app

USE scuba_db;

-- Create a sample table for dive sites
CREATE TABLE IF NOT EXISTS dive_sites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    depth INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO dive_sites (name, location, depth, description) VALUES
('Great Barrier Reef', 'Australia', 30, 'World-famous coral reef system'),
('Maui', 'Hawaii, USA', 60, 'Rich marine life and clear waters'),
('Belize Barrier Reef', 'Belize', 40, 'Second largest barrier reef system');

-- Create users table if needed
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
