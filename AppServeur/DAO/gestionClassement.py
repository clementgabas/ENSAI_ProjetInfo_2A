import sqlite3

def afficher_classement_jeu_oie():
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo, score, FROM Scores WHERE jeu = Oie ORDER BY score LIMIT 10") # On attribue l'id_jeu 2 au jeu de l'oie.
        classement_jeu_oie = cursor.fetchall()
    except:
        print("ERROR : API.afficher_classement_jeu_oie :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_jeu_oie

def afficher_classement_p4():
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo, score, FROM Scores WHERE jeu = P4 ORDER BY score LIMIT 10")  # On attribue l'id_jeu 1 au puissance 4.
        classement_jeu_puissance4 = cursor.fetchall()
    except:
        print("ERROR : API.afficher_classement_p4 :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_jeu_puissance4

def afficher_classement_general():
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo, SUM(score), FROM Scores  GROUP BY pseudo LIMIT 10")
        classement_general = cursor.fetchall()
    except:
        print("ERROR : API.afficher_classement_general :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_general
