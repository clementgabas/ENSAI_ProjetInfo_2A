#Main du client
import socket
from View.menu_Principal import Menu_Principal
from datetime import datetime


#Quand on lance l'appli client, on se connecte d'abord au serveur.
#Nous avonc choisi d'héberger le serveur en local (IP = 127.0.0.1) sur le port 5566 qui est libre.
HOST, PORT = ('localhost', 5566) #pour HOST, l'IP du local est 127.0.0.1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #init du socket

try:
    sock.connect((HOST, PORT))
    print(f"{str(datetime.now())} : Client connecté")
    #a ce moment la, le client est bien connecté au serveur de l'application.
    #On peut maintenant gérer l'application et permettre au clien de naviguer dedans
    #on envoit le client sur le menu principal de l'application

    MenuP1 = Menu_Principal()
    MenuP1.make_choice()


    data = "Données qu'on envoit au serveur"
    data = data.encode("utf8")
    sock.sendall(data)

except:
    print(f"{str(datetime.now())} : Connexion au serveur échouée.")
finally:
    print("Vous avez bien quitté l'application")
    sock.close()