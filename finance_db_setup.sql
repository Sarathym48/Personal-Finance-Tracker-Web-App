
-- --------------------------
-- Personal Finance Tracker
-- Complete Database Setup
-- --------------------------

-- 1) Create database
CREATE DATABASE IF NOT EXISTS finance_db;
USE finance_db;

-- 2) Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3) Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    description TEXT,
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4) Insert a sample user (replace password hash with actual hashed password if needed)
INSERT INTO users (username, password_hash)
SELECT 'testuser', 'dummyhash'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username='testuser');

-- 5) Insert a sample transaction for the sample user
INSERT INTO transactions (user_id, category, amount, description)
SELECT id, 'Food', 100.50, 'Sample transaction'
FROM users
WHERE username='testuser'
AND NOT EXISTS (SELECT 1 FROM transactions WHERE user_id=(SELECT id FROM users WHERE username='testuser'));
