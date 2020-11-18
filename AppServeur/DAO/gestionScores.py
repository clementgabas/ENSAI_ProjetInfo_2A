import sqlite3
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()

def get_nb_parties_jouees(pseudo, jeu):
    """
            Fonction qui renvoie le nombre de partie jouées pour un utilisateur.

            :parameter
            ----------
            pseudo : str
                Pseudo pour pour lequel on renvoie le nombre de partie jouées
            jeu : str
                Nom du jeu demandé

            :raise
            ------
            ConnectionAbortedError
                Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

            :return
            -------
            nombre : int
                Le nombre de partie jouées pour un utilisateur.

    """
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
    """
            Fonction qui renvoie le nombre de partie gagnées pour un utilisateur.

            :parameter
            ----------
            pseudo : str
                Pseudo pour pour lequel on renvoie le nombre de partie gagnées
            jeu : str
                Nom du jeu demandé

            :raise
            ------
            ConnectionAbortedError
                Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

            :return
            -------
            nombre : int
                Le nombre de partie gagnées pour un utilisateur.

    """
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
    """
            Procédure qui met à jour le nombre de partie jouées pour un utilisateur.

            :parameter
            ----------
            pseudo : str
                Pseudo pour pour lequel on renvoie le nombre de partie jouées
            jeu : str
                Nom du jeu demandé
            new_value : int
                nouvelle valeur du nombre de partie jouées

            :raise
            ------
            ConnectionAbortedError
                Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

            :return
            -------
            None

    """
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
    """
            Procédure qui met à jour le nombre de partie gagnées pour un utilisateur.

            :parameter
            ----------
            pseudo : str
                Pseudo pour pour lequel on renvoie le nombre de partie gagnées
            jeu : str
                Nom du jeu demandé
            new_value : int
                nouvelle valeur du nombre de partie gagnées

            :raise
            ------
            ConnectionAbortedError
                Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

            :return
            -------
            None

    """
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