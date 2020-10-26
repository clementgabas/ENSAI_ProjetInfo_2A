#Classe ThreadForClient qui permet la gestion de plusieurs clients en simultanné pr le serveur via les threads.
from datetime import datetime
import threading


class ThreadForClient(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        data = self.conn.recv(1024)
        data = data.decode("utf8")
        print(f"[{str(datetime.now())}]" + data)

