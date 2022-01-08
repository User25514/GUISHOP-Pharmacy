from datetime import datetime,date
class dataValidation:
    class Register:#[6]
        def nameVal(name):
            try:
                for x in name:
                    if x.isnumeric() == True or x == " ":
                        raise Exception
                    else:
                        pass
                return True

            except Exception:
                return False
        def dobVal(DOB):
            try:
                DOB = DOB.split("/")
                date1 = date(int(DOB[2]),int(DOB[1]),int(DOB[0]))
                date2 = datetime.now()
                date3 = date2.year - date1.year
                if date3 >= 18:
                    return True
                else:
                    raise Exception
            except Exception:
                return False
        def emailVal(email):
            try:
                atSymbol,dot = 0,0
                for x in email:
                    if x == "@":
                        atSymbol += 1
                    elif x == ".":
                        dot += 1
                if atSymbol == 1 and dot >= 1 and dot <= 2:
                    return True
                else:
                    raise Exception
            except Exception:
                return False

        def passwordVal(password):
            try:
                x = len(password)
                if (x < 15 and x >= 8):
                    cap,char,num = 0,0,0
                    for x in password:
                        if x.isnumeric() == True:
                            num += 1
                        elif x == " ":
                            raise Exception
                        elif x.isupper() == True:
                            cap += 1
                        elif x.isalpha() == True:
                            char += 1
                    if not(num > 1 and (char+cap) > 4 and cap > 1):
                        raise Exception
                    else:
                        return True
                else:
                    raise Exception
            except Exception:
                return False
