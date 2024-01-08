from flask import Flask, render_template, request, redirect, session
import secrets
import objet as action

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inscription", methods=["GET","POST"])
def inscryption():

    if request.method=="GET":
        return render_template("inscription.html", first_try = True)
    elif request.method=="POST":
        login = request.form["login"]
        mdp = request.form["mdp"]
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        new_user = action.User(nom, prenom, login, mdp)
        trouve = action.User.check_login_dispo(new_user, login)
        occurence = action.User.check_personnalite(new_user, prenom, nom)
        if (trouve != [] or occurence != []):  
            return render_template("inscription.html", first_try = False, already_exist = trouve, already_has_account = occurence)
        else:
            action.User.inscryption(new_user, nom, prenom, login, mdp)
            session["new_user"] = True
            return redirect("/connexion")
        
@app.route("/connexion", methods=["GET", "POST"])
def identification():

    if request.method=="GET":
        if 'new_user' in session:
            session.pop("new_user", None)
            return render_template("connexion.html", new_user = True)
        else:
            return render_template("connexion.html")
        
    if request.method=="POST":
        login = request.form["login"]
        mdp = request.form["mdp"]
        user = action.User(login = login, mdp = mdp)
        trouve = action.User.verification(user, login, mdp)
        #print(trouve)
        if trouve != []:
            id = trouve[0][0]
            nom = trouve[0][1]
            prenom = trouve[0][2]
            action.User.identification(user, nom, prenom, id)
            #print(user.nom, user.prenom)
            session["id"] = id
            session["nom"] = nom
            session["prenom"] = prenom
            session["login"] = user.login
            return redirect("/lobby")
        else:
            return render_template("connexion.html", not_found = True)

@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    user = action.User(session["nom"], session["prenom"], session["login"], id = session["id"])
    list_id_cave = action.User.caves_perso(user)
    #print("nb_cave",list_id_cave)
    if list_id_cave == None :
        return render_template("lobby.html", nb_cave = 0, connecte = True)
    else:  
        return render_template("lobby.html", list_cave = list_id_cave, connecte = True)
    
@app.route("/add_cave", methods=["GET", "POST"])
def add_cave():
    nom_cave = request.form["nom"]
    nb_etageres = request.form["nb_etageres"]
    localite = request.form["localisation"]
    cave = action.Cave(nb_etagere = nb_etageres, localisation = localite, nom = nom_cave)
    id_new_cave = action.Cave.new_cave(cave)
    #print(id_new_cave)
    user = action.User(session["nom"], session["prenom"], session["login"], id = session["id"])
    action.User.link_cave(user, id_new_cave)
    return redirect("/lobby")

@app.route("/del_cave", methods=["GET", "POST"])
def del_cave():
    id_cave_to_del = request.form["id"]
    #print("popopo : ", id_cave_to_del)
    cave = action.Cave(id=id_cave_to_del)
    action.Cave.del_cave(cave)
    return redirect("/lobby")

@app.route("/modify_cave", methods=["GET", "POST"])
def la_cave():
    #user = action.User(session["nom"], session["prenom"], session["login"], id = session["id"])
    if request.method=="POST":
        id_cave = request.form["id"]
        session["cave"] = id_cave
    else:
        id_cave = session["cave"]
    cave = action.Cave(id=id_cave)
    linked_etagere = action.Cave.linked_etagere(cave)
    return render_template("cave.html", list_etagere = linked_etagere, connecte = True)

@app.route("/deconnexion", methods=["GET", "POST"])
def deconnexion():
    session.clear()
    return redirect("/")

@app.route("/bouteille", methods=["GET", "POST"])
def bouteilles():
    list_vin = action.Vin.list_all_wine()
    return render_template("bouteille.html", list_bouteille = list_vin, connecte = True)

@app.route("/modify_etagere", methods=["GET", "POST"])
def conf_etagere():
    id_etagere = request.form["id"]
    session["id_etagere"] = id_etagere
    list_wine_region = action.Vin.list_all_region()
    return render_template("configure_etagere.html", connecte = True, list_region = list_wine_region)

@app.route("/reconfigure_etagere", methods=["GET", "POST"])
def reconf_etagere():
    region_etagere = request.form["Région"]
    capacité_etagere = request.form["capacité"]
    dispo_etagere = capacité_etagere
    id_etagere = session["id_etagere"]
    etagere = action.Etagère(id_etagere = id_etagere, region = region_etagere, capacite = capacité_etagere, disponibilite = dispo_etagere)
    action.Etagère.reconf(etagere)
    return redirect("/modify_cave")

if __name__ == "__main__" : 
    app.run(debug=True, host = "0.0.0.0", port = 80)