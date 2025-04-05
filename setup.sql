CREATE DATABASE IF NOT EXISTS policeDB;
USE policeDB;

CREATE TABLE IF NOT EXISTS employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    rank VARCHAR(50),
    contact VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS leaves (
    leave_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT,
    start_date DATE,
    end_date DATE,
    reason VARCHAR(255),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

CREATE TABLE IF NOT EXISTS shifts (
    shift_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT,
    shift_date DATE,
    shift_type VARCHAR(50),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);
