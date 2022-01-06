import time
import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qrcode
import cv2
import mainBack
import ast

backProcess = mainBack.backProcess()
data = {
    "User ID":"",
    "User Name":"",
    "Booking ID":"",
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
        "Rough_Timings":[],
        "Recipt Path":"[]",
    },
    "Shop":{
        "Status":False,
        "Categories":("Tablet","Liquid","Capsules"),
        "Section":"",
        "Name":"",
        "Date":"",
        "Recipt Path":"[]",
    },
    "Payment":{
        "Status":False,
        "Recipt Path":"[]",
    }
}
class frontProcess:
    class calendarPopup(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Calendar')
            self.setGeometry(300, 300, 385, 280)

            self.initUI()
        def initUI(self):
            self.calendar = QCalendarWidget(self)
            self.button = QPushButton(self)
            self.button.setText("Approve")
            self.button.move(20,240)
            self.button.clicked.connect(self.notification)
            self.calendar.move(0, 0)
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
                self.calendar.setMinimumDate(QDate(Year-118, Month, Day))
                self.calendar.setMaximumDate(QDate(Year-18, Month, Day))
            self.calendar.setSelectedDate(QDate(Year, Month, 1))
            self.calendar.clicked.connect(self.printDateInfo)

        def printDateInfo(self, qDate):
            self.qDate = qDate            
        def notification(self):
                data[data["Direction"]]["Date"] = '{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year())
                self.close()
    class DirectoryPopup(QWidget):

        def __init__(self):
            super().__init__()
            self.openFileNameDialog()
        def openFileNameDialog(self):
            data[data["Direction"]]["Recipt Path"] = QFileDialog.getExistingDirectory(self,"Select Where you would like the Reciept to save")

    
    def Book(layout,window):#[1] Confirmatin to the user that the slot was booked successfully.
        data["Direction"] = "Book"
        try:
            for x in range(0,100):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        window.setGeometry(100, 100, 380, 300)
        window.setFixedSize(380, 300)
        bookLabel1 = QLabel("Date: ")
        bookCal = frontProcess.calendarPopup()
        def bookCalendar():
            data["Direction"] = "Book"
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
                        offset = 8
                        for x in range(0,len(data["Book"]["Rough_Timings"])):

                            try:
                                print(x+offset," ",layout.itemAt(x+offset).widget().text())
                                layout.itemAt(x+offset).widget().deleteLater()
                            except:
                                pass
                        data["Book"]["Rough_Timings"] = data["Book"]["Rough_Time"]
                        for x in range(0,len(data["Book"]["Rough_Time"])-1):

                            LabelThing = QRadioButton("Slot " + str(x+1) + ": " + str(data["Book"]["Rough_Time"][x]))
                            LabelThing.Time = data["Book"]["Rough_Time"][x]
                            LabelThing.clicked.connect(TimeChoice)
                            layout.addWidget(LabelThing,x+offset,0)
                        
            except:
                pass

        qTimer = QTimer()
        qTimer.setInterval(1000)
        qTimer.timeout.connect(changeName)

        bookLabel2 = QLabel("Time: ")

        def TimeChoice():
            LabelThing = layout.sender()
            if LabelThing.isChecked():
                data["Book"]["Time"] = LabelThing.Time
        def RegisterToDatabase(Direction):

            print("imagine")
            if (data["Book"]["Time"] and data["Book"]["Date"]) != "":
                choice,data["Booking ID"] = backProcess.BookRegister(data["User ID"],data["Book"]["Time"],data["Book"]["Date"])
            else:
                choice = False
            alert = QMessageBox()
            if choice == True:
                alert = QMessageBox()
                alert.setText("Booked Successfully") 
                alert.exec()
                if Direction == True:
                    data[data["Direction"]]["Status"] = True
                    data["Direction"] = "Shop"
                    frontProcess.Shop(layout,window)
                pass
                #Book.show()
            else:
                alert = QMessageBox()
                alert.setText("Error, no date or time selected is free")
                alert.exec()
        def ExistingFile(Stat):
            
            frontProcess.DirectoryPopup()
            print(data["Book"]["Recipt Path"])
            if data["Book"]["Recipt Path"] != "[]":
                if Stat == True: # Existing File
                    pass
                elif Stat == False: # Existing Booking
                    pass
                else:
                    pass
        def BookingReceipt():
            #choice = backProcess.RegisterOrder(data["User ID"],medication["Orders"],data["Shop"]["Recipt Path"])
            pass
        bookButton1 = QPushButton("Pay Online")
        bookButton1.clicked.connect(frontProcess.Payment)
        bookButton2 = QPushButton("Order Online")
        bookButton2.clicked.connect(lambda: RegisterToDatabase(True))
       
        bookButton3 = QPushButton("Edit Current Order")
        bookButton3.clicked.connect(lambda: ExistingFile(True))
        bookButton4 = QPushButton("Order Inperson")
        bookButton4.clicked.connect(lambda: RegisterToDatabase(False))
        bookButton5 = QPushButton("Order online with Existing Booking")
        bookButton5.clicked.connect(lambda: ExistingFile(False))
        layout.addWidget(bookButton1,0,0)
        layout.addWidget(bookButton2,1,0)
        layout.addWidget(bookButton3,1,1)
        layout.addWidget(bookButton4,2,0)
        bookButton5.setWordWrap(True)
        layout.addWidget(bookButton5,2,1)
        layout.addWidget(bookLabel1,4,0)
        layout.addWidget(bookCalLoginbutton,5,0)
        layout.addWidget(bookLabel2,6,0)

        
        
    def Shop(layout,window):#[3][4][5] Browse medicines of the cargories provided.
        # Each product will be associated with a particular price and QR code.
        data["Direction"] = "Shop"
        try:
            for x in range(0,100):
                layout.itemAt(x).widget().deleteLater()
        except:
            pass
        window.setGeometry(100, 100, 500, 800)
        window.setFixedSize(500, 800)
        status, medication = backProcess.GrabMedication(data["Shop"]["Categories"])
        medication["Orders"] = {}
        if status == True:
            data["Shop"]["Section"] = data["Shop"]["Categories"][0]
            def CallMed():
                x,y,ID = 6,0,1
                for a in medication[data["Shop"]["Section"]]:
                    if x / 5 >= len(medication[data["Shop"]["Section"]]) / 2:
                        y += 1
                        x = 6
                    img=qrcode.make(medication[data["Shop"]["Section"]][a])
                    img.save(f'cache.png') 
                    label = QLabel()
                    pixmap = QPixmap('cache.png')
                    pixmap = pixmap.scaled(100, 100)
                    label.setPixmap(pixmap)
                    layout.addWidget(label,x-3,y)
                    layout.addWidget(QLabel(medication[data["Shop"]["Section"]][a]["Name"]),x-2,y)
                    layout.addWidget(QLabel(f"£{medication[data['Shop']['Section']][a]['Price']}"),x-1,y)
                    layout.addWidget(QLabel(f'Quantity: {medication[data["Shop"]["Section"]][a]["Quantity"]}'),x,y)
                    try:
                         medication[data["Shop"]["Section"]][a]["Text"] = QLineEdit(str(medication["Orders"][data["Shop"]["Section"]][a]["Quantity"]))
                    except:
                        medication[data["Shop"]["Section"]][a]["Text"] = QLineEdit()
                    layout.addWidget(medication[data["Shop"]["Section"]][a]["Text"],x+1,y)
                    medication[data["Shop"]["Section"]][a]["Error"] = QLabel()
                    layout.addWidget(medication[data["Shop"]["Section"]][a]["Error"],x+2,y)
                    x += 6
                    ID += 1
                return x,ID
            x,ID = CallMed()
        def CrossWindow():
            medication["Status"] = True
            for a in  medication[data["Shop"]["Section"]]:
                if a == "Orders" or a == "Status":
                    continue
                if  medication[data["Shop"]["Section"]][a]["Text"].text() == "":
                    continue
                elif int( medication[data["Shop"]["Section"]][a]["Text"].text()) > int(medication[data["Shop"]["Section"]][a]["Quantity"]):
                    medication[data["Shop"]["Section"]][a]["Error"].setText("Too many items")
                    medication["Status"] = False
                    break
                else:
                    b = {
                        "Name": medication[data["Shop"]["Section"]][a]["Name"],
                        "Price": float(medication[data["Shop"]["Section"]][a]["Price"]),
                        "Quantity": int(medication[data["Shop"]["Section"]][a]["Text"].text())
                    }
                    if not(data["Shop"]["Section"] in medication["Orders"]):
                        medication["Orders"][data["Shop"]["Section"]] = {}
                    medication["Orders"][data["Shop"]["Section"]][a] = b
                    if medication[data["Shop"]["Section"]][a]["Text"].text() == "0":
                        del medication["Orders"][data["Shop"]["Section"]][a]
                    else:
                        medication["Status"] = True
            
        def TimeChoice():
            LabelThing = layout.sender()
            if LabelThing.isChecked():
                CrossWindow()
                if medication["Status"] != False:
                    data["Shop"]["Section"] = LabelThing.Categories
                    try:
                        for x in range(0,100):
                            if ("Slot" in layout.itemAt(x).widget().text()) or (layout.itemAt(x).widget().text() == "Confirm") or (layout.itemAt(x).widget().text() == "[]" or (layout.itemAt(x).widget().text() == "Directory")or (layout.itemAt(x).widget().text() == "Go Back")):
                                continue
                            #print(x," - ",layout.itemAt(x).widget().text())
                            layout.itemAt(x).widget().deleteLater()
                    except:
                        pass
                    CallMed()
        def confirm():
            CrossWindow()
            if medication["Status"] != False:
                if len(medication["Orders"]) > 0 and data["Shop"]["Recipt Path"] != "[]":
                    #medication["Orders"]["User_Name"] = data["User Name"]
                    #choice = backProcess.report_html(medication["Orders"])
                    choice = backProcess.RegisterOrder(data["Booking ID"],data["User Name"],medication["Orders"],data["Shop"]["Recipt Path"])
                else:
                    choice = False
                
                alert = QMessageBox()
                if choice == True:
                    alert.setText("Recipt made Successfully") 
                    alert.exec()
                    pass
                    #Book.show()
                else:
                    alert.setText("Error, no date or time selected is free")
                    alert.exec()
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
        def GrabDirectory():
            DirectoryTimer.start()
            frontProcess.DirectoryPopup()
        DirectoryButton = QPushButton("Directory")
        DirectoryButton.clicked.connect(GrabDirectory)
        def GoBack():
            frontProcess.Book(layout,window)
        BackButton = QPushButton("Go Back")
        BackButton.clicked.connect(GoBack)
        layout.addWidget(BackButton,(x*4)*ID+3,2)
        layout.addWidget(DirectoryButton,(x*4)*ID+3,1)
        DirectoryDirection = QLabel("[]")
        layout.addWidget(DirectoryDirection,(x*4)*ID+4,0,1,3)
        def ChangeDirectoryName():
            if DirectoryDirection.text() != data["Shop"]["Recipt Path"]:
                DirectoryDirection.setText(data["Shop"]["Recipt Path"])
        DirectoryTimer = QTimer()
        DirectoryTimer.setInterval(1000)
        DirectoryTimer.timeout.connect(ChangeDirectoryName)
        
    def Payment():# Scan QR code on receipt.
        data["Direction"] = "Payment"
        frontProcess.DirectoryPopup()
        print(f"{data[data['Direction']]['Recipt Path']}/OrderCode.png")
        def ReadQR():
            img=cv2.imread(f"{data[data['Direction']]['Recipt Path']}/OrderCode.png")
            det=cv2.QRCodeDetector()
            val, pts, st_code=det.detectAndDecode(img)
            print(val)
            val = (val.replace("Pharmacy Order: ","")).split(",")
            val.append(data["User ID"])
            print(val)
            status,message = backProcess.PaymentRecall(val)
            alert = QMessageBox()
            if status == True:
                alert.setText(message) 
                alert.exec()
                pass
            else:
                alert.setText(message)
                alert.exec()
        print("Start")
        ReadQR()

        pass
def main(): # Login Register
    data["Direction"] = "Register"
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 300, 400)
    window.setFixedSize(300, 400)
    layout = QGridLayout(window)
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
        try:
            choice,data["User ID"],data["User Name"] = backProcess.Login(data["Login"]["Date"],logPassword.text())
            alert = QMessageBox()
            if choice == True:
                data[data["Direction"]]["Status"] = True
                data["Direction"] = "Book"
                frontProcess.Book(layout,window)
            else:
                alert = QMessageBox()
                alert.setText("Error")
                alert.exec()
        except:
            pass
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
    regLabel5 = QLabel("Must contain 2 capital letters, 1 number,between 8 and 15 characters long.")
    def regNotification():
        choice,data["User ID"] = backProcess.Register(regUsername.text(),data["Register"]["Date"],regEmail.text(),regPassword.text())
        data["User Name"] = regUsername.text()
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
            frontProcess.Book(layout,window)
        elif choice == False:
            alert.setText("Error")
        else:
            pass
        alert.exec()
    regButton1 = QPushButton("Approve")
    regButton1.clicked.connect(regNotification)
    #Login Stuff
    layout.addWidget(QLabel("Login: "),1,0)
    layout.addWidget(logLabel1,2,0)
    layout.addWidget(LogCalLoginbutton,3,0)
    layout.addWidget(logLabel2,4,0)
    layout.addWidget(logPassword,5,0,1,1)
    layout.addWidget(logButton1,6,0)
    #Register Stuff
    for a in range(0,14):
        for b in range(1,5):
            layout.addWidget(QLabel("|"),a,1,b,1)
    layout.addWidget(QLabel("Register: "),0,2,1,1)
    layout.addWidget(regLabel1,1,2,1,1)
    layout.addWidget(regUsername,2,2,1,1)
    layout.addWidget(regLabel2,3,2,1,1)
    layout.addWidget(regCalbutton,4,2,1,1)
    layout.addWidget(regLabel3,5,2,1,1)
    layout.addWidget(regEmail,6,2,1,1)
    layout.addWidget(regLabel4,7,2,1,1)
    layout.addWidget(regPassword,8,2,1,1)
    regLabel5.setWordWrap(True)
    layout.addWidget(regLabel5,9,2,3,1)
    layout.addWidget(regButton1,12,2,1,1)
    #
    window.setLayout(layout)
    window.show()
    #data["Direction"] = "Shop"
    #frontProcess.Shop(layout,window)
    #frontProcess.Book(layout,window)
    app.exec(app.exec_())
if __name__ == "__main__":
    main()
    pass
