# File Sharing Using Python

### Description
- File sharing can send any file using python sockets.
- It uses server and client connections to send file.
- One PC/laptop becomes server by running server.py file and any number of PCs/laptops can become client by running client.py

### Prerequisites

- [Python](https://www.python.org/downloads/)

### How To Run??

- Take client.py and server.py files one directory up.
- Run server in terminal/cmd using `python server.py` command.
- Change the ip address in client from `''` to the current ip of pc running server.py file.
  - On windows ip can be found by running `ipconfig`.
  - On Linux ip can be found by running `ifconfig`.
- Run client in terminal/cmd using `python client.py` command.
- Enter the path of the file from either server or client.
- Hurrayyyyy!!! File has been transfered successfully.
