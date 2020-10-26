#Main du serveur
import socket
import threading
from ThreadForClient import ThreadForClient

HOST, PORT = ('', 5566)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #init du socket
sock.bind((HOST, PORT))
print("Le serveur est démarré.")

while True:
    sock.listen()
    conn, address = sock.accept()
    print("En écoute...")

    my_thread = ThreadForClient(conn)
    my_thread.start()

conn.close() #on ferme la co à la fin quand on en a plus besoin
sock.close() #on ferme le socket à la fin quand on en a plus besoin