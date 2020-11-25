import sqlite3
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()

#-- does .. exist
def does_pseudo_exist(pseudo):
    """
    Fonction qui renvoie True si il existe dans la DB un utilisateur ayant ce pseudo, qui renvoie False sinon.

    :parameter
    ----------
    pseudo : str
        Pseudo dont on vérifie l'existance dans la DB.

    :raise
    ------
    ConnectionAbortedError
        Si une erreur se produit au cours de la communication avec la DB, l'erreur est levée..

    :return
    -------
    Bool : Bool
        Booléen qui précise si oui ou non le pseudo existe dans la DB.

    """
    Bool = False
    try: #on vérifie si le pseudo existe
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT identifiant FROM Utilisateur WHERE pseudo = ?", (pseudo,))
        ide = cursor.fetchone()
    except:
        print("erreur in does_pseudo_exist")
        raise ConnectionAbortedError
    finally:
        con.close()
    if ide == None: #le pseudo n'existe pas
        Bool = False
    else: #le pseudo existe
        Bool = True
    return Bool

def does_username_exist(username):
    """
    Fonction qui renvoie True si il existe dans la DB un utilisateur ayant cet identifiant, renvoie False sinon.

    :parameter
    ----------
    username : str
        Identifiant dont on cherche l'existance dans la DB.

    :raise
    ------
    ConnectionAbortedError
        Si une erreur se produit au cours de la communication avec la DB, l'erreur est levée.

    :return
    -------
    Bool : Bool
        Booléen qui précise si oui ou non l'identifiant existe dans la DB.

    """
    Bool = False
    try: #on vérifie si l'identifiant existe
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT pseudo FROM Utilisateur WHERE identifiant = ?", (username,))
        pse = cursor.fetchone()
    except:
        print("erreur in does_username_exist")
        raise ConnectionAbortedError
    finally:
        con.close()
    if pse == None: #le pseudo n'existe pas
        Bool = False
    else: #le pseudo existe
        Bool = True
    return Bool


#-- add ..
def add_user(username, pseudo, hpassword):
    """
    Procédure qui ajoute une utilisateur à la DB.

    :parameter
    ----------
    username : str
        Identifiant de l'utilisateur.
    pseudo : str
        Pseudo de l'utilisateur.
    hpassword : str
        Hash du mot de passe de l'utilisateur.

    :raise
    ------
    ConnectionAbortedError
        Si un erreur se produit au cours de la communication avec la DB,
        un rollback jusqu'au précédant commit à lieu et l'erreur est levée.

    :return
    -------
    None.

    """
    con = sqlite3.connect(db_address)
    cursor = con.cursor()
    try:
        cursor.execute(
            "INSERT INTO Utilisateur (pseudo, identifiant, mdp, est_connecte, en_file, en_partie)"
            " VALUES (?, ?, ?, 'False', 'False', 'False')",(pseudo, username, hpassword,))
        con.commit()
    except:
        print("erreur dans add_user")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def add_user_score(pseudo):
    """
        Procédure qui ajoute un utilisateur à la DB score.

        :parameter
        ----------
        pseudo : str
            Pseudo de l'utilisateur.

        :raise
        ------
        ConnectionAbortedError
            Si un erreur se produit au cours de la communication avec la DB,
            un rollback jusqu'au précédant commit à lieu et l'erreur est levée.

        :return
        -------
        None.

        """
    con = sqlite3.connect(db_address)
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO Scores (jeu, pseudo, nb_points, nb_parties_jouees, nb_parties_gagnees)"
                       " VALUES ('P4', ?, 1000, 0, 0)", (pseudo,))
        cursor.execute("INSERT INTO Scores (jeu, pseudo, nb_points, nb_parties_jouees, nb_parties_gagnees)"
                       " VALUES ('Oie', ?, 1000, 0, 0)", (pseudo,))
        con.commit()
    except:
        print("erreur dans add_user_score")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()


#-- get ..
def get_hpass_username(username):
    """
    Fonction qui renvoie le hash de mot de passe stocké dans la DB pour un identifiant donné.

    :parameter
    ----------
    username : str
        Identifiant associé au hmdp recherché.

    :raises
    ------
    ConnectionAbortedError
        Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
    ValueError
        pass

    :return
    -------
    hpass : str
        Renvoie le hash du mot de passe associé à l'identifiant en entrée.

    """
    try: #on récupère le hpass
        con = sqlite3.connect(db_address)
        cursor= con.cursor()
        cursor.execute("SELECT mdp FROM Utilisateur WHERE identifiant = ?", (username,))
        hpass = cursor.fetchone()
    except:
        print("Erreur dans get_hpass")
        raise ConnectionAbortedError
    finally:
        con.close()
    if hpass == None:
        print("le execute renvoie none, erreur dans get_hpass")
        raise ValueError
    return hpass[0]

def get_hpass_pseudo(pseudo):
    """
    Fonction qui renvoie le hash de mot de passe stocké dans la DB pour un pseudo donné.

    :parameter
    ----------
    pseudo : str
        pseudo associé au hmdp recherché.

    :raises
    ------
    ConnectionAbortedError
        Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
    ValueError
        pass

    :return
    -------
    hpass : str
        Renvoie le hash du mot de passe associé au pseudo en entrée.

    """
    try: #on récupère le hpass
        con = sqlite3.connect(db_address)
        cursor= con.cursor()
        cursor.execute("SELECT mdp FROM Utilisateur WHERE pseudo = ?", (pseudo,))
        hpass = cursor.fetchone()
    except:
        print("Erreur dans get_hpass")
        raise ConnectionAbortedError
    finally:
        con.close()
    if hpass == None:
        print("le execute renvoie none, erreur dans get_hpass")
        raise ValueError
    return hpass[0]

def get_pseudo(username):
    """
    Fonction qui renvoie le pseudo associé à un identifiant dans la DB

    :parameter
    ----------
    username : str
        Identifiant dont on souhaite le pseudo associé.

    :raises
    ------
    ConnectionAbortedError
        Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
    ValueError
        Si le pseudo n'existe pas.

    :return
    -------
    pseudo : str
        Pseudo associé à l'identifiant en entrée.

    """
    try: #on récupère le pseudo
        con = sqlite3.connect(db_address)
        cursor= con.cursor()
        cursor.execute("SELECT pseudo FROM Utilisateur WHERE identifiant = ?", (username,))
        pseudo = cursor.fetchone()
    except:
        print("erreur dans get_pseudo")
        raise ConnectionAbortedError
    finally:
        con.close()
    if pseudo == None:
        print("le execute renvoie none, erreur dans get_pseudo")
        raise ValueError
    return pseudo[0]

def get_est_connecte(username):
    """
        Fonction qui renvoie True si l'utilisateur ayant cet identifiant est connecté , renvoie False sinon.

        :parameter
        ----------
        username : str
            Identifiant dont on cherche l'existance dans la DB.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur se produit au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        Bool : Bool
            Booléen qui précise si oui ou non l'identifiant est connecté dans la DB.

    """
    try: #on récupère le pseudo
        con = sqlite3.connect(db_address)
        cursor= con.cursor()
        cursor.execute("SELECT est_connecte FROM Utilisateur WHERE identifiant = ?", (username,))
        est_co = cursor.fetchone()
    except:
        print("erreur dans get_pseudo")
        raise ConnectionAbortedError
    finally:
        con.close()
    if est_co == None:
        print("le execute renvoie none, erreur dans get_est_connecte")
        raise ValueError
    if est_co[0] == 'True':
        return True
    elif est_co[0] == 'False':
        return False
    else:
        print("le execute ne renvoie ni True ni False, erreur dans get_est_connecte")
        raise ValueError


#-- update ..
def update_est_connecte(ide, username_or_pseudo = 'username', nouvel_etat = 'True'):
    """
        Procédure qui permet de modifier la valeur est_connecté pour un utilisateur dans la DB en fonction de
        son pseudo ou de son identifiant.

        :parameter
        ----------
        ide : str
            nom de l'identifiant ou du pseudo de l'utilisateur dont on veut modifier la valeur du est_connecte.
        username_or_pseudo : str, optional
            Il faut préciser si le ide fournit correspond à l'identifiant ou au pseudo de l'utilisateur.
             username_or_pseudo est donc à valeur dans ('username', 'pseudo'). The default is 'username'.
        nouvel_etat : str, optional
            Il faut préciser si on veut mettre est_connecte à True ou à False.
            nouvel_etat est donc à valeur dans ('True','False'). The default is 'True'.

        :raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
        ValueError
            Si  :   - username_or_pseudo n'est ni égale au pseudo ni à l'identifiant
                    - nouvel_etat n'est pas un booléen

        :return
        -------
        None.

    """

    if not username_or_pseudo in ('username', 'pseudo'):
        print("username_or_pseudo doit prendre la valeur 'username' ou la valeur 'pseudo'!")
        raise ValueError
    if not nouvel_etat in ("True", "False"):
        print("nouvel_etat doit prendre la valeur 'True' ou 'False'!")
        raise ValueError
    if username_or_pseudo == 'username':
        try: #on update le statut "est_connecte" à True de l'utilisateur ayant l'username
            con = sqlite3.connect(db_address)
            cursor= con.cursor()
            cursor.execute("UPDATE Utilisateur SET est_connecte = ? WHERE identifiant = ?", (nouvel_etat, ide,))
            con.commit()
        except:
            print("erreur dans update_est_connecte")
            con.rollback()
            raise ConnectionAbortedError
        finally:
            con.close()
    elif username_or_pseudo == 'pseudo':
        try: #on update le statut "est_connecte" à True de l'utilisateur ayant le pseudo
            con = sqlite3.connect(db_address)
            cursor= con.cursor()
            cursor.execute("UPDATE Utilisateur SET est_connecte = ? WHERE pseudo = ?", (nouvel_etat, ide,))
            con.commit()
        except:
            print("erreur dans update_est_connecte")
            con.rollback()
            raise ConnectionAbortedError
        finally:
            con.close()

def update_en_partie_pseudo(pseudo, nouvel_etat):
    """
        Procédure qui permet de modifier la valeur en_partie pour un utilisateur dans la DB en fonction de son pseudo.

        :parameter
        ----------
        pseudo : str
            pseudo de l'utilisateur dont on veut modifier la valeur du en_partie.
        nouvel_etat : str
            Il faut préciser si on veut mettre en_partie à True ou à False.
            nouvel_etat est donc à valeur dans ('True','False')

        :raises
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
        ValueError
            Si nouvel_etat n'est pas un booléen.

        :return
        -------
        None.

    """
    if not nouvel_etat in ("True", "False"):
        print("nouvel_etat doit prendre la valeur 'True' ou 'False'!")
        raise ValueError
    try:  # on update le statut "en_partie" à True de l'utilisateur ayant le pseudo
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Utilisateur SET en_partie = ? WHERE pseudo = ?", (nouvel_etat, pseudo,))
        con.commit()
    except:
        print("erreur dans update_en_partie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_pseudo_table_utilisateur(old_pseudo, new_pseudo):
    """
        Procédure qui permet de mettre à jour le pseudo d'un utilisateur dans la table Utilisateurs.

        :parameter
        ----------
        old_pseudo : str
            pseudo de l'utilisateur qu'on veut modifier.
        new_pseudo : str
            pseudo de l'utilisateur qu'on veut mettre à la place.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.

    """
    try:  # on update le pseudo de l'utilisateur dans la table utilisateur
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Utilisateur SET pseudo = ? WHERE pseudo = ?", (new_pseudo, old_pseudo,))
        con.commit()
    except:
        print("erreur dans update_pseudo_table_utilisateur")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_pseudo_table_liste_amis(old_pseudo, new_pseudo):
    """
        Procédure qui permet de mettre à jour le pseudo d'un utilisateur dans la table Liste_Amis.

        :parameter
        ----------
        old_pseudo : str
            pseudo de l'utilisateur qu'on veut modifier.
        new_pseudo : str
            pseudo de l'utilisateur qu'on veut mettre à la place.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.

    """
    try:  # on update le pseudo de l'utilisateur dans la table liste amis
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Liste_Amis SET pseudo = ? WHERE pseudo = ?", (new_pseudo, old_pseudo,))
        cursor.execute("UPDATE Liste_Amis SET pseudo_ami = ? WHERE pseudo_ami = ?", (new_pseudo, old_pseudo,))
        con.commit()
    except:
        print("erreur dans update_pseudo_table_liste_ami")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_pseudo_table_score(old_pseudo, new_pseudo):
    """
        Procédure qui permet de mettre à jour le pseudo d'un utilisateur dans la table Scores.

        :parameter
        ----------
        old_pseudo : str
            pseudo de l'utilisateur qu'on veut modifier.
        new_pseudo : str
            pseudo de l'utilisateur qu'on veut mettre à la place.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.

    """
    try:  # on update le pseudo de l'utilisateur dans la table score
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Scores SET pseudo = ? WHERE pseudo = ?", (new_pseudo, old_pseudo,))
        con.commit()
    except:
        print("erreur dans update_pseudo_table_scores")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_pseudo_table_partie(old_pseudo, new_pseudo):
    """
        Procédure qui permet de mettre à jour le pseudo d'un utilisateur dans la table Parties.

        :parameter
        ----------
        old_pseudo : str
            pseudo de l'utilisateur qu'on veut modifier.
        new_pseudo : str
            pseudo de l'utilisateur qu'on veut mettre à la place.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.

    """
    try:  # on update le pseudo de l'utilisateur dans la table score
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Parties SET pseudo_proprietaire = ? WHERE pseudo_proprietaire = ?", (new_pseudo, old_pseudo,))
        con.commit()
    except:
        print("erreur dans update_pseudo_table_scores")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_pseudo_table_participation(old_pseudo, new_pseudo):
    """
        Procédure qui permet de mettre à jour le pseudo d'un utilisateur dans la table Participation.

        :parameter
        ----------
        old_pseudo : str
            pseudo de l'utilisateur qu'on veut modifier.
        new_pseudo : str
            pseudo de l'utilisateur qu'on veut mettre à la place.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.

    """
    try:  # on update le pseudo de l'utilisateur dans la table score
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Participation SET pseudo = ? WHERE pseudo = ?", (new_pseudo, old_pseudo,))
        con.commit()
    except:
        print("erreur dans update_pseudo_table_scores")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_pseudo_table_coup(old_pseudo, new_pseudo):
    """
        Procédure qui permet de mettre à jour le pseudo d'un utilisateur dans la table Coups.

        :parameter
        ----------
        old_pseudo : str
            pseudo de l'utilisateur qu'on veut modifier.
        new_pseudo : str
            pseudo de l'utilisateur qu'on veut mettre à la place.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.

    """
    try:  # on update le pseudo de l'utilisateur dans la table score
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Coups SET pseudo_joueur = ? WHERE pseudo_joueur = ?", (new_pseudo, old_pseudo,))
        con.commit()
    except:
        print("erreur dans update_pseudo_table_scores")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def update_pseudo(old_pseudo, new_pseudo):
    """
        Procédure qui permet de mettre à jour le pseudo d'un utilisateur dans les tables
        Scores, Utilisateurs, Liste_Amis, Parties, Participation et Coups
        via les fonctions : update_pseudo_table_utilisateur(old_pseudo, new_pseudo),
                            update_pseudo_table_liste_amis(old_pseudo, new_pseudo),
                            update_pseudo_table_score(old_pseudo, new_pseudo),
                            update_pseudo_table_partie(old_pseudo, new_pseudo),
                            update_pseudo_table_participation(old_pseudo, new_pseudo),
                            update_pseudo_table_coup(old_pseudo, new_pseudo),
        :parameter
        ----------
        old_pseudo : str
            pseudo de l'utilisateur qu'on veut modifier.
        new_pseudo : str
            pseudo de l'utilisateur qu'on veut mettre à la place.

        :raise
        ------
        None

        :return
        -------
        None.

    """
    update_pseudo_table_utilisateur(old_pseudo, new_pseudo)
    update_pseudo_table_liste_amis(old_pseudo, new_pseudo)
    update_pseudo_table_score(old_pseudo, new_pseudo)
    update_pseudo_table_partie(old_pseudo, new_pseudo)
    update_pseudo_table_participation(old_pseudo, new_pseudo)
    update_pseudo_table_coup(old_pseudo, new_pseudo)

def update_password(pseudo, new_hpassword):
    """
        Procédure qui permet de modifier le mot de passe pour un utilisateur dans la table Utilisateurs
        en fonction de son pseudo.

        :parameter
        ----------
        pseudo : str
            pseudo de l'utilisateur dont on veut modifier le mot de passe.
        new_hpassword : str
            nouveau mot de passe hashé

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.

    """
    try:  # on update le mdp dans la table utilisateur
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Utilisateur SET mdp = ? WHERE pseudo = ?", (new_hpassword, pseudo))
        con.commit()
    except:
        print("erreur dans update_password")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_stat(pseudo):
    """
    Fonction qui renvoie les statistique personnelles associées à un pseudo dans la table Utilisateurs.

    :parameter
    ----------
    pseudo : str
        pseudo dont on souhaite les statistique personnelles associées.

    :raise
    ------
    ConnectionAbortedError
        Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

    :return
    -------
    stat_perso : list
        Liste à un élément : le couple [nb_parties_jouees, nb_parties_gagnees].

    """
    try:  # on récupère les info interessante
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT SUM(nb_parties_jouees), SUM(nb_parties_gagnees) FROM Scores WHERE pseudo = ?", (pseudo,))
        stat_perso = cursor.fetchall()
    except:
        print("ERROR : API.afficher stat perso :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return stat_perso

def update_stat(pseudo):
    """
        Procédure qui réinitialise les statistique personnelles associées à un pseudo dans la table Utilisateurs.

        :parameter
        ----------
        pseudo : str
            pseudo de l'utilisateur dont on veut modifier le mot de passe.

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.
    """
    try:  # on update le mdp dans la table utilisateur
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Scores SET nb_points = 1000, nb_parties_jouees = 0, nb_parties_gagnees = 0 WHERE pseudo = ?", (pseudo,))
        con.commit()
    except:
        print("erreur dans update_stat")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()


#-- put
def put_all_users_disconnected():
    """
        Procédure qui réinitialise la valeur de est_connecte en False pour tous les utilisateurs
        dans la table Utilisateurs.

        :parameter
        ----------
        None

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.
    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Utilisateur SET est_connecte = 'False', en_file = 'False', en_partie = 'False'"
                       " WHERE est_connecte = 'True'", ())
        con.commit()
    except:
        print("erreur dans put_all_users_disconnected")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()


#-- delete
def delete_user_pseudo(pseudo):
    """
        Procédure qui supprime tous les éléments de la table Utilisateurs à un pseudo associé.

        :parameter
        ----------
        pseudo : str
            pseudo de l'utilisateur que l'on veut supprimer .

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        None.
    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("DELETE FROM Utilisateur WHERE pseudo = ?", (pseudo,))
        con.commit()
    except:
        print("erreur dans delete_user_pseudo")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()