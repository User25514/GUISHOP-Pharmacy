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
        "Date":"",
        "Password":""
    },
    "Login":{
        "Status":False,
        "Date":""
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
    layout = QGridLayout()
    def Timeslot():
        try:
            for x in range(0,100):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        #layout.addLayout()
    logLabel1 = QLabel()
    logLabel1.setText("DOB:")
    logLabel1.move(75,10)
    cal = frontProcess.calendarPopup()
    def logCalendar():
        data["Direction"] = "Login"
        qTimer.start()
        cal.show()
    LogCalLoginbutton = QPushButton()
    LogCalLoginbutton.setText("Calendar")
    LogCalLoginbutton.move(50,25)
    LogCalLoginbutton.clicked.connect(logCalendar)
    def changeName():
        try:
            if data["Login"]["Date"] != "":
                LogCalLoginbutton.setText(data["Login"]["Date"])
            if data["Register"]["Date"] != "":
                regCalbutton.setText(data["Register"]["Date"])
        except:
            pass
    qTimer = QTimer()
    qTimer.setInterval(1000)
    qTimer.timeout.connect(changeName)

    logLabel2 = QLabel()
    logLabel2.setText("Password:")
    logLabel2.move(60,50)
    logPassword = QLineEdit()
    logPassword.move(20,70)
    logPassword.setEchoMode(QLineEdit.Password)
    def logNotification():
        choice = backProcess.Login(data["Login"]["Date"],logPassword.text())
        alert = QMessageBox()
        if choice == True:
            data[data["Direction"]]["Status"] = True
            data["Direction"] = "Book"
            print(data)
            Timeslot()
            #Book = frontProcess.Book()
            #Book.show()
        else:
            alert = QMessageBox()
            alert.setText("Error")
            alert.exec()
    logButton1 = QPushButton()
    logButton1.setText("Login")
    logButton1.move(50,100)
    logButton1.clicked.connect(logNotification)

    #Register:
    regLabel1 = QLabel()
    regLabel1.setText("Name:")
    regUsername = QLineEdit()
    regLabel2 = QLabel()
    regLabel2.setText("DOB:")
    def regCalendar():
        data["Direction"] = "Register"
        qTimer.start()
        cal.show()
    regCalbutton = QPushButton()
    regCalbutton.setText("Calendar")
    regCalbutton.clicked.connect(regCalendar)

    
    regLabel3 = QLabel()
    regLabel3.setText("Email:")
    regEmail = QLineEdit()
    regLabel4 = QLabel()
    regLabel4.setText("Password:")
    regPassword = QLineEdit()
    regPassword.setEchoMode(QLineEdit.Password)
    regLabel5 = QLabel()
    regLabel5.setText("Must contain 2 capital letters\n1 number\nbetween 8 and 15 characters long.")
    def regNotification():
        choice = backProcess.Register(regUsername.text(),data["Register"]["Date"],regEmail.text(),regPassword.text())
        print(choice)
        alert = QMessageBox()
        if choice == True:
            alert.setText("Registered")
            data["Register"] = {
                "Status":True,
                "Name":"",
                "Date":"Calendar",
                "Password":""
            }
            Timeslot()
        elif choice == False:
            alert.setText("Error")
        else:
            pass
        alert.exec()
    regButton1 = QPushButton()
    regButton1.setText("Approve")
    regButton1.clicked.connect(regNotification)
    #Login Stuff
    layout.addWidget(QLabel("Login: "),0,0)
    layout.addWidget(logLabel1,1,0)
    layout.addWidget(LogCalLoginbutton,2,0)
    layout.addWidget(logLabel2,3,0)
    layout.addWidget(logPassword,4,0)
    layout.addWidget(logButton1,5,0)
    #Register Stuff
    layout.addWidget(QLabel("Register: "),0,1)
    layout.addWidget(regLabel1,1,1)
    layout.addWidget(regUsername,2,1)
    layout.addWidget(regLabel2,3,1)
    layout.addWidget(regCalbutton,4,1)
    layout.addWidget(regLabel3,5,1)
    layout.addWidget(regEmail,6,1)
    layout.addWidget(regLabel4,7,1)
    layout.addWidget(regPassword,8,1)
    layout.addWidget(regLabel5,9,1)
    layout.addWidget(regButton1,10,1)
    #
    window.setLayout(layout)
    window.show()
    app.exec(app.exec_())
if __name__ == "__main__":
    main()
