import socket
import json
import time
import threading


class Client(threading.Thread):
    def __init__(self, id):
        self.id = id
        super().__init__()

    def run(self):
        duration = 10  # here we say that a thread should live and send messages to server for 10 seconds only
        while duration != 0:
            s = socket.socket()
            host = socket.gethostname()
            port = 12345
            s.connect((host, port))  # connecting to the server
            data = {'id': self.id, 'timestamp': time.ctime()}
            jsondata = json.dumps(data)  # encoding message in json
            time.sleep(1)  # here the client waits for 1 second
            jsondata = jsondata.encode()
            s.send(jsondata)  # sending the message to the server
            data = s.recv(1024)  # receiving the message back
            data = data.decode()
            print(data)  # displaying what was received from the server
            duration -= 1
            s.close()

clients = []

# below 5 objects of a client are created
client1 = Client(1)
clients.append(client1)
client2 = Client(2)
clients.append(client2)
client3 = Client(3)
clients.append(client3)
client4 = Client(4)
clients.append(client4)
client5 = Client(5)
clients.append(client5)

for client in clients:
    client.start()

