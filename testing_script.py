import sqlite3
import db_functions as dbf
import Shell

# pot do testne mape
test_path = "C:\\Users\\nGregor\\Desktop\\TPOtest"

# pot do baze , ki se ostvari ob klicu funkcije startup() v Shell.py; trenutno ime baze nastavljeno na "db.db"
db_path = ".\\db.db"

# inicializacija baze in povezava na njo
Shell.startup(test_path)
cur = sqlite3.connect(db_path).cursor()

# pridobi celotne tabele
table_datoteka = cur.execute("SELECT * FROM Datoteka;").fetchall()
table_tag = cur.execute("SELECT * FROM Tag").fetchall()
table_oznacuje = cur.execute("SELECT * FROM Oznacuje").fetchall()

# izpisi podatke vsake tabele
print("Tabela Datoteka:")
for data in table_datoteka:
    print(data)
print("\nTabela Tag:")
for data in table_tag:
    print(data)
print("\nTabela Oznacuje:")
for data in table_oznacuje:
    print(data)


''' TESTIRANJE RAZREDA ZA HIERARHIJO TAGOV '''

# povezi se na pravilno bazo (v bazi "db.db" ni dodanih dodatnih tagov)
hierarchy_db = ".\\testing_hierarchy.db"
con = sqlite3.connect(hierarchy_db)

# ustvari objekt tipa TagDicts
td = dbf.TagDicts(con)
# izpisi hierarhicno strukturo tagov
print("\n\n\nHierarhija tagov v", hierarchy_db + ":")
td.print_tree()

# naziv taga, za katerega hocemo pridobiti pot
my_tag = "Metal"

path1 = td.format_tag_path(my_tag)   # default: vrni pot od taga do roota, vkljucno z root tagom
path2 = td.format_tag_path(my_tag, add_root=False)   # vrni pot od taga do roota, brez root taga
path3 = td.format_tag_path(my_tag, reverse=True)   # vrni pot od roota do taga, vkljucno z root tagom
path4 = td.format_tag_path(my_tag, add_root=False, reverse=True)    # vrni pot od roota do taga, brez root taga

# izpise vse zgoraj pridobljene poti
print("\n\nIzpis formatiranih poti za tag \"" + my_tag + "\":")
for path in [path1, path2, path3, path4]:
    print(path)
