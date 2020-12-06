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
    print('a')



def abc(rsName, rs, ufAddSub, ufMulDiv, ufLoadStore):
    for x in rs:
        if(x.pronto):
            if(rsName == 'ADD'):
                temEspaco, posicao = checkUF(ufAddSub)

                if(temEspaco):
                    ufAddSub[posicao].operation = x.op
                    ufAddSub[posicao].nCiclo = 5
                    ufAddSub[posicao].idRS = x.index()
                else:


            elif(rsName == 'MUL'):
                temEspaco, posicao = checkUF(ufMulDiv)
            
            elif(rsName == 'LOAD'):
                temEspaco, posicao = checkUF(ufLoadStore)
        else:
            print('a')


def checkUF(uf):
    count = 0
    
    for unit in uf:
        if(unit.operation == ""):
            return True, count
        
        count += 1
    
    return False, -1
