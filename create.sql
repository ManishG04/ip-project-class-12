DROP bank;

CREATE DATABASE bank;

USE bank;

CREATE TABLE users(
    accno int PRIMARY KEY,
    name char(20) NOT NULL,
    passwd varchar(30),
    balance float DEFAULT 0,
    branch char(3) DEFAULT "PAT",
);

INSERT INTO
    users (accno, name, passwd)
VALUES
    (1, "Aditya Nandan", "1234"),
    (2, "Rohit Sharma", "sharma"),
    (3, "Ayush", "ay#123");

SELECT
    *
FROM
    users;