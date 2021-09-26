import socket
class Connection:
    def __init__(self):
        self.Settings = {
            "HEADER" : 64,
            "PORT" : 5050,
            "FORMAT" : "utf-8",
            "DISCONNECT_MESSAGE" : "!DISCONNECT",
            "SERVER" : "172.21.128.1"}
        self.Settings["ADDR"] = (self.Settings["SERVER"],self.Settings["PORT"])
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(self.Settings["ADDR"]) 
    def send(self,msg):
        message = msg.encode(self.Settings["FORMAT"])
        msg_length = len(message)
        send_length = str(msg_length).encode(self.Settings["FORMAT"])
        send_length += b' ' * (self.Settings["HEADER"] - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
    def recieve(self):
        return self.client.recv(2048).decode(self.Settings["FORMAT"])
    def Disconnect(self):
        message = self.Settings["DISCONNECT_MESSAGE"].encode(self.Settings["FORMAT"])
        msg_length = len(message)
        send_length = str(msg_length).encode(self.Settings["FORMAT"])
        send_length += b' ' * (self.Settings["HEADER"] - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
class MessageHandler:
    def __init__(self):
        pass
    def commands(self,command):
        print("jesus")
        if command[0] == "-":
            print(command)

Sender = Connection()
while True:
    try:
        Sender.send(str(input("Message: ")))
        recieve = Sender.recieve()
        MessageHandler.commands(0,recieve)
    except Exception:
        print("Problem")
        Sender.Disconnect()
        break