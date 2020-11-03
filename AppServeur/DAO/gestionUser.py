import sqlite3

def does_pseudo_exist(pseudo):
    Bool = False
    try: #on vérifie si l'ami existe
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
    Bool = False
    try: #on vérifie si l'ami existe
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
    #procédure qui ajoute un utilisateur à la db
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

def get_hpass(username):
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
    try: #on récupère le hpass
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
    """username_or_pseudo in ('username','pseudo') ; nouvel_etat in ('True', 'False')"""

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