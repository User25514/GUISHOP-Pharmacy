import time
import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QTimer
import _thread
from mainValidation import dataValidation
from mainBack import backProcess
data = {
    "Direction":"",
    "Register":{
        "Status":False,
        "Name":"",
        "Date":"Calendar",
        "Password":""
    },
    "Login":{
        "Status":False,
        "Name":"",
        "Date":"Calendar"
    }
}
def funcTime(func):
    def wrapper(*args,**kwargs):
        before = time.time()
        val = func(*args,**kwargs)
        print(f"Ended: {time.time() - before} Seconds")
        return val

    return wrapper

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
            
            if data["Direction"] == "Book":
                self.calendar.setMinimumDate(QDate(Year, Month, Day))
                if (Day + 15) > calendar.monthrange(Year, Month)[1]:
                    newDay = (Day + 15) - calendar.monthrange(Year, Month)[1]
                    self.calendar.setMaximumDate(QDate(Year, Month+1, newDay))
                else:
                    self.calendar.setMaximumDate(QDate(Year, Month, Day + 15))
            else:
                self.calendar.setMinimumDate(QDate(Year-100, Month, Day))
                self.calendar.setMaximumDate(QDate(Year-18, Month, Day))
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
            self.setGeometry(500, 500, 350, 250)
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
            self.Calbutton.move(20,65)
            self.Calbutton.clicked.connect(calendar)

            self.qTimer = QTimer()
            self.qTimer.setInterval(1000)
            self.qTimer.timeout.connect(self.changename)
            self.qTimer.start()

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
            choice = backProcess.Register(self,self.Username.text(),data["Register"]["Date"],self.Email.text(),self.Password.text())
            alert = QMessageBox()
            if choice == True:
                alert.setText("Registered")
                self.close()
            elif choice == False:
                alert.setText("Error")
            else:
                pass
            alert.exec()
        def changename(self):
            self.Calbutton.setText(data["Register"]["Date"])
        
    class Login(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Login')
            self.setGeometry(500, 500, 200, 200)
            self.initUI()
        def initUI(self):
            reg = frontProcess.Register()
            self.label1 = QLabel(self)
            self.label1.setText("DOB:")
            self.label1.move(75,10)
            #self.DOB = QLineEdit(self)
            #self.DOB.move(20,30)
            cal = frontProcess.calendarPopup()
            def calendar():
                data["Direction"] = "Login"
                cal.show()
            self.CalLoginbutton = QPushButton(self)
            self.CalLoginbutton.setText("Calendar")
            self.CalLoginbutton.move(50,25)
            self.CalLoginbutton.clicked.connect(calendar)

            self.qTimer = QTimer()
            self.qTimer.setInterval(1000)
            self.qTimer.timeout.connect(self.changeName)
            self.qTimer.start()

            self.label4 = QLabel(self)
            self.label4.setText("Password:")
            self.label4.move(60,50)
            self.Password = QLineEdit(self)
            self.Password.move(20,70)
            self.Password.setEchoMode(QLineEdit.Password)

            self.button = QPushButton(self)
            self.button.setText("Login")
            self.button.move(50,100)
            self.button.clicked.connect(self.notification)

            self.label5 = QLabel(self)
            self.label5.setText("Or")
            self.label5.move(80,130)
            
            def register():
                reg.show()
                self.close()
            self.button = QPushButton(self)
            self.button.setText("Register")
            self.button.move(50,150)
            self.button.clicked.connect(register)

        def notification(self):
            choice = backProcess.Login(self,data["Login"]["Date"],self.Password.text())
            alert = QMessageBox()
            if choice == True:
                Book = frontProcess.Book()
                Book.show()
                self.close()
            else:
                alert = QMessageBox()
                alert.setText("Error")
                alert.exec()
        def changeName(self):
            self.CalLoginbutton.setText(data["Login"]["Date"])
    class Book(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Booking')
            self.setGeometry(500, 500, 1000, 1000)
            self.initUI()
        def initUI(self):
            reg = frontProcess.Register()
            self.label1 = QLabel(self)
            self.label1.setText("WOWWWW:")
            self.label1.move(75,10)
            #self.DOB = QLineEdit(self)
            #self.DOB.move(20,30)
            cal = frontProcess.calendarPopup()
            def calendar():
                data["Direction"] = "Login"
                cal.show()
            self.CalLoginbutton = QPushButton(self)
            self.CalLoginbutton.setText("Calendar")
            self.CalLoginbutton.move(50,25)
            self.CalLoginbutton.clicked.connect(calendar)

            self.qTimer = QTimer()
            self.qTimer.setInterval(1000)
            self.qTimer.timeout.connect(self.changeName)
            self.qTimer.start()

            self.label4 = QLabel(self)
            self.label4.setText("Password:")
            self.label4.move(60,50)
            self.Password = QLineEdit(self)
            self.Password.move(20,70)
            self.Password.setEchoMode(QLineEdit.Password)

            self.button = QPushButton(self)
            self.button.setText("Login")
            self.button.move(50,100)
            self.button.clicked.connect(self.notification)

            self.label5 = QLabel(self)
            self.label5.setText("Or")
            self.label5.move(80,130)
            
            def register():
                #alert = QMessageBox()
                #alert.setText('You clicked the button!')
                #alert.exec()
                reg.show()
                self.close()
            self.button = QPushButton(self)
            self.button.setText("Register")
            self.button.move(50,150)
            self.button.clicked.connect(register)

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
        def changeName(self):
            self.CalLoginbutton.setText(data["Login"]["Date"])
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
# https://youtu.be/82v2ZR-g6wY