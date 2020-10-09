import socket
import threading
import os

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('', 4444))


class Client:

    def __init__(self):
        self.send_file = None
        self.send_path = ''

    def __get_names(self):
        file_paths = []
        for file_number in range(int(input('Enter the number of files to be send: '))):
            file_paths.append(input(f"Enter the file path of {file_number + 1} file: "))
        return file_paths

    def send(self, client):
        file_paths = self.__get_names()
        for file in file_paths:
            print("Started sending: ", file)
            self.send_file = open(file, 'rb')
            self.send_path = self.__to_encoded_form(file.split('/')[-1] if '/' in file else file)

            send_file_size = self.__to_encoded_form(str({'header': f'{os.stat(file).st_size:<12}'}))
            send_file_name = self.__to_encoded_form(str({'header': f'{len(self.send_path):<12}'}))

            client.send(send_file_name)
            client.send(self.send_path)
            client.send(send_file_size)
            byte = self.send_file.read(26)
            while byte:
                client.send(byte)
                byte = self.send_file.read(26)
            self.send_file.close()
            print('done Sending: ', file)

    def __to_encoded_form(self, string):
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

threading.Thread(target=Client().send, args=[c]).start()
# threading.Thread(target=receive).start()
