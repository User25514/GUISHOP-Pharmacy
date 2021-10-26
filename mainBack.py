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
            self.cur.execute("CREATE TABLE Bookings (BookID,RegIDFK,dateTime)")
            self.cur.execute("CREATE TABLE Medication (MedID,Name,Price,Quantity)")
            self.cur.execute("CREATE TABLE Medication (MedID,Name,Price,Quantity)")
            self.con.commit()
        except:
            pass
        self.con.close()
    def Book(self,email,date):#[1][2] Books a free date/timeslot
        self.REG = dataValidation.Register
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute(f"INSERT INTO Bookings VALUES ('{date}','{email}')")
        self.con.commit()
        for row in self.cur.execute('SELECT * FROM Bookings ORDER BY date'):
            print(row)

        self.con.close()
        pass
    def ShopState():#[2][3] Choice to shop in person or thorough the application.
        pass
    def ShoppingRecipt():#[4] A recipt will be produced with details of what has been bought with the total price.
        # The receipt will be associated with a unique qr code that the user will use at the payment stage.
        pass
    def Register(self,name,dob,email,password):#[5] Make Account
        #[6];
        #print(f"{name}, {dob}, {email}, {password}")
        REG = dataValidation.Register
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        a = REG.nameVal(name)
        b = REG.dobVal(dob)
        c = REG.emailVal(email)
        d = REG.passwordVal(password)
        RegID = 0
        #print(a,b,c,d)
        if (a or b or c or d) == False:
            return False
        else:
            pass
        for row in cur.execute('SELECT * FROM Register ORDER BY RegID'):
            #print(row)
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
        return True
    def Login(self,dob,password):#[5] login
        #[7]
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Register ORDER BY name'):
            #print(row)
            if row[4] == password and row[2] == dob:
                con.close()
                return True
        con.close()
        return False
    class MultiThread():
        def DateCheck(DateDic):
            pass