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
    return render_template("connexion.html")
    
if __name__ == "__main__" : 
    app.run(debug=True)