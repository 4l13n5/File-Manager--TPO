import sqlite3

# https://www.sqlitetutorial.net/sqlite-python/

insert_command = 'INSERT INTO \"{}\"'\
                ' VALUES (\"{}\", \"{}\")'

select_command = "SELECT \"{}\" from \"{}\" WHERE tag = \"{}\""

delete_command = "DELETE FROM \"{}\" WHERE \"{}\""


def db_connect(sqlite3_file):
    con = None
    try:
        con = sqlite3.connect(sqlite3_file)
        return con
    except sqlite3.Error as err:
        print(err)
    return con

def db_max_id(con):
    cur = con.cursor()
    max = cur.execute("SELECT MAX(ID) FROM Datoteka").fetchall()[0][0]
    cur.close()
    return max

def db_custom(con,command):
    cur = con.cursor()
    output = cur.execute(command).fetchall()
    return output

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

def db_select(con, what, table, where):
    cur = con.cursor()
    cur.execute(select_command.format(what,table,where))
    return cur.fetchall()


def db_delete(con,table, where):
    cur = con.cursor()
    cur.execute(delete_command.format(table,where))

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
             "txt"  : "Document",
             "pdf" : "Document",
             "docx": "Document",
             "" : "Misc"}
    try:
        if list:
            return set([x for x in exte.values()])
        else:
            return exte[ext]
    except:
        return "Misc"


#internal use only
#if __name__ == "__main__":
#    def db_drop(con):
#        cur = con.cursor()
#        cur.execute("DROP TABLE files")






