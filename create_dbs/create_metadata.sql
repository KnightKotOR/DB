DROP SCHEMA metadata;

-- ==========================
-- DATABASE METADATA CATALOG
-- ==========================
CREATE DATABASE IF NOT EXISTS metadata
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE metadata;

-- ==========================
-- TABLE: dbs
-- ==========================
CREATE TABLE IF NOT EXISTS dbs (
    db_id INT AUTO_INCREMENT PRIMARY KEY,
    db_name VARCHAR(64) NOT NULL UNIQUE,
    db_alias VARCHAR(64) UNIQUE
) ENGINE=InnoDB;


-- ==========================
-- TABLE: db_tables
-- ==========================
CREATE TABLE IF NOT EXISTS db_tables (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    db_id INT NOT NULL,
    table_name VARCHAR(64) NOT NULL,
    table_alias VARCHAR(64) NULL,
    FOREIGN KEY (db_id) REFERENCES dbs(db_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ==========================
-- TABLE: db_columns
-- ==========================
CREATE TABLE IF NOT EXISTS db_columns (
    column_id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,
    column_name VARCHAR(64) NOT NULL,
    FOREIGN KEY (table_id) REFERENCES db_tables(table_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ==========================
-- TABLE: constraints
-- ==========================
CREATE TABLE IF NOT EXISTS key_names (
    key_id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,
    key_name VARCHAR(64) NOT NULL,
    type ENUM('PRIMARY', 'UNIQUE', 'FOREIGN', 'INDEX') NOT NULL,
    FOREIGN KEY (table_id) REFERENCES db_tables(table_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ==========================
-- TABLE: constraint_columns
-- ==========================
CREATE TABLE IF NOT EXISTS key_columns (
    kc_id INT AUTO_INCREMENT PRIMARY KEY,
    key_id INT NOT NULL,
    column_id INT NOT NULL,
    position INT NOT NULL,
    FOREIGN KEY (key_id) REFERENCES key_names(key_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (column_id) REFERENCES db_columns(column_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- ==========================
-- TABLE: referential_constraints
-- ==========================
CREATE TABLE IF NOT EXISTS foreign_keys (
    fk_id INT AUTO_INCREMENT PRIMARY KEY,
    pk_id INT NOT NULL,
    referenced_key_id INT NOT NULL,
    FOREIGN KEY (pk_id) REFERENCES key_names(key_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (referenced_key_id) REFERENCES key_names(key_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;