CREATE DATABASE IF NOT EXISTS ice_shows_management;
USE ice_shows_management;

-- =====================
-- TABLE: city
-- =====================
CREATE TABLE city (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(170) NOT NULL,
    region_code VARCHAR(2) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: users
-- =====================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    family VARCHAR(40) NOT NULL,
    name VARCHAR(40) NOT NULL,
    middlename VARCHAR(40),
    phone_number VARCHAR(30),
    email VARCHAR(254)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: organiser
-- =====================
CREATE TABLE organiser (
    organiser_id INT AUTO_INCREMENT PRIMARY KEY,
    family VARCHAR(40),
    name VARCHAR(40),
    middlename VARCHAR(40),
    phone_number VARCHAR(30),
    name_of_the_organization VARCHAR(240),
    company_address VARCHAR(100)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: ice_show
-- =====================
CREATE TABLE ice_show (
    ice_show_id INT AUTO_INCREMENT PRIMARY KEY,
    organiser_id INT NOT NULL,
    title VARCHAR(40) NOT NULL,
    date_of_the_event DATE NOT NULL,
    age_limit INT,
    FOREIGN KEY (organiser_id) REFERENCES organiser(organiser_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: ice_arena
-- =====================
CREATE TABLE ice_arena (
    ice_arena_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    title VARCHAR(40) NOT NULL,
    address VARCHAR(100) NOT NULL,
    capacity INT,
    coordinates DECIMAL(8,5),
    FOREIGN KEY (city_id) REFERENCES city(city_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: ice_show_ice_arena (junction)
-- =====================
CREATE TABLE ice_show_ice_arena (
    ice_show_ice_arena_id INT AUTO_INCREMENT PRIMARY KEY,
    ice_arena_id INT NOT NULL,
    ice_show_id INT NOT NULL,
    FOREIGN KEY (ice_arena_id) REFERENCES ice_arena(ice_arena_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (ice_show_id) REFERENCES ice_show(ice_show_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: controller
-- =====================
CREATE TABLE controller (
    controller_id INT AUTO_INCREMENT PRIMARY KEY,
    family VARCHAR(40),
    name VARCHAR(40),
    middlename VARCHAR(40),
    phone_number VARCHAR(30),
    experience INT,
    age INT,
    ice_arena_id INT,
    FOREIGN KEY (ice_arena_id) REFERENCES ice_arena(ice_arena_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: cashier
-- =====================
CREATE TABLE cashier (
    cashier_id INT AUTO_INCREMENT PRIMARY KEY,
    family VARCHAR(40),
    name VARCHAR(40),
    middlename VARCHAR(40),
    phone_number VARCHAR(30),
    experience INT,
    age INT,
    ice_arena_id INT,
    FOREIGN KEY (ice_arena_id) REFERENCES ice_arena(ice_arena_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: sector
-- =====================
CREATE TABLE sector (
    sector_id INT AUTO_INCREMENT PRIMARY KEY,
    ice_arena_id INT NOT NULL,
    number INT,
    condition_desc VARCHAR(20),
    FOREIGN KEY (ice_arena_id) REFERENCES ice_arena(ice_arena_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: row_
-- =====================
CREATE TABLE row_ (
    row_id INT AUTO_INCREMENT PRIMARY KEY,
    number INT,
    condition_desc VARCHAR(20),
    sector_id INT NOT NULL,
    FOREIGN KEY (sector_id) REFERENCES sector(sector_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: place
-- =====================
CREATE TABLE place (
    place_id INT AUTO_INCREMENT PRIMARY KEY,
    number INT,
    condition_desc VARCHAR(20),
    row_id INT NOT NULL,
    FOREIGN KEY (row_id) REFERENCES row_(row_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: ticket
-- =====================
CREATE TABLE ticket (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    cashier_id INT,
    sector_id INT,
    row_id INT,
    place_id INT,
    ice_show_id INT,
    cost DECIMAL(15,2),
    time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (cashier_id) REFERENCES cashier(cashier_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (sector_id) REFERENCES sector(sector_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (row_id) REFERENCES row_(row_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (place_id) REFERENCES place(place_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (ice_show_id) REFERENCES ice_show(ice_show_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;


-- =====================
-- TABLE: controller_checked_billet
-- =====================
CREATE TABLE controller_checked_billet (
    controller_checked_billet_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT,
    controller_id INT,
    FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (controller_id) REFERENCES controller(controller_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci;
