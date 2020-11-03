import sqlite3

def does_pseudo_exist(pseudo):
    """
    Fonction qui renvoit True si il existe dans la DB un utilisateur ayant ce pseudo, qui renvoit False sinon.

    Parameters
    ----------
    pseudo : str
        Pseudo dont on vérifie l'existance dans la DB.

    Raises
    ------
    ConnectionAbortedError
        Si une erreur se produit au cours de la communication avec la DB, l'erreur est levée..

    Returns
    -------
    Bool : Bool
        Booléen qui précise si oui ou non le pseudo existe dans la DB.

    """
    Bool = False
    try: #on vérifie si le pseudo existe
        con = sqlite3.connect("database/apijeux.db")
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
    Fonction qui renvoit True si il existe dans la DB un utilisateur ayant cet identifiant, renvoit False sinon.

    Parameters
    ----------
    username : str
        Identifiant dont on cherche l'existance dans la DB.

    Raises
    ------
    ConnectionAbortedError
        Si une erreur se produit au cours de la communication avec la DB, l'erreur est levée.

    Returns
    -------
    Bool : Bool
        Booléen qui précise si oui ou non l'identifiant existe dans la DB.

    """
    Bool = False
    try: #on vérifie si l'identifiant existe
        con = sqlite3.connect("database/apijeux.db")
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

def add_user(username, pseudo, hpassword):
    """
    Procédure qui ajoute une utilisateur à la DB.

    Parameters
    ----------
    username : str
        Identifiant de l'utilisateur.
    pseudo : str
        Pseudo de l'utilisateur.
    hpassword : str
        Hash du mot de passe de l'utilisateur.

    Raises
    ------
    ConnectionAbortedError
        Si un erreur se produit au cours de la communication avec la DB, un rollback jusqu'au précédant commit à lieu et l'erreur est levée.

    Returns
    -------
    None.

    """
    con = sqlite3.connect("database/apijeux.db")
    cursor = con.cursor()
    try:
        cursor.execute(
            "INSERT INTO Utilisateur (pseudo, identifiant, mdp, nbr_parties_jouees, nbr_parties_gagnees, est_connecte, en_file, en_partie) VALUES (?, ?, ?, 0, 0, 'False', 'False', 'False')",
            (pseudo, username, hpassword,))
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

        Parameters
        ----------
        pseudo : str
            Pseudo de l'utilisateur.

        Raises
        ------
        ConnectionAbortedError
            Si un erreur se produit au cours de la communication avec la DB, un rollback jusqu'au précédant commit à lieu et l'erreur est levée.

        Returns
        -------
        None.

        """
    con = sqlite3.connect("database/apijeux.db")
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO Scores (jeu, pseudo, score) VALUES ('P4', ?, 1000)", (pseudo,))
        cursor.execute("INSERT INTO Scores (jeu, pseudo, score) VALUES ('Oie', ?, 1000)", (pseudo,))
        con.commit()
    except:
        print("erreur dans add_user_score")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_hpass(username):
    """
    Fonction qui renvoit le hash de mot de passe stocké dans la DB pour un identifiant donné.

    Parameters
    ----------
    username : str
        Identifiant associé au hmdp recherché.

    Raises
    ------
    ConnectionAbortedError
        Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.
    ValueError
        pass

    Returns
    -------
    hpass : str
        Renvoit le hash du mot de passe associé à l'identifiant en entrée.

    """
    try: #on récupère le hpass
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT mdp FROM Utilisateur WHERE identifiant = ?", (username,))
        hpass = cursor.fetchone()
    except:
        print("Erreur dans get_hpass")
        raise ConnectionAbortedError
    finally:
        con.close()
    if hpass == None:
        print("le execute renvoit none, erreur dans get_hpass")
        raise ValueError
    return hpass[0]

def get_pseudo(username):
    """
    Fonction qui renvoit le pseudo associé à un identifiant dans la DB

    Parameters
    ----------
    username : str
        Identifiant dont on souhaite le pseudo associé.

    Raises
    ------
    ConnectionAbortedError
        DESCRIPTION.
    ValueError
        DESCRIPTION.

    Returns
    -------
    pseudo : str
        Pseudo associé à l'identifiant en entrée.

    """
    try: #on récupère le pseudo
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo FROM Utilisateur WHERE identifiant = ?", (username,))
        pseudo = cursor.fetchone()
    except:
        print("erreur dans get_pseudo")
        raise ConnectionAbortedError
    finally:
        con.close()
    if pseudo == None:
        print("le execute renvoit none, erreur dans get_pseudo")
        raise ValueError
    return pseudo[0]

def update_est_connecte(ide, username_or_pseudo = 'username', nouvel_etat = 'True'):
    """
    Procédure qui permet de modifier la valeur est_connecté pour un utilisateur dans la DB en fonction de son pseudo ou de son identifiant.

    Parameters
    ----------
    ide : str
        nom de l'identifiant ou du pseudo de l'utilisateur dont on veut modifier la valeur du est_connecte.
    username_or_pseudo : str, optional
        Il faut préciser si le ide fournit correspond à l'identifiant ou au pseudo de l'utilisateur. username_or_pseudo est donc à valeur dans ('username', 'pseudo'). The default is 'username'.
    nouvel_etat : str, optional
        Il faut préciser si on veut mettre est_connecte à True ou à False. nouvel_etat est donc à valeur dans ('True','False'). The default is 'True'.

    Raises
    ------
    ValueError
        DESCRIPTION.
    ConnectionAbortedError
        DESCRIPTION.

    Returns
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
            con = sqlite3.connect("database/apijeux.db")
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
            con = sqlite3.connect("database/apijeux.db")
            cursor= con.cursor()
            cursor.execute("UPDATE Utilisateur SET est_connecte = ? WHERE pseudo = ?", (nouvel_etat, ide,))
            con.commit()
        except:
            print("erreur dans update_est_connecte")
            con.rollback()
            raise ConnectionAbortedError
        finally:
            con.close()

def update_pseudo_table_utilisateur(old_pseudo, new_pseudo):
    try:  # on update le pseudo de l'utilisateur dans la table utilisateur
        con = sqlite3.connect("database/apijeux.db")
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
    try:  # on update le pseudo de l'utilisateur dans la table liste amis
        con = sqlite3.connect("database/apijeux.db")
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
    try:  # on update le pseudo de l'utilisateur dans la table score
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("UPDATE Scores SET pseudo = ? WHERE pseudo = ?", (new_pseudo, old_pseudo,))
        con.commit()
    except:
        print("erreur dans update_pseudo_table_scores")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()


def update_pseudo(old_pseudo, new_pseudo):
    update_pseudo_table_utilisateur(old_pseudo, new_pseudo)
    update_pseudo_table_liste_amis(old_pseudo, new_pseudo)
    update_pseudo_table_score(old_pseudo, new_pseudo)

