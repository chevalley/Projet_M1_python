import db

class Cave : 

    def __init__(self, id = 0 ,  nb_etagere = 0, localisation = "unknown", nom = "unknown"):
        self.nb_etagere = nb_etagere
        self.localisation = localisation
        self.nom = nom
        self.id = id
    
    def new_cave(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_new_cave(self.nb_etagere, self.localisation, self.nom))
        connection.commit()
        row = cursor.execute(db.sql_recup_id_new_cave())
        id_new_cave = db.adapte(row)[0][0]
        for num in range(1, int(self.nb_etagere)+1):
            cursor.execute(db.sql_new_etagere("unknown", "0", "0", id_new_cave, num))
            connection.commit()
        connection.close()
        #print("dans new_cave de objet :", id_new_cave)
        return id_new_cave
    
    def linked_etagere(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_list_etagere(self.id))
        data = db.adapte(row)
        list_etagere = []
        for etagere in range(len(data)):
            #                       num                region           capacite      disponibilite             id
            etagere_actuelle = [data[etagere][1], data[etagere][2],data[etagere][3], data[etagere][4], data[etagere][0]]
            list_etagere.append(etagere_actuelle)
        #print(list_etagere)
        return list_etagere
    
    def del_cave(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_remove_all_etageres(self.id))
        connection.commit()
        cursor.execute(db.sql_unpossessed_cave(self.id))
        connection.commit()
        cursor.execute(db.sql_remove_cave(self.id))
        connection.commit()
        connection.close()
        #print("dans new_cave de objet :", id_new_cave)

class Etagère :
    def __init__(self, id_etagere, num = 0, region = "unknown", disponibilite = 0, capacite = 0, id_cave = 0):
        self.id = id_etagere
        self.num = num
        self.region = region
        self.disponibilite = disponibilite
        self.capacite = capacite 
        self.id_cave = id_cave

    def reconf(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        print("ici", self.id)
        cursor.execute(db.sql_conf_etagere(self.id, self.region, self.capacite, self.disponibilite))
        connection.commit()
        connection.close()

    def list_linked_wine(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        row =cursor.execute(db.sql_possessed_wine(self.id))
        data = db.adapte(row)
        connection.close()
        #print("là :",data)
        list_bouteille = []
        for linked_bouteille in range(len(data)):
            #print("là :", linked_bouteille)
            bouteille_actuelle = [data[linked_bouteille][1], data[linked_bouteille][2]]
            list_bouteille.append(bouteille_actuelle)
        return list_bouteille

    def info_etagere(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        row =cursor.execute(db.sql_select_etagere(self.id))
        data = db.adapte(row)
        connection.close()
        self.region = data[0][2]
        self.capacite = data[0][3]
        self.disponibilite = data[0][4]
        self.id_cave = data[0][5]

class Vin :
    def __init__(self, domaine, nom, type, année, region, note_perso, prix):
        self.domaine = domaine
        self.nom = nom
        self.type = type
        self.année = année
        self.region = region
        self.note_perso = note_perso
        self.prix = prix

    def list_all_wine():
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_list_wine())
        data = db.adapte(row)
        connection.close()
        list_vin = []
        for vin in range(len(data)):
            vin_actuel = [data[vin][1], data[vin][2], data[vin][3], data[vin][4], data[vin][5], data[vin][6]]
            list_vin.append(vin_actuel)
        return list_vin

    def list_all_region():
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_list_region())
        data = db.adapte(row)
        connection.close()
        list_region = []
        for vin in range(len(data)):
            region = [data[vin][0]]
            list_region.append(region[0])
        #print(list_region)
        return list_region

    def select_vin(list_vin_id):
        connection = db.connect_db()
        cursor = connection.cursor()
        list_data_vin = []
        for id_vin in list_vin_id:
            row = cursor.execute(db.sql_select_vin(id_vin))
            data = db.adapte(row)
            #print("ici", data)#      nom         domaine     type        année       prix
            list_data_vin.append([data[0][1], data[0][2], data[0][3], data[0][4], data[0][6]])
            #print("la", list_data_vin)
        connection.close()
        return list_data_vin

class User :
    def __init__(self, nom = "unknown", prenom = "unknown", login = "unknown", mdp = "unknown", id = 0):
        self.nom = nom
        self.prenom = prenom
        self.login = login
        self.mdp = mdp
        self.id = id

    def check_login_dispo(self, login):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_check_dispo(login))
        data = db.adapte(row)
        connection.close()
        return data

    def check_personnalite(self, prenom, nom):
            connection = db.connect_db()
            cursor = connection.cursor()
            row = cursor.execute(db.sql_check_perso(nom, prenom))
            data = db.adapte(row)
            connection.close()
            return data

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
        data = db.adapte(row)
        connection.close()
        return data

    def identification(self, nom, prenom, id):
        self.nom = nom
        self.prenom = prenom
        self.id = id

    def caves_perso(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_list_cave(self.id))
        data = db.adapte(row)
        connection.close()
        caves_trouvees = []
        for cave in range(len(data)) :  
            cave_actuelle = [data[cave][3], data[cave][4], data[cave][5], data[cave][1]]
            caves_trouvees.append(cave_actuelle)
        #print("ici : ", caves_trouvees)
        return caves_trouvees
    
    def link_cave(self, id_cave):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_link_cave(self.id, id_cave))
        connection.commit()
        connection.close()
        return 0
