from ReservationStation import checkRS
from ReservationStation import fillStation


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


def executar(uf, rs, PC):
    
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
                resultado = ~station.vj
                
            elif (x.operation == "blt"):
                if(station.vj > station.vk):
                    
            elif (x.operation == "bgt"):
                if(station.vj < station.vk):

            elif (x.operation == "beq"):

            elif (x.operation == "bne"):

            elif (x.operation == "j"):
                
            elif (x.operation == "lw"):
                resultado = Memoria[station.A]

            elif (x.operation == "sw"):
                resultado = station.vj


## como funcionam os valores das operações booleanas
## utilização do PC na main...
## a instrução sai da unidade funcional somente quando é escrita?
## os operandoas das funções de desvio estão bugados, como passar eles nas RS?
## como fazer as operações lógicas