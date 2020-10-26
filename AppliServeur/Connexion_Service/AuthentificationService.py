import psycopg2
from Connexion_Service.MDP_Service import MDP
from datetime import datetime

def authentification(identifiant, mot_de_passe):
    
    mdp = MDP(mot_de_passe)
    hashMDP = mdp.hashMDP

    #On se connecte d'abbord à la DB
    conn = psycopg2.connect(database = "nom de la DB", user = "nom de user", host = "ip de l'host (localhost)", password = "mdp", port = "port")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT pseudo FROM utilisateur WHERE identifiant = %s AND hash_password = %s", (identifiant, hashMDP)) #MAJ des champs et nom de table important mdrr
        pseudo = cursor.fetchone()
    except :
        print(f"[{dtr(datetime.now())}]: Une erreur s'est produite.")
        raise ConnectionAbortedError
    finally:
        try:
            self.connector.close()
        except:
            print(f"[{str(datetime.now())}]: Une erreur s'est produite au cours de la déconnexion de la base de donnée {self.DBname}.")
            raise ConnectionAbortedError

    if pseudo == None: #id ou mdp incorrect
        #print("Identifiant ou mot de passe incorrect.")
        return (False, "no_pseudo")
    else:
        pseudo = pseudo[0]
        return (True, pseudo)


