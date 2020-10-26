#Importation des modules
import PyInquirer as inquirer
from View.abstractView import AbstractView
import View.menu_Utilisateur_Co as MUC
import socket
from datetime import datetime

HOST, PORT = ('localhost', 5566)

#Création du menu de connexion

class Menu_Connexion(AbstractView):
    def display_info(self):
        print("Bienvenue sur le menu de connexion")
    def make_choice(self):
        self.questions = [
            {
                'type': 'input',
                'name': 'Identifiant',
                'message': "Veuillez insérer votre identifiant",
            },
            {
                'type' : 'password',
                'name' : 'Password',
                'message' : "Veuillez insérer votre mot de passe",
            }
        ]
        while True:
            self.reponse = inquirer.prompt(self.questions)
            identifiant, mdp = self.reponse["Identifiant"], self.reponse["Password"]
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init du socket
                sock.connect((HOST, PORT))
                sock.send("Demande d'authentification".encode("utf8")) #on prévient le serveur qu'on demande à se connecter
                print(f"[{str(datetime.now())}]: Demande d'authentification envoyée")
                sock.connect((HOST, PORT))
                sock.send(identifiant.encode("utf8")) #on envoit le id
                sock.connect((HOST, PORT))
                sock.send(mdp.encode("utf8")) #on envoit ld mdp
            except:
                print(f"[{str(datetime.now())}]: erreur lors de la demande d'authentification au serveur")
                break

            #en fonction de ce que renvoit le serveur :
            # si le serveur répond conenxion = True, on se connecte
            # sinon, on réessaye

            # if connexion :
            # Co = MUC.Menu_User_Co()
            # return Co.make_choice()
            # else:
            # print("Id ou mdp incorrect. Veuillez reessayer")
            # return self.make_choice




            #on envoit au serveur id et mdp et on lui demande si on peut se connecter.



if __name__ == "__main__": 
    menu_Connexion1 = Menu_Connexion()


# Les réponses des utilisateurs sont stockés dans : menu_Connexion1.reponse["Identifiant"] et (menu_Connexion1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
