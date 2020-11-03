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
