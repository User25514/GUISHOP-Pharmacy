import time
import sqlite3
import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
import _thread
data = {
    "Direction":"",
    "Register":{
        "Status":False,
        "Name":"",
        "Date":"",
        "Password":""
    },
    "Login":{
        "Status":False,
        "Name":"",
        "Date":""
    }
}
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
    def Register(self,name,dob,email,password):#[5] Make Account
        #[6];
        self.REG = dataValidation.Register
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        a = self.REG.nameVal(name)
        b = self.REG.dobVal(dob)
        c = self.REG.emailVal(email)
        d = self.REG.passwordVal(password)
        print(name,dob,email,password)
        print(a,b,c,d)
        if (a or b or c or d) == False:
            return False
        else:
            pass
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)
            if row[2] == email:
                self.con.close()
                return False
        self.cur.execute(f"INSERT INTO Register VALUES ('{name}','{dob}','{email}','{password}')")
        self.con.commit()
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)

        self.con.close()
        return True
        pass
    def Login(self,dob,password):#[5] login
        #[7]
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)
            if row[3] == password and row[1] == dob:
                self.con.close()
                return True
        self.con.close()
        return False
        pass
    class MultiThread():
        def DateCheck(DateDic):
            pass
class frontProcess:# PythonQT https://build-system.fman.io/pyqt5-tutorial
    def __init__(self):
        pass
    class calendarPopup(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Calendar Demo')
            self.setGeometry(300, 300, 350, 250)
            self.initUI()
        def initUI(self):
            self.calendar = QCalendarWidget(self)
            self.button = QPushButton(self)
            self.button.setText("Approve")
            self.button.move(20,210)
            self.button.clicked.connect(self.notification)
            self.calendar.move(20, 20)
            self.calendar.setGridVisible(True)
            Year = datetime.now().year
            Month = datetime.now().month
            Day = datetime.now().day
            self.qDate = QDate(Year, Month, Day)
            self.calendar.setMinimumDate(QDate(Year, Month, Day))
            if (Day + 15) > calendar.monthrange(Year, Month)[1]:
                newDay = (Day + 15) - calendar.monthrange(Year, Month)[1]
                self.calendar.setMaximumDate(QDate(Year, Month+1, newDay))
            else:
                self.calendar.setMaximumDate(QDate(Year, Month, Day + 15))
            self.calendar.setSelectedDate(QDate(Year, Month, 1))
            self.calendar.clicked.connect(self.printDateInfo)

        def printDateInfo(self, qDate):
            self.qDate = qDate
            print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))

        def notification(self):
                #alert = QMessageBox()
                print(self.qDate)
                data[data["Direction"]]["Date"] = '{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year())
                
                print(data)
                #alert.setText('{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year()))
                #alert.exec()
                self.close()
    class Register(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Register')
            self.setGeometry(300, 300, 350, 250)
            self.initUI()
            #_thread.start_new_thread(backProcess.MultiThread.DateCheck, (DateCheck,))
        def initUI(self):
            self.label1 = QLabel(self)
            self.label1.setText("Name:")
            self.label1.move(20,10)
            self.Username = QLineEdit(self)
            self.Username.move(20,30)

            self.label2 = QLabel(self)
            self.label2.setText("DOB:")
            self.label2.move(20,50)
            #self.DOB = QLineEdit(self)
            #self.DOB.move(20,70)
            cal = frontProcess.calendarPopup()
            def calendar():
                data["Direction"] = "Register"
                cal.show()
            self.Calbutton = QPushButton(self)
            self.Calbutton.setText("Calendar")
            self.Calbutton.move(200,60)
            self.Calbutton.clicked.connect(calendar)


            self.label3 = QLabel(self)
            self.label3.setText("Email:")
            self.label3.move(20,90)
            self.Email = QLineEdit(self)
            self.Email.move(20,110)

            self.label4 = QLabel(self)
            self.label4.setText("Password:")
            self.label4.move(20,130)
            self.Password = QLineEdit(self)
            self.Password.move(20,150)
            self.Password.setEchoMode(QLineEdit.Password)
            self.label5 = QLabel(self)
            self.label5.setText("Must contain 2 capital letters\n1 number\nbetween 8 and 15 characters long.")
            self.label5.move(170,133)

            self.button = QPushButton(self)
            self.button.setText("Approve")
            self.button.move(20,210)
            self.button.clicked.connect(self.notification)

        def notification(self):
            choice = backProcess.Register(self,self.Username.text(),self.DOB.text(),self.Email.text(),self.Password.text())
            alert = QMessageBox()
            if choice == True:
                alert.setText("Registered")
                self.close()
            elif choice == False:
                alert.setText("Error")
            else:
                pass
            alert.exec()
        
    class Login(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Login')
            self.setGeometry(300, 300, 350, 250)
            self.initUI()
        def initUI(self):
            self.label1 = QLabel(self)
            self.label1.setText("DOB:")
            self.label1.move(20,10)
            self.DOB = QLineEdit(self)
            self.DOB.move(20,30)

            self.label4 = QLabel(self)
            self.label4.setText("Password:")
            self.label4.move(20,50)
            self.Password = QLineEdit(self)
            self.Password.move(20,70)
            self.Password.setEchoMode(QLineEdit.Password)

            self.button = QPushButton(self)
            self.button.setText("Approve")
            self.button.move(20,210)
            self.button.clicked.connect(self.notification)

        def notification(self):
            choice = backProcess.Login(self,self.DOB.text(),self.Password.text())
            alert = QMessageBox()
            if choice == True:
                alert.setText("Logged In")
                self.close()
            elif choice == False:
                alert.setText("Error")
            else:
                pass
            alert.exec()
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
def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    cal = frontProcess.calendarPopup()
    reg = frontProcess.Register()
    Login = frontProcess.Login()
    button = QPushButton('Register')
    button2 = QPushButton('Calendar')
    button3 = QPushButton('Login')
    #line = QLineEdit("Here")
    #layout.addWidget(line)
    def notification():
        #alert = QMessageBox()
        #alert.setText('You clicked the button!')
        #alert.exec()
        reg.show()
    def calendar():
        cal.show()
    def login():
        Login.show()
    button.clicked.connect(notification)
    button2.clicked.connect(calendar)
    button3.clicked.connect(login)
    layout.addWidget(button)
    layout.addWidget(button2)
    layout.addWidget(button3)
    window.setLayout(layout)
    window.show()
    app.exec(app.exec_())
if __name__ == "__main__":
    main()



#frontProcess.f1(0)
#Test.Val()
#rem = backProcess()
#rem.Register()
#rem.Register()
#rem.Login()
