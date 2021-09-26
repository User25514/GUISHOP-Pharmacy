import socket
import threading
import pandas as pd

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
                Response = MessageHandler.commands(0,msg)
                self.Settings["conn"].send(Response.encode(self.Settings["FORMAT"]))
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
class MessageHandler:
    def __init__(self):
        pass
    def commands(self,command):
        if command[0] == "-":
            command = command.split("-")
            if command[1] == "login":
                Data = pd.read_csv('GUISHOP-Pharmacy\Databases\Credentials.csv')
                for x in range(0,len(Data)):
                    if command[2] == str(Data.iloc[x]["DOB"]):
                        if command[3] == str(Data.iloc[x]["Password"]):
                            return "Login Successful"
                return "No User"
            elif command[1] == "register":
                Data = pd.read_csv('GUISHOP-Pharmacy\Databases\Credentials.csv')
                print(Data)
                for x in range(0,len(Data)):
                    print(command[4])
                    print(str(Data.iloc[x]["Email"]))
                    if not(command[4] == str(Data.iloc[x]["Email"])) and len(command[5]) >= 8 and len(command[5]) <= 15:
                        PasswordRule = {
                            "Caps Min" : 1,
                            "Caps Max" : len(command[5])-2,
                            "Caps Num" : 0,
                            "Numbers Min" : 1,
                            "Numbers Max" : len(command[5])-2,
                            "Numbers Num" : 0
                        }
                        for x in command[5]:
                            if x.isupper() == True:
                                PasswordRule["Caps Num"] += 1
                                if PasswordRule["Caps Num"] >= PasswordRule["Caps Max"]:
                                    return "Password Error"
                            elif x.isnumeric() == True:
                                PasswordRule["Numbers Num"] += 1
                                if PasswordRule["Numbers Num"] >= PasswordRule["Numbers Max"]:
                                    return "Password Error"
                        f = open('GUISHOP-Pharmacy\Databases\Credentials.csv', "a")
                        f.write(f"{len(Data)},{command[2]},{command[3]},{command[4]},{command[5]}\n")
                        f.close()
                        return "Register Successful"
                    else:
                        return "Email In Use"
        return "Error"

print("Starting")
Sender = Connection()
Sender.start()
