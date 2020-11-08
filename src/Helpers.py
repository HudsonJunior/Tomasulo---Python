from Register import RegisterClass

def getRegisterList():
        registerList = []

        for i in range(15):
            register = RegisterClass(0, 0 , "")
            registerList.append(register)
        
        return registerList

