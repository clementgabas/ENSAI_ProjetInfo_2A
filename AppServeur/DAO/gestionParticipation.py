import sqlite3
db_address = "database/apijeux.db"

def update_est_pret(pseudo, id_partie, TrueOrFalse):
    TrueOrFalse = TrueOrFalse.lower()
    if TrueOrFalse not in ('true', 'false'):
        print("L'argument TrueOrFalse doit être 'True' ou 'False'.")
        raise ValueError
    if TrueOrFalse.lower() == 'true':
        TrueOrFalse = 'True'
    elif TrueOrFalse.lower()=='false':
        TrueOrFalse = 'False'
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Participation SET est_pret = ? WHERE pseudo = ? AND id_partie = ?", (TrueOrFalse,pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans uptade_est_pret")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_ordre(id_partie):
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

def update_ordre(pseudo, id_partie):
    ordre_dernier_joueur_actuel = get_ordre(id_partie)[-1][1]
    print(ordre_dernier_joueur_actuel)
    ordre_pseudo = ordre_dernier_joueur_actuel+1
    print(ordre_pseudo)

    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Participation SET ordre = ? WHERE pseudo = ? AND id_partie = ? ", (ordre_pseudo, pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans update_ordre")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
