/*==============================================================*/
/* Table: Datoteka                                              */
/*==============================================================*/
create table Datoteka (
   FID                  INT             not null,
   Filepath             VARCHAR(1024)   not null,
   Filename             VARCHAR(256)    not null,
   constraint PK_DATOTEKA primary key (FID)
);
////
/*==============================================================*/
/* Table: Tag                                                   */
/*==============================================================*/
create table Tag (
   TName                VARCHAR(64)      not null,
   Parent               VARCHAR(64)          null,
   FOREIGN KEY(Parent) 	REFERENCES Tag(TName),
   constraint PK_TAG primary key (TName)
);
////
/*==============================================================*/
/* Table: Oznacuje                                              */
/*==============================================================*/
create table Oznacuje (
   FileID                 INT4             not null,
   TagName                VARCHAR(64)      not null,
   FOREIGN KEY(FileID) 	  REFERENCES Datoteka(FID),
   FOREIGN KEY(TagName)   REFERENCES Tag(TName),
   constraint PK_OZNACUJE primary key (FileID, TagName)
);
////
/*==============================================================*/
/* Index: OZNACUJE_FK                                           */
/*==============================================================*/
create  index OZNACUJE_FK on Oznacuje (
FileID
);
////
/*==============================================================*/
/* Trigger: PosodobiStarse                                      */
/*==============================================================*/
CREATE TRIGGER PosodobiStarse
BEFORE DELETE
ON Tag
BEGIN
	UPDATE Tag
	SET Parent = OLD.Parent
	WHERE Parent = OLD.TName;

	UPDATE Oznacuje
	SET TagName = OLD.Parent
	WHERE TagName = OLD.TName;
END;
////
/*==============================================================*/
/* Trigger: IzbrisiOznacuje                                     */
/*==============================================================*/
CREATE TRIGGER IzbrisiOznacuje
BEFORE DELETE
ON Datoteka
BEGIN
    DELETE FROM Oznacuje
    WHERE fileID = OLD.FID;
END;


