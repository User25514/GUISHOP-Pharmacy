import time

def funcTime(func):
    def wrapper(*args,**kwargs):
        before = time.time()
        val = func(*args,**kwargs)
        print(f"Ended: {time.time() - before} Seconds")
        return val

    return wrapper



class dataValidation:
    class Register:#[6]
        def nameVal(name):
            pass
        def dobVal(DOB):
            pass
        def emailVal(email):
            pass
        def passwordVal(password):
            pass 
    class Login:#[7]
        def dobVal(DOB):
            pass
        def passwordVal(password):
            pass
    pass
class backProcess:
    def Book():#[1][2] Books a free date/timeslot
        pass
    def ShopState():#[2][3] Choice to shop in person or thorough the application. 
        pass
    def ShoppingRecipt():#[4] A recipt will be produced with details of what has been bought with the total price. 
        # The receipt will be associated with a unique qr code that the user will use at the payment stage.
        pass
    def Register():#[5] Make Account
        #[6]
        pass
    def Login():#[5] login
        #[7]
        pass
    pass
class frontProcess:# PythonQT
    @funcTime
    def f1(self):
        print("hello")
    def BookNotification():#[1] Confirmatin to the user that the slot was booked successfully.
        pass
    def Shop():#[3][4][5] Browse medicines of the cargories provided.
        # Each product will be associated with a particular price and QR code.
        pass
    def Payment():# Scan QR code on receipt.
        pass
if __name__ == "__main__":
    backProcess.Book()
    pass


frontProcess.f1(0)