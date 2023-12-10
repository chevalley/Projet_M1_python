import db

class Cave : 

    def __init__(self, nb_etagere, localisation):
        self.nb_etagere = nb_etagere
        self.localisation = localisation


class Etagère :

    def __init__(self, id_etagere, region, disponibilite, capacite):
        self.num = id_etagere
        self.region = region
        self.disponibilite = disponibilite
        self.capacite = capacite


class Vin :
    def __init__(self, domaine, nom, type, année, region, commentaires, note_perso, photo, prix):
        self.domaine = domaine
        self.nom = nom
        self.type = type
        self.année = année
        self.region = region
        self.commentaire = commentaires
        self.note_perso = note_perso
        self.photo = photo
        self.prix = prix

class User :
    def __init__(self, nom, prenom, login, mdp):
        self.nom = nom
        self.prenom = prenom
        self.login = login
        self.mdp = mdp

    def check_login_dispo(self, login):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_check_dispo(login))
        connection.close()
        data = db.adapte(row)
        print(vars(data))
        

    def inscryption(self, nom, prenom, login, mdp):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_new_user(login, mdp, nom, prenom))
        connection.commit()
        connection.close()
    
    def verification(self, login, mdp):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_authentification(login, mdp))
        connection.close()
        data = db.adapte(row)
        print(vars(data))