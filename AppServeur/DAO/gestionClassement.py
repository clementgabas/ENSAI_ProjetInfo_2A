import sqlite3

def afficher_classement_jeu(nom_jeu):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo, score FROM Scores WHERE jeu = ? ORDER BY score", (nom_jeu,))
        classement_jeu = cursor.fetchall()
    except:
        print("ERROR : API.afficher_classement_jeu:")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_jeu

def afficher_classement_general():
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo, SUM(score) FROM Scores  GROUP BY pseudo LIMIT 10")
        classement_general = cursor.fetchall()
    except:
        print("ERROR : API.afficher_classement_general :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_general