import sqlite3
from mainValidation import dataValidation

class backProcess:
    def __init__(self):
        self.REG = dataValidation.Register
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        try:
            self.cur.execute("CREATE TABLE Register (name,dob,email,password)")
            self.con.commit()
        except:
            pass
    def Book():#[1][2] Books a free date/timeslot
        self.REG = dataValidation.Register
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute(f"INSERT INTO Register VALUES ('{name}','{dob}','{email}','{password}')")
        self.con.commit()
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
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
        self.REG = dataValidation.Register
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        a = self.REG.nameVal(name)
        b = self.REG.dobVal(dob)
        c = self.REG.emailVal(email)
        d = self.REG.passwordVal(password)
        print(name,dob,email,password)
        print(a,b,c,d)
        if (a or b or c or d) == False:
            return False
        else:
            pass
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)
            if row[2] == email:
                self.con.close()
                return False
        self.cur.execute(f"INSERT INTO Register VALUES ('{name}','{dob}','{email}','{password}')")
        self.con.commit()
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)

        self.con.close()
        return True
        pass
    def Login(self,dob,password):#[5] login
        #[7]
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        for row in self.cur.execute('SELECT * FROM Register ORDER BY name'):
            print(row)
            if row[3] == password and row[1] == dob:
                self.con.close()
                return True
        self.con.close()
        return False
        pass
    class MultiThread():
        def DateCheck(DateDic):
            pass