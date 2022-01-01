import sqlite3
from mainValidation import dataValidation

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
                return True, row[0]
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
                    Medication[x][row[0]] = {'Name':row[1],'Price':row[2],'Quantity':row[3]}
        except: 
            con.close()
            return False, []
        con.close()
        return True, Medication
    class MultiThread():
        def DateCheck(DateDic):
            pass
