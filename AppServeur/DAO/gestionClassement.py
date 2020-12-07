import sqlite3
import DAO.gestion as DBgestion
db_address = DBgestion.get_db_address()


def afficher_classement_jeu(nom_jeu,pseudo):
    """
        Fonction qui retourne les 10 premiers du classement mondial du jeu demandé

        :parameter
        ----------
        nom_jeu : str
            Nom du jeu demandé pour le classement
        pseudo : str
            Pseudo pour pour lequel on affiche le classement

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
         classement_jeu : list
                Liste des dix premiers du classement mondial du jeu demandé comprenant rang, pseudo,
                nombre de points, nombre parties jouées et nombre parties gagnées
                ainsi que ceux du pseudo qui demande.


    """
    try:
        con = sqlite3.connect(db_address)
        cursor= con.cursor()
        cursor2 = con.cursor()
        cursor.execute("SELECT RANK () OVER ( ORDER BY nb_points DESC, nb_parties_jouees ASC ) as rang,"
                       " pseudo, nb_points, nb_parties_jouees ,nb_parties_gagnees "
                       "FROM Scores WHERE jeu = ? ORDER BY rang ASC LIMIT 10", (nom_jeu,))

        cursor2.execute("SELECT pseudo, nb_points, nb_parties_jouees ,nb_parties_gagnees  "
                        "FROM Scores WHERE jeu = ? AND pseudo = ? ", (nom_jeu,pseudo,))
        classement_jeu_user = cursor2.fetchall()
        pos_user=[]
        classement_jeu_all = cursor.fetchall()
        for i in classement_jeu_all:
            if pseudo in i :
                pos_user.append(i)
        if pos_user==[]:
            pos_user.append(['hors classement',classement_jeu_user[0][0],classement_jeu_user[0][1],
                             classement_jeu_user[0][2],classement_jeu_user[0][3]])

        classement_jeu = classement_jeu_all + [["","",""]] + pos_user

    except:
        print("ERROR : API.afficher_classement_jeu:")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_jeu

def afficher_classement_general(pseudo):
    """
        Fonction qui retourne les 10 premiers du classement mondial général

        :parameter
        ----------
        pseudo : str
            Pseudo pour pour lequel on affiche le classement

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        classement_general : list
            Liste des dix premiers du classement mondial général comprenant rang, pseudo,nombre de points
            en somme cumulée, nombre parties jouées et nombre parties gagnées
            ainsi que ceux du pseudo qui demande.

    """
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT RANK () OVER ( ORDER BY SUM(nb_points) DESC, nb_parties_jouees ASC ) as rang,"
                       " pseudo, SUM(nb_points) AS nb_tot, nb_parties_jouees ,nb_parties_gagnees "
                       "FROM Scores  GROUP BY pseudo ORDER BY rang ASC LIMIT 10")

        cursor2 = con.cursor()
        cursor2.execute("SELECT pseudo, SUM(nb_points), nb_parties_jouees ,nb_parties_gagnees"
                        " FROM Scores WHERE pseudo = ? ", (pseudo,))

        classement_general_user = cursor2.fetchall()
        classement_general_all = cursor.fetchall()
        pos_user = []
        for i in classement_general_all:
            if pseudo in i :
                pos_user.append(i)
        if pos_user==[]:
            pos_user.append(['hors classement',classement_general_user[0][0],classement_general_user[0][1],
                             classement_general_user[0][2],classement_general_user[0][3]])

        classement_general = classement_general_all + [["","",""]] + pos_user
    except:
        print("ERROR : API.afficher_classement_general :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_general

def afficher_classement_jeu_friends(nom_jeu,pseudo):
    """
        Fonction qui retourne les 10 premiers du classement entre amis du jeu demandé

        :parameter
        ----------
        nom_jeu : str
            Nom du jeu demandé pour le classement
        pseudo : str
            Pseudo pour pour lequel on affiche le classement

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        classement_jeu_friends : list
            Liste des dix premiers du classement entre amis du jeu demandé comprenant rang, pseudo,
            nombre de points, nombre parties jouées et nombre parties gagnées
            ainsi que ceux du pseudo qui demande.


    """
    try:
        con = sqlite3.connect(db_address)
        cursor= con.cursor()
        cursor2 = con.cursor()
        #cursor.execute("SELECT nb_points FROM Scores WHERE jeu = ? ORDER BY nb_points DESC LIMIT 10", (nom_jeu,))
        cursor.execute("SELECT RANK () OVER ( ORDER BY nb_points DESC, nb_parties_jouees ASC ) AS rang,"
                       " pseudo, nb_points, nb_parties_jouees ,nb_parties_gagnees FROM "
                       "(SELECT Scores.jeu ,Scores.pseudo, Scores.nb_points, Scores.nb_parties_jouees ,"
                       "Scores.nb_parties_gagnees FROM Scores, Liste_Amis "
                       "WHERE Scores.pseudo = Liste_Amis.pseudo_ami AND Liste_Amis.pseudo = ? "
                       "UNION "
                       "SELECT jeu, pseudo, nb_points,nb_parties_jouees, nb_parties_gagnees "
                       "FROM Scores WHERE pseudo = ?)"
                       " WHERE jeu = ?  ORDER BY rang ASC", (pseudo, pseudo, nom_jeu,))
        cursor2.execute("SELECT pseudo, nb_points, nb_parties_jouees ,nb_parties_gagnees"
                        " FROM Scores WHERE jeu = ? AND pseudo = ? ", (nom_jeu,pseudo,))
        classement_jeu_friends_user = cursor2.fetchall()
        pos_friends_user=[]
        classement_jeu_friends_all = cursor.fetchall()
        for i in classement_jeu_friends_all:
            if pseudo in i :
                pos_friends_user.append(i)
        if pos_friends_user==[]:
            pos_friends_user.append(['hors classement',
                                     classement_jeu_friends_user[0][0],classement_jeu_friends_user[0][1]])

        classement_jeu_friends = classement_jeu_friends_all + [["","",""]] + pos_friends_user

    except:
        print("ERROR : API.afficher_classement_jeu:")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_jeu_friends

def afficher_classement_general_friends(pseudo):
    """
        Fonction qui retourne les 10 premiers du classement entre amis général

        :parameter
        ----------
        pseudo : str
            Pseudo pour pour lequel on affiche le classement

        :raise
        ------
        ConnectionAbortedError
            Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

        :return
        -------
        classement_general_friends : list
            Liste des dix premiers du classement entre amis général comprenant rang, pseudo,nombre de points
            en somme cumulée, nombre parties jouées et nombre parties gagnées
            ainsi que ceux du pseudo qui demande.

    """
    try:
        con = sqlite3.connect(db_address)
        cursor= con.cursor()
        cursor.execute("SELECT RANK () OVER ( ORDER BY SUM(nb_points) DESC ) AS rang, pseudo, SUM(nb_points) AS nb_tot,"
                       " nb_parties_jouees ,nb_parties_gagnees FROM "
                       "(SELECT Scores.jeu ,Scores.pseudo, Scores.nb_points, Scores.nb_parties_jouees,"
                       "Scores.nb_parties_gagnees FROM Scores, Liste_Amis "
                       "WHERE Scores.pseudo = Liste_Amis.pseudo_ami AND Liste_Amis.pseudo = ? "
                       " UNION"
                       " SELECT jeu, pseudo, nb_points,nb_parties_jouees, nb_parties_gagnees"
                       " FROM Scores WHERE pseudo = ?)"
                       "GROUP BY pseudo ORDER BY rang ASC LIMIT 10", (pseudo, pseudo,))

        cursor2 = con.cursor()
        cursor2.execute("SELECT pseudo, SUM(nb_points) FROM Scores WHERE pseudo = ? ", (pseudo,))

        classement_general_friends_user = cursor2.fetchall()
        classement_general_friends_all = cursor.fetchall()
        pos_friends_user = []
        for i in classement_general_friends_all:
            if pseudo in i :
                pos_friends_user.append(i)
        if pos_friends_user==[]:
            pos_friends_user.append(['hors classement',
                                     classement_general_friends_user[0][0],classement_general_friends_user[0][1]])

        classement_general_friends = classement_general_friends_all + [["","",""]] + pos_friends_user
    except:
        print("ERROR : API.afficher_classement_general :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return classement_general_friends
