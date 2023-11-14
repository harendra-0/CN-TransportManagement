CREATE DATABASE transportManagement;
use transportManagement;

CREATE TABLE login (
    userID VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL
);

CREATE TABLE adminlogin (
    userID VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL
);

CREATE TABLE authlogin (
    userID VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL
);

CREATE TABLE users (
	fullName VARCHAR(255) NOT NULL,
    userType VARCHAR(255) NOT NULL,
    Contact VARCHAR(255) NOT NULL,
    EmailID VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL
);

CREATE TABLE newUsers (
	fullName VARCHAR(255) NOT NULL,
    userType VARCHAR(255) NOT NULL,
    Contact VARCHAR(255) NOT NULL,
    EmailID VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL
);

CREATE TABLE tempUsers (
	fullName VARCHAR(255) NOT NULL,
    userType VARCHAR(255) NOT NULL,
    Contact VARCHAR(255) NOT NULL,
    EmailID VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL,
    otp VARCHAR(255) NOT NULL
);

CREATE TABLE requests (
    requestID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    usertype VARCHAR(100),
    guestName VARCHAR(100),
    contactNum VARCHAR(100),
    departureFrom VARCHAR(100),
    departureTo VARCHAR(100),
    departureTiming VARCHAR(100),
    departureDate VARCHAR(100),
    Capacity VARCHAR(1000),
    Reason VARCHAR(2000),
    status VARCHAR(100) DEFAULT 'Pending',
    approvedBy VARCHAR(100) DEFAULT 'None',
    reasonToCancel VARCHAR(255) DEFAULT ' - '
);

CREATE TABLE requestsAuth (
    requestID INT PRIMARY KEY,
    username VARCHAR(100),
    usertype VARCHAR(100),
    guestName VARCHAR(100),
    contactNum VARCHAR(100),
    departureFrom VARCHAR(100),
    departureTo VARCHAR(100),
    departureTiming VARCHAR(100),
    departureDate VARCHAR(100),
    Capacity VARCHAR(1000),
    Reason VARCHAR(2000),
    status VARCHAR(100) DEFAULT 'Pending',
    approvedBy VARCHAR(100) DEFAULT 'None',
    remarks VARCHAR(255) DEFAULT ' - '
);

CREATE TABLE requestAprAdminDT (
	requestID INT PRIMARY KEY,
    approvedBy VARCHAR(100),
    dateNtime VARCHAR(100) DEFAULT ' '
);

CREATE TABLE requestAprAuthDT (
	requestID INT PRIMARY KEY,
    approvedBy VARCHAR(100),
    dateNtime VARCHAR(100) DEFAULT ' '
);

DROP TABLE requestAprAuthDT;

ALTER TABLE requests
ALTER COLUMN reasonToCancel SET DEFAULT '-';

INSERT INTO requests (username, usertype, departureFrom, departureTo, departureTiming, departureDate, Capacity, Reason)
VALUES ('manpreet.singh', 'Visitor', 'Motera', 'IIT Gandhinagar', '11:00PM', '2023-10-11', 1, 'N/A');


INSERT INTO transportManagement.login(userID, pwd) VALUES
('harry', 'harry@123');

INSERT INTO transportManagement.adminlogin(userID, pwd) VALUES
('harry', 'harry@123');

INSERT INTO transportManagement.authlogin(userID, pwd) VALUES
('naval', 'naval@123');

SHOW TABLES;
DROP TABLE requests;
DROP TABLE requestsAuth;
SELECT * FROM tempUsers;
SELECT * FROM adminlogin;
SELECT * FROM newUsers;
SELECT * FROM requestsAuth;
SELECT * FROM requestAprAdminDT;
SELECT * FROM requests;
DROP TABLE requests;
SELECT * FROM authlogin;
SELECT * FROM login WHERE userID = 'harry';
