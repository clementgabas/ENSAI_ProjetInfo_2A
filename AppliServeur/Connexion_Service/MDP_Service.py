import hashlib , binascii , os


class MDP:

    def __init__(self, password):
        self.mdp = password
        self.hashedMDP = hashMDP(self)
        self.antiSQLmdp = anti_SQL_injection(self)

    def hashMDP(self):
        #source:https://www.vitoshacademy.com/hashing-passwords-in-python/
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        hash = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', self.mdp.encode('utf-8'), salt, 100000))
        return(salt + hash).decode('ascii')

    def isLegal(self):
        mot_de_passe_entre = self.mdp

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
        
    def anti_SQl_injection(self):
        text = self.mdp
        for lettre in text:
            if lettre in (";", "\n", "\r", "\,", "',", "\x00", "\x1a", ):
                text = text.replace(lettre, "")
        text = text.replace("'", "''")
        text = text.replace("--", "")
        text = text.replace("NUL", "")

        return text