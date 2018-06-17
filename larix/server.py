import socket
import json
import time
import threading


class Server(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)  # receiving json-message from a client
            data = data.decode()
            print(data)  # displaying json-message from the client
            data = json.loads(data)  # here we change json to dict to be able to change the timestamp
            data['timestamp'] = time.ctime()  # updating timestamp
            data = json.dumps(data)
            data = data.encode()
            conn.send(data)  # sending the updated json-message to the client
            conn.close()


server = Server()

server.start()
