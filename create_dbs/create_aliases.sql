-- ==========================
-- DATABASE FOR USER ALIASES
-- ==========================
CREATE DATABASE IF NOT EXISTS query_aliases
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE query_aliases;

-- ==========================
-- TABLE: db_aliases
-- Псевдонимы для баз данных
-- ==========================
CREATE TABLE IF NOT EXISTS db_aliases (
    alias_db_id INT AUTO_INCREMENT PRIMARY KEY,
    db_meta_id INT NOT NULL,                   -- Ссылка на реальную БД в metadata.dbs
    db_alias_name VARCHAR(64) NULL UNIQUE -- Псевдоним, который будет использовать пользователь
) ENGINE=InnoDB;

-- ==========================
-- TABLE: table_aliases
-- Псевдонимы для таблиц
-- ==========================
CREATE TABLE IF NOT EXISTS table_aliases (
    alias_table_id INT AUTO_INCREMENT PRIMARY KEY,
    table_meta_id INT NOT NULL,                    -- Ссылка на реальную таблицу в metadata.db_tables
    table_alias_name VARCHAR(64) NOT NULL UNIQUE -- Псевдоним, который будет использовать пользователь
) ENGINE=InnoDB;

-- ==========================
-- TABLE: column_aliases
-- Псевдонимы для столбцов
-- ==========================
CREATE TABLE IF NOT EXISTS column_aliases (
    alias_column_id INT AUTO_INCREMENT PRIMARY KEY,
    column_meta_id INT NOT NULL,                    -- Ссылка на реальный столбец в metadata.db_columns
    column_alias_name VARCHAR(64) NOT NULL UNIQUE -- Псевдоним, который будет использовать пользователь
) ENGINE=InnoDB;