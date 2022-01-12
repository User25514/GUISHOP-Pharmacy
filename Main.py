import sys
from datetime import datetime
import calendar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qrcode
import cv2
import mainBack
import pytest
backProcess = mainBack.backProcess()

class frontProcess:
    class calendarPopup(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Calendar')
            self.setGeometry(100, 100, 385, 300)
            self.setFixedSize(385, 300)
            self.initUI()
        def initUI(self):
            self.calendar = QCalendarWidget(self)
            self.button = QPushButton(self)
            self.button.setText("Approve")
            self.button.move(20,240)
            self.button.clicked.connect(self.Confirmation)
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
                else:self.calendar.setMaximumDate(QDate(Year, Month, Day + 15))
            else:
                self.calendar.setMinimumDate(QDate(Year-118, Month, Day))
                self.calendar.setMaximumDate(QDate(Year-18, Month, Day))
            self.calendar.setSelectedDate(QDate(Year, Month, 1))
            self.calendar.clicked.connect(self.SaveDate)
        def SaveDate(self, qDate):self.qDate = qDate            
        def Confirmation(self):
                data[data["Direction"]]["Date"] = '{0}/{1}/{2}'.format(self.qDate.month(), self.qDate.day(), self.qDate.year())
                self.close()
    class DirectoryPopup(QWidget):
        def __init__(self):
            super().__init__()
            self.OpenFolderDirectory()
        def OpenFolderDirectory(self):
            data[data["Direction"]]["Reciept Path"] = "[]"
            data[data["Direction"]]["Reciept Path"] = QFileDialog.getExistingDirectory(self,"Select The location to save or read your reciept")
            if data[data["Direction"]]["Reciept Path"] == "": data[data["Direction"]]["Reciept Path"] = "[]"
    def Book(layout,window):#[1] Confirmatin to the user that the slot was booked successfully.
        data["Direction"] = "Book"
        try:
            for x in range(0,100):layout.itemAt(x).widget().deleteLater()
        except: pass
        window.setWindowTitle('Menu')
        window.setGeometry(100, 100, 380, 400)
        window.setFixedSize(396, 448)
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
                    offset = 8
                    for x in range(0,len(data["Book"]["Rough_Timings"])):
                        try:
                            layout.itemAt(x+offset).widget().deleteLater()
                        except: pass
                    if Status == True:
                        
                        data["Book"]["Rough_Timings"] = data["Book"]["Rough_Time"]
                        for x in range(0,len(data["Book"]["Rough_Time"])-1):

                            LabelThing = QRadioButton("Slot " + str(x+1) + ": " + str(data["Book"]["Rough_Time"][x]))
                            LabelThing.Time = data["Book"]["Rough_Time"][x]
                            LabelThing.clicked.connect(TimeChoice)
                            layout.addWidget(LabelThing,x+offset,0)     
                    else: pass
            except:pass
        qTimer = QTimer()
        qTimer.setInterval(1000)
        qTimer.timeout.connect(changeName)
        bookLabel2 = QLabel("Time: ")
        def TimeChoice():
            LabelThing = layout.sender()
            if LabelThing.isChecked():data["Book"]["Time"] = LabelThing.Time
        def RegisterToDatabase(Direction):
            data["Direction"] = "Book"
            frontProcess.DirectoryPopup()
            if data["Book"]["Reciept Path"] != "[]":
                if (data["Book"]["Time"] and data["Book"]["Date"]) != "":choice,Status = backProcess.BookRegister(data["User ID"],data["User Name"],data["Book"]["Time"],data["Book"]["Date"],data["Book"]["Reciept Path"])
                else: choice,Status = False,"Failed to Book"
                alert = QMessageBox()
                if choice == True:
                    data["Booking ID"] = Status
                    alert.setText("Booked Successfully") 
                    alert.exec()
                    if Direction == True:
                        data[data["Direction"]]["Status"] = True
                        data["Direction"] = "Shop"
                        frontProcess.Shop(layout,window)
                else:
                    alert.setText(Status)
                    alert.exec()
        def ReadQR(Name):
            try:
                img=cv2.imread(f"{data[data['Direction']]['Reciept Path']}/{Name}Code.png")
                det=cv2.QRCodeDetector()
                val, pts, st_code=det.detectAndDecode(img)
                val = ((val.split(" "))[2]).split(",")
                val.append(str(data["User ID"]))
                return val
            except:
                return False
        def ExistingFile(Stat):
            data["Direction"] = "Book"
            frontProcess.DirectoryPopup()
            if data["Book"]["Reciept Path"] != "[]":
                if Stat == True: # Existing File
                    if (val := ReadQR("Order")) != False:
                        statRec, message, data["Shop"]["Order"]= backProcess.OrderRecall(val)
                        alert = QMessageBox()
                        if statRec == True:
                            data["Booking ID"] = val[1]
                            alert.setText("Order found!") 
                            alert.exec()
                            frontProcess.Shop(layout,window)
                        else:
                            alert.setText(message)
                            alert.exec()
                    else:
                        alert = QMessageBox()
                        alert.setText("QR code not found") 
                        alert.exec()
                elif Stat == False: # Existing Booking
                    if (val := ReadQR("Book")) != False:
                        statRec, message = backProcess.BookRecallData(val)
                        alert = QMessageBox()
                        if statRec == True:
                            data["Booking ID"] = val[0]
                            alert.setText("Booking found!") 
                            alert.exec()
                            frontProcess.Shop(layout,window)
                        else:
                            alert.setText(message)
                            alert.exec()
                    else:
                        alert = QMessageBox()
                        alert.setText("QR code not found") 
                        alert.exec()
                else: pass
        def Payment():# Scan QR code on receipt.
            data["Direction"] = "Payment"
            frontProcess.DirectoryPopup()
            if data["Payment"]["Reciept Path"] != "[]":
                val = ReadQR("Order")
                status,message = backProcess.PaymentRecall(val)
                alert = QMessageBox()
                if status == True:
                    alert.setText(message) 
                else:
                    alert.setText(message)
                alert.exec()
        bookButton1 = QPushButton("Pay Online")
        bookButton1.clicked.connect(Payment)
        bookButton2 = QPushButton("Order Online")
        bookButton2.clicked.connect(lambda: RegisterToDatabase(True))
        bookButton3 = QPushButton("Edit Current Order")
        bookButton3.clicked.connect(lambda: ExistingFile(True))
        bookButton4 = QPushButton("Order Inperson")
        bookButton4.clicked.connect(lambda: RegisterToDatabase(False))
        bookButton5 = QPushButton("Order online with\nExisting Booking")
        bookButton5.clicked.connect(lambda: ExistingFile(False))
        layout.addWidget(bookButton1,0,0)
        layout.addWidget(bookButton2,1,0)
        layout.addWidget(bookButton3,1,1)
        layout.addWidget(bookButton4,2,0)
        layout.addWidget(bookButton5,2,1)
        layout.addWidget(bookLabel1,4,0)
        layout.addWidget(bookCalLoginbutton,5,0)
        layout.addWidget(bookLabel2,6,0)
    def Shop(layout,window):#[3][4][5] Browse medicines of the cargories provided.
        data["Direction"] = "Shop"
        try:
            for x in range(0,100): layout.itemAt(x).widget().deleteLater()
        except: pass
        window.setWindowTitle('Shop')
        window.setGeometry(100, 100, 500, 800)
        window.setFixedSize(500, 800)
        status, medication = backProcess.GrabMedication(data["Shop"]["Categories"])
        medication["Orders"] = {}
        if status == True:
            data["Shop"]["Section"] = data["Shop"]["Categories"][0]
            medication["Orders"] = data["Shop"]["Order"]
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
                    try: medication[data["Shop"]["Section"]][a]["Text"] = QLineEdit(str(medication["Orders"][data["Shop"]["Section"]][a]["Quantity"]))
                    except:
                        try: medication[data["Shop"]["Section"]][a]["Text"] = QLineEdit(str(data["Shop"]["Order"][data["Shop"]["Section"]][a]["Quantity"]))
                        except: medication[data["Shop"]["Section"]][a]["Text"] = QLineEdit()
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
                if a == "Orders" or a == "Status": continue
                if  medication[data["Shop"]["Section"]][a]["Text"].text() == "": 
                    try:medication["Orders"][data["Shop"]["Section"]].pop(a)
                    except: pass
                elif int( medication[data["Shop"]["Section"]][a]["Text"].text()) > int(medication[data["Shop"]["Section"]][a]["Quantity"]):
                    medication[data["Shop"]["Section"]][a]["Error"].setText("Too many items")
                    medication["Status"] = False
                    break
                else:
                    b = {"Name": medication[data["Shop"]["Section"]][a]["Name"],
                        "Price": float(medication[data["Shop"]["Section"]][a]["Price"]),
                        "Quantity": int(medication[data["Shop"]["Section"]][a]["Text"].text())}
                    if not(data["Shop"]["Section"] in medication["Orders"]): medication["Orders"][data["Shop"]["Section"]] = {}
                    medication["Orders"][data["Shop"]["Section"]][a] = b
                    try:
                        if int(medication[data["Shop"]["Section"]][a]["Text"].text()) > 0: medication["Status"] = True
                        else: raise Exception
                    except Exception:medication["Orders"][data["Shop"]["Section"]].pop(a)
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
                            layout.itemAt(x).widget().deleteLater()
                    except: pass
                    CallMed()
        def confirm():
            data["Direction"] = "Shop"
            frontProcess.DirectoryPopup()
            if data["Shop"]["Reciept Path"] != "[]":
                CrossWindow()
                if medication["Status"] != False:
                    if len(medication["Orders"]) > 0 and data["Shop"]["Reciept Path"] != "[]":
                        choice = backProcess.RegisterOrder(data["Booking ID"],data["User Name"],medication["Orders"],data["Shop"]["Reciept Path"])
                    else: choice = False
                    alert = QMessageBox()
                    if choice == True:
                        alert.setText("Reciept made Successfully") 
                        alert.exec()
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
        BackButton = QPushButton("Go Back")
        BackButton.clicked.connect(lambda: frontProcess.Book(layout,window))
        layout.addWidget(BackButton,(x*4)*ID+3,2)
def main(): # Login Register
    data["Direction"] = "Register"
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 300, 400)
    window.setFixedSize(300, 400)
    layout = QGridLayout(window)
    window.setWindowTitle('Login')
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
            if data["Login"]["Date"] != "":LogCalLoginbutton.setText(data["Login"]["Date"])
            if data["Register"]["Date"] != "": regCalbutton.setText(data["Register"]["Date"])
        except: pass
    qTimer = QTimer()
    qTimer.setInterval(1000)
    qTimer.timeout.connect(changeName)
    logLabel2 = QLabel("Password: ")
    logPassword = QLineEdit()
    logPassword.setEchoMode(QLineEdit.Password)
    def logNotification():
        data["Direction"] = "Login"
        try:
            choice,data["User ID"],data["User Name"] = backProcess.Login(data["Login"]["Date"],logPassword.text())
            alert = QMessageBox()
            if choice == True:
                data[data["Direction"]]["Status"] = True
                data["Direction"] = "Book"
                alert.setText("Logged in")
                alert.exec()
                frontProcess.Book(layout,window)
            else:
                alert.setText(data["User ID"])
                data["User ID"] = ""
                alert.exec()
        except: pass
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
        data["Direction"] = "Register"
        choice,data["User ID"] = backProcess.Register(regUsername.text(),data["Register"]["Date"],regEmail.text(),regPassword.text())
        alert = QMessageBox()
        if choice == True:
            data["User Name"] = regUsername.text()
            alert.setText("Registered")
            data["Register"] = {
                "Status":True,
                "Name":"",
                "Date":"Calendar",
                "Password":""}
            data["Direction"] = "Book"
            frontProcess.Book(layout,window)
        elif choice == False:
            alert.setText(data["User ID"] )
            data["User ID"] = ""
        else: pass
        alert.exec()
    regButton1 = QPushButton("Register")
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
        for b in range(1,5): layout.addWidget(QLabel("|"),a,1,b,1)
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
    window.setLayout(layout)
    window.show()
    try:
        app.exec(app.exec_())
    except:pass
class runeverything(object):
    def call_everything(self):
        for name in dir(self):
            obj = getattr(self, name)
            if callable(obj) and name != 'call_everything' and name[:2] != '__': obj()
class Testing():
    def __init__(self):
        self.Curl()
    class BackEndTest(runeverything):
        class BookRecallTest(runeverything):
            def TrueDataVal(self):
                now = datetime.now()
                assert backProcess.BookRecall(now.strftime("%d/%m/%Y"))[0] == True
            @pytest.mark.xfail
            def FalseDataVal(self):
                assert backProcess.BookRecall("") == (False,False)
                assert backProcess.BookRecall("19/8/2000") == (False,False)
                assert NewDat["BookingTest"]["Time"] not in backProcess.BookRecall(NewDat["BookingTest"]["Date"])[1]  
        class BookRecallDataTest(runeverything):
            def TrueDataVal(self):
                assert backProcess.BookRecallData((NewDat["BookingTest"]["Booking ID"],"","",NewDat["BookingTest"]["User ID"]))[0] == True
            @pytest.mark.xfail
            def FalseDataVal(self):
                assert backProcess.BookRecallData((NewDat["BookingTest"]["Booking ID"],"","","0")) == (False,"Error with Booking")
                assert backProcess.BookRecallData(("0","","","0")) == (False,"No Booking was found")
        class OrderRecallTest(runeverything):
            def TrueDataVal(self):
                assert backProcess.OrderRecall((NewDat["OrderTest"]["Order ID"],NewDat["OrderTest"]["Booking ID"]))[0] == True
            @pytest.mark.xfail
            def FalseDataVal(self):
                assert backProcess.OrderRecall((NewDat["OrderTest"]["Order ID"],"0")) == (False,"Error with Order",False)
                assert backProcess.OrderRecall(("0","0")) == (False,"No Order was found",False)
        class RegisterTest(runeverything):
            @pytest.mark.xfail
            def FalseDataVal(self):
                assert backProcess.Register("","","","") == (False,"Input Empty")
                assert backProcess.Register(NewDat["RegisterTest"]["Name"],NewDat["RegisterTest"]["DOB"],NewDat["RegisterTest"]["Email"],"TestPass") == (False,"Invalid Password")
                assert backProcess.Register(NewDat["RegisterTest"]["Name"],NewDat["RegisterTest"]["DOB"],NewDat["RegisterTest"]["Email"],NewDat["RegisterTest"]["Password"]) == (False,"Email already in use")
                assert backProcess.Register("David12",NewDat["RegisterTest"]["DOB"],NewDat["RegisterTest"]["Email"],NewDat["RegisterTest"]["Password"]) == (False,"Invalid Name")
        class LoginTest(runeverything):
            def TrueDataVal(self):
                assert backProcess.Login(NewDat["RegisterTest"]["DOB"],NewDat["RegisterTest"]["Password"])[0] == True
            @pytest.mark.xfail
            def FalseDataVal(self):
                assert backProcess.Login("1/7/1900","TestPass") == (False,"No account found","")
        class GrabMedicationTest(runeverything):
            def TrueDataVal(self):
                assert backProcess.GrabMedication(["Tablet"])[0] == True
            @pytest.mark.xfail
            def FalseDataVal(self):
                assert backProcess.GrabMedication(["Something Non Existent"]) == (False,[])
        def Curl(self):
            BookRecall = self.BookRecallTest()
            BookRecall.call_everything()
            print("BookRecall Test: Pass")
            BookRecallData = self.BookRecallDataTest()
            BookRecallData.call_everything()
            print("BookRecalData Test: Pass")
            OrderRecall = self.OrderRecallTest()
            OrderRecall.call_everything()
            print("OrderRecall Test: Pass")
            Register = self.RegisterTest()
            Register.call_everything()
            print("Register Test: Pass")
            Login = self.LoginTest()
            Login.call_everything()
            print("Login Test: Pass")
            GrabMedication = self.GrabMedicationTest()
            GrabMedication.call_everything()
            print("GrabMedication Test: Pass")
            pass
    def Curl(self):
        BET = self.BackEndTest()
        BET.call_everything()
        pass




if __name__ == "__main__":
    state = "Main"
    if state == "Main":
        data = {"User ID":"",
            "User Name":"",
            "Booking ID":"",
            "Direction":"",
            "Register":{"Status":False,
                "Name":"",
                "Date":"",
                "Password":""},
            "Login":{"Status":False,
                "Date":""},
            "Book":{"Status":False,
                "Date":"",
                "Time":"",
                "Rough_Time":[],
                "Rough_Timings":[],
                "Reciept Path":"[]"},
            "Shop":{"Status":False,
                "Categories":("Tablet","Liquid","Capsules"),
                "Section":"",
                "Name":"",
                "Date":"",
                "Reciept Path":"[]",
                "Order":{},},
            "Payment":{"Status":False,
                "Reciept Path":"[]"}}
        main()
    elif state == "Test":
        import sqlite3
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        NewDat ={
            "BookingTest":{
                "User ID":"",
                "Booking ID":"",
                "Date":"",
                "Time":"",
            },
            "RegisterTest":{
                "User ID":"",
                "Name":"",
                "DOB":"",
                "Email":"",
                "Password":"",
            },
            "OrderTest":{
                "Order ID":"",
                "Booking ID":"",}
        }
        for row in cur.execute('SELECT * FROM Bookings'): break
        NewDat["BookingTest"]["Booking ID"] = row[0]
        NewDat["BookingTest"]["User ID"] = row[1]
        NewDat["BookingTest"]["Date"] = row[2]
        NewDat["BookingTest"]["Time"] = row[3]
        for row in cur.execute('SELECT * FROM Register'): break
        NewDat["RegisterTest"]["User ID"] = row[0]
        NewDat["RegisterTest"]["Name"] = row[1]
        NewDat["RegisterTest"]["DOB"] = row[2]
        NewDat["RegisterTest"]["Email"] = row[3]
        NewDat["RegisterTest"]["Password"] = row[4]
        for row in cur.execute('SELECT * FROM Orders'): break
        NewDat["OrderTest"]["Order ID"] = row[0]
        NewDat["OrderTest"]["Booking ID"] = row[1]
        con.close()
        Test = Testing()
    pass
