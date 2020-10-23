def is_mdp_legal(mot_de_passe_entre):
    is_legal = True
    #on veut que le mot de passe comporte au moins 8 caractères
    if len(mot_de_passe_entre) < 8:
        is_legal = False
        print("Le mot de passe n'est pas assez long.")

    #on veut que le mot de passe contienne au moins 1 minuscule
    if not any(car.islower() for car in mot_de_passe_entre):
        is_legal = False
        print("Le mot de passe doit contenir au moins une lettre minuscule.")

    #on veut que le mot de passe contienne au moins 1 majuscule
    if not any(car.isupper() for car in mot_de_passe_entre):
        is_legal = False
        print("Le mot de passe doit contenir au moins une lettre majuscule.")

    #on veut que le mot de passe contienne au moins 1 chiffre
    if not any(car.isdigit() for car in mot_de_passe_entre):
        is_legal = False
        print("Le mot de passe doit contenir au moins un chiffre.")

    #on veut que le mot de passe contienne au moins 1 caractère spécial
    special_car_list = "!@#$%&_=?"
    if not any(car in special_car_list for car in mot_de_passe_entre):
        is_legal = False
        print("Le mot de passe doit contenir un caractère 'spécial' parmis la liste suivante : ' !@#$%&_=? '. ")

    forbidden_car_list = ";"
    if any(car in forbidden_car_list for car in mot_de_passe_entre):
        is_legal = False
        print("Le mot de passe contient un caractère spécial interdit.")

    return is_legal

import hashlib , binascii , os

def hacherMotDePasse(motDePasse):
    #source:https://www.vitoshacademy.com/hashing-passwords-in-python/
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hash = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', motDePasse.encode('utf-8'), salt, 100000))
    return(salt + hash).decode('ascii')

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

def anti_SQl_injection(text):
    for lettre in text:
        if lettre in (";", "\n", "\r", "\,", "',", "\x00", "\x1a", ):
            text = text.replace(lettre, "")
    text = text.replace("'", "''")
    text = text.replace("--", "")
    text = text.replace("NUL", "")

    return text