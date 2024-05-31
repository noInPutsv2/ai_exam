CREATE TABLE users (
id int IDENTITY(1,1) PRIMARY KEY,
username varchar(60) NOT NULL,
password varchar(60) NOT NULL,
email varchar(60) NOT NULL,
house varchar(60)
);