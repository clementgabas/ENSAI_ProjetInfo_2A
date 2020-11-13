import sqlite3
db_address = "database/apijeux.db"
liste_couleurs_autorisees = ['bleu', 'rouge', 'vert', 'jaune', 'magenta', 'cyan', 'gris']

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

def get_position_ordre(pseudo, id_partie):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT ordre FROM Participation WHERE id_partie = ? AND pseudo = ?", (id_partie,pseudo,))
        ordre = cursor.fetchall()[0][0]
    except:
        print("erreur dans get_position_ordre")
        raise ConnectionAbortedError
    finally:
        con.close()
    return ordre

def update_ordre(pseudo, id_partie):
    ordre_dernier_joueur_actuel = get_ordre(id_partie)[-1][1]
    ordre_pseudo = ordre_dernier_joueur_actuel+1

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

def get_used_color(id_partie):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT couleur FROM Participation WHERE id_partie = ?", (id_partie,))
        liste_couleur = cursor.fetchall()
    except:
        print("erreur dans get_used_color")
        raise ConnectionAbortedError
    finally:
        con.close()
    liste = []
    for elem in liste_couleur:
        liste.append(elem[0])
    return liste

def get_free_color(id_partie):
    used_colors = get_used_color(id_partie)
    free_color_list = []
    for col in liste_couleurs_autorisees:
        if col not in used_colors:
            free_color_list.append(col)
    return free_color_list

def is_color_free(id_partie, color):
    used_colors = get_used_color(id_partie)
    if color in used_colors:
        return False
    return True

def update_color(pseudo, id_partie, color):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("UPDATE Participation SET couleur = ? WHERE pseudo = ? AND id_partie = ? ", (color, pseudo, id_partie))
        con.commit()
    except:
        print("erreur dans update_color")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def get_couleur(pseudo, id_partie):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT couleur FROM Participation WHERE pseudo = ? AND id_partie = ? ", (pseudo, id_partie))
        couleur = cursor.fetchone()[0]
    except:
        print("erreur dans get_couleur")
        raise ConnectionAbortedError
    finally:
        con.close()
    return couleur

def number_of_ready(id_partie):
    try:
        con = sqlite3.connect(db_address)
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(est_pret) FROM Participation WHERE est_pret = 'True' AND id_partie = ?", (id_partie,))
        nombre = cursor.fetchone()[0]
    except:
        print("erreur dans number_of_ready")
        raise ConnectionAbortedError
    finally:
        con.close()
    return nombre