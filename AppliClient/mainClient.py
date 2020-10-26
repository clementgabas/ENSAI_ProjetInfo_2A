#Main du client
import socket

HOST, PORT = ('localhost', 5566) #pour HOST, l'IP du local est 127.0.0.1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #init du socket

try:
    sock.connect((HOST, PORT))
    print("Client connecté")

    data = "Données qu'on envoit au serveur"
    data = data.encode("utf8")
    sock.sendall(data)

except:
    print("Connexion au serveur échouée.")
finally:
    sock.close()