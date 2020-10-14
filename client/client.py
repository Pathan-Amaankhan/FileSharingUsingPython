import socket
import threading
import os

from SendReceiveClasses.Receiving import Receiving
from SendReceiveClasses.Sending import Sending

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('', 4444))


class Client:
    def __init__(self, client):
        self.client = client

    def start_send(self):
        Sending(self.client).send()

    def start_receive(self):
        Receiving(self.client).listen()


threading.Thread(target=Client(c).start_send).start()
threading.Thread(target=Client(c).start_receive).start()
