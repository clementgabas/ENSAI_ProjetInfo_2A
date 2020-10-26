#Main du serveur
import socket
import threading
from datetime import datetime
from ThreadForClient import ThreadForClient
from Connexion_Service.AuthentificationService import authentification


HOST, PORT = ('', 5566)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #init du socket
sock.bind((HOST, PORT))
print(f"[{str(datetime.now())}]: Le serveur est démarré.")

while True:
    sock.listen()
    conn, address = sock.accept()
    data = conn.recv(1024)
    data = data.decode("utf8")

    if "Demande d'authentification".lower() in data.lower(): #le client souhaite se connecter
        print("demande d'authenf recue")
        val = []
        for i in range(2): #on récupère l'id et le mdp transmis par le client
            print("boucle" + str(i))
            sock.listen()
            conn, address = sock.accept()
            data = conn.recv(1024)
            data = data.decode("utf8")
            val.append(data)
        ide, mdp_pas_hash = val[0], val[1]

        authenTuple = authentification(ide, mdp_pas_hash)

        if authenTuple[0]: #l'authentification c'est bien déroulée
            pseudo = authenTuple[1]
            print(f"[{str(datetime.now())}]: Les critères d'authentification du client sont corrects. Il peut s'authentifier.")
        else:
            pass

    elif data == "Demande de création de compte":
        pass
    else:
        print(f"[{str(datetime.now())}]:" + data)

    my_thread = ThreadForClient(conn)
    my_thread.start()

conn.close() #on ferme la co à la fin quand on en a plus besoin
sock.close() #on ferme le socket à la fin quand on en a plus besoin