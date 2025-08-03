-- Create database and user
CREATE DATABASE IF NOT EXISTS kanban_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'kanban_user'@'%' IDENTIFIED BY 'kanban_password';
GRANT ALL PRIVILEGES ON kanban_db.* TO 'kanban_user'@'%';
FLUSH PRIVILEGES;

-- Use the database
USE kanban_db;