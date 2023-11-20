class Cave : 

    def __init__(self, nb_etagere, localisation):
        self.nb_etagere = nb_etagere
        self.localisation = localisation


class Etagère :

    def __init__(self, id_etagere, region, disponibilite, contenance):
        self.num = id_etagere
        self.region = region
        self.disponibilite = disponibilite
        self.contenance = contenance


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
