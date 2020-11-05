import sqlite3
from datetime import datetime


def add_partie(pseudo_chef, jeu, nb_places_tot):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        heure = str(datetime.now())
        cursor.execute(
            "INSERT INTO Parties (jeu, date_debut, pseudo_proprietaire, places_total, places_dispo) VALUES (?,?,?,?,?)", (jeu, heure, pseudo_chef, nb_places_tot, nb_places_tot-1,))
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

def add_to_participation(id_partie, pseudo):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO Participation (pseudo, id_partie) VALUES (?, ?);",(pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans add_to_participation")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def choix_couleur(id_partie, pseudo, couleur):
    pass