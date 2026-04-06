-- ─────────────────────────────────────────────────────────────
-- SEN 311 Group H - Database Setup Script
-- ─────────────────────────────────────────────────────────────

-- 1. Create the database safely
CREATE DATABASE IF NOT EXISTS miva_app_db;

-- 2. Select the database
USE miva_app_db;

-- 3. Clear old table if the grader runs the script twice
DROP TABLE IF EXISTS users;

-- 4. Create the required table
CREATE TABLE users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) NOT NULL UNIQUE,
    gender     ENUM('male', 'female', 'other') NOT NULL,
    password   VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);