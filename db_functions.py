import sqlite3
from os import path

# https://www.sqlitetutorial.net/sqlite-python/

insert_command = 'INSERT INTO \"{}\"'\
                ' VALUES (\"{}\", \"{}\")'

select_command = "SELECT Datoteka.ID, Datoteka.Path " \
         "FROM Datoteka " \
         "JOIN oznacuje on Datoteka.ID=oznacuje.ID " \
         "JOIN Tag ON oznacuje.Tag = Tag.Tag " \
         "WHERE Tag.Tag=\'{}\'"

delete_command = "DELETE FROM \"{}\" where tag = \"{}\""

import os

folder_path = os.path.dirname(os.path.realpath(__file__))

create_command = open(folder_path + path.sep + "FileS.sql", "r").read().split("////")

def db_connect(sqlite3_file):
    con = None
    try:
        f = False
        if not path.exists(folder_path + path.sep + "file.db"):
            f = True
        con = sqlite3.connect(folder_path + path.sep + sqlite3_file)
        cur = con.cursor()
        if f:
            for str in create_command:
                cur.execute(str)
        return con
    except sqlite3.Error as err:
        print(err)
    return con

def db_max_id(con):
    cur = con.cursor()
    max = cur.execute("SELECT MAX(ID) FROM Datoteka").fetchall()[0][0]
    cur.close()
    return max


def db_insert_file(con, abspath):
    cur = con.cursor()
    try:
        fileID = db_max_id(con)+1
    except:
        fileID=1
    cur.execute(insert_command.format("Datoteka",fileID, abspath))
    db_update_linker(con,fileID,extension_index(abspath.split('.')[-1]))
    con.commit()

def db_insert_tag(con, tag, parent):
    cur = con.cursor()
    cur.execute(insert_command.format("Tag",tag, parent))
    con.commit()

def db_update_linker(con,fileID,tag):
    cur = con.cursor()
    cur.execute(insert_command.format("oznacuje",fileID, tag))
    con.commit()

def db_select(con, tag):
    cur = con.cursor()
    cur.execute(select_command.format(tag))
    return cur.fetchall()


def db_delete(con, tag):
    cur = con.cursor()
    cur.execute(delete_command.format(tag))

def extension_index(ext,list=False):
    exte = { "png" : "Picture",
             "jpg" : "Picture",
             "bmp" : "Picture",
             "jpeg": "Picture",
             "gif" : "Picture",
             "mp4" : "Video",
             "mov" : "Video",
             "mkv" : "Video",
             "avi" : "Video",
             "webm": "Video",
             "mp3" : "Audio",
             "wav" : "Audio",
             "flac" : "Audio",
             "" : "Misc"}
    try:
        if list:
            return set([x for x in exte.values()])
        else:
            return exte[ext]
    except:
        return "Misc"


#internal use only
if __name__ == "__main__":
    def db_drop():
        os.remove(folder_path + path.sep + "file.db")

def db_custom(con,command):
    cur = con.cursor()
    output = cur.execute(command).fetchall()
    return output


select_command = "SELECT * from Datoteka"
select2 = "SELECT * from Tag"
select3 = "SELECT * from oznacuje"

select = "SELECT Datoteka.ID, Datoteka.Path " \
         "FROM Datoteka " \
         "JOIN oznacuje on Datoteka.ID=oznacuje.ID " \
         "JOIN Tag ON oznacuje.Tag = Tag.Tag " \
         "WHERE oznacuje.Tag=\'{}\'"



if __name__ == "__main__":

    db_drop()
    con = db_connect("file.db")

    #Dodamo file in tage
    db_insert_file(con, "neki/neki/neki.neki")
    db_insert_tag(con, "Misc", "root")
    db_insert_file(con, "neki/neki.png")
    db_insert_tag(con, "Picture", "root")

    #Izpišemo Datoteka tabelo
    print(db_custom(con, select_command))
    #izpišemo Tag tabelo
    print(db_custom(con, select2))
    #Izpišemo označuje tabelo
    print(db_custom(con, select3))

    #Selectamo vse
    print(db_custom(con, select.format("Picture")))
    print(db_custom(con, select.format("Misc")))



