
def verify_password(stored_password, provided_password):
    #source:https://www.vitoshacademy.com/hashing-passwords-in-python/
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)).decode('ascii')
    return pwdhash == stored_password

import sqlite3
class DataBase:
    #source : https://youtu.be/p_dE8DD-oNs?t=395
    def __init__(self, name, user, password, host="localhost"):
        self.DBname = name
        self.host = host
        self.user = user
        self.password = password
        self.connector = None
     
    def __getConnexionToDB__(self):
        try:
            self.connector = sqlite3.connect(self.host, self.DBname, self.user, self.password)
            print(f"Vous êtes bien connectés à la base de données {self.DBname}.")
        except:
            print(f"Une erreur s'est produite au cours de la connexion à la base de donnée {self.DBname}.")
            raise ConnectionAbortedError

    def __getCursor__(self):
        return self.connector.cursor()

    def __getDisconnexionFromDB__(self):
        try:
            self.connector.close()
            print(f"Vous avez bien été déconnectés de la base de données {self.DBname}.")
        except:
            print(f"Une erreur s'est produite au cours de la déconnexion de la base de donnée {self.DBname}.")
            raise ConnectionAbortedError

def authentification(givenID, givenMDP):

    if givenID != anti_SQl_injection(givenID) or givenMDP != anti_SQl_injection(givenMDP):
        return (False, "SQL_injection_FALSE")

    DBconnexion = DataBase("TableUtilisateur", "utilisateur", "mdp") #MAJ importante
    con = DBconnexion.__getConnexionToDB__()
    cursor = DBconnexion.__getCursor__()

    hashMDP = hacherMotDePasse(givenMDP)

    try:
        cursor.execute("SELECT pseudo FROM tableutilisateur WHERE identifiant = %s AND hash_password = %s", (givenID, hashMDP)) #MAJ des champs et nom de table important mdrr
        pseudo = cursor.fetchone()
    except :
        print("Une erreur s'est produite.")
        raise ConnectionAbortedError
    finally:
        DBconnexion.__getDisconnexionFromDB__()

    if pseudo == None: #id ou mdp incorrect
        print("Identifiant ou mot de passe incorrect.")
        return (False, "no_pseudo")
    else:
        pseudo = pseudo[0]
        return (True, pseudo)

