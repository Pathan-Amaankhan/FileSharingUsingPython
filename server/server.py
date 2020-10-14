import socket
import threading

from SendReceiveClasses.Receiving import Receiving
from SendReceiveClasses.Sending import Sending

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 4444))

s.listen()


class Server:
    def __init__(self, client):
        self.client = client

    def start_receive(self):
        Receiving(self.client).listen()

    def start_send(self):
        Sending(self.client).send()


while True:
    c, addr = s.accept()
    print(addr, c)
    threading.Thread(target=Server(c).start_send).start()
    threading.Thread(target=Server(c).start_receive).start()
