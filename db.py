import sqlite3

connection = sqlite3.connect("./viticulture.db")

cursor = connection.cursor()


#cursor.execute("CREATE TABLE Vin (nom TEXTE, type TEXT, region TEXTE, note_p INTEGER);")

#query = """INSERT INTO Vin (nom, type, region, note_p) VALUES ("Bordelais", "Rouge", "Nouvelle-Aquitaine", 12);"""
#cursor.execute(query)
query = "INSERT INTO Vin (nom, type, region, note_p) VALUES ('Chigneron', 'Rosé', 'Auvergne-Rhône-Alpes', 20);"
cursor.execute(query)
print(connection.total_changes)
connection.commit()
connection.close()

connection = sqlite3.connect("./viticulture.db")
cursor = connection.cursor()
rows = cursor.execute("SELECT * FROM Vin")
data = rows.fetchall()
print(data) 
