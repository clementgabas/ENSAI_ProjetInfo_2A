import sqlite3
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()

def get_nb_parties_jouees(pseudo, jeu):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT nb_parties_jouees FROM Scores WHERE pseudo = ? AND jeu = ?", (pseudo,jeu,))
        nombre = cursor.fetchone()[0]
    except:
        print("erreur in get_nb_parties_jouees")
        raise ConnectionAbortedError
    finally:
        con.close()
    return nombre

def get_nb_parties_gagnees(pseudo, jeu):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT nb_parties_gagnees FROM Scores WHERE pseudo = ? AND jeu = ?", (pseudo, jeu))
        nombre = cursor.fetchone()[0]
    except:
        print("erreur in get_nb_parties_gagnees")
        raise ConnectionAbortedError
    finally:
        con.close()
    return nombre

def update_nb_parties_jouees(pseudo, jeu, new_value):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Scores SET nb_parties_jouees = ? WHERE pseudo = ? AND jeu = ?", (new_value, pseudo,jeu,))
        con.commit()
    except:
        print("erreur in update_nb_parties_jouees")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_nb_parties_gagnees(pseudo, jeu, new_value):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Scores SET nb_parties_gagnees = ? WHERE pseudo = ? AND jeu = ?",
                       (new_value, pseudo, jeu,))
        con.commit()
    except:
        print("erreur in update_nb_parties_jouees")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()