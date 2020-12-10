from ReservationStation import checkRS
from ReservationStation import fillStation
from ReservationStation import ReservationStationClass
from FunctionalUnit import FunctionalUnitClass


def BuscaInstrucoes(IR, listInstrucoes, PC):
    IR =  listInstrucoes[PC]
    PC += 1
    
    return IR, PC


def Despacho(IR, rsAddSub, rsMulDiv, rsLoadStore, listRegisters, flagOcorreuDespacho):
    IR = IR.replace(',', '')
    instrucao  = IR.split(' ')
    opcode = instrucao[0]

    if(flagOcorreuDespacho):
        if(opcode == 'mul' or opcode == 'div'):
            temEspaco, posicao = checkRS(rsMulDiv)
            if(temEspaco):
                flagOcorreuDespacho = True
                estacao = rsMulDiv[posicao]
                rsMulDiv[posicao], listRegisters = fillStation(estacao, instrucao, opcode, listRegisters, 'MUL', posicao)
            else:
                flagOcorreuDespacho = False
                
        elif(opcode == 'lw' or opcode == 'sw'):
            temEspaco, posicao = checkRS(rsLoadStore)
            if(temEspaco):
                flagOcorreuDespacho = True
                estacao = rsLoadStore[posicao]
                rsLoadStore[posicao], listRegisters = fillStation(estacao, instrucao, opcode, listRegisters, 'LOAD', posicao)
            else:
                flagOcorreuDespacho = False

        else :
            temEspaco, posicao = checkRS(rsAddSub)
            if(temEspaco):
                flagOcorreuDespacho = True
                estacao = rsAddSub[posicao]
                rsAddSub[posicao], listRegisters = fillStation(estacao, instrucao, opcode, listRegisters, 'ADD', posicao)
            else:
                flagOcorreuDespacho = False
    
    return rsMulDiv, rsAddSub, rsLoadStore, listRegisters, flagOcorreuDespacho


def Execucao(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore):
    executar(ufAddSub, rsAddSub)
    executar(ufMulDiv, rsMulDiv)
    executar(ufLoadStore, rsLoadStore)



#se tiver espaço, colocar a instrução na uf
def AdicionarEmUF(rsName, rs, ufAddSub, ufMulDiv, ufLoadStore):
    for x in rs:
        if(x.pronto):
            if(rsName == 'ADD'):
                temEspaco, posicao = checkUF(ufAddSub)

                if(temEspaco):
                    ufAddSub[posicao].operation = x.op
                    ufAddSub[posicao].nCiclo = 5
                    ufAddSub[posicao].idRS = x.index()

            elif(rsName == 'MUL'):
                temEspaco, posicao = checkUF(ufMulDiv)
                if(temEspaco):
                    ufMulDiv[posicao].operation = x.op
                    ufMulDiv[posicao].nCiclo = 5
                    ufMulDiv[posicao].idRS = x.index()
            
            elif(rsName == 'LOAD'):
                temEspaco, posicao = checkUF(ufLoadStore)
                if(temEspaco):
                    ufLoadStore[posicao].operation = x.op
                    ufLoadStore[posicao].nCiclo = 5
                    ufLoadStore[posicao].idRS = x.index()
        else:
            print('a')
            

# def escrita(uf):
#     for x in uf:


def DecrementaCiclosUF (uf):

    for x in uf:
        if(x.nCiclos > 0):
            x.nCiclos -= 1

            if(x.nCiclos == 0):
                x.execCompleta = True


def checkUF(uf):
    count = 0
    
    for unit in uf:
        if(unit.operation == ""):
            return True, count
        
        count += 1
    
    return False, -1


def executar(uf, rs, PC, BufferMemoria):
    
    for x in uf:
        if(x.execCompleta):
            station = rs[x.idRS]
            
            if (x.operation == "add"):
                resultado = int(station.vj) + int(station.vk)
                
            elif (x.operation == "addi"):
                resultado = int(station.vj) + int(station.vk)
                
            elif (x.operation == "sub"):
                resultado = int(station.vj) - int(station.vk)

            elif (x.operation == "subi"):
                resultado = int(station.vj) - int(station.vk)

            elif (x.operation == "mul"):
                resultado = int(station.vj) * int(station.vk)
                
            elif (x.operation == "div"):
                resultado = int(station.vj) / int(station.vk)

            elif (x.operation == "and"):
                resultado = int(station.vj) & int(station.vk)

            elif (x.operation == "or"):
                resultado = int(station.vj) | int(station.vk)

            elif (x.operation == "not"):
                resultado = ~int(station.vj)
                
            elif (x.operation == "blt"):
                if(station.Vj > station.Vk):
                    resultado = station.A
                else:
                    resultado = -1

            elif (x.operation == "bgt"):
                if(station.Vj < station.Vk):
                    resultado = station.A
                else:
                    resultado = -1

            elif (x.operation == "beq"):

                if(station.Vj == station.Vk):
                    resultado = station.A
                else: 
                    resultado = -1

            elif (x.operation == "bne"):

                if(station.Vj != station.Vk):
                    resultado = station.A
                else: 
                    resultado = -1

            elif (x.operation == "j"):

                resultado = station.vj       

            elif (x.operation == "lw"):
                resultado = BufferMemoria[station.A]

            elif (x.operation == "sw"):
                BufferMemoria[station.A] = station.vk

            x.resultado = resultado

def escrita(ufAddSub, ufMulDiv, ufLoadDiv, rsAddSub, rsMulDiv, rsLoadStore, listRegister):
    ## só pode uma escrita por vez, vamos priorizar a uf de soma por poder conter desvios
    
    escreveu, rsAddSub, ufAddSub, listRegister = Escrita(ufAddSub, rsAddSub, listRegister, 'ADD')
    if(escreveu):
        
        return (ufAddSub, ufMulDiv, ufLoadDiv, rsAddSub, rsMulDiv, rsLoadStore, listRegister)

    escreveu, rsMulDiv, ufMulDiv, listRegister = Escrita(ufMulDiv, rsMulDiv, listRegister, 'MUL')
    
    if(escreveu):
        return (ufAddSub, ufMulDiv, ufLoadDiv, rsAddSub, rsMulDiv, rsLoadStore, listRegister)

    escreveu, rsLoadStore, ufLoadStore, listRegister = Escrita(ufLoadDiv, rsLoadStore, listRegister, 'LOAD')
    
    return (ufAddSub, ufMulDiv, ufLoadDiv, rsAddSub, rsMulDiv, rsLoadStore, listRegister)

def Escrita(uf, rs, listRegister, rsName, PC):
    teveEscrita = False
    ocorreuDesvio = False
    
    for x in uf:
        if(x.nCiclos == 0):
            if(x.operation == 'blt' or x.operation == 'bgt' or x.operation == 'beq' or x.operation == 'bne' or x.operation == 'j'):
                if(x.resultado != -1):
                    PC = x.resultado
                    ocorreuDesvio = True

                else:
                    rs = limpaEstacao(rs, x.idRs)
                
            elif(x.operation == 'lw' or x.operation == 'sw'):
            
            else:
                if(x.idRs == listRegister[uf.idDestino]).Qi:
                    #escrita do resultado
                    listRegister[uf.idDestino].value = x.result

                    #tira a referencia do resultado na lista de registradores
                    listRegister[uf.idDestino].Qi = -1
                    teveEscrita = True
                
                #limpeza das estruturas
                index = uf.index(x)
                rs = limpaEstacao(rs, x.idRs)
                uf[index] = FunctionalUnitClass("", 0, -1, -1, False, -1)    

                #retirar as dependencias de dados
                for r in rs:
                    rIndex = r.index()
                    idQj, rsQj = r.Qj.split('-')

                    if(idQj == x.idRs and rsQj == rsName):
                        r.Vj = x.resultado
                        r.Qj = ''

                    idQk, rsQk = r.Qk.split('-')

                    if(idQk == x.idRs and rsQk == rsName):
                        r.Vk = x.resultado
                        r.Qk = ''
                    
                    rs[rIndex] = r

    return teveEscrita, rs, uf, listRegister, ocorreuDesvio

 
def limpaEstacao(rs, index):
    rs[index] = ReservationStationClass(False, False, "", 0, 0, "", "", "") 
    return rs


## como funcionam os valores das operações booleanas
## utilização do PC na main... // tem um buffer de instrucoes pra colocar as ins ai vc trabalha com o pc nisso (pc referene a ordem do despacho?)
## a instrução sai da unidade funcional somente quando é escrita? //sim
## os operandoas das funções de desvio estão bugados, como passar eles nas RS? // passar o valor do imediato no A
## como fazer as operações lógicas


## como atualizar o valor de R5 + 10 que estará no A na RS?


## validar instrução que entrou antes do desvio mas o desvio foi escrito antes, essa instrução vai ser apagada?
## finalizar lógica de escrita para as diferentes tipo de instrução
