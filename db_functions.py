from collections import defaultdict
import sqlite3
import os

# https://www.sqlitetutorial.net/sqlite-python/

"""
DATABASE STRUCTURE:
Datoteka(FID, Filepath, Filename)
Tag(TName, Parent)
Oznacuje(FileID, TagName)
"""

# universal commands
insert_command = 'INSERT OR REPLACE INTO \"{}\" VALUES (\"{}\", {})'   # ze obstaja -> ni napake, prepise oz. posodobi
insert_command2 = 'INSERT INTO \"{}\" VALUES (\"{}\", {})'   # originalen univerzalen insert
select_command = "SELECT \"{}\" FROM \"{}\" WHERE {}"
delete_command = "DELETE FROM \"{}\" WHERE {}"

# path to .sql file for database creation
creation_filepath = "./FileS.sql"

# list of commands for database creation; read from creation_filepath
with open(creation_filepath) as creation_file:
    creation_commands = creation_file.read().split("////")


# povezi se na bazo; ustvari bazo, ce ne obstaja
def db_connect(sqlite3_file):
    con = None
    try:
        db_exists = True if not os.path.exists(sqlite3_file) else False  # check if database exists
        con = sqlite3.connect(sqlite3_file)
        cur = con.cursor()
        if db_exists:
            for command in creation_commands:
                cur.execute(command)
    except sqlite3.Error as err:
        print(err)
    return con


# vrne najvecji FID (tabela Datoteka)
def db_max_id(con):
    cur = con.cursor()
    max_id = cur.execute("SELECT MAX(FID) FROM Datoteka").fetchone()[0]
    cur.close()
    return max_id


# vrne rezultat poljubne poizvedbe; command = poljubna poizvedba
def db_custom(con, command):
    cur = con.cursor()
    output = cur.execute(command).fetchall()
    return output


# funkcija za vstavljanje v tabelo Datoteka
def db_insert_file(con, abspath, filename, extension_tag=False):
    cur = con.cursor()
    try:
        fileID = cur.execute(select_command.format("FID", "Datoteka", "Filepath = \"" + abspath + "\"")).fetchone()[0]
    except:
        try:
            fileID = db_max_id(con) + 1
        except:
            fileID = 1
    path_and_name = "\"" + abspath + "\", \"" + filename + "\""
    cur.execute(insert_command.format("Datoteka", fileID, path_and_name))
    if extension_tag:
        db_update_linker(con, fileID, extension_index(abspath.split('.')[-1].lower()))
    con.commit()


# funkcija za vstavljanje v tabelo Tag
def db_insert_tag(con, tag, parent):
    cur = con.cursor()
    if parent != "null":
        parent = "\"" + parent + "\""
    cur.execute(insert_command.format("Tag", tag, parent))
    con.commit()


# funkcja za vstavljanje v tabelo Oznacuje
def db_update_linker(con, fileID, tag):
    cur = con.cursor()
    tag = "\"" + tag + "\""
    cur.execute(insert_command.format("Oznacuje", fileID, tag))
    con.commit()


# izvede zeljen SELECT stavek in vrne celoten rezultat
def db_select(con, what, table, where):
    cur = con.cursor()
    cur.execute(select_command.format(what, table, where))
    return cur.fetchall()


# funkcija, s katero se izvaja brisanje iz baze
def db_delete(con, table, where):
    cur = con.cursor()
    cur.execute(delete_command.format(table, where))


# vrne pripadajoce ime taga glede na koncnico datoteke oz. seznam tagov, ce velja list=True
def extension_index(ext, list=False):
    exte = {"png": "Picture",
            "jpg": "Picture",
            "bmp": "Picture",
            "jpeg": "Picture",
            "gif": "Picture",
            "mp4": "Video",
            "mov": "Video",
            "mkv": "Video",
            "avi": "Video",
            "webm": "Video",
            "mp3": "Audio",
            "wav": "Audio",
            "flac": "Audio",
            "txt": "Document",
            "pdf": "Document",
            "docx": "Document",
            "": "Misc"}
    try:
        if list:
            exte_tags = []
            for tag in exte.values():
                if tag not in exte_tags:
                    exte_tags.append(tag)
            return exte_tags
        else:
            return exte[ext]
    except:
        return "Misc"


# class for retrieving information about tag hierarchy
class TagDicts:
    children_dict = defaultdict(lambda: [])
    parents_dict = {}

    def __init__(self, con):
        cur = con.cursor()
        tag_table = cur.execute("select * from tag").fetchall()
        for child, parent in tag_table:
            if parent is not None:
                self.children_dict[parent].append(child)
                self.parents_dict[child] = parent

    # prints out hierarchical dependency of tags
    def print_tree(self, root_name="ROOT", depth=""):
        print(root_name)
        for value in self.children_dict[root_name]:
            print(depth + "|__", end="")
            self.print_tree(value, depth + "|  ")

    # returns list of path from stated tag to root node
    def from_tag_to_root(self, tag):
        to_root_path = [tag]
        current = tag
        while current != "ROOT":
            to_root_path.append(self.parents_dict[current])
            current = self.parents_dict[current]
        return to_root_path

    # returns path from tag to root in string form
    # add_root -> defines if root node included
    # reverse=False -> tag to root; reverse=True root to tag
    def format_tag_path(self, tag, add_root=True, reverse=False):
        to_root_path = self.from_tag_to_root(tag)
        if not add_root:
            to_root_path.remove("ROOT")
        if reverse:
            to_root_path = to_root_path[::-1]
        format_string = ""
        for node in to_root_path:
            format_string += node
            format_string += "->"
        return format_string[:-2]


# internal use only
# if __name__ == "__main__":
#    def db_drop(con):
#        cur = con.cursor()
#        cur.execute("DROP TABLE files")
