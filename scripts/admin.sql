CREATE TABLE admin (
id int IDENTITY(1,1) PRIMARY KEY,
username varchar(60) NOT NULL,
name varchar(60) NOT NULL,
password varchar(60) NOT NULL,
);

INSERT INTO admin (username, name, password) VALUES ('test', 'Line', 'test')