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
        print('a')
    else :
        print('a')
def checkRS(rs):
    count = 0

    for station in rs:
        if(not station.busy):
            return True, count
        
        count += 1
    
    return False, -1

def fillStation(station, instruction, opcode, listRegisters, rsName, posicao):
    station.busy = True
    station.op = opcode
    
    ## add r0, r5, r10

    if len(instruction) == 4:
        operando1 = int(instruction[2].replace('r', ''))
        operando2 = int(instruction[3].replace('r', ''))
        destino = int(instruction[1].replace('r', ''))

        reg = listRegisters[operando1]

        if(reg.Qi == -1):
            station.Vj = reg.value
        else:
            station.Qj = '{}-{}'.format(reg.Qi, rsName)
        
        listRegisters[destino].Qi = posicao
        listRegisters[destino].rs_name = rsName

        if(opcode == 'subi' or opcode =='addi' or opcode == 'blt' or opcode == 'bgt' or opcode == 'beq' or opcode == 'bne'):
            station.Vk = operando2
        else:
            reg = listRegisters[operando2]

            if(reg.Qi == -1):
                station.Vk = reg.value
            else:
                station.Qk = '{}-{}'.format(reg.Qi, rsName)

    elif len(instruction) == 3 :
        
        if (opcode == "not"):
            destino = int(instruction[1]).replace('r', '')
            operando1 = int(instruction[2]).replace('r', '')
            reg = listRegisters[operando1]

            if (reg.Qi == -1):
                station.Vj = reg.value
            else:
                station.Qj = '{}-{}'.format(reg.Qi, rsName)
            
            listRegisters[destino].Qi = posicao
            listRegisters[destino].rs_name = rsName
        ## 10(r0) --> 10 + r0
        else:
            operando1 = instruction[1].replace('r', '') #rd ou rs
            M = instruction[2].split('(') #imm(rs ou rt)
            imm = M[0]
            reg_name_imm = M[1].replace(')', '')
            station.A = '{}+{}'.format(imm, reg_name_imm)
            
            operando2 = reg_name_imm.replace('r', '')

            reg_imm = listRegisters[int(operando2.replace('r', ''))]

            reg_rs = listRegisters[int(operando1)]

            if (opcode == "lw"):
                destino = int(instruction[1]).replace('r', '')
                
                if (reg_imm.Qi == -1):
                    station.Vj = reg_imm.value
                else:
                    station.Qj = '{}-{}'.format(reg_imm.Qi, rsName)

                listRegisters[destino].Qi = posicao
                listRegisters[destino].rs_name = rsName
            
            else:

                if (reg_imm.Qi == -1):
                    station.Vj = reg_imm.value
                else:
                    station.Qj = '{}-{}'.format(reg_imm.Qi, rsName)

                if (reg_rs.Qi == -1):
                    station.Vk = reg_rs.value
                else:
                    station.Qk = '{}-{}'.format(reg_rs.Qi, rsName)
                    
#sd r2,0(r1)
# rs = 9
# M[9]
# lw rd, imm(rs)
# rd - M[imm+rs]

#Ld r2 [0, r1]
#LD R2,0(R1)


## validar com o prof sobre a lógica do load e store

    elif (len(instruction) == 2) :
        station.Vj = instruction[1] 
    
