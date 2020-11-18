import sqlite3
import DAO.gestion as DBgestion
import DAO.gestionParticipation as DBparticipation
db_address = DBgestion.get_db_address()

#foncr
def add_new_coup(id_partie, num_coup , pseudo_joueur, new_position, prochain_tour): #post
    """
        Procédure qui enregistre un nouveau coup
        composé de id_partie, num_coup , pseudo_joueur, new_position et prochain_tour

        Parameters
        ----------
        id_partie : int
            identifiant de la partie auquelle on ajoute un nouveau coup
        num_coup : float
            numéro du coup à ajouter
        pseudo_joueur : str
            pseudo du joueur qui a joué ,ou non, le coup à ajouter
        new_position : int
            position du joueur à la suite du coup à ajouter
        prochain_tour : int
            entier qui défini si le joueur peut jouer son coup la prochaine fois que ce sera son tour

        Raise
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
             un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Return
        -------
        None.
    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("INSERT INTO Coups (id_partie, num_coup ,pseudo_joueur, position, prochain_tour) "
                       "VALUES (?, ?, ?, ?,?)", (id_partie, num_coup , pseudo_joueur, new_position, prochain_tour,))
        con.commit()
    except:
        print("erruer dans add_new_coup")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_last_coup(id_partie): #get
    """
        Fonction qui retourne le dérnier coup joué dans la partie

        Parameters
        ----------
        id_partie : int
            identifiant de la partie

        Raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
        ValueError
            Si une erreur a lieu dans la valeur récupéré lors de la requète SQL

        Return
        -------
        last_coup : tuple
            Tuple contenant le numéro du dernier coup joué dans la partie

    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT MAX(num_coup) FROM Coups WHERE id_partie = ? ",(id_partie,))
        last_coup = cursor.fetchone()
    except:
        print("verif_tour_joueur")
        raise ConnectionAbortedError
    finally:
        con.close()
    if last_coup == None:
        print("le execute renvoie none, erreur dans get_last_coup")
        raise ValueError
    return last_coup

def get_old_coup(id_partie, pseudo_joueur):
    """
        Fonction qui retourne le dérnier coup joué dans la partie

        Parameters
        ----------
        id_partie : int
            identifiant de la partie
        pseudo_joueur : text
            pseudo du joueur à qui c'est le tour

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
        ValueError
            Si une erreur a lieu dans la valeur prochain_tour est superieure à 1 lors de la requète SQL

        Return
        -------
        old_coup : tuple
                Tuple contenant l'identifiant de la partie, numéro du dernier coup joué par le joueur,
                le pseudo du joueur, la position du joueur et l'état du joueur au prochain tour.

    """
    try :
        con = sqlite3.connect(db_address)
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
    """
        Procédure qui enregistre le coup initial de la partie
        composé de id_partie, num_coup -compris entre 0 et 1 exclu-, pseudo_joueur,
        new_position égal à -1 et prochain_tour égal à 1

        Parameters
        ----------
        id_partie : int
            identifiant de la partie auquelle on ajoute un nouveau coup
        pseudo_joueur : str
                pseudo du joueur qui a joué ,ou non, le coup à ajouter

        Raise
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
             un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Return
        -------
        None.
    """
    position = DBparticipation.get_position_ordre(pseudo, id_partie)
    zero_value = position * 0.1
    try :
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("INSERT INTO Coups (id_partie, num_coup, pseudo_joueur, position, prochain_tour)"
                       " VALUES (?,?,?,-1,1)", (id_partie,zero_value, pseudo,))
        con.commit()
    except :
        print("erreur dans add_coup_zero")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_all_coups(id_partie):
    """
           Fonction qui retourne tous les coups joués dans la partie.

           Parameters
           ----------
           id_partie : int
               identifiant de la partie

           Raise
           ------
           ConnectionAbortedError
               Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

           Return
           -------
           liste_coups : list
                   Tuple contenant l'identifiant de la partie, numéro du coup ,
                   le pseudo du joueur, la position du joueur et son état au prochain tour pour tous les
                   coups joués dans la partie.
       """
    try :
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Coups WHERE id_partie = ? AND num_coup >= 1 ORDER BY num_coup ASC", (id_partie,))
        liste_coups = cursor.fetchall()
    except :
        print("erreur dans get_all_coup")
        raise ConnectionAbortedError
    finally:
        con.close()
    return liste_coups

def delete_all_coups(id_partie):
    """
        Procédure qui supprime tous le coups de la partie.

        Parameter
        ----------
        id_partie : int
            identifiant de la partie auquelle on veut supprimer tous les coups


        Raise
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
             un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Return
        -------
        None.
    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("DELETE FROM Coups WHERE id_partie = ?;", (id_partie,))
        con.commit()
    except:
        print("erreur dans delete_all_coups")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
