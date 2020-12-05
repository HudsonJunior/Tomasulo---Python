def BuscaInstrucoes(IR, listInstrucoes, PC):
    IR =  listInstrucoes[PC]
    PC += 1
    
    return IR, PC

def Despacho(IR, rsAddSub, rsMulDiv, rsLoadStore, listRegisters):
    IR = IR.replace(',', '')
    instrucao  = IR.split(' ')
    opcode = instrucao[0]
    
    if(opcode == 'mul' or opcode == 'div'):
        temEspaco, posicao = checkRS(rsMulDiv)

        if(temEspaco):
            estacao = rsMulDiv[posicao]
            rsMulDiv[posicao] = fillStation(estacao)
        else:
            print('a')
        
    
    elif(opcode == 'lw' or opcode == 'sw'):
        
    else :
        
def checkRS(rs):
    count = 0

    for station in rs:
        if(not station.busy):
            return true, count
        
        count += 1
    
    return false, -1

def fillStation(station, instruction, opcode, listRegisters, rsName, posicao):
    station.busy = True
    station.op = opcode
    
    if(len(instruction) = 3):
        operando1 = int(instruction[1].replace('r', ''))
        operando2 = int(instruction[2].replace('r', ''))
        destino = int(instruction[0].replace('r', ''))

        reg = listRegisters[operando1]

        if(reg.Qi == -1):
            station.Vj = reg.value
        else:
            station.Qj = reg.Qi
        
        listRegisters[destino].Qi = posicao
        listRegisters[destino].rs_name = rsName
        


    elif(len(instruction) = 2):

    elif(len(instruction) = 1):

    
