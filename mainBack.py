import sqlite3
from mainValidation import dataValidation
import pandas as pd
import numpy as np
import qrcode
class backProcess:
    def __init__(self):
        self.REG = dataValidation.Register
        print("CHEK")
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        try:
            self.cur.execute("CREATE TABLE Register (RegID,name,dob,email,password)")
            self.cur.execute("CREATE TABLE Bookings (BookID,RegIDFK,Date,Time)")
            self.cur.execute("CREATE TABLE Tablet (TabletID,Name,Price,Quantity)")
            self.cur.execute("CREATE TABLE Liquid (LiquidID,Name,Price,Quantity)")
            self.cur.execute("CREATE TABLE Capsules (CapsulesID,Name,Price,Quantity)")
            self.cur.execute("CREATE TABLE Orders (OrderID,UserIDFK,OrderQRCode)")
            self.con.commit()
        except:
            pass
        self.con.close()
    def BookRecall(self,Date):#[1][2] Books a free date/timeslot
        print(Date)
        if (Date) == "":
            return False, False
        #[7]
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        Times = ["08:00","10:00","12:00","14:00","16:00","18:00"]
        print("Oke")
        for row in cur.execute('SELECT * FROM Bookings'):
            #print(row)
            if row[2] == Date:
                Times.remove(row[3])
        con.close()
        print("Returning")
        if len(Times) == 0:
            return False, False
        else:
            return True, Times
    def BookRegister(self,USID,BookTime,BookDate):
        print("-------------",USID,"-",BookTime,"-",BookDate)
        if ((BookTime or BookDate) == ""):
            print("Die")
            return False
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        RegID = 0
        for row in cur.execute('SELECT * FROM Bookings'):
            RegID = row[0]
        cur.execute(f"INSERT INTO Bookings VALUES ('{int(RegID)+1}','{USID}','{BookDate}','{BookTime}')")
        con.commit()
        #for row in cur.execute('SELECT * FROM Register ORDER BY RegID'):
            #print(row)

        con.close()
        return True
    def ShopState():#[2][3] Choice to shop in person or thorough the application.
        pass
    def ShoppingRecipt():#[4] A recipt will be produced with details of what has been bought with the total price.
        # The receipt will be associated with a unique qr code that the user will use at the payment stage.
        pass
    def Register(self,name,dob,email,password):#[5] Make Account
        #[6];
        if (name or dob or email or password) == "":
            return False
        print(f"{name}, {dob}, {email}, {password}")
        REG = dataValidation.Register
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        a = REG.nameVal(name)
        b = REG.dobVal(dob)
        c = REG.emailVal(email)
        d = REG.passwordVal(password)
        RegID = 0
        print(a,b,c,d)
        if (a or b or c or d) == False:
            return False
        else:
            pass
        for row in cur.execute('SELECT * FROM Register'):
            print(row)
            RegID = row[0]
            row[3]
            if row[3] == email:
                con.close()
                return False
        cur.execute(f"INSERT INTO Register VALUES ('{int(RegID)+1}','{name}','{dob}','{email}','{password}')")
        con.commit()
        #for row in cur.execute('SELECT * FROM Register ORDER BY RegID'):
            #print(row)

        con.close()
        return True, int(RegID)+1
    def Login(self,dob,password):#[5] login
        if (dob or password) == "":
            return False
        #[7]
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Register ORDER BY name'):
            #print(row)
            if row[4] == password and row[2] == dob:
                con.close()
                return True, row[0],row[1]
        con.close()
        return False
    def GrabMedication(self,Tables):
        #[8]
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        Medication = {}
        try:
            for x in Tables:
                Medication[x] = {}
                for row in cur.execute(f'SELECT * FROM {x}'):
                    #print(row)
                    Medication[x][row[0]] = {'Name':row[1],'Price':row[2],'Quantity':row[3],"QRCode":qrcode.make((x,row[0],row[1]))}
        except:
            con.close()
            return False, []
        con.close()
        return True, Medication
    def RegisterOrder(self,ID,Order,Path):
        
        if (ID or Order) == "":
            return False
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        
        img=qrcode.make(Order)
        img.save(f'{Path}/OrderCode.png') 
        OrderID = ""
        for row in cur.execute('SELECT * FROM Orders'):
            OrderID = row[0]
        if OrderID == "":
            OrderID = 1
        print(OrderID, " ",ID," "," ",Order)
        cur.execute(f"INSERT INTO Orders VALUES ('{int(OrderID)+1}','{ID}','{img}')")
        con.commit()
        #for row in cur.execute('SELECT * FROM Register ORDER BY RegID'):
            #print(row)

        con.close()
        self.report_html(Order,Path)
        return True
    def report_html(self,Order,Path):
        from datetime import datetime
        
        html = """<html><head>
<title>Pharmacy Receipt</title>
<style type="text/css">
h1, h2, h3, h4, h5, h6, p{ margin: 0;}
</style></head>
<body style="padding:0; margin:0; -webkit-text-size-adjust:none; -ms-text-size-adjust:100%; background-color:#e8e8e8; font-family: Helvetica, sans-serif; font-size:14px; line-height:24px; color:#000000;" id="body">
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse;"><tr>
<td bgcolor="#EBEBEB" style="font-size:0px">&zwnj;</td>
<td align="center" width="600" bgcolor="#FFFFFF">
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
<tr><td align="center">
<h1 style="font-weight: lighter; padding-top: 30px; padding-bottom: 20px;">Thank you for your order!</h1>
</td> </tr>
<tr><td align="center">
<h4 style="font-weight: lighter; color: #999999; padding-top: 10px; padding-bottom: 5px;" > -+todaysdate+- </h4>

</td></tr>
<tr><td align="center">
<h4 style="font-weight: lighter; color: #999999; padding-top: 10px; padding-bottom: 5px;" > -+name+- </h4>

</td></tr>
<tr><td><table id=billtable width="70%" border="0" cellspacing="0" cellpadding="0" align="center" style="border-collapse: collapse;">
<tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000;">
<td style="padding-top: 5px; padding-bottom: 5px;">Name</td>
<td style="padding-top: 5px; padding-bottom: 5px;">Quantity</td>
<td style="padding-top: 5px; padding-bottom: 5px;">Price</td>
</tr>
-+InsertLine+-
-+InsertTotal+-

</table></td></tr>
<tr><td align="center">
<img src='OrderCode.png' width="400">
</td></tr>
</table></td><td bgcolor="#EBEBEB" style="font-size:0px">&zwnj;</td>
</tr>
</table>
</body>
</html>"""
        print(Order)

        def tableInsert():
            Table = []
            TotalQ = 0
            TotalP = 0
            print("Table Insert")
            for a in Order:
                print(a)
                print(Order[a])
                if a == "User_Name" or a == "User_ID":
                    continue
                for x in Order[a]:
                    print(Order[a][x])
                    Table.append(f"""<tr style="border-top: 1px solid #999999;">
            <td style="padding-top: 5px; padding-bottom: 5px;">{Order[a][x]["Name"]}</td>
            <td style="padding-top: 5px; padding-bottom: 5px;">{Order[a][x]["Quantity"]}</td>
            <td style="padding-top: 5px; padding-bottom: 5px;">£{Order[a][x]["Price"]}</td>
        </tr>""")
                    TotalQ += int(Order[a][x]["Quantity"])
                    TotalP += float(Order[a][x]["Quantity"])*float(Order[a][x]["Price"])
            return TotalQ,TotalP, Table
        def totalInsert(TotalQ, TotalP):
            return f"""<tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000;">
        <td style="padding-top: 5px; padding-bottom: 5px;">Total</td>
        <td style="padding-top: 5px; padding-bottom: 5px;">{TotalQ}</td>
        <td style="padding-top: 5px; padding-bottom: 5px;">£{round(TotalP,2)}</td>
    </tr>"""
        TotalQ, TotalP, Table = tableInsert()
        html = html.replace('-+InsertLine+-', '\n'.join(Table))
        html = html.replace('-+InsertTotal+-', totalInsert(TotalQ, TotalP))
        now = datetime.now()
        html = html.replace("-+todaysdate+-", now.strftime("%d/%m/%Y %H:%M:%S"))
        html = html.replace("-+name+-", Order["User_Name"])
        # dd/mm/YY H:M:S
        with open(f'{Path}/report.html', 'w') as f:
            f.write(html)
        #import cv2
        #img=cv2.imread("hello.png")
        #det=cv2.QRCodeDetector()
        #val, pts, st_code=det.detectAndDecode(img)
        #print(val)
        return True
