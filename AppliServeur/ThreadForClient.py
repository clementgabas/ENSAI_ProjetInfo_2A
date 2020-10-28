#Classe ThreadForClient qui permet la gestion de plusieurs clients en simultanné pr le serveur via les threads.
from datetime import datetime
import threading
from Connexion_Service.AuthentificationService import authentification


class ThreadForClient(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        data = self.conn.recv(1024)
        data = data.decode("utf8")
        if "Demande d'authentification".lower() in data.lower(): #le client souhaite se connecter
            val = []
            for i in range(2): #on récupère l'id et le mdp transmis par le client
                data2 = self.conn.recv(1024)
                data2 = data2.decode("utf8")
                print("data recue : " + str(data2))
                val.append(data2)
            ide, mdp_pas_hash = val[0], val[1]
            return print("val = {}".format(val))

        #    authentuple = authentification(ide, mdp_pas_hash)

        #    if authentuple[0]: #l'authentification c'est bien déroulée
        #        pseudo = authentuple[1]
        #        print(f"[{str(datetime.now())}]: les critères d'authentification du client sont corrects. il peut s'authentifier.")
        #    else:
        #        pass

        #elif data == "demande de création de compte":
        #    pass
        #else:
        #    print(f"[{str(datetime.now())}]:" + data)

        else:
            print(f"[{str(datetime.now())}]: " + str(data))



