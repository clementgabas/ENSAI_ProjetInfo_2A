import psycopg2
from Connexion_Service.MDP_Service import MDP

def authentification(identifiant, mot_de_passe):
    
    mdp = MDP(mot_de_passe)

    #On se connecte d'abbord à la DB
    conn = psycopg2.connect(database = "nom de la DB", user = "nom de user", host = "ip de l'host (localhost)", password = "mdp", port = "port")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT pseudo FROM tableutilisateur WHERE identifiant = %s AND hash_password = %s", (givenID, hashMDP)) #MAJ des champs et nom de table important mdrr
        pseudo = cursor.fetchone()
    except :
        print("Une erreur s'est produite.")
        raise ConnectionAbortedError
    finally:
        try:
            self.connector.close()
            print(f"Vous avez bien été déconnectés de la base de données {self.DBname}.")
        except:
            print(f"Une erreur s'est produite au cours de la déconnexion de la base de donnée {self.DBname}.")
            raise ConnectionAbortedError


