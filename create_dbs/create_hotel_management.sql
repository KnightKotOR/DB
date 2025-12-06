CREATE DATABASE IF NOT EXISTS hotel_management;
USE hotel_management;

-- =========================================
-- LEVEL 1 — Reference Tables
-- =========================================

CREATE TABLE IF NOT EXISTS hotel (
  hotel_id CHAR(36) NOT NULL PRIMARY KEY,
  hotel_name VARCHAR(64) NOT NULL,
  hotel_rating INT,
  hotel_room_count INT NOT NULL,
  hotel_country VARCHAR(56) NOT NULL,   -- longest country name = 56
  hotel_city VARCHAR(168) NOT NULL,     -- longest city name = 168
  hotel_street VARCHAR(58) NOT NULL,    -- longest street name = 58
  hotel_postal_code VARCHAR(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS client (
  client_id CHAR(36) NOT NULL PRIMARY KEY,
  client_name VARCHAR(32) NOT NULL,
  client_last_name VARCHAR(64) NOT NULL,
  client_middle_name VARCHAR(32),
  client_birthday DATETIME NOT NULL,
  client_phone VARCHAR(20),
  client_email VARCHAR(64),
  client_bank_details VARCHAR(32),
  client_passport_number VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS room_type (
  room_type_id CHAR(36) NOT NULL PRIMARY KEY,
  room_type_name VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS room_status_name (
  room_status_name_id CHAR(36) NOT NULL PRIMARY KEY,
  room_status_name VARCHAR(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS additional_service_status_name (
  additional_service_status_name_id CHAR(36) NOT NULL PRIMARY KEY,
  additional_service_status_name VARCHAR(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS payment_method (
  payment_method_id CHAR(36) NOT NULL PRIMARY KEY,
  payment_method_name VARCHAR(18) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS payment_status_name (
  payment_status_name_id CHAR(36) NOT NULL PRIMARY KEY,
  payment_status_name VARCHAR(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS booking_status_name (
  booking_status_name_id CHAR(36) NOT NULL PRIMARY KEY,
  booking_status_name VARCHAR(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- LEVEL 2 — Core Business Entities
-- =========================================

CREATE TABLE IF NOT EXISTS additional_service (
  additional_service_id CHAR(36) NOT NULL PRIMARY KEY,
  hotel_id CHAR(36) NOT NULL,
  additional_service_name VARCHAR(21) NOT NULL,
  additional_service_price DECIMAL(10,2) NOT NULL,
  additional_service_description TEXT,
  CONSTRAINT fk_add_service_hotel FOREIGN KEY (hotel_id)
    REFERENCES hotel(hotel_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS room (
  room_id CHAR(36) NOT NULL PRIMARY KEY,
  room_type_id CHAR(36) NOT NULL,
  hotel_id CHAR(36) NOT NULL,
  room_capacity INT NOT NULL,
  room_price_per_night DECIMAL(10,2) NOT NULL,
  room_number INT NOT NULL,
  room_floor INT NOT NULL,
  CONSTRAINT fk_room_type FOREIGN KEY (room_type_id)
    REFERENCES room_type(room_type_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_room_hotel FOREIGN KEY (hotel_id)
    REFERENCES hotel(hotel_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS booking (
  booking_id CHAR(36) NOT NULL PRIMARY KEY,
  hotel_id CHAR(36) NOT NULL,
  client_id CHAR(36) NOT NULL,
  booking_arrival_date DATETIME NOT NULL,
  booking_departure_date DATETIME NOT NULL,
  booking_duration INT NOT NULL,
  CONSTRAINT fk_booking_hotel FOREIGN KEY (hotel_id)
    REFERENCES hotel(hotel_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_booking_client FOREIGN KEY (client_id)
    REFERENCES client(client_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- LEVEL 3 — Transactional / Status Tables
-- =========================================

CREATE TABLE IF NOT EXISTS payment (
  payment_id CHAR(36) NOT NULL PRIMARY KEY,
  booking_id CHAR(36) NOT NULL,
  client_id CHAR(36) NOT NULL,
  payment_method_id CHAR(36) NOT NULL,
  payment_sum DECIMAL(10,2) NOT NULL,
  payment_date DATETIME NOT NULL,
  CONSTRAINT fk_payment_booking FOREIGN KEY (booking_id)
    REFERENCES booking(booking_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_payment_client FOREIGN KEY (client_id)
    REFERENCES client(client_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_payment_method FOREIGN KEY (payment_method_id)
    REFERENCES payment_method(payment_method_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS room_status (
  room_status_id CHAR(36) NOT NULL PRIMARY KEY,
  room_id CHAR(36) NOT NULL,
  room_status_name_id CHAR(36) NOT NULL,
  room_status_date DATETIME NOT NULL,
  CONSTRAINT fk_room_status_room FOREIGN KEY (room_id)
    REFERENCES room(room_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_room_status_name FOREIGN KEY (room_status_name_id)
    REFERENCES room_status_name(room_status_name_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS booking_room (
  booking_room_id CHAR(36) NOT NULL PRIMARY KEY,
  room_id CHAR(36) NOT NULL,
  booking_id CHAR(36) NOT NULL,
  CONSTRAINT fk_booking_room_room FOREIGN KEY (room_id)
    REFERENCES room(room_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_booking_room_booking FOREIGN KEY (booking_id)
    REFERENCES booking(booking_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS additional_service_status (
  additional_service_status_id CHAR(36) NOT NULL PRIMARY KEY,
  additional_service_id CHAR(36) NOT NULL,
  additional_service_status_name_id CHAR(36) NOT NULL,
  additional_service_status_date DATETIME NOT NULL,
  CONSTRAINT fk_service_status_service FOREIGN KEY (additional_service_id)
    REFERENCES additional_service(additional_service_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_service_status_name FOREIGN KEY (additional_service_status_name_id)
    REFERENCES additional_service_status_name(additional_service_status_name_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS booking_additional_service (
  booking_additional_service_id CHAR(36) NOT NULL PRIMARY KEY,
  additional_service_id CHAR(36) NOT NULL,
  booking_id CHAR(36) NOT NULL,
  CONSTRAINT fk_booking_add_service_service FOREIGN KEY (additional_service_id)
    REFERENCES additional_service(additional_service_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_booking_add_service_booking FOREIGN KEY (booking_id)
    REFERENCES booking(booking_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS booking_status (
  booking_status_id CHAR(36) NOT NULL PRIMARY KEY,
  booking_id CHAR(36) NOT NULL,
  booking_status_name_id CHAR(36) NOT NULL,
  booking_status_date DATETIME NOT NULL,
  CONSTRAINT fk_booking_status_booking FOREIGN KEY (booking_id)
    REFERENCES booking(booking_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_booking_status_name FOREIGN KEY (booking_status_name_id)
    REFERENCES booking_status_name(booking_status_name_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================
-- LEVEL 4 — Payment Status Tracking
-- =========================================

CREATE TABLE IF NOT EXISTS payment_status (
  payment_status_id CHAR(36) NOT NULL PRIMARY KEY,
  payment_id CHAR(36) NOT NULL,
  payment_status_name_id CHAR(36) NOT NULL,
  payment_status_date DATETIME NOT NULL,
  CONSTRAINT fk_payment_status_payment FOREIGN KEY (payment_id)
    REFERENCES payment(payment_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_payment_status_name FOREIGN KEY (payment_status_name_id)
    REFERENCES payment_status_name(payment_status_name_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
