import sqlite3
from mainValidation import dataValidation
import qrcode
import ast
from datetime import datetime
class backProcess:
    def __init__(self):
        self.REG = dataValidation.Register
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        SQLList = ["CREATE TABLE Register (RegID,name,dob,email,password)",
            "CREATE TABLE Bookings (BookID,RegIDFK,Date,Time,BookQRCode)",
            "CREATE TABLE Tablet (TabletID,Name,Price,Quantity)",
            "CREATE TABLE Liquid (LiquidID,Name,Price,Quantity)",
            "CREATE TABLE Capsules (CapsulesID,Name,Price,Quantity)",
            "CREATE TABLE Orders (OrderID,BookingIDFK,Order,OrderQRCode)",
            "CREATE TABLE Payments (PaymentID,OrderIDFK,Date,Time)"]
        for i in SQLList:
            try:
                self.cur.execute(i)
                self.con.commit()
            except: pass
        self.con.close()
    def BookRecall(self,Date):
        now = datetime.now()
        if Date == "": return False, False
        elif int((Date.split("/"))[2]) < int(now.strftime("%Y")): return False, False
        elif int((Date.split("/"))[2]) == int(now.strftime("%Y")):
            if int((Date.split("/"))[1]) < int(now.strftime("%m")): return False, False
            elif int((Date.split("/"))[1]) == int(now.strftime("%m")):
                if int((Date.split("/"))[0]) < int(now.strftime("%d")): return False, False
                else: pass
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        Times = ["08:00","10:00","12:00","14:00","16:00","18:00"]
        for row in cur.execute('SELECT * FROM Bookings'):
            if row[2] == Date: Times.remove(row[3])
        con.close()
        if len(Times) == 0: return False, Times
        else: return True, Times
    def BookRegister(self,USID,Name,BookTime,BookDate,Path):
        if ((BookTime or BookDate) == ""): return False, "No Time Or Date selcted"
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        RegID = 0
        for row in cur.execute('SELECT * FROM Bookings'):
            if row[1] == USID and row[2] == BookDate:
                con.close()
                return False, "You have a booking already today"
            RegID = row[0]
        img=qrcode.make(f"Pharmacy Book: {int(RegID)+1},{BookDate},{BookTime}")
        img.save(f'{Path}/BookCode.png')
        cur.execute(f"INSERT INTO Bookings VALUES ('{int(RegID)+1}','{USID}','{BookDate}','{BookTime}','{img}')")
        con.commit()
        con.close()
        backProcess.report_html(0,"Book",(BookTime,BookDate),Path,Name)
        return True,int(RegID)+1
    def BookRecallData(self,IDs):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Bookings'):
            if row[0] == IDs[0] and row[1] == IDs[3]:
                con.close()
                return True, "Successful"
            elif row[0] == IDs[0] and row[1] != IDs[3]:
                con.close()
                return False, "Error with Booking"
        con.close()
        return False, "No Booking was found"
    def PaymentRecall(self,IDs):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Orders'):
            if row[0] == IDs[0] and row[1] == IDs[1]:
                Order = row[2]
                for Bookingrow in cur.execute('SELECT * FROM Bookings'):
                    if Bookingrow[0] == IDs[1] and Bookingrow[1] == IDs[2]:
                        PaymentID = ""
                        for row in cur.execute('SELECT * FROM Payments'):
                            PaymentID = int(row[0])+1
                            if row[1] == IDs[0]:
                                con.close()
                                return False, "Order already paid"
                        if PaymentID == "": PaymentID = 1
                        now = datetime.now()
                        date = (now.strftime("%d/%m/%Y"),now.strftime("%H:%M"))
                        cur.execute(f"INSERT INTO Payments VALUES ('{int(PaymentID)}','{IDs[0]}','{date[0]}','{date[1]}')")
                        con.commit()
                        con.close()
                        backProcess.EditOrders(0,Order)
                        return True, "Successful"
                con.close()
                return False, "Error with Booking"
        con.close()
        return False, "No Order was found"
    def OrderRecall(self,IDs):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Orders'):
            if row[0] == IDs[0] and row[1] == IDs[1]:
                con.close()
                return True, "Successful", ast.literal_eval(row[2])
            elif row[0] == IDs[0] and row[1] != IDs[1]:
                con.close()
                return False, "Error with Order",False
        con.close()
        return False, "No Order was found",False
    def EditOrders(self,Order):
        Order = ast.literal_eval(Order)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for a in Order:
            for b in Order[a]:
                for Quantity in cur.execute(f"SELECT Quantity FROM {a} WHERE {a}ID='{b}'"): break
                cur.execute(f"UPDATE {a} SET Quantity = {int(Quantity[0])-int(Order[a][b]['Quantity'])} WHERE {a}ID='{b}'")
                con.commit()
        con.close()
    def Register(self,name,dob,email,password):#[5] Make Account #[6];
        if (name or dob or email or password) == "": return False,"Input Empty"
        REG = dataValidation.Register
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        RegID = 0
        if REG.nameVal(name) == False: return False, "Invalid Name"
        elif REG.dobVal(dob) == False: return False, "Invalid Date of Birth"
        elif REG.emailVal(email) == False: return False , "Invalid Email"
        elif REG.passwordVal(password) == False: return False, "Invalid Password"
        else: pass
        for row in cur.execute('SELECT * FROM Register'):
            RegID = row[0]
            row[3]
            if row[3] == email:
                con.close()
                return False, "Email already in use"
        cur.execute(f"INSERT INTO Register VALUES ('{int(RegID)+1}','{name}','{dob}','{email}','{password}')")
        con.commit()
        con.close()
        return True, int(RegID)+1
    def Login(self,dob,password):#[5] login #[7]
        if (dob or password) == "":  return False, "Empty Fields",""
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Register ORDER BY name'):
            if row[4] == password and row[2] == dob:
                con.close()
                return True, row[0],row[1]
        con.close()
        return False, "No account found", ""
    def GrabMedication(self,Tables):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        Medication = {}
        try:
            for x in Tables:
                Medication[x] = {}
                for row in cur.execute(f'SELECT * FROM {x}'): Medication[x][row[0]] = {'Name':row[1],'Price':row[2],'Quantity':row[3],"QRCode":qrcode.make((x,row[0],row[1]))}
        except:
            con.close()
            return False, []
        con.close()
        return True, Medication
    def RegisterOrder(self,ID,Name,Order,Path):
        if (ID or Order) == "": return False
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        OrderID = ""
        Change = False
        for row in cur.execute('SELECT * FROM Orders'):
            if row[1] == ID:
                Change = True
                OrderID = int(row[0])
                break
            OrderID = int(row[0])+1
        if OrderID == "": OrderID = 1
        for row in cur.execute('SELECT * FROM Payments'):
            if row[1] == str(OrderID):
                con.close()
                return False, "Order already paid"
        img=qrcode.make(f"Pharmacy Order: {int(OrderID)},{int(ID)}")
        img.save(f'{Path}/OrderCode.png') 
        New = str(Order).replace("'",'"')   
        if Change == False: cur.execute(f"INSERT INTO Orders VALUES ('{int(OrderID)}','{ID}','{str(New)}','{img}')")
        else: cur.execute(f"UPDATE Orders SET 'Order'='{New}' WHERE OrderID='{OrderID}'")            
        con.commit()
        con.close()
        backProcess.report_html(0,"Order",Order,Path,Name)
        return True
    def report_html(self,Stat,Order,Path,Name):
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
<!--+InsertHeadings+-->
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
        now = datetime.now()
        html = html.replace("<!--+todaysdate+-->", now.strftime("%d/%m/%Y %H:%M"))
        html = html.replace("<!--+name+-->", Name)
        if Stat == "Order":
            class OrderFunctions():
                def headingInsert():
                    Headings = []
                    Headings.append('<tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000;">')
                    for a in Order:
                        for b in Order[a]:
                            for c in Order[a][b]:
                                Headings.append(f'<td style="padding-top: 5px; padding-bottom: 5px;">{c}</td>')
                            break
                        break
                    Headings.append('</tr>')
                    return '\n'.join(Headings)
                def tableInsert():
                    Table,TotalQ,TotalP = [],0,0
                    for a in Order:
                        if a == "User_Name" or a == "User_ID" or a == "Order_ID": continue
                        for b in Order[a]:
                            Table.append('<tr style="border-top: 1px solid #999999;">')
                            for c in Order[a][b]: 
                                if c == "Price": Table.append(f'<td style="padding-top: 5px; padding-bottom: 5px;">£{Order[a][b][c]}</td>')
                                else: Table.append(f'<td style="padding-top: 5px; padding-bottom: 5px;">{Order[a][b][c]}</td>')
                            Table.append('</tr>')
                            TotalQ += int(Order[a][b]["Quantity"])
                            TotalP += float(Order[a][b]["Quantity"])*float(Order[a][b]["Price"])
                    return TotalQ,TotalP, Table
                def totalInsert(TotalQ, TotalP):
                    return f"""<tr style="border-top: 2px solid #000000; border-bottom: 2px solid #000000;">
                    <td style="padding-top: 5px; padding-bottom: 5px;">Total</td>
                    <td style="padding-top: 5px; padding-bottom: 5px;">£{round(TotalP,2)}</td>
                    <td style="padding-top: 5px; padding-bottom: 5px;">{TotalQ}</td>\n</tr>"""
            html = html.replace("<!--+Windowtitle+-->","Pharmacy Order")
            html = html.replace("<!--+title+-->","Pharmacy receipt:")
            html = html.replace("<!--+ImageQR+-->",'<img src="OrderCode.png" width="400">')
            TotalQ, TotalP, Table = OrderFunctions.tableInsert()
            Headings = OrderFunctions.headingInsert()
            html = html.replace('<!--+InsertHeadings+-->', Headings)
            html = html.replace('<!--+InsertLine+-->', '\n'.join(Table))
            html = html.replace('<!--+InsertTotal+-->', OrderFunctions.totalInsert(TotalQ, TotalP))
            Receipt = "OrderReceipt"
        elif Stat == "Book":
            html = html.replace("<!--+Windowtitle+-->","Pharmacy Booking")
            html = html.replace("<!--+title+-->","Pharmacy Bookings")
            html = html.replace('<!--+InsertHeadings+-->', f'<tr style="border-top: 1px solid #999999;"><td align="center">Your booking is for: {Order[0]} at {Order[1]}</td></tr>')
            html = html.replace("<!--+ImageQR+-->",'<img src="BookCode.png" width="400">')
            Receipt = "BookingReceipt"

        # dd/mm/YY H:M:S
        with open(f'{Path}/{Receipt}.html', 'w') as f: f.write(html)
        
  