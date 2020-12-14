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
    idDestino = -1
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
    
def executarOperacao(uf, rs, memoriaDados):
    resultado = -1
    for x in uf:
        if(x.execPronta):
            station = rs[x.idRS]
            
            if (x.operation == "add"):
                resultado = int(station.Vj) + int(station.Vk)
                
            elif (x.operation == "addi"):
                resultado = int(station.Vj) + int(station.Vk)
                
            elif (x.operation == "sub"):
                resultado = int(station.Vj) - int(station.Vk)

            elif (x.operation == "subi"):
                resultado = int(station.Vj) - int(station.Vk)

            elif (x.operation == "mul"):
                resultado = int(station.Vj) * int(station.Vk)
                
            elif (x.operation == "div"):
                resultado = int(int(station.Vj) / int(station.Vk))

            elif (x.operation == "and"):
                resultado = int(station.Vj) & int(station.Vk)

            elif (x.operation == "or"):
                resultado = int(station.Vj) | int(station.Vk)

            elif (x.operation == "not"):
                resultado = ~int(station.Vj)
                
            elif (x.operation == "blt"):
                if(station.Vj < station.Vk):
                    resultado = station.A
                else:
                    resultado = -1

            elif (x.operation == "bgt"):
                if(station.Vj > station.Vk):
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

                resultado = station.Vj

            elif (x.operation == "lw"):
                imediato = int(station.A.split('+')[0])
                A = imediato + station.Vj
                resultado = memoriaDados[A]

            elif (x.operation == "sw"):
                imediato = int(station.A.split('+')[0])
                A = imediato + station.Vj
                resultado = (station.Vk, A)

            index = uf.index(x)
            x.resultado = resultado
            uf[index] = x
            
    return uf
    
def Escrita(ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, PC, memoriaDados, instrucaoDesvio):
    ## só pode uma escrita por vez, vamos priorizar a uf de soma por poder conter desvios
    escreveu = False
    
    escreveu, rsAddSub, ufAddSub, listRegister, PC, memoriaDados , ocorreuDesvio, rsAddSub, rsMulDiv, rsLoadStore, instrucaoDesvio = escreverResultado(ufAddSub, rsAddSub, rsAddSub, rsMulDiv, rsLoadStore, listRegister, PC, memoriaDados, instrucaoDesvio)
    if(escreveu):
        if(ocorreuDesvio):
            rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore = Helpers.limpaEstruturas(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore)

        return (ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, memoriaDados, PC, ocorreuDesvio, instrucaoDesvio)

    escreveu, rsMulDiv, ufMulDiv, listRegister, PC, memoriaDados , ocorreuDesvio, rsAddSub, rsMulDiv, rsLoadStore, instrucaoDesvio = escreverResultado(ufMulDiv, rsMulDiv, rsAddSub, rsMulDiv, rsLoadStore,listRegister, PC, memoriaDados, instrucaoDesvio)
    
    if(escreveu):
        return (ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, memoriaDados, PC , ocorreuDesvio, instrucaoDesvio)

    escreveu, rsLoadStore, ufLoadStore, listRegister, PC, memoriaDados, ocorreuDesvio, rsAddSub, rsMulDiv, rsLoadStore, instrucaoDesvio = escreverResultado(ufLoadStore, rsLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, PC, memoriaDados, instrucaoDesvio)
    
    return (ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegister, memoriaDados, PC , ocorreuDesvio, instrucaoDesvio)


def escreverResultado(uf, rs, rsAddSub, rsMulDiv, rsLoadStore, listRegister, PC, memoriaDados, instrucaoDesvio):
    teveEscrita = False
    ocorreuDesvio = False
    
    for x in uf:
        if(x.nCiclo == 0 and not teveEscrita and not ocorreuDesvio):
            teveEscrita = True

            if(x.operation == 'blt' or x.operation == 'bgt' or x.operation == 'beq' or x.operation == 'bne' or x.operation == 'j'):
                instrucaoDesvio = False
                if(x.resultado != -1):
                    PC = x.resultado
                    ocorreuDesvio = True
                    
            elif (x.operation == 'sw'):
                resultado, A = x.resultado
                memoriaDados[A] = resultado

            else: # no caso do load é a mesma coisa das outras operações
                if x.idRS == listRegister[x.idDestino].Qi:
                    #escrita do resultado
                    listRegister[x.idDestino].value = x.resultado

                    #tira a referencia do resultado na lista de registradores
                    listRegister[x.idDestino].Qi = -1
                    listRegister[x.idDestino].rs_name = ''

                #retirar as dependencias de dados
                retiraDependencia(rsAddSub, rs[x.idRS].nome[:-1], x)
                retiraDependencia(rsMulDiv, rs[x.idRS].nome[:-1], x)
                retiraDependencia(rsLoadStore, rs[x.idRS].nome[:-1], x)
            # limpeza da estação de reserva e unidade
            index = uf.index(x)
            rs = limpaEstacao(rs, x.idRS)
            uf[index] = FunctionalUnitClass("", -1, -1, -1, False, -1)

    return teveEscrita, rs, uf, listRegister, PC, memoriaDados, ocorreuDesvio, rsAddSub, rsMulDiv, rsLoadStore, instrucaoDesvio

def retiraDependencia(rs, rsName, x):
    for r in rs:
        rIndex = rs.index(r)

        if(rIndex != x.idRS or rsName != rs[x.idRS].nome):
            if(r.Qj != ''):
                idQj, rsQj = r.Qj.split('-')

                if(int(idQj) == x.idRS and rsQj == rsName):
                    r.Vj = x.resultado
                    r.Qj = ''

            
            if(r.Qk != ''):
                idQk, rsQk = r.Qk.split('-')

                if(int(idQk) == x.idRS and rsQk == rsName):
                    r.Vk = x.resultado
                    r.Qk = ''

            # atualizar estado da estação para pronto caso não tenha mais dependencia
            if(r.Qj == '' and r.Qk == '' and r.busy):
                r.pronto = True

            rs[rIndex] = r

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
