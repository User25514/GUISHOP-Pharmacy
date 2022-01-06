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
            self.cur.execute("CREATE TABLE Orders (OrderID,BookingIDFK,Order,OrderQRCode)")
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
            return False, False
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        RegID = 0
        for row in cur.execute('SELECT * FROM Bookings'):
            RegID = row[0]
        cur.execute(f"INSERT INTO Bookings VALUES ('{int(RegID)+1}','{USID}','{BookDate}','{BookTime}')")
        con.commit()

        con.close()
        return True,int(RegID)+1
    def PaymentRecall(self,IDs):
        #[9]
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Orders'):
            print("Orders: ",row)
            if row[0] == IDs[0] and row[1] == IDs[1]:
                for Bookingrow in cur.execute('SELECT * FROM Bookings'):
                    print("Booking: ",Bookingrow)
                    if Bookingrow[0] == IDs[1] and Bookingrow[1] == IDs[2]:
                        con.close()
                        backProcess.EditOrders(RegID)
                        return True, "Successful"
                con.close()
                return False, "Error with Booking"
        con.close()
        return False, "No Order was found"
    def EditOrders(self,RegID):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute(f"INSERT INTO Orders VALUES ('{int(OrderID)}','{ID}','{str(New)}','{img}')")
        con.commit()
        con.close()
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


    def RegisterOrder(self,ID,Name,Order,Path):
        print(f"Register: {ID}, {Order}, {Path}")
        if (ID or Order) == "":
            return False
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        OrderID = ""
        for row in cur.execute('SELECT * FROM Orders'):
            print(row)
            OrderID = int(row[0])+1
        if OrderID == "":
            OrderID = 1
        #Order["Order_ID"] = int(OrderID)+1
        img=qrcode.make(f"Pharmacy Order: {int(OrderID)},{int(ID)}")
        img.save(f'{Path}/OrderCode.png') 
        New = str(Order).replace("'",'"')        
        cur.execute(f"INSERT INTO Orders VALUES ('{int(OrderID)}','{ID}','{str(New)}','{img}')")
        con.commit()
        con.close()
        
        backProcess.report_html(0,"Order",Order,Path,Name)
        return True
    def report_html(self,Stat,Order,Path,Name):
        from datetime import datetime
        
        html = """<html><head>
<title><!--+Windowtitle+--></title>
<style type="text/css">
h1, h2, h3, h4, h5, h6, p{ margin: 0;}
</style></head>
<body style="padding:0; margin:0; -webkit-text-size-adjust:none; -ms-text-size-adjust:100%; background-color:#e8e8e8; font-family: Helvetica, sans-serif; font-size:14px; line-height:24px; color:#000000;" id="body">
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse;"><tr>
<td bgcolor="#EBEBEB" style="font-size:0px">&zwnj;</td>
<td align="center" width="600" bgcolor="#FFFFFF">
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
<tr><td align="center">
<h1 style="font-weight: lighter; padding-top: 30px; padding-bottom: 20px;"><!--+title+--></h1>
</td> </tr>
<tr><td align="center">
<h4 style="font-weight: lighter; color: #999999; padding-top: 10px; padding-bottom: 5px;" > <!--+todaysdate+--> </h4>

</td></tr>
<tr><td align="center">
<h4 style="font-weight: lighter; color: #999999; padding-top: 10px; padding-bottom: 5px;" > <!--+name+--> </h4>

</td></tr>
<tr><td><table id=billtable width="70%" border="0" cellspacing="0" cellpadding="0" align="center" style="border-collapse: collapse;">
<tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000;">
<!--+InsertHeadings+-->
</tr>

<!--+InsertLine+-->
<!--+InsertTotal+-->

</table></td></tr>
<tr><td align="center">
<!--+ImageQR+-->
</td></tr>
</table></td><td bgcolor="#EBEBEB" style="font-size:0px">&zwnj;</td>
</tr>
</table>
</body>
</html>"""
        def headingInsert():
            Headings = []
            print("Start")
            for a in Order:
                for b in Order[a]:
                    for c in Order[a][b]:
                        print(f"-{a} -{b} -{c}")
                        Headings.append(f'<td style="padding-top: 5px; padding-bottom: 5px;">{c}</td>')
                    break
                break
            print(Headings)
            return '\n'.join(Headings)
        def tableInsert():
            Table,TotalQ,TotalP = [],0,0

            for a in Order:
                if a == "User_Name" or a == "User_ID" or a == "Order_ID":
                    continue
                for b in Order[a]:
                    Table.append('<tr style="border-top: 1px solid #999999;">')
                    for c in Order[a][b]:
                        Table.append(f'<td style="padding-top: 5px; padding-bottom: 5px;">{Order[a][b][c]}</td>')
                    Table.append('</tr>')
                    TotalQ += int(Order[a][b]["Quantity"])
                    TotalP += float(Order[a][b]["Quantity"])*float(Order[a][b]["Price"])
            return TotalQ,TotalP, Table
        def totalInsert(TotalQ, TotalP):
            return f"""<tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000;">
            <td style="padding-top: 5px; padding-bottom: 5px;">Total</td>
            <td style="padding-top: 5px; padding-bottom: 5px;">£{round(TotalP,2)}</td>
            <td style="padding-top: 5px; padding-bottom: 5px;">{TotalQ}</td>\n</tr>"""
        now = datetime.now()
        html = html.replace("<!--+todaysdate+-->", now.strftime("%d/%m/%Y %H:%M:%S"))
        html = html.replace("<!--+name+-->", Name)
        
        if Stat == "Order":
            html = html.replace("<!--+Windowtitle+-->","Pharmacy Order")
            html = html.replace("<!--+title+-->","Pharmacy receipt:")
            html = html.replace("<!--+ImageQR+-->",'<img src="OrderCode.png" width="400">')
            TotalQ, TotalP, Table = tableInsert()
            Headings = headingInsert()
            html = html.replace('<!--+InsertHeadings+-->', Headings)
            html = html.replace('<!--+InsertLine+-->', '\n'.join(Table))
            html = html.replace('<!--+InsertTotal+-->', totalInsert(TotalQ, TotalP))
        elif Stat == "IDK":
            html = html.replace("<!--+title+-->","Pharmacy Order")

        
        # dd/mm/YY H:M:S
        with open(f'{Path}/report.html', 'w') as f:
            f.write(html)
        
  
#Order = {'Tablet': {'1': {'Name': 'Benylin', 'Price': 4.15, 'Quantity': 1}, '2': {'Name': 'Buscopan', 'Price': 3.5, 'Quantity': 2}, '3': {'Name': 'Nytol Herbal', 'Price': 5.99, 'Quantity': 3}, '4': {'Name': 'Dulcolax Adult', 'Price': 2.99, 'Quantity': 4}, '5': 
#{'Name': 'Gaviscon', 'Price': 8.49, 'Quantity': 5}, '6': {'Name': 'Panadol Paracetamol', 'Price': 2.6, 'Quantity': 6}, '7': {'Name': 'Nurofren', 'Price': 1.89, 'Quantity': 7}, 
#'8': {'Name': 'Beechams', 'Price': 2.99, 'Quantity': 8}, '9': {'Name': 'Nexium', 'Price': 6.0, 'Quantity': 9}}, 'Liquid': {'1': {'Name': 'Beecharms Cold and Flu', 'Price': 3.99, 'Quantity': 10}, '2': {'Name': 'Nurofren', 'Price': 2.99, 'Quantity': 11}, '3': {'Name': 'Nytol', 'Price': 6.0, 'Quantity': 12}, '4': {'Name': 'Gaviscon Heatburn', 'Price': 11.0, 'Quantity': 13}, '5': {'Name': 'Vovania Chesty', 'Price': 4.2, 'Quantity': 14}, '6': {'Name': 'Dulcosoft Liquid', 'Price': 8.99, 'Quantity': 15}, '7': {'Name': 'Calcough', 'Price': 4.0, 'Quantity': 16}, '8': {'Name': 'Benylin', 'Price': 8.0, 'Quantity': 17}, 
#'9': {'Name': 'Covania', 'Price': 7.5, 'Quantity': 18}}, 'Capsules': {'1': {'Name': 'Lemsip Max Day3.50', 'Price': 3.5, 'Quantity': 19}, '2': {'Name': 'Buscopan', 'Price': 6.0, 'Quantity': 20}, '3': {'Name': 'Sudafed', 'Price': 4.49, 'Quantity': 21}, '4': {'Name': 'Lemsip Cough Max', 'Price': 4.99, 'Quantity': 22}, '5': {'Name': 'Benylin Cold and Flu', 'Price': 5.0, 'Quantity': 23}, '6': {'Name': 'Galphram', 'Price': 1.29, 'Quantity': 24}, '7': {'Name': 'Colpermin', 'Price': 6.19, 'Quantity': 25}, '8': {'Name': 'Flarin ', 
#'Price': 5.29, 'Quantity': 26}, '9': {'Name': 'DuloEase', 'Price': 3.5, 'Quantity': 27}}, 'User_ID': '1', 'User_Name': 'Yan'}
#backProcess.report_html(0,"Order",Order,"C:/Users/robso/Desktop")
#backProcess.RegisterOrder(0,str(1), {'Tablet': {'4': {'Name': 'Dulcolax Adult', 'Price': 2.99, 'Quantity': 12}, '5': {'Name': 'Gaviscon', 'Price': 8.49, 'Quantity': 8}, '6': {'Name': 'Panadol Paracetamol', 'Price': 2.6, 'Quantity': 3}},"User_Name":"Yan"}, "C:/Users/robso/Desktop")