#Main du serveur
import socket
import threading

class ThreadForClient(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        data = self.conn.recv(1024)
        data = data.decode("utf8")
        print(data)



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