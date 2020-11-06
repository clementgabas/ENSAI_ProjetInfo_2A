import sqlite3
from datetime import datetime

def add_parametre(id_Partie,duree_tour, condition_victoire, Taille_plateau):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO Parametres (id_Partie, duree_tour, condition_victoire, Taille_plateau) "
                       "VALUES (?, ?, ?, ?)", (id_Partie, duree_tour, condition_victoire, Taille_plateau,))
        con.commit()
    except:
        print("erreur dans add_amitie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()