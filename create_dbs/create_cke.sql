CREATE DATABASE IF NOT EXISTS composite_key_example
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE composite_key_example;


-- =====================================
-- TABLE: departments
-- =====================================
CREATE TABLE departments (
    dept_code VARCHAR(10) NOT NULL,
    region_code VARCHAR(5) NOT NULL,
    dept_name VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (dept_code, region_code)
) ENGINE=InnoDB;


-- =====================================
-- TABLE: employees
-- =====================================
CREATE TABLE employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_code VARCHAR(10) NOT NULL,
    region_code VARCHAR(5) NOT NULL,
    emp_name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    FOREIGN KEY (dept_code, region_code)
        REFERENCES departments(dept_code, region_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- =====================================
-- TABLE: projects
-- =====================================
CREATE TABLE projects (
    dept_code VARCHAR(10) NOT NULL,
    region_code VARCHAR(5) NOT NULL,
    project_code VARCHAR(20) NOT NULL,
    project_name VARCHAR(150),
    PRIMARY KEY (dept_code, region_code, project_code),
    FOREIGN KEY (dept_code, region_code)
        REFERENCES departments(dept_code, region_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;


-- =====================================
-- TABLE: employee_projects
-- =====================================
CREATE TABLE employee_projects (
    emp_id INT NOT NULL,
    dept_code VARCHAR(10) NOT NULL,
    region_code VARCHAR(5) NOT NULL,
    project_code VARCHAR(20) NOT NULL,
    assigned_date DATE,
    PRIMARY KEY (emp_id, dept_code, region_code, project_code),
    FOREIGN KEY (emp_id)
        REFERENCES employees(emp_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (dept_code, region_code, project_code)
        REFERENCES projects(dept_code, region_code, project_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

USE composite_key_example;

-- =====================================
-- Fill departments
-- =====================================
INSERT INTO departments (dept_code, region_code, dept_name) VALUES
('HR', 'R01', 'Human Resources North'),
('HR', 'R02', 'Human Resources South'),
('IT', 'R01', 'Information Technology North'),
('IT', 'R02', 'Information Technology South'),
('FIN', 'R01', 'Finance North'),
('FIN', 'R02', 'Finance South'),
('MKT', 'R01', 'Marketing North'),
('MKT', 'R02', 'Marketing South'),
('OPS', 'R01', 'Operations North'),
('OPS', 'R02', 'Operations South');

-- =====================================
-- Fill employees
-- =====================================
INSERT INTO employees (dept_code, region_code, emp_name, position) VALUES
('HR', 'R01', 'Alice Johnson', 'HR Manager'),
('HR', 'R02', 'Bob Carter', 'HR Specialist'),
('IT', 'R01', 'Charlie Smith', 'Software Engineer'),
('IT', 'R02', 'Diana Evans', 'System Administrator'),
('FIN', 'R01', 'Ethan Brown', 'Accountant'),
('FIN', 'R02', 'Fiona Davis', 'Financial Analyst'),
('MKT', 'R01', 'George Wilson', 'Marketing Lead'),
('MKT', 'R02', 'Hannah Moore', 'SEO Specialist'),
('OPS', 'R01', 'Ian Thompson', 'Operations Coordinator'),
('OPS', 'R02', 'Julia Roberts', 'Supply Chain Manager');

-- =====================================
-- Fill projects
-- =====================================
INSERT INTO projects (dept_code, region_code, project_code, project_name) VALUES
('HR', 'R01', 'P001', 'Recruitment Automation'),
('HR', 'R02', 'P002', 'Employee Satisfaction Survey'),
('IT', 'R01', 'P003', 'Intranet Redesign'),
('IT', 'R02', 'P004', 'Cloud Migration'),
('FIN', 'R01', 'P005', 'Budget Optimization'),
('FIN', 'R02', 'P006', 'Expense Tracking System'),
('MKT', 'R01', 'P007', 'Social Media Expansion'),
('MKT', 'R02', 'P008', 'Ad Campaign Revamp'),
('OPS', 'R01', 'P009', 'Warehouse Automation'),
('OPS', 'R02', 'P010', 'Logistics Optimization');

-- =====================================
-- Fill employee_projects
-- =====================================
INSERT INTO employee_projects (emp_id, dept_code, region_code, project_code, assigned_date) VALUES
(1, 'HR', 'R01', 'P001', '2025-01-15'),
(2, 'HR', 'R02', 'P002', '2025-02-10'),
(3, 'IT', 'R01', 'P003', '2025-03-01'),
(4, 'IT', 'R02', 'P004', '2025-03-10'),
(5, 'FIN', 'R01', 'P005', '2025-04-05'),
(6, 'FIN', 'R02', 'P006', '2025-04-20'),
(7, 'MKT', 'R01', 'P007', '2025-05-01'),
(8, 'MKT', 'R02', 'P008', '2025-05-15'),
(9, 'OPS', 'R01', 'P009', '2025-06-01'),
(10, 'OPS', 'R02', 'P010', '2025-06-20');