import sqlite3

connection = sqlite3.connect("./viticulture.db")
###SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'; <----- permet de vérifier si la table existe déjà     
cursor = connection.cursor()

#query = "CREATE TABLE Vin (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nom TEXTE, type TEXT, region TEXTE, note_p INTEGER);"
#cursor.execute(query)
query = "CREATE TABLE Etagere (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, region TEXT, contenance INTEGER, disponibilite INTEGER);"
cursor.execute(query)
query = "CREATE TABLE Cave (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nb_etagere INTEGER, localisation TEXTE);"
cursor.execute(query)



#query = """INSERT INTO Vin (nom, type, region, note_p) VALUES ("Bordelais", "Rouge", "Nouvelle-Aquitaine", 12);"""
#cursor.execute(query)
#query = "INSERT INTO Vin (nom, type, region, note_p) VALUES ('Chigneron', 'Rosé', 'Auvergne-Rhône-Alpes', 20);"
#cursor.execute(query)
print(connection.total_changes)
connection.commit()
connection.close()

connection = sqlite3.connect("./viticulture.db")
cursor = connection.cursor()
rows = cursor.execute("SELECT * FROM Vin")
data = rows.fetchall()
print(data) 


