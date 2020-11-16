import sqlite3
from datetime import datetime
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()



def add_parametre(id_Partie,duree_tour, condition_victoire, Taille_plateau):
    """
        Procédure qui enregistre de nouveaux paramètres
        couposéés de id_Partie, duree_tour , condition_victoire et Taille_plateau

        Parameters
        ----------
        id_Partie : int
            identifiant de la partie auquelle on modifie les paramètres
        duree_tour : int
            durée pour jouer son coup
        condition_victoire : int
            condition de victoire pour remporter la partie
        Taille_plateau : int
            Taille du plateau de jeu

        Raises
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
             un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Returns
        -------
        None.
        """
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
    """
        Fonction qui vérifie si la partie a déjà des paramètres

        Parameters
        ----------
        id_partie : int
            identifiant de la partie

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        Booléen :
            True si des paramètres ont déjà été définis.
            False sinon



    """
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

def put_parametre(id_Partie, duree_tour, condition_victoire, Taille_plateau):
    """
        Procédure qui met à jour de les paramètres
        couposéés de id_Partie, duree_tour , condition_victoire et Taille_plateau

        Parameters
        ----------
        id_Partie : int
            identifiant de la partie auquelle on modifie les paramètres
        duree_tour : int
            durée pour jouer son coup
        condition_victoire : int
            condition de victoire pour remporter la partie
        Taille_plateau : int
            Taille du plateau de jeu

        Raises
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
             un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Returns
        -------
        None.
        """

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