from Register import RegisterClass
from FunctionalUnit import FunctionalUnitClass
from ReservationStation import ReservationStationClass
from LoadStoreBuffer import LoadStoreBufferClass

def getRegisterList():
    registerList = []

    for i in range(15):
        register = RegisterClass(-1, -1 , "")
        registerList.append(register)
    
    return registerList

def getLoadStoreBuffer():
    loadStoreBuffer = []

    for i in range(15):
        loadStoreBuffer = LoadStoreBufferClass('', '', -1)
    
    return loadStoreBuffer

def getUFList():
    ufList = []

    for i in range(2):
        uf = FunctionalUnitClass("", 0, -1, -1, False, -1)
        ufList.append(uf)
    
    return ufList

def getRSList():
    rsList = []

    for i in range(8):
        rs = ReservationStationClass(False, False, "", 0, 0, "", "", "")
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

    BufferLoadStore = getLoadStoreBuffer()

    return listRegisters, memoriaDados, memoriaInstrucoes, ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, BufferLoadStore

def limpaEstruturas(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore):
    ufAddSub = getUFList()
    ufMulDiv = getUFList()
    ufLoadStore = getUFList()

    rsAddSub = getRSList()
    rsMulDiv = getRSList()
    rsLoadStore = getRSList()

    return rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore