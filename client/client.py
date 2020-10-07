import socket
import threading
import os

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('', 4444))


class Client:

    def __init__(self, client):
        self.file = None
        self.path = ''
        self.client = client
        self.file_paths = []

    def start(self):
        for file_number in range(int(input('Enter the number of files to be send: '))):
            self.file_paths.append(input(f"Enter the file path of {file_number+1} file: "))

    def send(self):
        self.start()
        for file in self.file_paths:
            print("Started sending: ", file)
            self.file = open(file, 'rb')
            self.path = self.to_encoded_form(file)
            send_file_name = self.to_encoded_form(str({'header': f'{len(self.path):<12}'}))

            send_file_size = self.to_encoded_form(str({'header': f'{os.stat(self.path).st_size:<12}'}))

            self.client.send(send_file_name)
            self.client.send(self.path)
            self.client.send(send_file_size)
            byte = self.file.read(26)
            while byte:
                self.client.send(byte)
                byte = self.file.read(26)
            self.file.close()
            print('done Sending: ', file)

    def to_encoded_form(self, string):
        return string.encode('utf-8')


# def receive():
#     global connection
#     file = open('recieved_by_client.apk', 'wb')
#     while True:
#         rec = c.recv(1024)
#         if rec:
#             try:
#                 if rec.decode('utf-8') == 'end of file':
#                     break
#             except:
#                 pass
#             file.write(rec)
#             print(rec)
#             print('received')
#     print('closed')
#     file.close()
#     while True:
#         if not connection:
#             c.close()
#             break

threading.Thread(target=Client(c).send).start()
# threading.Thread(target=receive).start()
