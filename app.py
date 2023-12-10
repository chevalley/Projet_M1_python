from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import db
import objet as action

app = Flask(__name__)

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
        print(trouve)
        return render_template("inscription.html", first_try = False, already_exist = trouve)
        
        

if __name__ == "__main__" : 
    app.run(debug=True)