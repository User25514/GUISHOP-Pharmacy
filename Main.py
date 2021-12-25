import time
import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import _thread
import mainBack
backProcess = mainBack.backProcess()
data = {
    "User ID":0,
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
        "Date":"",
        "Time":"",
    },
    "Shop":{
        "Status":False,
        "Name":"",
        "Date":""
    }
}
class frontProcess:
    def __init__(self):
        pass
    class calendarPopup(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Calendar')
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
            print(data["Direction"])
            if data["Direction"] == "Book":
                print("Book Time")
                self.calendar.setMinimumDate(QDate(Year, Month, Day))
                if (Day + 15) > calendar.monthrange(Year, Month)[1]:
                    newDay = (Day + 15) - calendar.monthrange(Year, Month)[1]
                    self.calendar.setMaximumDate(QDate(Year, Month+1, newDay))
                else:
                    self.calendar.setMaximumDate(QDate(Year, Month, Day + 15))
            else:
                self.calendar.setMinimumDate(QDate(Year-118, Month, Day))
                self.calendar.setMaximumDate(QDate(Year-18, Month, Day))
            self.calendar.setSelectedDate(QDate(Year, Month, 1))
            self.calendar.clicked.connect(self.printDateInfo)

        def printDateInfo(self, qDate):
            self.qDate = qDate            

        def notification(self):
                data[data["Direction"]]["Date"] = '{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year())
                self.close()
    
    def Book(layout,window):#[1] Confirmatin to the user that the slot was booked successfully.
        try:
            for x in range(0,100):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        bookLabel1 = QLabel("Date: ")
        bookCal = frontProcess.calendarPopup()
        def bookCalendar():
            print(data)
            qTimer.start()
            bookCal.show()
        bookCalLoginbutton = QPushButton("Calendar")
        bookCalLoginbutton.clicked.connect(bookCalendar)
        def changeName():
            try:
                if data["Book"]["Date"] != "" and bookCalLoginbutton.text() != data["Book"]["Date"]:
                    bookCalLoginbutton.setText(data["Book"]["Date"])
                    print("Run")
                    print(data["Book"]["Date"])
                    Status, Times = backProcess.BookRecall(data["Book"]["Date"])
                    print(Times)
                    if Status == True:
                        print("less go")
                        for x in range(0,len(Times)-1):
                            LabelThing = QRadioButton("Slot " + str(x+1) + ": " + str(Times[x]))
                            LabelThing.Time = Times[x]
                            print(x+4)
                            LabelThing.clicked.connect(TimeChoice)
                            layout.addWidget(LabelThing,x+3,1)
                            print(x)
            except:
                pass

        qTimer = QTimer()
        qTimer.setInterval(1000)
        qTimer.timeout.connect(changeName)

        bookLabel2 = QLabel("Time: ")

        def TimeChoice():
            LabelThing = layout.sender()
            if LabelThing.isChecked():
                print("Country is %s" % (LabelThing.Time))
                data["Book"]["Time"] = LabelThing.Time
        def BookInperson():
            print(data["Book"])

            choice, = backProcess.Login(data["Login"]["Date"],bookPassword.text())
            alert = QMessageBox()
            if choice == True:
                data[data["Direction"]]["Status"] = True
                data["Direction"] = "Book"
                print(data)
                #frontProcess.Shop(layout)
                frontProcess.Book(layout)
                #Book.show()
            else:
                alert = QMessageBox()
                alert.setText("Error")
                alert.exec()

        bookButton1 = QPushButton("Order Online")
        #bookButton1.clicked.connect()
        bookButton2 = QPushButton("Book Inperson")
        bookButton2.clicked.connect(BookInperson)
        #layout.addWidget(QLabel("Login: "),0,1)
        layout.addWidget(bookLabel1,0,1)
        layout.addWidget(bookCalLoginbutton,1,1)
        layout.addWidget(bookLabel2,2,1)

        layout.addWidget(bookButton1,9,0)
        layout.addWidget(bookButton2,9,1)
        
    def Shop(layout):#[3][4][5] Browse medicines of the cargories provided.
        # Each product will be associated with a particular price and QR code.
        try:
            for x in range(0,100):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        status, medication = backProcess.GrabMedication(0)
        if status == True:
            x,y,ID = 5,0,1
            print(medication)
            for a in medication:
                if a == "Status":
                    continue
                if x / 4 >= len(medication) / 2:
                    y += 1
                    x = 5
                layout.addWidget(QLabel(medication[a]["Name"]),x-2,y)
                layout.addWidget(QLabel(f"£{medication[a]['Price']}"),x-1,y)
                layout.addWidget(QLabel(medication[a]["Quantity"]),x,y)
                medication[a]["Text"] = QLineEdit()
                layout.addWidget(medication[a]["Text"],x+1,y)
                medication[a]["Error"] = QLabel()
                layout.addWidget(medication[a]["Error"],x+2,y)
                x += 5
                ID += 1
        def confirm():
            medication["Orders"] = {}
            for a in medication:
                if a == "Orders" or a == "Status":
                    continue
                if medication[a]["Text"].text() == "":
                    continue
                elif int(medication[a]["Text"].text()) > int(medication[a]["Quantity"]):
                    medication[a]["Error"].setText("Too many items")
                    medication["Status"] = False
                    continue
                else:
                    medication["Orders"][a] = int(medication[a]["Text"].text())
                medication["Orders"][a] = {}
                medication["Orders"][a]["Quantity"] = medication[a]["Text"].text()
                medication["Status"] = True
            #backProcess.UpdateMedication(medication)
            if medication["Status"] == True:
                pass
            else:
                pass
        Status = QPushButton("Confirm")
        Status.clicked.connect(confirm)
        layout.addWidget(Status,(x*4)*ID+2,0)
    def Payment():# Scan QR code on receipt.
        pass
def main(): # Login Register
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QGridLayout()
    logLabel1 = QLabel("DOB: ")
    cal = frontProcess.calendarPopup()
    def logCalendar():
        data["Direction"] = "Login"
        qTimer.start()
        cal.show()
    LogCalLoginbutton = QPushButton("Calendar")
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

    logLabel2 = QLabel("Password: ")
    logPassword = QLineEdit()
    logPassword.setEchoMode(QLineEdit.Password)
    def logNotification():
        choice,data["User ID"] = backProcess.Login(data["Login"]["Date"],logPassword.text())
        alert = QMessageBox()
        if choice == True:
            data[data["Direction"]]["Status"] = True
            data["Direction"] = "Book"
            print(data)
            #frontProcess.Shop(layout)
            frontProcess.Book(layout,window)
            #Book.show()
        else:
            alert = QMessageBox()
            alert.setText("Error")
            alert.exec()
    logButton1 = QPushButton("Login")
    logButton1.move(50,100)
    logButton1.clicked.connect(logNotification)

    #Register:
    regLabel1 = QLabel("Name: ")
    regUsername = QLineEdit()
    regLabel2 = QLabel("DOB: ")
    def regCalendar():
        data["Direction"] = "Register"
        qTimer.start()
        cal.show()
    regCalbutton = QPushButton("Calendar")
    regCalbutton.clicked.connect(regCalendar)

    
    regLabel3 = QLabel("Email: ")
    regEmail = QLineEdit()
    regLabel4 = QLabel("Password: ")
    regPassword = QLineEdit()
    regPassword.setEchoMode(QLineEdit.Password)
    regLabel5 = QLabel("Must contain 2 capital letters\n1 number\nbetween 8 and 15 characters long.")
    def regNotification():
        choice,data["User ID"] = backProcess.Register(regUsername.text(),data["Register"]["Date"],regEmail.text(),regPassword.text())
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
            data["Direction"] = "Book"
            print(data)
            #frontProcess.Shop(layout)
            frontProcess.Book(layout,window)
        elif choice == False:
            alert.setText("Error")
        else:
            pass
        alert.exec()
    regButton1 = QPushButton("Approve")
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
    data["Direction"] = "Book"
    print(data)
    #frontProcess.Shop(layout)
    frontProcess.Book(layout,window)
    app.exec(app.exec_())
if __name__ == "__main__":
    main()
