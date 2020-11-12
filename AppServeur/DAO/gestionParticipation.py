import sqlite3


def update_est_pret(pseudo, id_partie, TrueOrFalse):
    TrueOrFalse = TrueOrFalse.lower()
    if TrueOrFalse not in ('true', 'false'):
        print("L'argument TrueOrFalse doit être 'True' ou 'False'.")
        raise ValueError
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("UPDATE Participation SET est_pret = ? WHERE pseudo = ? AND id_partie = ?", (TrueOrFalse,pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans uptade_est_pret")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
    return id_partie