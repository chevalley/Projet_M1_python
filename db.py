import sqlite3

connection = sqlite3.connect("./viticulture.db")
###SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'; <----- permet de vérifier si la table existe déjà     
cursor = connection.cursor()


query = "CREATE TABLE Vin (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nom TEXTE, type TEXT, region TEXTE, note_p INTEGER);"
cursor.execute(query)

query = "CREATE TABLE Etagere (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, region TEXT, capacite INTEGER, disponibilite INTEGER, id_cave INTEGER NOT NULL FOREIGN KEY);"
cursor.execute(query)

query = "CREATE TABLE Cave (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nb_etagere INTEGER, localisation TEXTE);"
cursor.execute(query)

query = "CREATE TABLE User (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, login TEXTE, mdp TEXTE, nom TEXTE, prenom TEXTE)"
cursor.execute(query)

query = "CREATE TABLE Possession (id_user INTERGER NOT NULL FOREIGN KEY, id_cave INTEGER NOT NULL FOREIGN KEY);"
cursor.execute(query)

query = "CREATE TABLE Contenu (id_etagere INTERGER NOT NULL FOREIGN KEY, id_vin INTEGER NOT NULL FOREIGN KEY, quantite INTEGER);"
cursor.execute(query)

query = "CREATE TABLE Evaluation (id_user INTEGER NOT NULL FOREIGN KEY, id_vin INTEGER NOT NULL FOREIGN KEY);"
cursor.execute(query)


connection.close()

def new_user(login, mdp):
    query = "INSERT INTO User (login, mdp) VALUES (" + login + ", " + mdp + ");"
    return query

def authentification(login, mdp):
    query = "SELECT id, nom, prenom FROM User WHERE login = " + login + " AND mdp = " + mdp + " ;" 
    return query

def new_cave(nb_etagere, localisation, id_user):
    query1 = "INSERT INTO Cave (nb_etagere, localisation) VALUES (" + nb_etagere + ", " + localisation + ");"
    id_cave = "SELECT id  FROM Cave WHERE id = (SELECT MAX(id) FROM Cave);"
    query2 = "INSERT INTO Possession (id_user, id_cave) VALUES (" + id_user +", " + id_cave + ")"
    return query1, query2

def share_cave(id_user, id_cave):
    query = "INSERT INTO Possession (id_user, id_cave) VALUES (" + id_user + ", " + id_cave + ");"
    return query

def list_cave(id_user):
    query = "SELECT * FROM Possession JOIN Cave ON Possession.id_cave = Cave.id WHERE id_user = " + id_user + " ;" 
    return query

def remove_cave(id_cave):
    query = "DELETE FROM Cave WHERE id = " + id_cave + " ;"
    return query

def list_etagere(id_cave): # ---> ne permet pas de récupérer le contenu : nécessité de créer une requête qui annoncera quelles bouteilles sont déjà présentes
    query = "SELECT * FROM Etagere WHERE id_cave = " + id_cave + " ;"
    return query

def new_etagere(region, capacite, disponibilite, id_cave):
    query = "INSERT INTO Etagere (region, capacite, disponibilite, id_cave) VALUES (" + region + ", " + capacite + ", " + disponibilite + ", " + id_cave + ") ;"
    return query

def remove_etagere(id_etagere):
    query = "DELETE FROM Etagere WHERE id = " + id_etagere + "; "
    return query

def list_linked_wine(region):
    query = "SELECT * from Vin WHERE region = " + region + "; "
    return query

def add_bottles(id_etagere, id_vin, quantite, dispo):
    query1 = "INSERT INTO Contenu (id_etagere, id_vin, quantite) VALUES (" + id_etagere + ", " + id_vin + ", " + quantite + ") ;"
    query2 = "UPDATE Etagere SET disponibilite = " + dispo + " WHERE id = "+ id_etagere +" ;"
    return query1, query2

#def remove_bottles(id_etagere, id_vin, quantite): 
#----> prochaine requête à faire, nécessite de mettre au claire la recupération des bouteilles déjà présentes dans l'étagère
#----> devra potentiellement etre divisé en deux fonctions selon la qté de bouteilles du même types restantes dans l'étagère

#query = "INSERT INTO Vin (nom, type, region, note_p) VALUES ("Bordelais", "Rouge", "Nouvelle-Aquitaine", 12);"
#cursor.execute(query)
#query = "INSERT INTO Vin (nom, type, region, note_p) VALUES ('Chigneron', 'Rosé', 'Auvergne-Rhône-Alpes', 20);"
#cursor.execute(query)
#print(connection.total_changes)
#connection.commit()


#connection = sqlite3.connect("./viticulture.db")
#cursor = connection.cursor()
#rows = cursor.execute("SELECT * FROM Vin")
#data = rows.fetchall()
#print(data) 
