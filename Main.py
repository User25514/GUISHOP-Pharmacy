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
    "User ID":1,
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
        "Rough_Time":[],
        "Rough_Timings":[]
    },
    "Shop":{
        "Status":False,
        "Categories":("Tablet","Liquid","Capsules"),
        "Section":"",
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
            self.setGeometry(300, 300, 350, 250)
            #if (data["Register"]["Status"] or data["Login"]["Status"]) == True:
                #self.setGeometry(300, 300, 1000, 1000)
            #else:
                #self.setGeometry(300, 300, 350, 250)
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
                    data["Book"]["Time"] = ""
                    bookCalLoginbutton.setText(data["Book"]["Date"])

                    Status, data["Book"]["Rough_Time"] = backProcess.BookRecall(data["Book"]["Date"])
                    if Status == True:
                        for x in range(0,len(data["Book"]["Rough_Timings"])):

                            try:
                                layout.itemAt(x+4).widget().deleteLater()
                            except:
                                pass
                        data["Book"]["Rough_Timings"] = data["Book"]["Rough_Time"]
                        for x in range(0,len(data["Book"]["Rough_Time"])-1):

                            LabelThing = QRadioButton("Slot " + str(x+1) + ": " + str(data["Book"]["Rough_Time"][x]))
                            LabelThing.Time = data["Book"]["Rough_Time"][x]
                            LabelThing.clicked.connect(TimeChoice)
    
                            try:
                                print(x+4," ",layout.itemAt(x+4).widget().text())
                            except:
                                pass
                            layout.addWidget(LabelThing,x+5,1)
                        bookButton2 = QPushButton("Book Inperson")
                        bookButton2.clicked.connect(BookInperson)
                        layout.addWidget(bookButton2,20,1)
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
            if (data["Book"]["Time"] and data["Book"]["Date"]) != "":
                choice = backProcess.BookRegister(data["User ID"],data["Book"]["Time"],data["Book"]["Date"])
            else:
                choice = False
            alert = QMessageBox()
            if choice == True:
                alert = QMessageBox()
                alert.setText("Booked Successfully") 
                alert.exec()
                pass
                #Book.show()
            else:
                alert = QMessageBox()
                alert.setText("Error, no date or time selected is free")
                alert.exec()
        def BookOnline():
            data[data["Direction"]]["Status"] = True
            data["Direction"] = "Shop"
            print(data)
            frontProcess.Shop(layout)
        bookButton1 = QPushButton("Order Online")
        bookButton1.clicked.connect(BookOnline)

        #layout.addWidget(QLabel("Login: "),0,1)
        layout.addWidget(bookLabel1,0,1)
        layout.addWidget(bookCalLoginbutton,1,1)
        layout.addWidget(bookLabel2,2,1)

        layout.addWidget(bookButton1,20,0)
        
        
    def Shop(layout):#[3][4][5] Browse medicines of the cargories provided.
        # Each product will be associated with a particular price and QR code.
        try:
            for x in range(0,100):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        status, medication = backProcess.GrabMedication(data["Shop"]["Categories"])
        medication["Orders"] = {}
        if status == True:
            
            print(medication)

            data["Shop"]["Section"] = data["Shop"]["Categories"][0]
            def CallMed():
                x,y,ID = 5,0,1
                for a in medication[data["Shop"]["Section"]]:
                    #print(medication[data["Shop"]["Section"]][a])
                    if x / 4 >= len(medication[data["Shop"]["Section"]]) / 2:
                        y += 1
                        x = 5
                    layout.addWidget(QLabel(medication[data["Shop"]["Section"]][a]["Name"]),x-2,y)
                    layout.addWidget(QLabel(f"£{medication[data['Shop']['Section']][a]['Price']}"),x-1,y)
                    layout.addWidget(QLabel(medication[data["Shop"]["Section"]][a]["Quantity"]),x,y)
                    medication[data["Shop"]["Section"]][a]["Text"] = QLineEdit()
                    layout.addWidget(medication[data["Shop"]["Section"]][a]["Text"],x+1,y)
                    medication[data["Shop"]["Section"]][a]["Error"] = QLabel()
                    layout.addWidget(medication[data["Shop"]["Section"]][a]["Error"],x+2,y)
                    x += 5
                    ID += 1
                return x,y,ID
            x,y,ID = CallMed()
        def confirm():
            print("confirming")
            
            for a in  medication[data["Shop"]["Section"]]:
                if a == "Orders" or a == "Status":
                    continue
                if  medication[data["Shop"]["Section"]][a]["Text"].text() == "":
                    continue
                elif int( medication[data["Shop"]["Section"]][a]["Text"].text()) > int(medication[data["Shop"]["Section"]][a]["Quantity"]):
                    medication[data["Shop"]["Section"]][a]["Error"].setText("Too many items")
                    medication["Status"] = False
                    continue
                else:
                    medication["Orders"][data["Shop"]["Section"]] = {}
                    medication["Orders"][data["Shop"]["Section"]][a] = int(medication[data["Shop"]["Section"]][a]["Text"].text())
                if medication[data["Shop"]["Section"]][a]["Text"].text() == "0":
                    del medication["Orders"][data["Shop"]["Section"]][a]
                else:
                    medication["Orders"][data["Shop"]["Section"]][a] = {}
                    medication["Orders"][data["Shop"]["Section"]][a]["Quantity"] = medication[data["Shop"]["Section"]][a]["Text"].text()
                    medication["Status"] = True
            #backProcess.UpdateMedication(medication)
            if medication["Status"] == True:
                pass
            else:
                pass
            print(medication["Orders"])
        def TimeChoice():
            LabelThing = layout.sender()
            if LabelThing.isChecked():
                print("Country is %s" % (LabelThing.Categories))
                data["Shop"]["Section"] = LabelThing.Categories
                print("Recon")
                try:
                    for x in range(0,100):
                        print(x," - ",layout.itemAt(x).widget().text())
                except:
                    pass
                print("Recon Done")
                try:
                    for x in range(0,100):
                        print(x," - ",layout.itemAt(x).widget().text())
                        if ("Slot" in layout.itemAt(x).widget().text()) or (layout.itemAt(x).widget().text() == "Confirm"):
                            print("Stop")
                            continue
                        #print(x," - ",layout.itemAt(x).widget().text())
                        print("Deleted")
                        layout.itemAt(x).widget().deleteLater()
                except:
                    pass
                CallMed()
        counter = 0
        for a in data["Shop"]["Categories"]:
            LabelThing = QRadioButton("Slot " + str(counter) + ": " + str(a))
            LabelThing.Categories = a
            LabelThing.clicked.connect(TimeChoice)
            layout.addWidget(LabelThing,(x*4)*ID+2,counter)
            counter += 1
        ConfirmButton = QPushButton("Confirm")
        ConfirmButton.clicked.connect(confirm)

        layout.addWidget(ConfirmButton,(x*4)*ID+3,0)

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
    #print(data)
    #frontProcess.Shop(layout)
    frontProcess.Book(layout,window)
    app.exec(app.exec_())
if __name__ == "__main__":
    main()
