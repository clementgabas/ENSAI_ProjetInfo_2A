import sqlite3
from datetime import datetime
import DAO.gestion as DBgestion

db_address = DBgestion.get_db_address()


def add_partie(pseudo_chef, jeu, nb_places_tot):
    """
        Fonction qui enregistre une nouvelle partie dans la table Parties et qui retourne le numéro de la partie

        Parameters
        ----------
        pseudo_chef : str
            pseudo du joueur chef, celui qui crée la salle
        jeu : str
            Nom du jeu sur lequel va se jouer la partie
        nb_places_tot : int
            nombre de place maximale dans la partie

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        id_partie : int
            identifiant de la salle qui est aussi celui de la partie.

    """

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
    """
        Fonction qui verifie l'existence d'une partie via la table Parties

        Parameters
        ----------
        id_partie : int
            identifiant de la partie qui est recherchée

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        bool :
            False : Si l'identifiant de la partie n'est pas dans la tabble Parties, donc si la partie n'existe pas.
            True : Sinon

    """

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
    """
        Fonction qui verifie le nombre de places libres dans une partie via la table Parties

        Parameters
        ----------
        id_partie : int
            identifiant de la partie qui est vérifiée

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        nb : int
            Nombre de place libre qu'il y a dans la partie

    """
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
    """
        Fonction qui verifie le nombre total de places dans une partie via la table Parties

        Parameters
        ----------

        id_partie : int
            identifiant de la partie qui est vérifiée

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        nb : int
            Nombre total de place qu'il y a dans la partie

    """
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
    """
        Fonction qui verifie le nombre de participant dans une partie les fonctions
        check_cb_places_tot et check_cb_places_libres

        Parameters
        ----------
        id_partie : int
            identifiant de la partie qui est vérifiée

        Raises
        ------
        None

        Returns
        -------
        type = int :
            Nombre de particimpant qu'il y a dans la partie

    """

    return check_cb_places_tot(id_partie) - check_cb_places_libres(id_partie)


def update_parties_nb_place(id_partie, nb_places_restantes):
    """
        Procédure qui met à jour le nombre  de places restante dans une partie via la table Parties

        Parameters
        ----------
        id_partie : int
            identifiant de la partie qui est à mettre à jour
        nb_places_restantes : int
            nombre de place restante à mettre à jour

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        None
    """
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
    """
        Procédure qui met à jour le nombre  de places restante dans une partie via la table Parties

        Parameters
        ----------
        id_partie : int
            identifiant de la partie qui est à mettre à jour
        pseudo : str
            pseudo du joueur qui rejoint la partie
        nb_places : int
            nombre de place restante dans la partie que rejoins le joueur.

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
        ValueError
            Si le nombre de place restante dans la partie est nulle, le joueur ne peut rejoindre la partie car il n'y a
            plus de place pour lui

        Returns
        -------
        None
    """
    if nb_places < 1:
        print("il n'y a pas assez de place, erreur dans add_to_participation")
        raise ValueError
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("INSERT INTO Participation (pseudo, id_partie, ordre) VALUES (?, ?, 0);", (pseudo, id_partie))
        con.commit()
        update_parties_nb_place(id_partie, nb_places - 1)
    except:
        print("erreur dans add_to_participation")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()


def delete_from_participation(id_partie, pseudo, nb_places):
    """
        Procédure qui supprime un participant d'une partie via la table Participation et qui met à jouer le nombre de
        places restantes dans la table Parties

        Parameters
        ----------
        id_partie : int
            identifiant de la partie qui est à mettre à jour
        pseudo : str
            pseudo du joueur qui rejoint la partie
        nb_places : int
            nombre de place restante dans la partie avant que le joueur ne la quitte.

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        None
    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("DELETE FROM Participation WHERE pseudo = ? AND id_partie = ?;", (pseudo, id_partie))
        con.commit()
        update_parties_nb_place(id_partie, nb_places + 1)
    except:
        print("erreur dans delete_from_participation")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()


def delete_partie(id_partie):
    """
        Procédure qui supprime une partie via la table Parties.

        Parameters
        ----------
        id_partie : int
            identifiant de la partie qui est à supprimer

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        None
    """
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
    """
        Fonction qui renvoie tous les participants présent dans une salle.

        Parameters
        ----------
        id_salle : int
            identifiant de la partie (i.e salle) qui est vérifiée

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        membre : list
            Liste contenant les pseudos des membres présent dans la salle.

    """
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
    """
        Fonction qui renvoie le jeu pour lequel la salle a été créée via la table Parties.

        Parameters
        ----------
        id_salle : int
            identifiant de la partie (i.e salle) qui est vérifiée

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        jeu : list
            Liste à un élément contenant le jeu pour lequel la salle a été créée.

    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT jeu FROM Parties WHERE id_partie = ? ;", (id_salle,))
        jeu = cursor.fetchall()
    except:
        print("erreur dans get_jeu_salle")
        raise ConnectionAbortedError
    finally:
        con.close()
    return jeu


def lancer_partie(id_salle):
    """
        Procédure qui lance une partie, via la table Parties en mettant à jour les valeurs de statut et aquiltour.

        Parameters
        ----------
        id_salle : int
            identifiant de la partie qui est à mettre à jour

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        None
    """
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


def get_aquiltour(id_salle):  ##
    """
        Fonction qui renvoie le numéro du joueur qui doit jouer via la table Parties.

        Parameters
        ----------
        id_salle : int
            identifiant de la partie (i.e salle) qui est vérifiée

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        aquiltour : int
            Numéro du joueur qui doit jouer son tour dans la partie

    """
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
    """
        Procédure qui met à jour le numero du joueur qui doit jouer, via la table Parties,
        en mettant à jour la valeur de aquiltour.

        Parameters
        ----------
        id_salle : int
            identifiant de la partie qui est à mettre à jour

        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        Returns
        -------
        None
    """
    current_aquiltour, nbr_participant = get_aquiltour(id_salle), get_nbr_participants(id_salle)
    if current_aquiltour == nbr_participant:
        new_aquiltour = 1
    else:
        new_aquiltour = current_aquiltour + 1
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Parties SET aquiltour = ? WHERE id_partie = ?", (new_aquiltour, id_salle))
        con.commit()
    except:
        print("erreur dans update_aquiltour")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
