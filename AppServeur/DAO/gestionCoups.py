import sqlite3
import DAO.gestion as DBgestion
import DAO.gestionParticipation as DBparticipation
db_address = DBgestion.get_db_address()

#foncr
def add_new_coup(id_partie, num_coup , pseudo_joueur, new_position, prochain_tour): #post
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO Coups (id_partie, num_coup , pseudo_joueur, position, prochain_tour "
                       "VALUES (?, ?, ?, ?,?)", (id_partie, num_coup , pseudo_joueur, new_position, prochain_tour,))
        con.commit()
    except:
        print("add_coup")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_last_coup(id_partie): #get
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT MAX(num_coup) FROM Coups WHERE id_partie = ? ",(id_partie,))
        last_coup = cursor.fetchone()
    except:
        print("verif_tour_joueur")
        raise ConnectionAbortedError
    finally:
        con.close()
    if last_coup == None:
        print("le execute renvoie none, erreur dans last_coup")
        raise ValueError
    return last_coup

def get_old_coup(id_partie, pseudo_joueur):
    try :
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Coups WHERE id_partie = ? AND pseudo_joueur = ?"
                   "ORDER BY num_coup DESC", (id_partie, pseudo_joueur,))
        old_coup = cursor.fetchone()
    except :
        print("get_old_coup")
        raise ConnectionAbortedError
    finally:
        con.close()
    if old_coup == None:
        #si ca renvoit None, c'est que c'est le premier tour du joueur. On ajotue donc le coup 0
        add_coup_zero(id_partie, pseudo_joueur)
        return get_old_coup(id_partie, pseudo_joueur)
    elif old_coup[4] > 1 :
        print("erreur dans get_old_coup")
        raise ValueError
    return old_coup


def add_coup_zero(id_partie, pseudo):
    position = DBparticipation.get_position_ordre(pseudo, id_partie)
    zero_value = position * 0.1
    try :
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("INSERT INTO Coups (id_partie, num_coup, pseudo_joueur, position, prochain_tour) VALUES (?,?,?,-1,1)", (id_partie,zero_value, pseudo,))
        con.commit()
    except :
        print("erreur dans add_coup_zero")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

