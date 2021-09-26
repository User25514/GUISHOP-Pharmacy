import socket
import threading
class Connection:
    def __init__(self):
        self.Settings = {
            "HEADER" : 64,
            "PORT" : 5050,
            "FORMAT" : "utf-8",
            "DISCONNECT_MESSAGE" : "!DISCONNECT",
            "SERVER" : socket.gethostbyname(socket.gethostname())}
        self.Settings["ADDR"] = (self.Settings["SERVER"],self.Settings["PORT"])
        self.HOST = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.Settings["ADDR"])
    def handle_client(self):
        print(f"Connection: {self.Settings['ADDR']} connected")
        connected = True
        while connected:
            msg_length = self.Settings["conn"].recv(self.Settings["HEADER"]).decode(self.Settings["FORMAT"])
            if msg_length:
                msg_length = int(msg_length)
                msg = self.Settings["conn"].recv(msg_length).decode(self.Settings["FORMAT"])
                if msg == self.Settings["DISCONNECT_MESSAGE"]:
                    connected = False
                    break
                print(f'[{self.Settings["addr"]}]: {msg}')
                self.Settings["conn"].send(str(input("REPLY: ")).encode(self.Settings["FORMAT"]))
            else:
                pass
        self.Settings["conn"].close()
        print(f"Connection: {self.Settings['ADDR']} disconnected")
    def start(self):
        self.server.listen()
        print(f"Listening on {self.Settings['SERVER']}")
        while True:
            self.Settings["conn"], self.Settings["addr"] = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=())
            thread.start()
            print(f"Active connections: {threading.activeCount()-1}")
print("Starting")
Sender = Connection()
Sender.start()
