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

def anti_SQl_injection(text):
    copy_text = text
    for lettre in text:
        if lettre in (";", "\n", "\r", "\,", "',", "\x00", "\x1a", ):
            text = text.replace(lettre, "")
    text = text.replace("'", "''")
    text = text.replace("--", "")
    text = text.replace("NUL", "")

    if text!=copy_text:
        return False
    return True