import sqlite3


#------------------------------------------------#

#Fonction manipulation base de donnée

connection = sqlite3.connect("./viticulture.db")

#cursor = connection.cursor()



#cursor.execute("SQL query")

def connect_db():
    return sqlite3.connect("./viticulture.db")

def adapte(sql_data):
    py_data = sql_data.fetchall()
    return py_data

#------------------------------------------------#
### Requêtes concernant la création des tables
### Commentées car utilisées qu'une fois

#query = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';" <----- permet de vérifier si la table existe déjà     
#cursor.execute(query)

#query = "CREATE TABLE Vin (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nom TEXTE, domaine TEXT, type TEXT, année INTEGER, region TEXT, note_m INTEGER, prix REAL);"
#cursor.execute(query)

#query = "CREATE TABLE Etagere (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, num INTEGER, region TEXT, capacite INTEGER, disponibilite INTEGER, id_cave INTEGER, FOREIGN KEY(id_cave) REFERENCES Cave(id));"
#cursor.execute(query)

#query = "CREATE TABLE Cave (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nb_etagere INTEGER, localisation TEXTE, nom TEXTE);"
#cursor.execute(query)

#query = "CREATE TABLE User (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, login TEXTE, mdp TEXTE, nom TEXTE, prenom TEXTE)"
#cursor.execute(query)

#query = "CREATE TABLE Possession (id_user INTEGER, id_cave INTEGER, FOREIGN KEY(id_user) REFERENCES User(id), FOREIGN KEY(id_cave) REFERENCES Cave(id));"
#cursor.execute(query)

#query = "CREATE TABLE Contenu (id_etagere INTEGER, id_vin INTEGER, quantite INTEGER, FOREIGN KEY(id_etagere) REFERENCES Etagere(id), FOREIGN KEY(id_vin) REFERENCES Vin(id));"
#cursor.execute(query)

#query = "CREATE TABLE Evaluation (id_user INTEGER, id_vin INTEGER, note_perso INTEGER, commentaire TEXT, FOREIGN KEY(id_user) REFERENCES User(id), FOREIGN KEY(id_vin) REFERENCES Vin(id));"
#cursor.execute(query)

connection.close()

#------------------------------------------------#

###Fonction d'usage
#Fonction en lien avec le user
def sql_check_dispo(login):
    query = "SELECT login FROM User WHERE login = '"+ login +"'; "
    return query

def sql_check_perso(nom, prenom):
    query = "SELECT nom, prenom FROM User WHERE nom = '"+ nom +"' AND prenom ='" + prenom + "'; "
    return query

def sql_new_user(login, mdp, nom, prenom):
    query = "INSERT INTO User (login, mdp, nom, prenom) VALUES ('" + login + "', '" + mdp + "', '" + nom + "', '" + prenom + "');"
    return query

def sql_authentification(login, mdp):
    query = "SELECT id, nom, prenom FROM User WHERE login = '" + login + "' AND mdp = '" + mdp + "' ;" 
    return query

#Fonction en lien avec les caves

def sql_new_cave(nb_etagere, localisation, nom):
    query = "INSERT INTO Cave (nb_etagere, localisation, nom) VALUES ('" + nb_etagere + "', '" + localisation + "', '" + nom + "');"
    return query

def sql_recup_id_new_cave():
    query = "SELECT id  FROM Cave WHERE id = (SELECT MAX(id) FROM Cave);"
    return query

def sql_link_cave(id_user, id_cave):
    query = "INSERT INTO Possession (id_user, id_cave) VALUES ('" + str(id_user) +"', '" + str(id_cave) + "');"
    return query

def sql_list_cave(id_user):
    query = "SELECT * FROM Possession JOIN Cave ON Possession.id_cave = Cave.id WHERE id_user = '" + str(id_user) + "' ;" 
    return query

def sql_unpossessed_cave(id_cave):
    query = "DELETE FROM Possession WHERE id_cave = '" + id_cave + "' ;"
    return query

def sql_remove_cave(id_cave):
    query = "DELETE FROM Cave WHERE id = '" + str(id_cave) + "' ;"
    return query

#Fonction en lien avec les étagères

def sql_list_etagere(id_cave): # ---> ne permet pas de récupérer le contenu : nécessité de créer une requête qui annoncera quelles bouteilles sont déjà présentes
    query = "SELECT * FROM Etagere WHERE id_cave = '" + id_cave + "' ;"
    return query

def sql_new_etagere(region, capacite, disponibilite, id_cave, num):
    query = "INSERT INTO Etagere (region, capacite, disponibilite, id_cave, num) VALUES ('" + region + "', '" + str(capacite) + "', '" + str(disponibilite) + "', '" + str(id_cave) + "', '" + str(num) + "') ;"
    return query

def sql_remove_all_etageres(id_cave):
    query = "DELETE FROM Etagere WHERE id_cave = '" + str(id_cave) + "'; "
    return query

#Fonction en lien avec les bouteilles
def sql_list_linked_wine(region):
    query = "SELECT * from Vin WHERE region = '" + region + "'; "
    return query

def sql_add_bottle(id_etagere, id_vin, quantite):
    query = "INSERT INTO Contenu (id_etagere, id_vin, quantite) VALUES ('" + id_etagere + "', '" + id_vin + "', '" + quantite + "') ;"
    return query

def sql_fill_etagere(dispo, id_etagere):
    query = "UPDATE Etagere SET disponibilite = '" + dispo + "' WHERE id = '"+ id_etagere +"' ;"
    return query

#def remove_bottles(id_etagere, id_vin, quantite): 
#----> prochaine requête à faire, nécessite de mettre au claire la recupération des bouteilles déjà présentes dans l'étagère
#----> devra potentiellement etre divisé en deux fonctions selon la qté de bouteilles du même types restantes dans l'étagère


#------------------------------------------------#

###Bric-à-Brac
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

