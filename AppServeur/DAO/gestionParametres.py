import sqlite3
from datetime import datetime
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()



def add_parametre(id_Partie,duree_tour, condition_victoire, Taille_plateau):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("INSERT INTO Parametres (id_partie, duree_tour, condition_victoire, taille_plateau) "
                       "VALUES (?, ?, ?, ?)", (id_Partie, duree_tour, condition_victoire, Taille_plateau,))
        con.commit()
    except:
        print("erreur dans add_param")

        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def verif_parametre(id_partie):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Parametres WHERE id_partie = ?",(id_partie,))
        verif_exist = cursor.fetchall()

    except:
        print("verif_tour_joueur")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
    if verif_exist == None:
        print("le execute renvoie none, erreur dans last_coup")
        raise ValueError
    elif verif_exist == [] :
        return False
    else :
        return True

def put_parametre(id_Partie,duree_tour, condition_victoire, Taille_plateau):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Parametres SET "
                       "duree_tour = ?, "
                       "condition_victoire = ?, "
                       "Taille_plateau = ? "
                       "WHERE id_partie = ?", (duree_tour, condition_victoire, Taille_plateau, id_Partie,))
        con.commit()
    except:
        print("erreur dans add_param")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()