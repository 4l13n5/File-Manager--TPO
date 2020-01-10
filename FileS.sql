/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     09/01/2020 12:21:42                          */
/*==============================================================*/

/*==============================================================*/
/* Table: Datoteka                                              */
/*==============================================================*/
create table Datoteka (
   ID                   INT      		not null,
   Path                 VARCHAR(256)    not null,
   Name					VARCHAR(256)	not null,
   constraint PK_DATOTEKA primary key (ID)
);


/*==============================================================*/
/* Table: Tag                                                   */
/*==============================================================*/
create table Tag (
   Name                 VARCHAR(64)			 not null,
   Parent               VARCHAR(64)          null,
   FOREIGN KEY(Parent) 	REFERENCES Tag(Name),
   constraint PK_TAG primary key (Name)
);

/*==============================================================*/
/* Table: Oznacuje                                              */
/*==============================================================*/
create table Oznacuje (
   fileID               INT4                 not null,
   TagName              VARCHAR(64)          not null,
   FOREIGN KEY(fileID) 		REFERENCES Datoteka(ID),
   FOREIGN KEY(TagName) 	REFERENCES Tag(Name),
   constraint PK_OZNACUJE primary key (fileID, TagName)
);

/*==============================================================*/
/* Index: OZNACUJE_FK                                           */
/*==============================================================*/
create  index OZNACUJE_FK on Oznacuje (
fileID
);

/*==============================================================*/
/* Trigger: PosodobiStarse                                      */
/*==============================================================*/
CREATE TRIGGER PosodobiStarse
BEFORE DELETE
ON Tag
BEGIN
	UPDATE Tag
	SET Parent = OLD.Parent
	WHERE Parent = OLD.Name;
	
	UPDATE Oznacuje
	SET TagName = OLD.Parent
	WHERE TagName = OLD.Name;
END;


