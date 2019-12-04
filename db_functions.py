import sqlite3

# https://www.sqlitetutorial.net/sqlite-python/

create_command = "CREATE TABLE IF NOT EXISTS files (\
                                filename text NOT NULL,\
                                tag text\
                                );"

insert_command = 'INSERT INTO files'\
                ' VALUES (\"{}\", \"{}\")'

select_command = "SELECT rowid, filename, tag from files WHERE tag = \"{}\""

delete_command = "DELETE FROM files where tag = \"{}\""


def db_create(sqlite3_file):
    con = None
    try:
        con = sqlite3.connect(sqlite3_file)
        cursor = con.cursor()
        cursor.execute(create_command)
        return con
    except sqlite3.Error as err:
        print(err)
    return con


def db_insert(con, filename, tag):
    cur = con.cursor()
    cur.execute(insert_command.format(filename, tag))
    con.commit()


def db_select(con, tag):
    cur = con.cursor()
    cur.execute(select_command.format(tag))
    return cur.fetchall()


def db_delete(con, tag):
    cur = con.cursor()
    cur.execute(delete_command.format(tag))

#internal use only
if __name__ == "__main__":
    def db_drop(con):
        cur = con.cursor()
        cur.execute("DROP TABLE files")


def test():
    con = db_create("/home/nikocar1103/Desktop/dbfile.db")
    db_insert(con, "neki.py", "pyfile")
    db_insert(con, "neki2.c", "cfile")
    db_insert(con, "neki3.c", "cfile")
    print(db_select(con, "cfile"))
    db_drop(con)
    con.close()

if __name__ == "__main__":
    test()
