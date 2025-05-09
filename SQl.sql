create database flaskdb

use flaskdb

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE phones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(100),
    ram VARCHAR(20),
    storage VARCHAR(20),
    camera VARCHAR(100),
    battery VARCHAR(50),
    price DECIMAL(10,2),
    image TEXT(1000)
);