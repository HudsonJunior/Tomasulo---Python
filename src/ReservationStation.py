class ReservationStationClass:
    def __init__(self, nome, pronto, busy, op, Vj, Vk, Qj, Qk, A, idDestino, executando):
        self.nome = nome
        self.pronto = pronto
        self.busy = busy
        self.op = op
        self.Vj = Vj
        self.Vk = Vk
        self.Qj = Qj
        self.Qk = Qk
        self.A = A
        self.idDestino = idDestino
        self.executando = executando


def checkRS(rs):
    count = 0

    for station in rs:
        if(not station.busy):
            count = rs.index(station)
            return True, count
        
        count += 1
    
    return False, -1

def fillStation(station, instruction, opcode, listRegisters, rsName, posicao):
    station.busy = True
    station.op = opcode    
    instrucaoDesvio = False
    destino = -1

    if len(instruction) == 4:
        operando1 = int(instruction[2].replace('r', ''))
        operando2 = int(instruction[3].replace('r', ''))
        destino = int(instruction[1].replace('r', ''))
        
        
        # se for uma instrução de desvio, o valor destino vai valer pro vj, operando1 pro vk e operando2 pro A
        if(opcode == 'blt' or opcode == 'bgt' or opcode == 'beq' or opcode == 'bne'):
            reg = listRegisters[destino]

            if(reg.Qi == -1):
                station.Vj = int(reg.value)
            else:
                station.Qj = '{}-{}'.format(reg.Qi, reg.rs_name)
            
            reg = listRegisters[operando1]
            
            if(reg.Qi == -1):
                station.Vk = int(reg.value)
            else:
                station.Qk = '{}-{}'.format(reg.Qi, reg.rs_name)

            station.A = operando2

            instrucaoDesvio = True


        # se não for, atribui os valores normal e atualizar o registrador de destino para a instrucao atual
        else:
            reg = listRegisters[operando1]

            #validar o registrador do operando 1 (se esta sendo usado)

            if(reg.Qi == -1):
                station.Vj = int(reg.value)
            else:
                station.Qj = '{}-{}'.format(reg.Qi, reg.rs_name)

            listRegisters[destino].Qi = posicao
            listRegisters[destino].rs_name = rsName

            #validar se operando 2 é imediato ou registrador 
            if(opcode == 'subi' or opcode =='addi'):
                station.Vk = int(operando2)

            else:
                #se não for imediato fazer a validação se ele está ocupado
                reg = listRegisters[operando2]

                if(reg.Qi == -1):
                    station.Vk = int(reg.value)
                else:
                    station.Qk = '{}-{}'.format(reg.Qi, reg.rs_name)

    elif len(instruction) == 3 :
        
        if (opcode == "not"):
            destino = int(instruction[1].replace('r', ''))
            operando1 = int(instruction[2].replace('r', ''))
            
            reg = listRegisters[operando1]

            #verificar se o operando 1 esta sendo usado
            if (reg.Qi == -1):
                station.Vj = reg.value
            else:
                station.Qj = '{}-{}'.format(reg.Qi, reg.rs_name)
            
            #atualizar o registrador de destino para a instrucao atual
            listRegisters[destino].Qi = posicao
            listRegisters[destino].rs_name = rsName

        else: # Load ou Store

            operando1 = int(instruction[1].replace('r', '')) #rd ou rs
            M = instruction[2].split('(') #[imm, rs)]
            imm = int(M[0])
            reg_name_imm = M[1].replace(')', '')
            station.A = '{}+{}'.format(imm, reg_name_imm)
            
            operando2 = int(reg_name_imm.replace('r', ''))

            reg_imm = listRegisters[operando2]

            reg_rs = listRegisters[operando1]

            if (opcode == "lw"):
                destino = operando1
                
                #validar o reg_imm 
                if (reg_imm.Qi == -1):
                    station.Vj = reg_imm.value
                else:
                    station.Qj = '{}-{}'.format(reg_imm.Qi, reg_imm.rs_name)

                #atualiar o registrador de destino para a instrucao atual
                listRegisters[destino].Qi = posicao
                listRegisters[destino].rs_name = rsName
            
            else: #opcode sw

                #validar o reg_imm (destino)
                if (reg_imm.Qi == -1):
                    station.Vj = reg_imm.value
                else:
                    station.Qj = '{}-{}'.format(reg_imm.Qi, reg_imm.rs_name)

                #validar o reg_rs (fonte)
                if (reg_rs.Qi == -1):
                    station.Vk = reg_rs.value
                else:
                    station.Qk = '{}-{}'.format(reg_rs.Qi, reg_rs.rs_name)

    #salto incondicional
    elif (len(instruction) == 2) :
        station.Vj = int(instruction[1])

        instrucaoDesvio = True

    if(station.Qj == '' and station.Qk == ''):
        station.pronto = True
    
    station.idDestino = destino

    return station, listRegisters, instrucaoDesvio

def limpaEstacao(rs, index):
    rs[index] = ReservationStationClass(rs[index].nome, False, False, "", 0, 0, "", "", "", -1, False) 
    return rs
