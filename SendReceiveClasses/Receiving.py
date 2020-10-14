import os
import sys


class Receiving(object):
    def __init__(self, client):
        self.client = client
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

        self.send = None

    def listen(self):
        while True:
            self._receive_data(self.listen_received_bytes)
            if self.listen_received_data: self._first_msg_flag_functionality() if self.listen_first_msg_flag else self._setting_path_and_file_data()

    def _receive_data(self, bytes_to_receive):
        self.listen_received_data = self.client.recv(bytes_to_receive)
        return self.listen_received_data

    def _setting_path_and_file_data(self):
        self._set_path_of_file() if self.listen_name_flag else self._second_msg_flag_functionality() if self.listen_second_msg_flag else self._write_in_file()

    def _set_path_of_file(self):
        self.listen_path += self.listen_received_data.decode('utf-8')
        self.listen_name_len -= self.listen_received_bytes
        if self.listen_name_len < self.listen_received_bytes:
            if self.listen_name_len > 0: self.listen_path += self._receive_data(self.listen_name_len).decode('utf-8')
            self.listen_name_flag = not self.listen_name_flag
            self.listen_received_bytes = 26
            self.listen_file = open(self.listen_path, 'wb')
            print("Receiving: ", self.listen_path)

    def _write_in_file(self):
        self.listen_file.write(self.listen_received_data)
        if len(self.listen_received_data) != 26 and self.listen_msg_len > 26: self.listen_msg_len += abs(
            26 - len(self.listen_received_data))
        self.listen_msg_len -= self.listen_received_bytes
        print('completed: ', round(100 - ((self.listen_msg_len / self.listen_total_file_length) * 100)), '%')
        if self.listen_msg_len < self.listen_received_bytes:
            if self.listen_msg_len > 0: self.listen_file.write(self._receive_data(self.listen_msg_len))
            print('completed:  100 %')
            self.listen_file.close()
            print('Received: ', self.listen_file.name)
            self.__init__(self.client)

    def _first_msg_flag_functionality(self):
        self.listen_first_msg_flag = not self.listen_first_msg_flag
        self.listen_name_len = int(eval(self.listen_received_data.decode('utf-8'))['header'])
        self.listen_received_bytes = self.listen_name_len if self.listen_name_len < self.listen_received_bytes else self.listen_received_bytes

    def _second_msg_flag_functionality(self):
        self.listen_second_msg_flag = not self.listen_second_msg_flag
        self.listen_msg_len = int(eval(self.listen_received_data.decode('utf-8'))['header'])
        self.listen_total_file_length = self.listen_msg_len
        self.listen_received_bytes = self.listen_msg_len if self.listen_msg_len < self.listen_received_bytes else self.listen_received_bytes
