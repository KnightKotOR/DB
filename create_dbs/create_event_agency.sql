CREATE DATABASE event_agency;
USE event_agency;

CREATE TABLE client (
    client_id INT NOT NULL,
    surname VARCHAR(50),
    name VARCHAR(50),
    middlename VARCHAR(50),
    date_of_birth DATE,
    phone_number VARCHAR(30),
    email VARCHAR(50),
    PRIMARY KEY (client_id)
);

CREATE TABLE agency (
    agency_id INT NOT NULL,
    name VARCHAR(50),
    phone_number VARCHAR(30),
    email VARCHAR(50),
    address VARCHAR(50),
    PRIMARY KEY (agency_id)
);

CREATE TABLE place (
    place_id INT NOT NULL,
    address VARCHAR(50),
    area INT,
    capacity INT,
    rental_cost INT,
    PRIMARY KEY (place_id)
);

CREATE TABLE supplier (
    supplier_id INT NOT NULL,
    name VARCHAR(50),
    phone_number VARCHAR(30),
    email VARCHAR(50),
    PRIMARY KEY (supplier_id)
);

CREATE TABLE service (
    service_id INT NOT NULL,
    name VARCHAR(50),
    cost INT,
    unit_of_measurement VARCHAR(20),
    PRIMARY KEY (service_id)
);

CREATE TABLE manager (
    manager_id INT NOT NULL,
    surname VARCHAR(50),
    name VARCHAR(50),
    middlename VARCHAR(50),
    phone_number VARCHAR(30),
    email VARCHAR(50),
    agency_id INT NOT NULL,
    PRIMARY KEY (manager_id),
    FOREIGN KEY (agency_id) REFERENCES agency(agency_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE list_of_supplier_services (
    contract_id INT NOT NULL,
    supplier_id INT,
    service_id INT,
    PRIMARY KEY (contract_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES service(service_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE list_of_suppliers (
    contract_id INT NOT NULL,
    agency_id INT,
    supplier_id INT,
    PRIMARY KEY (contract_id),
    FOREIGN KEY (agency_id) REFERENCES agency(agency_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE event (
    event_id INT NOT NULL,
    type VARCHAR(20),
    date DATE,
    theme VARCHAR(50),
    budget INT,
    client_id INT,
    manager_id INT,
    place_id INT,
    PRIMARY KEY (event_id),
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (manager_id) REFERENCES manager(manager_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (place_id) REFERENCES place(place_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE services_at_the_event (
    service_at_the_event_id INT NOT NULL,
    event_id INT,
    service_id INT,
    supplier_id INT,
    PRIMARY KEY (service_at_the_event_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES service(service_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE review (
    review_id INT NOT NULL,
    grade INT,
    client_id INT,
    supplier_id INT,
    service_at_the_event_id INT,
    PRIMARY KEY (review_id),
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (service_at_the_event_id) REFERENCES services_at_the_event(service_at_the_event_id) ON DELETE SET NULL ON UPDATE CASCADE
);
