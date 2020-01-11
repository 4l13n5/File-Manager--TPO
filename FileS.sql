
create table Datoteka (
   ID                   INT      not null,
   Path                 VARCHAR(256)         null,
   constraint PK_DATOTEKA primary key (ID)
);

////
create table Tag (
   Tag                  VARCHAR(64)			 not null,
   Parent               VARCHAR(64)          null,
   FOREIGN KEY(Parent) 	REFERENCES Tag(Tag),
   constraint PK_TAG primary key (Tag)
);
////
create table oznacuje (
   ID                   INT4                 null,
   Tag                  VARCHAR(64)          null,
   FOREIGN KEY(ID) 		REFERENCES Datoteka(ID),
   FOREIGN KEY(Tag) 	REFERENCES Tag(Tag)

   
);
////

create  index OZNACUJE_FK on oznacuje (
ID
);

////
CREATE TRIGGER PosodobiStarse
BEFORE DELETE
ON Tag
BEGIN
	UPDATE Tag
	SET Parent = OLD.Parent
	WHERE Parent = OLD.Tag;

	UPDATE Oznacuje
	SET Tag = OLD.Parent
	WHERE Tag = OLD.Tag;
END;

////
CREATE TRIGGER izbrisiOznacuje
AFTER DELETE
ON Datoteka
BEGIN
    DELETE FROM oznacuje
    WHERE ID = OLD.ID;
END;
