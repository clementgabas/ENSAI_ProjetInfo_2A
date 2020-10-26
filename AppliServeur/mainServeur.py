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

    if data == "Demande d'authentification":
        pass
    else:
    print(f"[{str(datetime.now())}]:" + data)

    my_thread = ThreadForClient(conn)
    my_thread.start()

conn.close() #on ferme la co à la fin quand on en a plus besoin
sock.close() #on ferme le socket à la fin quand on en a plus besoin