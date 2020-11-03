import sqlite3
from datetime import datetime

def are_pseudos_friends(pseudo1, pseudo2):
    #fonction qui renvoit un bool précisant si oui ou non pseudo1 est ami avec pseudo2
    Bool = False
    try:  # on vérifie si le lien d'amitié n'existe pas déjà
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT date_ajout FROM Liste_Amis WHERE pseudo = ? and pseudo_ami = ?", (pseudo1, pseudo2,))
        pse = cursor.fetchone()
    except:
        print("erreur dans are_pseudos_friends")
        raise ConnectionAbortedError
    finally:
        con.close()
    if pse != None: #pseudo1 est ami avec pseudo2
        Bool = True
    else: #pseudo1 n'est pas ami avec pseudo2
        Bool = False
    return Bool

def add_amitie(pseudo1, pseudo2):
    #procédure qui ajoute à pseudo1 une amitié avec pseudo2
    try:  # on ajoute le lien d'amitié
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        date = str(datetime.now())
        cursor.execute("INSERT INTO Liste_Amis (pseudo, pseudo_ami, date_ajout) VALUES (?, ?, ?)", (pseudo1, pseudo2, date,))
        con.commit()
    except:
        print("erreur dans add_amitie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def sup_amitie(pseudo1, pseudo2):
    #procédure qui ajoute à pseudo1 une amitié avec pseudo2
    try:  # on supprime le lien d'amitié
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("DELETE from Liste_Amis WHERE pseudo = ? and pseudo_ami = ?", (pseudo1, pseudo2))
        con.commit()
    except:
        print("erreur dans sup_amitie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def afficher_liste_amis(pseudo):
    #fonction qui retourne la liste des amis de pseudo
    try: #on affiche la liste des amis
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo_ami, date_ajout FROM Liste_Amis WHERE pseudo = ?", (pseudo,))
        liste_amis = cursor.fetchall()
    except:
        print("ERROR : API.afficherlisteamis :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return liste_amis
