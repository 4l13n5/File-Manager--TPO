/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     09/01/2020 12:21:42                          */
/*==============================================================*/

/*drop table Datoteka;

drop index JE_DEL_FK;

drop table Tag;

drop index OZNACUJE_FK;

drop table oznacuje;*/

/*==============================================================*/
/* Table: Datoteka                                              */
/*==============================================================*/
create table Datoteka (
   ID                   INT      not null,
   Path                 VARCHAR(256)         null,
   constraint PK_DATOTEKA primary key (ID)
);


/*==============================================================*/
/* Table: Tag                                                   */
/*==============================================================*/
create table Tag (
   Tag                  VARCHAR(64)			 not null,
   Parent               VARCHAR(64)          null,
   FOREIGN KEY(Parent) 	REFERENCES Tag(Tag),
   constraint PK_TAG primary key (Tag)
);

/*==============================================================*/
/* Table: oznacuje                                              */
/*==============================================================*/
create table oznacuje (
   ID                   INT4                 null,
   Tag                  VARCHAR(64)          null,
   FOREIGN KEY(ID) 		REFERENCES Datoteka(ID),
   FOREIGN KEY(Tag) 	REFERENCES Tag(Tag)

   
);

/*==============================================================*/
/* Index: OZNACUJE_FK                                           */
/*==============================================================*/
create  index OZNACUJE_FK on oznacuje (
ID
);



