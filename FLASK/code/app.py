# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 12:25:50 2020

@author: Maël
"""
import os as os
from flask import Flask, render_template, url_for, flash, redirect
from forms import FormulaireInscription, FormulaireConnection

os.chdir("C:/Users/Maël/Projet-Info/FLASK/code")

app = Flask(__name__)

#la clé secrète permet de protéger l'application
app.config['SECRET KEY'] = '51f3f5f1841cfa6a80d484c73bb858c2'
posts = [
    {"auteurs" :" Romane, Clément, Hugo, Zacharie, Mael",
     "titre" : 'projet informatique',
     'date_publication' : ''
      }
    ]
@app.route('/api/accueil/')
def accueil():
    return render_template("accueil.html",posts=posts,title="Accueil")

@app.route('/api/classements/')
def classements():
    dictionnaire = {
        'nombre de points' : [],
        'classement au jeu de l_oie' : 0,
        'classement au puissance quatre' : 0
    }
    return jsonify(dictionnaire)


@app.route("/api/inscription", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Compte créé pour {form.username.data}!', 'success')
        return redirect(url_for('accueil'))
    return render_template('connection.html', title='Connection', form=form)


@app.route("/api/connection", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin' and form.password.data == 'password':
            flash('Connection établie', 'success')
            return redirect(url_for('home'))
        else:
            flash('Erreur d\'authentification, veuillez vérifier votre pseudonyme et votre mot de passe', 'danger')
    return render_template('inscription.html', title='Inscription', form=form)
    
if __name__ == "__main__":
    app.run(debug=True)