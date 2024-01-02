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
    if list_id_cave == []:
        return render_template("lobby.html", nb_cave = 0)
    else:
        
        return render_template("lobby.html", list_id_cave)

if __name__ == "__main__" : 
    app.run(debug=True, host = "0.0.0.0", port = 80)