import Helpers
import Pipeline
from LoadStoreQueue import LoadStoreQueue
from prettytable import PrettyTable


def main():
    listRegisters, memoriaDados, memoriaInstrucoes, ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, BufferLoadStore = Helpers.getStructures()
    clock = 0
    ## PC aponta para a próxima instrução da Busca 
    PC = 0
    ## DC aponta para a próxima instrução do Despacho
    DC = 0 ## "despacho control"
    IR = ""

    flagOcorreuDespacho = True ## inicializada com True para a primeira instrução poder ser despachada

    ## fila de Load e Store para controlar a sequência despachada
    loadStoreQueue = []

    ## abertura do arquivo de instrucoes
    fileName = input("Nome do arquivo de entrada: ")
    instructionFile = open(fileName, "r")
    listInstrucoes = instructionFile.readlines()
    for ins in listInstrucoes:
        index = listInstrucoes.index(ins)
        ins = ins.replace('\n', '')
        listInstrucoes[index] = ins
    instrucaoDespacho = '' ## Instrucao a ser despachada
    acabouDespacho = False
    ocorreuDesvio = False
    instrucaoDesvio = False
    tamanhoListaInstrucoes = len(listInstrucoes) - 1
    tamanhoMemoriaInstrucoes = len(memoriaInstrucoes) - 1

    ## ADD R10, R5, R0
    ## SUB R20, R56, R30
    imprimirEstruturas(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore, listRegisters, memoriaDados, clock, memoriaInstrucoes)

    clock = clock + 1

    while(not terminou(rsAddSub, rsMulDiv, rsLoadStore, ocorreuDesvio, acabouDespacho)):
        
        ## Escrita
        ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegisters, memoriaDados, PC, ocorreuDesvio, instrucaoDesvio = Pipeline.Escrita(ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, listRegisters, PC, memoriaDados, instrucaoDesvio)
        
        if(not ocorreuDesvio):
            ## Execucao
            ufAddSub, ufMulDiv, ufLoadStore, LoadStoreQueue = Pipeline.Execucao(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore, PC, memoriaDados, loadStoreQueue)
            
            ## Despacho da instrucao
            if (flagOcorreuDespacho and not acabouDespacho and not instrucaoDesvio and memoriaInstrucoes != []):
                instrucaoDespacho = memoriaInstrucoes[DC]                
                ## Verifica se o despacho atual é o último na lista de instrucoes
                if(DC == tamanhoListaInstrucoes or (PC == tamanhoListaInstrucoes + 1 and DC == tamanhoMemoriaInstrucoes)):
                    acabouDespacho = True
                else:
                    DC = DC + 1

            
                rsMulDiv, rsAddSub, rsLoadStore, listRegisters, flagOcorreuDespacho, instrucaoDesvio = Pipeline.Despacho(instrucaoDespacho, rsAddSub, rsMulDiv, rsLoadStore, listRegisters, flagOcorreuDespacho, loadStoreQueue)
        
            ## Busca da instrucao
            if(PC <= tamanhoListaInstrucoes):
                IR, PC = Pipeline.BuscaInstrucoes(IR, listInstrucoes, PC)
                memoriaInstrucoes.append(IR)
                tamanhoMemoriaInstrucoes = len(memoriaInstrucoes) - 1

        else:
            memoriaInstrucoes = []
            DC = 0
            flagOcorreuDespacho = True
            acabouDespacho = False
            ocorreuDesvio = False
            instrucaoDesvio = False
            IR = ""
            instrucaoDespacho = ''
        
        imprimirEstruturas(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore, listRegisters, memoriaDados, clock, memoriaInstrucoes)
    
        clock = clock + 1


## Funcao para retornar True se acabaram todas as etapas de todas as instruções, caso contrario retorna False
def terminou(rsAddSub, rsMulDiv, rsLoadStore, ocorreuDesvio, acabouDespacho):
    flag1 = False
    flag2 = False
    flag3 = False

    for rs in rsAddSub:
        if(not rs.busy):
            flag1 = True
        else:
            flag1 = False
            break

    for rs in rsMulDiv:
        if(not rs.busy):
            flag2 = True
        else:
            flag2 = False
            break
    for rs in rsLoadStore:
        if(not rs.busy):
            flag3 = True
        else:
            flag3 = False
            break

    
    if(flag1 and flag2 and flag3 and acabouDespacho and not ocorreuDesvio):
        return True

    return False


def imprimirEstruturas(rsAddSub, rsMulDiv, rsLoadStore, ufAddSub, ufMulDiv, ufLoadStore, listRegister, memoriaDados, clock, memoriaInstrucoes):
    print('--------------------------------------------------------------------------------')
    print('\nCLOCK:{}\n'.format(clock))
    
    print("Estações de reserva:")
    printEstacao(rsAddSub, 'ADD')
    printEstacao(rsMulDiv, 'MUL')
    printEstacao(rsLoadStore, 'LOAD')
    print('\n')
    
    print('Lista de registradores:')
    printRegistradores(listRegister)
    print('\n')
    
    print('Memória de dados')
    printMemoria(memoriaDados)
    print('\n')

    print('Unidade funional')
    print('ADD')
    printUf(ufAddSub)
    print('MUL')
    printUf(ufMulDiv)
    print('LOAD')
    printUf(ufLoadStore)
    print('\n')


def printMemoriaIns(memoriaInstrucoes):
    print(memoriaInstrucoes)

def printUf(uf):
    t = PrettyTable(['Operação', 'nCiclo', 'idRs', 'execPronta', 'resultado', 'idDestino'])
    t.add_row([uf[0].operation, uf[0].nCiclo, uf[0].idRS, uf[0].execPronta, uf[0].resultado, uf[0].idDestino])
    t.add_row([uf[1].operation, uf[1].nCiclo, uf[1].idRS, uf[1].execPronta, uf[1].resultado, uf[1].idDestino])

    print(t)

def printEstacao(rs, rsName):
    t = PrettyTable(['Nome', 'Pronto', 'Busy', 'OP', 'Vj', 'Vk', 'Qj', 'Qk', 'A'])
    count = 0
    
    for x in rs:
        t.add_row([x.nome, x.pronto, x.busy, x.op, x.Vj, x.Vk, x.Qj, x.Qk, x.A])
        count = count + 1

    print(t)

def printRegistradores(listRegister):
    t = PrettyTable([' ', 'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14'])
    t.add_row(['RsName', listRegister[0].rs_name, listRegister[1].rs_name, listRegister[2].rs_name, listRegister[3].rs_name, listRegister[4].rs_name, listRegister[5].rs_name, listRegister[6].rs_name, listRegister[7].rs_name, listRegister[8].rs_name, listRegister[9].rs_name, listRegister[10].rs_name, listRegister[11].rs_name, listRegister[12].rs_name, listRegister[13].rs_name,listRegister[14].rs_name])
    t.add_row(['Qi', listRegister[0].Qi, listRegister[1].Qi, listRegister[2].Qi, listRegister[3].Qi, listRegister[4].Qi, listRegister[5].Qi, listRegister[6].Qi, listRegister[7].Qi, listRegister[8].Qi, listRegister[9].Qi, listRegister[10].Qi, listRegister[11].Qi, listRegister[12].Qi, listRegister[13].Qi,listRegister[14].Qi])
    t.add_row(['Valor', listRegister[0].value, listRegister[1].value, listRegister[2].value, listRegister[3].value, listRegister[4].value, listRegister[5].value, listRegister[6].value, listRegister[7].value, listRegister[8].value, listRegister[9].value, listRegister[10].value, listRegister[11].value, listRegister[12].value, listRegister[13].value,listRegister[14].value])

    print(t)
    

def printMemoria(memoriaDados):
    print(memoriaDados, sep ="| ")

main()

## Assumimos que não tem problema alguma instrução que vem antes do desvio não escrever o seu resultado antes 
## de tomar o desvio

## Na unidade funcional, o campo idDestino deve conter a posicao do registrador de destino, 
## caso não tiver um destino, este campo deve conter o valor -1

## Assumimos que a ordem para verificar na hora de adicionar uma instrucao na unidade funcional será pela ordem na
## estacao de reserva

## Colocamos valores aleatórios para a memória de dados