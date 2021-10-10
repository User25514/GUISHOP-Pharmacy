import time
import sqlite3
from PyQt5.QtWidgets import QApplication, QLabel

def funcTime(func):
    def wrapper(*args,**kwargs):
        before = time.time()
        val = func(*args,**kwargs)
        print(f"Ended: {time.time() - before} Seconds")
        return val

    return wrapper
class Test():
    def Val():
        check1 = dataValidation.Register.nameVal("Dave")
        check2 = dataValidation.Register.nameVal("Jeremy2")
        check3 = dataValidation.Register.nameVal("Jared ")
        if check1 == True and check2 == False and check3 == False:
            print("Register.name\n[] Approved")
        else:
            print("Register.name\n[] Failed")
        check1 = dataValidation.Register.emailVal("wow@gmail.co.uk")
        check2 = dataValidation.Register.emailVal("AnotherOne@yahoo.com")
        check3 = dataValidation.Register.emailVal("AAAAAAA@gmail")
        check4 = dataValidation.Register.emailVal("GoodGame.com")
        if check1 == check2 == True and check3 == check4 == False:
            print("Register.emailVal\n[] Approved")
        else:
            print("Register.emailVal\n[] Failed")
        check1 = dataValidation.Register.passwordVal("MyNameIsYan11")
        check2 = dataValidation.Register.passwordVal("dav 54")
        check3 = dataValidation.Register.passwordVal("David")
        check4 = dataValidation.Register.passwordVal("SuperloooooooooongString1245")
        if check1 == True and check2 == check3 == check4 == False:
            print("Register.passwordVal\n[] Approved")
        else:
            print("Register.passwordVal\n[] Failed")
    def Test():
        pass
class dataValidation:
    class Register:#[6]
        def nameVal(name):
            try:
                num = 0
                for x in name:
                    if x.isnumeric() == True or x == " ":
                        raise Exception
                    else:
                        pass
                return True

            except Exception:
                return False
        def dobVal(DOB):
            try:
                return True
            except Exception:
                return False
        def emailVal(email):
            try:
                atSymbol,dot = 0,0
                for x in email:
                    if x == "@":
                        atSymbol += 1
                    elif x == ".":
                        dot += 1
                if atSymbol == 1 and dot >= 1 and dot <= 2:
                    return True
                else:
                    raise Exception
            except Exception:
                return False

        def passwordVal(password):
            try:
                x = len(password)
                if (x < 15 and x >= 8):
                    cap,char,num = 0,0,0
                    for x in password:
                        if x.isnumeric() == True:
                            num += 1
                        elif x == " ":
                            raise Exception
                        elif x.isupper() == True:
                            cap += 1
                        elif x.isalpha() == True:
                            char += 1
                    if not(num > 1 and (char+cap) > 4 and cap > 1):
                        raise Exception
                    else:
                        return True
                else:
                    raise Exception
            except Exception:
                return False

    class Login:#[7]
        def dobVal(DOB):
            try:
                pass
            except Exception:
                return False
        def passwordVal(password):
            try:
                pass
            except Exception:
                return False
class backProcess:
    def __init__(self):
        self.REG = dataValidation.Register
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        try:
            self.cur.execute("CREATE TABLE Register (name,dob,email,password)")
            self.con.commit()
        except:
            pass
    def Book():#[1][2] Books a free date/timeslot
        pass
    def ShopState():#[2][3] Choice to shop in person or thorough the application.
        pass
    def ShoppingRecipt():#[4] A recipt will be produced with details of what has been bought with the total price.
        # The receipt will be associated with a unique qr code that the user will use at the payment stage.
        pass
    def Register(self):#[5] Make Account
        #[6];
        a = b = c = d = False
        while True:
            if a == False:
                name = str(input("Name: "))
            if b == False:
                dob = str(input("DOB: "))
            if c == False:
                email = str(input("Email: "))
            if d == False:
                password = str(input("Password: "))
            a = self.REG.nameVal(name)
            b = self.REG.dobVal(dob)
            c = self.REG.emailVal(email)
            d = self.REG.passwordVal(password)
            if (a and b and c and d) == True:
                break
        self.cur.execute(f"INSERT INTO Register VALUES ('{name}','{dob}','{email}','{password}')")
        self.con.commit()
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)

        #self.con.close()
        pass
    def Login(self):#[5] login
        #[7]
        name = str(input("Name: "))
        dob = str(input("DOB: "))
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)
            if row[0] == name and row[1] == dob:
                print("Granted")
        pass
    pass
class frontProcess:# PythonQT https://build-system.fman.io/pyqt5-tutorial
    def __init__(self):
        pass

    @funcTime
    def f1(self):
        print("hello")
    def BookNotification():#[1] Confirmatin to the user that the slot was booked successfully.
        pass
    def Shop():#[3][4][5] Browse medicines of the cargories provided.
        # Each product will be associated with a particular price and QR code.
        pass
    def Payment():# Scan QR code on receipt.
        pass
if __name__ == "__main__":
    backProcess.Book()
    pass


#frontProcess.f1(0)
#Test.Val()
#rem = backProcess()
#rem.Register()
#rem.Register()
#rem.Login()
