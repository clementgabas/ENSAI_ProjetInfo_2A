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

def create_coup(id_partie):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute(f"CREATE TABLE Coup{id_partie} ('id_partie'	INTEGER, 'num_coup' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 'pseudo_joueur' INTEGER,'position' INTEGER, 'prochain_tour' INTEGER);",())
        con.commit()
    except:
        print("erreur dans create_coup")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
