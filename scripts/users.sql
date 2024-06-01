CREATE TABLE users (
id int IDENTITY(1,1) PRIMARY KEY,
username varchar(60) NOT NULL,
password varchar(60) NOT NULL,
email varchar(60) NOT NULL,
house varchar(60)
);

CREATE PROCEDURE login 
   @Username varchar(60),
   @Password varchar(60)
AS
    SELECT id 
    FROM dbo.users 
    WHERE username = @Username AND password = @Password
GO;