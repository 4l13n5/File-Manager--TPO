import os
import shutil
import db_functions as db
import  sqlite3 as sq
import numpy

def changedir(command):
    os.chdir(command[1])

def overwrite(path):
    if os.path.isfile(path):
            print("Prepiši datoteko? y/n")
            i = input()
            if i == "y":
                return True
            else:
                return False
    if os.path.isdir(path):
        print("Prepisovanje map ni dovoljeno.")
        return False
    return True

def move(command,remove=False):
    try:
        if os.path.isdir(command[2]):
            command[2] = command[2]+"\\"+command[1]
        if overwrite(command[2]):
            shutil.copy(command[1],command[2])
            if remove:
                os.remove(command[1])
        return
    except:
        print("Nedefinirana napaka.")

def list(command):
    try:
        list = [os.path.abspath(x) for x in os.listdir(command[1])]
        return list

    except FileNotFoundError:
        print("Datoteka ne obstaja")
    except IndexError:
        list = [os.path.abspath(x) for x in os.listdir(".")]
        return list

def makef(command):
    try:
        if overwrite(command[1]):
            open(command[1],"w+")
        else:
            return
    except ValueError:
        print("Nepravilen vnos.")
    except IndexError:
        print("Nepravilna sintaksa.")

def maked(command):

    if os.path.isfile(command[1]):
        print("Obstaja datoteka z enakim imenom.")
        return
    elif os.path.isdir(command[1]):
        print("Prepisovanje map ni dovoljeno.")
        return
    else:
        os.mkdir(command[1])

def remove(command):
    try:
        os.remove(command[1])
    except IndexError:
        print("Nepravilna sintaksa.")
    except FileNotFoundError:
        print("Datoteka ne obstaja")

def fil(command):
    list = find_l(command[1],".")
    for x in list:
        print(x)
    return

def find_l(dir):
    match = []
    for subdir, dirs, files in os.walk(dir,topdown=True):
        for x in files:
            match.append(os.path.join(os.path.abspath(subdir),x))
    return match

def ls_printer(object):
    for x in object:
        print(x+"  ",end="")

def fls(fold):
    all = list(["",fold])
    for x in all:
        if os.path.isdir(x):
            all.extend(fls(x))
    return all

def fls_printer(object):
    for x in object:
        print(x+"  \n",end="")





def read_command(command):
    call = command.split(" ")
    if call[0] == "cd":
        changedir(call)
    elif call[0] == "cp":
        move(call)
    elif call[0] == "mv":
        move(call,True)
    elif call[0] == "ls":
        ls_printer(list(call))
    elif call[0] == "mkfile":
        makef(call)
    elif call[0] == "rm":
        remove(call)
    elif call[0] == "mkdir":
        maked(call)
    elif call[0] == "fil":
        fil(call)
    elif call[0] == "fls":
        fls_printer(fls("."))

    elif call[0] == "exit":
        return True
    else:
        return False
    print("\n" + os.getcwd())

def startup(folder):
    con = sq.connect(".\\dbs.db")
    filelist = find_l(folder)
    db.db_insert_tag(con,"ROOT","ROOT")
    for x in db.extension_index("",True):
        db.db_insert_tag(con,x,"ROOT")
    for x in filelist:
        db.db_insert_file(con,x)

    return

con = sq.connect(".\\dbs.db")
cur = con.cursor()
a=cur.execute("SELECT * FROM Tag")


startup('D:\Wallpaper')
