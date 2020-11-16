import sqlite3
from datetime import datetime
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()


def add_partie(pseudo_chef, jeu, nb_places_tot):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        heure = str(datetime.now())
        cursor.execute(
            "INSERT INTO Parties (jeu, date_debut, pseudo_proprietaire, places_total, places_dispo, statut) "
            "VALUES (?,?,?,?,?, 'en préparation')", (jeu, heure, pseudo_chef, nb_places_tot, nb_places_tot,))
        cursor.execute("SELECT id_partie from Parties WHERE pseudo_proprietaire = ? "
                       "AND date_debut = ?", (pseudo_chef, heure))
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
        con = sqlite3.connect(db_address)
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
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT places_dispo FROM Parties WHERE id_partie = ?", (id_partie,))
        nb = cursor.fetchone()[0]
    except:
        print("erreur dans check_cb_places_libres")
        raise ConnectionAbortedError
    finally:
        con.close()
        return nb

def check_cb_places_tot(id_partie):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT places_total FROM Parties WHERE id_partie = ?", (id_partie,))
        nb = cursor.fetchone()[0]
    except:
        print("erreur dans check_cb_places_total")
        raise ConnectionAbortedError
    finally:
        con.close()
        return nb
    
def get_nbr_participants(id_partie):
    return check_cb_places_tot(id_partie) - check_cb_places_libres(id_partie)

def update_parties_nb_place(id_partie, nb_places_restantes):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Parties SET places_dispo = ? WHERE id_partie = ?", (nb_places_restantes, id_partie))
        con.commit()
    except:
        print("erreur dans update_parties_nb_places")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def add_to_participation(id_partie, pseudo, nb_places):
    if nb_places <1:
        print("il n'y a pas assez de place, erreur dans add_to_participation")
        raise ValueError
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("INSERT INTO Participation (pseudo, id_partie, ordre) VALUES (?, ?, 0);",(pseudo, id_partie))
        con.commit()
        update_parties_nb_place(id_partie, nb_places-1)
    except:
        print("erreur dans add_to_participation")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def delete_from_participation(id_partie, pseudo, nb_places):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("DELETE FROM Participation WHERE pseudo = ? AND id_partie = ?;", (pseudo, id_partie))
        con.commit()
        update_parties_nb_place(id_partie, nb_places+1)
    except:
        print("erreur dans delete_from_participation")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def delete_partie(id_partie):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("DELETE FROM Parties WHERE id_partie = ?;", (id_partie,))
        con.commit()
    except:
        print("erreur dans delete_partie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()


def get_membres_salle(id_salle):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT pseudo FROM Participation WHERE id_partie = ?;", (id_salle,))
        membres = cursor.fetchall()
    except:
        print("erreur dans voir_membres_salle")
        raise ConnectionAbortedError
    finally:
        con.close()
    return membres

def get_jeu_salle(id_salle):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT jeu FROM Parties WHERE id_partie = ?;", (id_salle,))
        membres = cursor.fetchall()
    except:
        print("erreur dans get_jeu_salle")
        raise ConnectionAbortedError
    finally:
        con.close()
    return membres

def lancer_partie(id_salle):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Parties SET statut = 'en cours', aquiltour = 1 WHERE id_partie = ?", (id_salle,))
        con.commit()
    except:
        print("erreur dans lancer_partie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_aquiltour(id_salle):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT aquiltour FROM Parties WHERE id_partie = ?", (id_salle,))
        aquiltour = cursor.fetchone()[0]
    except:
        print("erreur dans get_aquiltour")
        raise ConnectionAbortedError
    finally:
        con.close()
    return aquiltour

def update_aquiltour(id_salle):
    current_aquiltour, nbr_participant = get_aquiltour(id_salle), get_nbr_participants(id_salle)
    if current_aquiltour == nbr_participant:
        new_aquiltour = 1
    else:
        new_aquiltour = current_aquiltour+1
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Parties SET aquiltour = ? WHERE id_partie = ?", (new_aquiltour,id_salle))
        con.commit()
    except:
        print("erreur dans update_aquiltour")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
