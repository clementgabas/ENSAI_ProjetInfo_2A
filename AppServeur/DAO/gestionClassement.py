import sqlite3

def afficher_classement_jeu(nom_jeu,pseudo):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor2 = con.cursor()
        #cursor.execute("SELECT nb_points FROM Scores WHERE jeu = ? ORDER BY nb_points DESC LIMIT 10", (nom_jeu,))
        cursor.execute("SELECT RANK () OVER ( ORDER BY nb_points DESC ), pseudo, nb_points FROM Scores WHERE jeu = ? ORDER BY nb_points DESC LIMIT 10", (nom_jeu,))

        #cursor.execute("SELECT (SELECT COUNT(*) + 1 FROM Scores S WHERE S.jeu = P.jeu AND P.nb_points < S.nb_points) AS Rang, P.pseudo, P.nb_points FROM Scores P WEHRE P.jeu = ? ORDER BY P.nb_points Desc", (nom_jeu,))
        cursor2.execute("SELECT pseudo, nb_points FROM Scores WHERE jeu = ? AND pseudo = ? ", (nom_jeu,pseudo,))
        classement_jeu_user = cursor2.fetchall()
        pos_user=[]
        classement_jeu_all = cursor.fetchall()
        for i in classement_jeu_all:
            if pseudo in i :
                pos_user.append(i)
        if pos_user==[]:
            pos_user.append(['hors classement',classement_jeu_user[0][0],classement_jeu_user[0][1]])

        classement_jeu = classement_jeu_all + [["","",""]] + pos_user

    except:
        print("ERROR : API.afficher_classement_jeu:")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_jeu

def afficher_classement_general(pseudo):
    try:
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT RANK () OVER ( ORDER BY SUM(nb_points) DESC ), pseudo, SUM(nb_points) AS nb_tot FROM Scores  GROUP BY pseudo ORDER BY nb_tot DESC LIMIT 10")

        cursor2 = con.cursor()
        cursor2.execute("SELECT pseudo, SUM(nb_points) FROM Scores WHERE pseudo = ? ", (pseudo,))

        classement_general_user = cursor2.fetchall()
        classement_general_all = cursor.fetchall()
        pos_user = []
        for i in classement_general_all:
            if pseudo in i :
                pos_user.append(i)
        if pos_user==[]:
            pos_user.append(['hors classement',classement_general_user[0][0],classement_general_user[0][1]])

        classement_general = classement_general_all + [["","",""]] + pos_user
    except:
        print("ERROR : API.afficher_classement_general :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_general