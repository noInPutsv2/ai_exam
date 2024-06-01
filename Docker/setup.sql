-- Create the database
CREATE DATABASE AI_DB_EXAM;
GO

-- Use the database, we just created
USE AI_DB_EXAM;
GO

-- Create users table
CREATE TABLE users (
    id int IDENTITY(1,1) PRIMARY KEY,
    username varchar(60) NOT NULL,
    password varchar(60) NOT NULL,
    email varchar(60) NOT NULL,
    house varchar(60)
);
GO 

-- create user_logs table 
CREATE TABLE user_logs (
    log_id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    id int NOT NULL,
    time_stamp DATETIME NOT NULL,
    log_in BIT NOT NULL,
    CONSTRAINT id FOREIGN KEY (id) REFERENCES users(id)
);
GO

-- Create login procedure
CREATE PROCEDURE login 
   @Username varchar(60),
   @Password varchar(60)
AS
BEGIN
    SELECT id 
    FROM dbo.users 
    WHERE username = @Username AND password = @Password
END;
GO