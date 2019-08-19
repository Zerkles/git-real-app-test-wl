CREATE TABLE Rooms (id BIGSERIAL PRIMARY KEY,name VARCHAR (128) NOT NULL,available BOOLEAN);

INSERT INTO Rooms (id,name,available)
VALUES (123,'adam',true);

INSERT INTO Rooms
VALUES (222,'bob',False);

INSERT INTO Rooms
VALUES (456123,'daniel',True);
