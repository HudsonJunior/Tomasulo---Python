from Register import RegisterClass
from FunctionalUnit import FunctionalUnitClass
from ReservationStation import ReservationStationClass


def getRegisterList():
    registerList = []

    for i in range(15):
        register = RegisterClass(-1, -1 , "")
        registerList.append(register)
    
    return registerList

def getUFList():
    ufList = []

    for i in range(2):
        uf = FunctionalUnitClass("", 0, "")
        ufList.append(uf)
    
    return ufList

def getRSList():
    rsList = []

    for i in range(8):
        rs = ReservationStationClass(False, "", 0, 0, 0, 0, "")
        rsList.append(rs)
    
    return rsList

def getStructures():
    listRegisters = getRegisterList()

    memoriaDados = [0 for i in range(256)]

    memoriaInstrucoes = []

    ufAddSub = getUFList()

    ufMulDiv = getUFList()

    ufLoadStore = getUFList()
    
    rsAddSub = getRSList()

    rsMulDiv = getRSList()

    rsLoadStore = getRSList()

    return listRegisters, memoriaDados, memoriaInstrucoes, ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore