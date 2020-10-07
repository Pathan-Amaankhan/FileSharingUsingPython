import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 4444))

s.listen()


class Server:

    def __init__(self):
        self.name_flag = True
        self.received_bytes = 26
        self.path = ''
        self.second_msg_flag = True
        self.first_msg_flag = True
        self.name_len = None
        self.received_data = None
        self.msg_len = None
        self.file = None

    def listen(self, client, addr):
        while True:
            self.receive_data(client, self.received_bytes)
            if self.received_data: self.first_msg_flag_functionality() if self.first_msg_flag else self.setting_path_and_file_data(client)

    def receive_data(self, client, bytes_to_receive):
        self.received_data = client.recv(bytes_to_receive)
        return self.received_data

    def setting_path_and_file_data(self, client):
        self.set_path_of_file(client) if self.name_flag else self.second_msg_flag_functionality() if self.second_msg_flag else self.write_in_file(client)

    def set_path_of_file(self, client):
        self.path += self.received_data.decode('utf-8')
        self.name_len -= self.received_bytes
        if self.name_len < self.received_bytes:
            if self.name_len > 0: self.path += self.receive_data(client, self.name_len).decode('utf-8')
            self.name_flag = not self.name_flag
            self.received_bytes = 26
            self.file = open(self.path, 'wb')
            print("Receiving: ", self.path)

    def write_in_file(self, client):
        self.file.write(self.received_data)
        if len(self.received_data) != 26 and self.msg_len > 26: self.msg_len += abs(26 - len(self.received_data))
        self.msg_len -= self.received_bytes
        if self.msg_len < self.received_bytes:
            if self.msg_len > 0: self.file.write(self.receive_data(client, self.msg_len))
            self.file.close()
            print('Received: ', self.file.name)
            self.__init__()

    def first_msg_flag_functionality(self):
        self.first_msg_flag = not self.first_msg_flag
        self.name_len = int(eval(self.received_data.decode('utf-8'))['header'])
        self.received_bytes = self.name_len if self.name_len < self.received_bytes else self.received_bytes

    def second_msg_flag_functionality(self):
        self.second_msg_flag = not self.second_msg_flag
        self.msg_len = int(eval(self.received_data.decode('utf-8'))['header'])
        self.received_bytes = self.msg_len if self.msg_len < self.received_bytes else self.received_bytes


# def send(c, addr):
#     global connection
#     while connection:
#         file = open('app-debug.apk', 'rb')
#         byte = file.read(1)
#         while byte:
#             c.send(byte)
#             byte = file.read(1)
#         file.close()
#         time.sleep(5)
#         c.send('end of file'.encode('utf-8'))
#         connection = False
#     print('done')


while True:
    c, addr = s.accept()
    print(addr, c)
    threading.Thread(target=Server().listen, args=(c, addr)).start()
    # threading.Thread(target=send, args=(c, addr)).start()
