/*==============================================================*/
/* DBMS name:      Sybase SQL Anywhere 10                       */
/* Created on:     2. 12. 2019 09:11:28                         */
/*==============================================================*/


if exists(select 1 from sys.sysforeignkey where role='FK_RELATION_RELATIONS_TAGS') then
    alter table Relationship_1
       delete foreign key FK_RELATION_RELATIONS_TAGS
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_RELATION_RELATIONS_FILES') then
    alter table Relationship_1
       delete foreign key FK_RELATION_RELATIONS_FILES
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_TAGS_PARENT-CH_TAGS') then
    alter table Tags
       delete foreign key "FK_TAGS_PARENT-CH_TAGS"
end if;

if exists(
   select 1 from sys.sysindex i, sys.systable t
   where i.table_id=t.table_id 
     and i.index_name='Files_PK'
     and t.table_name='Files'
) then
   drop index Files.Files_PK
end if;

if exists(
   select 1 from sys.systable 
   where table_name='Files'
     and table_type in ('BASE', 'GBL TEMP')
) then
    drop table Files
end if;

if exists(
   select 1 from sys.sysindex i, sys.systable t
   where i.table_id=t.table_id 
     and i.index_name='Relationship_2_FK'
     and t.table_name='Relationship_1'
) then
   drop index Relationship_1.Relationship_2_FK
end if;

if exists(
   select 1 from sys.sysindex i, sys.systable t
   where i.table_id=t.table_id 
     and i.index_name='Relationship_1_FK'
     and t.table_name='Relationship_1'
) then
   drop index Relationship_1.Relationship_1_FK
end if;

if exists(
   select 1 from sys.sysindex i, sys.systable t
   where i.table_id=t.table_id 
     and i.index_name='Relationship_1_PK'
     and t.table_name='Relationship_1'
) then
   drop index Relationship_1.Relationship_1_PK
end if;

if exists(
   select 1 from sys.systable 
   where table_name='Relationship_1'
     and table_type in ('BASE', 'GBL TEMP')
) then
    drop table Relationship_1
end if;

if exists(
   select 1 from sys.sysindex i, sys.systable t
   where i.table_id=t.table_id 
     and i.index_name='parent-child_FK'
     and t.table_name='Tags'
) then
   drop index Tags."parent-child_FK"
end if;

if exists(
   select 1 from sys.sysindex i, sys.systable t
   where i.table_id=t.table_id 
     and i.index_name='Tags_PK'
     and t.table_name='Tags'
) then
   drop index Tags.Tags_PK
end if;

if exists(
   select 1 from sys.systable 
   where table_name='Tags'
     and table_type in ('BASE', 'GBL TEMP')
) then
    drop table Tags
end if;

/*==============================================================*/
/* Table: Files                                                 */
/*==============================================================*/
create table Files 
(
   "File ID"            numeric                        not null,
   "File Name"          varchar(1024),
   "File Location"      varchar(1024),
   constraint PK_FILES primary key ("File ID")
);

/*==============================================================*/
/* Index: Files_PK                                              */
/*==============================================================*/
create unique index Files_PK on Files (
"File ID" ASC
);

/*==============================================================*/
/* Table: Relationship_1                                        */
/*==============================================================*/
create table Relationship_1 
(
   Tag                  varchar(1024)                  not null,
   "File ID"            numeric                        not null,
   constraint PK_RELATIONSHIP_1 primary key clustered (Tag, "File ID")
);

/*==============================================================*/
/* Index: Relationship_1_PK                                     */
/*==============================================================*/
create unique clustered index Relationship_1_PK on Relationship_1 (
Tag ASC,
"File ID" ASC
);

/*==============================================================*/
/* Index: Relationship_1_FK                                     */
/*==============================================================*/
create index Relationship_1_FK on Relationship_1 (
Tag ASC
);

/*==============================================================*/
/* Index: Relationship_2_FK                                     */
/*==============================================================*/
create index Relationship_2_FK on Relationship_1 (
"File ID" ASC
);

/*==============================================================*/
/* Table: Tags                                                  */
/*==============================================================*/
create table Tags 
(
   Tag                  varchar(1024)                  not null,
   Tag_Tag              varchar(1024),
   constraint PK_TAGS primary key (Tag)
);

/*==============================================================*/
/* Index: Tags_PK                                               */
/*==============================================================*/
create unique index Tags_PK on Tags (
Tag ASC
);

/*==============================================================*/
/* Index: "parent-child_FK"                                     */
/*==============================================================*/
create index "parent-child_FK" on Tags (
Tag_Tag ASC
);

alter table Relationship_1
   add constraint FK_RELATION_RELATIONS_TAGS foreign key (Tag)
      references Tags (Tag)
      on update restrict
      on delete restrict;

alter table Relationship_1
   add constraint FK_RELATION_RELATIONS_FILES foreign key ("File ID")
      references Files ("File ID")
      on update restrict
      on delete restrict;

alter table Tags
   add constraint "FK_TAGS_PARENT-CH_TAGS" foreign key (Tag_Tag)
      references Tags (Tag)
      on update restrict
      on delete restrict;

