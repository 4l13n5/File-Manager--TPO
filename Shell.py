import os
import shutil

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
        print("Nedefinnirana napaka.")



    except FileNotFoundError:
        print("Izvorna datoteka ne obstaja.")
    except FileExistsError:
        print("Ciljna datoteka že obstaja.")
    except IndexError:
        print("Nepravilna sintaksa.")

def list(command):
    try:
        list = ["\\" + x if os.path.isdir(x) else x for x in os.listdir(command[1])]
        for x in list:
            print(x+"  ",end="")
    except FileNotFoundError:
        print("Datoteka ne obstaja")
    except IndexError:
        list = ["\\" + x if os.path.isdir(x) else x for x in os.listdir(".")]
        for x in list:
            print(x+"  ",end="")

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

def find_l(file,dir):
    match = []
    list = [x for x in os.listdir(dir)]
    for x in list:
        if x == file:
            match.append(os.path.abspath(x))
        if os.path.isdir(x):
            match.extend(find_l(file,x))

    return match


def read_command(command):
    call = command.split(" ")
    if call[0] == "cd":
        changedir(call)
    elif call[0] == "cp":
        move(call)
    elif call[0] == "mv":
        move(call,True)
    elif call[0] == "ls":
        list(call)
    elif call[0] == "mkfile":
        makef(call)
    elif call[0] == "rm":
        remove(call)
    elif call[0] == "mkdir":
        maked(call)
    elif call[0] == "fil":
        fil(call)

    elif call[0] == "exit":
        return True
    else:
        return False
    print("\n" + os.getcwd())





os.scandir(".")
print(os.getcwd())

while(1):
    command = input()
    if read_command(command):
        break
