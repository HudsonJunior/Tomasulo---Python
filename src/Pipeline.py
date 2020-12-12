from ReservationStation import checkRS, fillStation, ReservationStationClass, limpaEstacao
from FunctionalUnit import FunctionalUnitClass, checkUF, AdicionarEmUF, DecrementaCiclosUF 
from LoadStoreQueue import LoadStoreQueue
import Helpers

def BuscaInstrucoes(IR, listInstrucoes, PC):
    IR =  listInstrucoes[PC]
    PC = PC + 1
    
    return IR, PC


def Despacho(IR, rsAddSub, rsMulDiv, rsLoadStore, listRegisters, flagOcorreuDespacho, loadStoreQueue):
    IR = IR.replace(',', '')
    instrucao  = IR.split(' ')
    opcode = instrucao[0]
    instrucaoDesvio = False

    if(flagOcorreuDespacho):
        if(opcode == 'mul' or opcode == 'div'):
            temEspaco, posicao = checkRS(rsMulDiv)
            if(temEspaco):
                flagOcorreuDespacho = True
                estacao = rsMulDiv[posicao]
                rsMulDiv[posicao], listRegisters, instrucaoDesvio = fillStation(estacao, instrucao, opcode, listRegisters, 'MUL', posicao)
            else:
                flagOcorreuDespacho = False
                
        elif(opcode == 'lw' or opcode == 'sw'):
            temEspaco, posicao = checkRS(rsLoadStore)
            if(temEspaco):
                flagOcorreuDespacho = True
                estacao = rsLoadStore[posicao]
                rsLoadStore[posicao], listRegisters, instrucaoDesvio = fillStation(estacao, instrucao, opcode, listRegisters, 'LOAD', posicao)
                
                loadStoreQueue.append(LoadStoreQueue(posicao))
            else:
                flagOcorreuDespacho = False

        else :
            temEspaco, posicao = checkRS(rsAddSub)
            if(temEspaco):
                flagOcorreuDespacho = True
                estacao = rsAddSub[posicao]
                rsAddSub[posicao], listRegisters, instrucaoDesvio = fillStation(estacao, instrucao, opcode, listRegisters, 'ADD', posicao)
            else:
                flagOcorreuDespacho = False
    
    return rsMulDiv, rsAddSub, rsLoadStore, listRegisters, flagOcorreuDespacho, instrucaoDesvio


def Execucao(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore, PC, MemoriaDados, loadStoreQueue):
    ## decrementar o numero de ciclos restantes nas unidades funcionais
    ufAddSub = DecrementaCiclosUF(ufAddSub)
    ufMulDiv = DecrementaCiclosUF(ufMulDiv)
    ufLoadStore = DecrementaCiclosUF(ufLoadStore)
    
    ## execucao das instrucoes que estao na unidade funcional
    ufAddSub = executarOperacao(ufAddSub, rsAddSub, MemoriaDados)
    ufMulDiv = executarOperacao(ufMulDiv, rsMulDiv, MemoriaDados)
    ufLoadStore = executarOperacao(ufLoadStore, rsLoadStore, MemoriaDados)
    
    ## verificar se tem espaço na unidade funcional e caso tenha, adicionar a instrução    
    ufAddSub, ufLoadStore, ufMulDiv, loadStoreQueue = AdicionarEmUF('ADD', rsAddSub, ufAddSub, ufMulDiv, ufLoadStore, loadStoreQueue)
    ufAddSub, ufLoadStore, ufMulDiv, loadStoreQueue = AdicionarEmUF('LOAD', rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore, loadStoreQueue)
    ufAddSub, ufLoadStore, ufMulDiv, loadStoreQueue = AdicionarEmUF('MUL', rsMulDiv, ufAddSub, ufMulDiv, ufLoadStore, loadStoreQueue)

    return ufAddSub, ufMulDiv, ufLoadStore, loadStoreQueue
    
def executarOperacao(uf, rs, MemoriaDados):
    
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
                resultado = MemoriaDados[station.A].valor

            elif (x.operation == "sw"):
                resultado = (station.vk, station.A)

            index = uf.index(x)
            x.resultado = resultado
            uf[index] = x
            
    return uf
    
def Escrita(ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, PC, memoriaDados):
    ## só pode uma escrita por vez, vamos priorizar a uf de soma por poder conter desvios
    escreveu = False
    
    escreveu, rsAddSub, ufAddSub, listRegister, PC, memoriaDados , ocorreuDesvio = escreverResultado(ufAddSub, rsAddSub, listRegister, 'ADD', PC, memoriaDados)
    if(escreveu):
        if(ocorreuDesvio):
            rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore = Helpers.limpaEstruturas(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore)

        return (ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, memoriaDados, PC, ocorreuDesvio)

    escreveu, rsMulDiv, ufMulDiv, listRegister, PC, memoriaDados , ocorreuDesvio = escreverResultado(ufMulDiv, rsMulDiv, listRegister, 'MUL', PC, memoriaDados)
    
    if(escreveu):
        return (ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, memoriaDados, PC , ocorreuDesvio)

    escreveu, rsLoadStore, ufLoadStore, listRegister, PC, memoriaDados, ocorreuDesvio = escreverResultado(ufLoadStore, rsLoadStore, listRegister, 'LOAD', PC, memoriaDados)
    
    return (ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, memoriaDados, PC , ocorreuDesvio)


def escreverResultado(uf, rs, listRegister, rsName, PC, memoriaDados):
    teveEscrita = False
    ocorreuDesvio = False
    
    for x in uf:
        if(x.nCiclos == 0 and not teveEscrita and not ocorreuDesvio):
            teveEscrita = True

            if(x.operation == 'blt' or x.operation == 'bgt' or x.operation == 'beq' or x.operation == 'bne' or x.operation == 'j'):
                if(x.resultado != -1):
                    PC = x.resultado
                    ocorreuDesvio = True
                    
            elif (x.operation == 'sw'):
                resultado, A = x.resultado
                memoriaDados[A] = resultado

            else: # no caso do load é a mesma coisa das outras operações
                if x.idRs == listRegister[x.idDestino].Qi:
                    #escrita do resultado
                    listRegister[x.idDestino].value = x.resultado

                    #tira a referencia do resultado na lista de registradores
                    listRegister[x.idDestino].Qi = -1

                #retirar as dependencias de dados
                for r in rs:
                    rIndex = rs.index(r)

                    if(rIndex != x.idRs):
                        idQj, rsQj = r.Qj.split('-')

                        if(int(idQj) == x.idRs and rsQj == rsName):
                            r.Vj = x.resultado
                            r.Qj = ''

                        idQk, rsQk = r.Qk.split('-')

                        if(int(idQk) == x.idRs and rsQk == rsName):
                            r.Vk = x.resultado
                            r.Qk = ''
                            
                        # atualizar estado da estação para pronto caso não tenha mais dependencia
                        if(r.Qj == '' and r.Qk == ''):
                            r.pronto = True

                        rs[rIndex] = r

            # limpeza da estação de reserva e unidade
            index = uf.index(x)
            rs = limpaEstacao(rs, x.idRs)
            uf[index] = FunctionalUnitClass("", 0, -1, -1, False, -1)

    return teveEscrita, rs, uf, listRegister, PC, memoriaDados, ocorreuDesvio
    
## como funcionam os valores das operações booleanas
## utilização do PC na main... // tem um buffer de instrucoes pra colocar as ins ai vc trabalha com o pc nisso (pc referene a ordem do despacho?)
## a instrução sai da unidade funcional somente quando é escrita? //sim
## os operandoas das funções de desvio estão bugados, como passar eles nas RS? // passar o valor do imediato no A
## como fazer as operações lógicas


## como atualizar o valor de R5 + 10 que estará no A na RS?


## validar instrução que entrou antes do desvio mas o desvio foi escrito antes, essa instrução vai ser apagada?
## finalizar lógica de escrita para as diferentes tipo de instrução


## rever a parte de sw e lw para a execucao e buffer de load e store
## colocar os endereços efetivos onde?
