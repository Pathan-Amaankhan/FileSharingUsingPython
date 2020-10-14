import os
import sys


class Sending(object):
    def __init__(self, client):
        self.send_file = None
        self.send_path = ''
        self.client = client
        print("Just Type the path to send the file")

    def _get_names(self):
        file_paths = [input()]
        # for file_number in range(int(input('Enter the number of files to be send: '))):
        #     file_paths.append(input(f"Enter the file path of {file_number + 1} file: "))
        return file_paths

    def send(self):
        while True:
            file_paths = self._get_names()
            for file in file_paths:
                print("Started sending: ", file)
                self.send_file = open(file, 'rb')
                self.send_path = self._to_encoded_form(file.split('/')[-1] if '/' in file else file)

                send_file_size = self._to_encoded_form(str({'header': f'{os.stat(file).st_size:<12}'}))
                send_file_name = self._to_encoded_form(str({'header': f'{len(self.send_path):<12}'}))

                self.client.send(send_file_name)
                self.client.send(self.send_path)
                self.client.send(send_file_size)
                byte = self.send_file.read(26)
                while byte:
                    self.client.send(byte)
                    byte = self.send_file.read(26)
                self.send_file.close()
                print('done Sending: ', file)

    def _to_encoded_form(self, string):
        return string.encode('utf-8')
