import sqlite3
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()
liste_couleurs_autorisees = ['bleu', 'rouge', 'vert', 'jaune', 'magenta', 'cyan', 'gris']

def update_est_pret(pseudo, id_partie, TrueOrFalse):
    """
        Procédure qui met à jour le bouléen est_pret dans la table Participation pour un jouur particulier,
        dans une salle particulière

        Parameters
        ----------
        pseudo: str
            pseudo du joueur qui signale si il est prêt ou non
        id_Partie : int
            identifiant de la partie
        TrueOrFalse : str
            reponse du joueur, à savoir si il est prêt ou non

        Raises
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
            un rollback jusqu'au commit précédant a lieu et l'erreur est levée.
        ValueError
            Si l'argument TrueOrFalse n'est ni 'true' ni 'false'.

        Returns
        -------
        None.
    """

    TrueOrFalse = TrueOrFalse.lower()
    if TrueOrFalse not in ('true', 'false'):
        print("L'argument TrueOrFalse doit être 'True' ou 'False'.")
        raise ValueError
    if TrueOrFalse.lower() == 'true':
        TrueOrFalse = 'True'
    elif TrueOrFalse.lower() =='false':
        TrueOrFalse = 'False'
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Participation SET est_pret = ? "
                       "WHERE pseudo = ? AND id_partie = ?", (TrueOrFalse,pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans uptade_est_pret")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_ordre(id_partie):
    """
        Fonction qui retourne les joueurs et l'odre dans lequel ils vont jouer cette partie.

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
        ordre : list
                Liste contenant le couple le pseudo et l'ordre dans lequel il vont jouer la partie, tout cela ordonnée
                par ordre croissant.

    """

    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT pseudo, ordre FROM Participation WHERE id_partie = ? ORDER BY ordre ASC", (id_partie,))
        ordre = cursor.fetchall()
    except:
        print("erreur dans get_ordre")
        raise ConnectionAbortedError
    finally:
        con.close()
    return ordre

def get_position_ordre(pseudo, id_partie):
    """
        Fonction qui retourne l'odre dans lequel un joueur en particulier va jouer son tour.

        Parameters
        ----------
        id_partie : int
            identifiant de la partie
        pseudo: str
            pseudo du joueur
        Raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.


        Returns
        -------
        ordre : int
                Entier définissant l'ordre du joueur en question.

    """

    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT ordre FROM Participation WHERE id_partie = ? AND pseudo = ?", (id_partie,pseudo,))
        ordre = cursor.fetchall()[0][0]
    except:
        print("erreur dans get_position_ordre")
        raise ConnectionAbortedError
    finally:
        con.close()
    return ordre

def update_ordre(pseudo, id_partie):
    """
        Procédure qui met à jour l'ordre de passage d'un joueur dans une partie
        Cette procédure est faite dans la table Participation

        Parameters
        ----------
        pseudo: str
            pseudo du joueur à qui on doit mettre à jour l'ordre de passage
        id_partie : int
            identifiant de la partie dans laquelle on met à jour l'odre de passage

        Raises
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
            un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Returns
        -------
        None.
    """
    ordre_dernier_joueur_actuel = get_ordre(id_partie)[-1][1]
    ordre_pseudo = ordre_dernier_joueur_actuel+1

    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Participation SET ordre = ? "
                       "WHERE pseudo = ? AND id_partie = ? ", (ordre_pseudo, pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans update_ordre")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_used_color(id_partie):
    """
        Fonction qui retourne la liste des couleurs déjà choisies par les joueurs d'une partie.

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
        liste : list
                Liste des couleurs déjà prises dans la partie en question.

    """

    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT couleur FROM Participation WHERE id_partie = ?", (id_partie,))
        liste_couleur = cursor.fetchall()
    except:
        print("erreur dans get_used_color")
        raise ConnectionAbortedError
    finally:
        con.close()
    liste = []
    for elem in liste_couleur:
        liste.append(elem[0])
    return liste

def get_free_color(id_partie):
    """
        Fonction qui retourne la liste des couleurs encore disponibles pour les joueurs d'une partie.

        Parameters
        ----------
        id_partie : int
            identifiant de la partie
        Raises
        ------
        None ######

        Returns
        -------
        liste : list
                Liste des couleurs encore disponibles dans la partie en question.

    """

    used_colors = get_used_color(id_partie)
    free_color_list = []
    for col in liste_couleurs_autorisees:
        if col not in used_colors:
            free_color_list.append(col)
    return free_color_list

def is_color_free(id_partie, color):
    """
        Fonction qui retourne un booléen selon la disponibilitée d'une couleur dans une partie

        Parameters
        ----------
        id_partie : int
            identifiant de la partie
        color : str
            couleur en question

        Raises
        ------
        None

        Returns
        -------
        Bool :
            True :
                Si la couleur est disponible dans cette partie.
            False :
                Si la couleur est déja prise par un autre joueur.

    """

    used_colors = get_used_color(id_partie)
    if color in used_colors:
        return False
    return True

def update_color(pseudo, id_partie, color):
    """
        Procédure qui attribu à un joueur la couleur choisie dans une partie
        Cette procédure est faite dans la table Participation

        Parameters
        ----------
        pseudo: str
            pseudo du joueur qui a choisi une couleur
        id_partie : int
            identifiant de la partie dans laquelle le joueur a fait son choix
        color : str
            couleur choisie par le joueur pour cette partie

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
        cursor.execute("UPDATE Participation SET couleur = ? WHERE pseudo = ? AND id_partie = ? "
                       , (color, pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans update_color")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_couleur(pseudo, id_partie):
    """
        Fonction qui retourne un la couleur choisie par un joueur particulier dans une partie

        Parameters
        ----------
        pseudo: str
            pseudo du joueur auquel on cherche à savoir la couleur choisie
        id_partie : int
            identifiant de la partie

        Raises
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
            un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Returns
        -------
        couleur : str
            Couleur attribuée au joueur.

    """

    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT couleur FROM Participation WHERE pseudo = ? AND id_partie = ? ", (pseudo, id_partie))
        couleur = cursor.fetchone()[0]
    except:
        print("erreur dans get_couleur")
        raise ConnectionAbortedError
    finally:
        con.close()
    return couleur

def number_of_ready(id_partie):
    """
        Fonction qui retourne le nombre de joueur prêt dans la partie

        Parameters
        ----------
        id_partie : int
            identifiant de la partie

        Raises
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB,
            un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

        Returns
        -------
        nombre : int
            Nombre de joueur actuellement prêt à jouer dans la partie.
    """

    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(est_pret) FROM Participation"
                       " WHERE est_pret = 'True' AND id_partie = ?", (id_partie,))
        nombre = cursor.fetchone()[0]
    except:
        print("erreur dans number_of_ready")
        raise ConnectionAbortedError
    finally:
        con.close()
    return nombre