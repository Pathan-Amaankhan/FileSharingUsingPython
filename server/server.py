import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 4444))

s.listen()


class Server:

    def __init__(self):
        self.listen_name_flag = True
        self.listen_received_bytes = 26
        self.listen_total_file_length = 0
        self.listen_path = ''
        self.listen_second_msg_flag = True
        self.listen_first_msg_flag = True
        self.listen_name_len = None
        self.listen_received_data = None
        self.listen_msg_len = None
        self.listen_file = None

    def listen(self, client):
        while True:
            self.__receive_data(client, self.listen_received_bytes)
            if self.listen_received_data: self.__first_msg_flag_functionality() if self.listen_first_msg_flag else self.__setting_path_and_file_data(client)

    def __receive_data(self, client, bytes_to_receive):
        self.listen_received_data = client.recv(bytes_to_receive)
        return self.listen_received_data

    def __setting_path_and_file_data(self, client):
        self.__set_path_of_file(client) if self.listen_name_flag else self.__second_msg_flag_functionality() if self.listen_second_msg_flag else self.__write_in_file(client)

    def __set_path_of_file(self, client):
        self.listen_path += self.listen_received_data.decode('utf-8')
        self.listen_name_len -= self.listen_received_bytes
        if self.listen_name_len < self.listen_received_bytes:
            if self.listen_name_len > 0: self.listen_path += self.__receive_data(client, self.listen_name_len).decode('utf-8')
            self.listen_name_flag = not self.listen_name_flag
            self.listen_received_bytes = 26
            self.listen_file = open(self.listen_path, 'wb')
            print("Receiving: ", self.listen_path)

    def __write_in_file(self, client):
        self.listen_file.write(self.listen_received_data)
        if len(self.listen_received_data) != 26 and self.listen_msg_len > 26: self.listen_msg_len += abs(26 - len(self.listen_received_data))
        self.listen_msg_len -= self.listen_received_bytes
        print('completed: ', round(100 - ((self.listen_msg_len / self.listen_total_file_length) * 100)), '%')
        if self.listen_msg_len < self.listen_received_bytes:
            if self.listen_msg_len > 0: self.listen_file.write(self.__receive_data(client, self.listen_msg_len))
            print('completed:  100 %')
            self.listen_file.close()
            print('Received: ', self.listen_file.name)
            self.__init__()

    def __first_msg_flag_functionality(self):
        self.listen_first_msg_flag = not self.listen_first_msg_flag
        self.listen_name_len = int(eval(self.listen_received_data.decode('utf-8'))['header'])
        self.listen_received_bytes = self.listen_name_len if self.listen_name_len < self.listen_received_bytes else self.listen_received_bytes

    def __second_msg_flag_functionality(self):
        self.listen_second_msg_flag = not self.listen_second_msg_flag
        self.listen_msg_len = int(eval(self.listen_received_data.decode('utf-8'))['header'])
        self.listen_total_file_length = self.listen_msg_len
        self.listen_received_bytes = self.listen_msg_len if self.listen_msg_len < self.listen_received_bytes else self.listen_received_bytes








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
    threading.Thread(target=Server().listen, args=[c]).start()
    # threading.Thread(target=send, args=(c, addr)).start()