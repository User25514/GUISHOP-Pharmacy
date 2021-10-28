import time
import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QTimer
import _thread
import mainBack
backProcess = mainBack.backProcess()
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
        "Date":"Calendar"
    },
    "Book":{
        "Status":False,
        "Name":"",
        "Date":"Calendar"
    }
}
class frontProcess:# PythonQT https://build-system.fman.io/pyqt5-tutorial
    def __init__(self):
        pass
    class calendarPopup(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Calendar Demo')
            if (data["Register"]["Status"] or data["Login"]["Status"]) == True:
                self.setGeometry(300, 300, 1000, 1000)
            else:
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
            #print('{0}/{1}/{2}'.format(qDate.month(), qDate.day(), qDate.year()))
            

        def notification(self):
                #alert = QMessageBox()
                #print(self.qDate)
                data[data["Direction"]]["Date"] = '{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year())
                
                #print(data)
                #alert.setText('{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year()))
                #alert.exec()
                self.close()
    class Register(QWidget):
        def initUI(self):
            layout = QVBoxLayout()
            label1 = QLabel()
            
            label1.setText("Name:")
            Username = QLineEdit()

            label2 = QLabel()
            label2.setText("DOB:")
            cal = frontProcess.calendarPopup()
            def calendar():
                data["Direction"] = "Register"
                qTimer.start()
                cal.show()
            Calbutton = QPushButton()
            Calbutton.setText("Calendar")
            Calbutton.clicked.connect(calendar)
            def changename():
                Calbutton.setText(data["Register"]["Date"])
            qTimer = QTimer()
            qTimer.setInterval(1000)
            qTimer.timeout.connect(changename)
            
            label3 = QLabel()
            label3.setText("Email:")
            Email = QLineEdit()
            label4 = QLabel()
            label4.setText("Password:")
            Password = QLineEdit()
            Password.setEchoMode(QLineEdit.Password)
            label5 = QLabel()
            label5.setText("Must contain 2 capital letters\n1 number\nbetween 8 and 15 characters long.")
            def notification():
                choice = backProcess.Register(Username.text(),data["Register"]["Date"],Email.text(),Password.text())
                alert = QMessageBox()
                if choice == True:
                    alert.setText("Registered")
                    data["Register"] = {
                        "Status":True,
                        "Name":"",
                        "Date":"Calendar",
                        "Password":""
                    }
                    Login = frontProcess.Login.initUI(0)
                    try:
                        for x in range(0,10):
                            layout.itemAt(x).widget().deleteLater()
                    except:
                        pass
                    layout.addLayout(Login)
                elif choice == False:
                    alert.setText("Error")
                else:
                    pass
                alert.exec()
            button1 = QPushButton()
            button1.setText("Approve")
            button1.clicked.connect(notification)
            layout.addWidget(label1)
            layout.addWidget(Username)
            layout.addWidget(label2)
            layout.addWidget(Calbutton)
            layout.addWidget(label3)
            layout.addWidget(Email)
            layout.addWidget(label4)
            layout.addWidget(Password)
            layout.addWidget(label5)
            layout.addWidget(button1)
            return layout
        
    class Login(QWidget):
        def initUI(self):
            layout = QVBoxLayout()
            reg = frontProcess.Register.initUI(0)
            label1 = QLabel()
            label1.setText("DOB:")
            label1.move(75,10)
            cal = frontProcess.calendarPopup()
            def calendar():
                data["Direction"] = "Login"
                qTimer.start()
                cal.show()
            CalLoginbutton = QPushButton()
            CalLoginbutton.setText("Calendar")
            CalLoginbutton.move(50,25)
            CalLoginbutton.clicked.connect(calendar)
            def changeName():
                CalLoginbutton.setText(data["Login"]["Date"])
            qTimer = QTimer()
            qTimer.setInterval(1000)
            qTimer.timeout.connect(changeName)

            label2 = QLabel()
            label2.setText("Password:")
            label2.move(60,50)
            Password = QLineEdit()
            Password.move(20,70)
            Password.setEchoMode(QLineEdit.Password)
            def notification(elf):
                choice = backProcess.Login(data["Login"]["Date"],Password.text())
                alert = QMessageBox()
                if choice == True:
                    data[data["Direction"]]["Status"] = True
                    data["Direction"] = "Book"
                    print(data)
                    Book = frontProcess.Book()
                    Book.show()
                else:
                    alert = QMessageBox()
                    alert.setText("Error")
                    alert.exec()
            button1 = QPushButton()
            button1.setText("Login")
            button1.move(50,100)
            button1.clicked.connect(notification)

            label3 = QLabel()
            label3.setText("Or")
            label3.move(80,130)
            
            def register():
                try:
                    for x in range(0,10):
                        layout.itemAt(x).widget().deleteLater()
                except:
                    pass
                layout.addLayout(reg)
            button2 = QPushButton()
            button2.setText("Register")
            button2.move(50,150)
            button2.clicked.connect(register)
            layout.addWidget(label1)
            layout.addWidget(CalLoginbutton)
            layout.addWidget(label2)
            layout.addWidget(Password)
            layout.addWidget(button1)
            layout.addWidget(label3)
            layout.addWidget(button2)
            return layout
    
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
    Login = frontProcess.Login.initUI(0)
    register = frontProcess.Register.initUI(0)
    cal = frontProcess.calendarPopup()
    reg = frontProcess.Register()
    #Login = frontProcess.Login()
    button = QPushButton('Register')
    button2 = QPushButton('Calendar')
    button3 = QPushButton('Login')
    button4 = QPushButton('Change')
    button5 = QPushButton('Change2')
    def notification():
        reg.show()
    def calendar():
        cal.show()
    def login():
        Login.show()
    def change():
        try:
            for x in range(0,5):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        layout.addLayout(Login)
    def change2():
        try:
            for x in range(0,10):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        layout.addLayout(register)
    #Login.show()
    button.clicked.connect(notification)
    button2.clicked.connect(calendar)
    button3.clicked.connect(login)
    layout.addWidget(button)
    layout.addWidget(button2)
    layout.addWidget(button3)
    layout.addWidget(button4)
    button4.clicked.connect(change)
    button5.clicked.connect(change2)
    window.setLayout(layout)
    window.show()
    app.exec(app.exec_())
if __name__ == "__main__":
    main()
