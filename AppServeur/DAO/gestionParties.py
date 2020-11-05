import sqlite3
from datetime import datetime


def add_partie(pseudo_chef, jeu, nb_places_tot):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        heure = str(datetime.now())
        cursor.execute(
            "INSERT INTO Parties (jeu, date_debut, pseudo_proprietaire, places_total, places_dispo) VALUES (?,?,?,?,?)", (jeu, heure, pseudo_chef, nb_places_tot, nb_places_tot,))
        cursor.execute("SELECT id_partie from Parties WHERE pseudo_proprietaire = ? AND date_debut = ?", (pseudo_chef, heure))
        id_partie = cursor.fetchone()[0]
        con.commit()
    except:
        print("erreur dans add_partie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
    return id_partie

def does_partie_exist(id_partie):
    try:
        Bool = True
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT jeu FROM Parties where id_partie = ?", (id_partie,))
        id_partie = cursor.fetchone()
    except:
        print("erreur dans does_partie_exist")
        raise ConnectionAbortedError
    finally:
        con.close()
    if id_partie == None:
        Bool = False
    return Bool

def check_cb_places_libres(id_partie):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT places_dispo FROM Parties WHERE id_partie = ?", (id_partie,))
        nb = cursor.fetchone()[0]
    except:
        print("erreur dans check_cb_places_libres")
        raise ConnectionAbortedError
    finally:
        con.close()
        return nb


def add_to_participation(id_partie, pseudo, nb_places):
    if nb_places <1:
        print("il n'y a pas assez de place, erreur dans add_to_participation")
        raise ValueError
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO Participation (pseudo, id_partie) VALUES (?, ?);",(pseudo, id_partie))
        cursor.execute("UPDATE Parties SET places_dispo = ? WHERE id_partie = ?", (nb_places-1, id_partie))
        con.commit()
    except:
        print("erreur dans add_to_participation")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def choix_couleur(id_partie, pseudo, couleur):
    pass