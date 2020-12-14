class FunctionalUnitClass:
    def __init__(self, operation, nCiclo, idRS, idDestino, execPronta, resultado):
        self.operation = operation
        self.nCiclo = nCiclo
        self.idRS = idRS
        self.execPronta = execPronta
        self.resultado = resultado
        self.idDestino = idDestino


def DecrementaCiclosUF (uf):

    for x in uf:
        if(x.nCiclo > 0):
            x.nCiclo -= 1

            if(x.nCiclo == 0):
                x.execPronta = True
        index = uf.index(x)
        uf[index] = x

    return uf


def checkUF(uf):
    count = 0
    
    for unit in uf:
        if(unit.operation == ""):
            return True, count
        
        count += 1
    
    return False, -1

def AdicionarEmUF(rsName, rs, ufAddSub, ufMulDiv, ufLoadStore, loadStoreQueue):
    for x in rs:
        if(x.pronto and not x.executando):
            # funcao "checkUf" valida se tem espaço na unidade funcional
            if(rsName == 'ADD'):
                temEspaco, posicao = checkUF(ufAddSub)

                # adicionar a instrução na UF de ADD
                if(temEspaco):
                    x.executando = True

                    ufAddSub[posicao].operation = x.op
                    ufAddSub[posicao].nCiclo = 5
                    ufAddSub[posicao].idRS = rs.index(x)
                    ufAddSub[posicao].idDestino = x.idDestino

            elif(rsName == 'MUL'):
                temEspaco, posicao = checkUF(ufMulDiv)
                if(temEspaco):
                    x.executando = True

                    ufMulDiv[posicao].operation = x.op

                    #operacoes de mul e div tem numero de ciclos diferentes
                    if(x.op == 'div'):
                        ufMulDiv[posicao].nCiclo = 20
                    else:
                        ufMulDiv[posicao].nCiclo = 10

                    ufMulDiv[posicao].idRS = rs.index(x)
                    ufMulDiv[posicao].idDestino = x.idDestino
            
            elif(rsName == 'LOAD'):
                index = rs.index(x)
                
                #se for o primeiro da fila de loadStore e ela estiver pronta, adicionar na unidade funcional
                if(loadStoreQueue[0].idRs == index):
                    loadStoreQueue.pop(0)
                    temEspaco, posicao = checkUF(ufLoadStore)
                    if(temEspaco):
                        x.executando = True

                        ufLoadStore[posicao].operation = x.op
                        ufLoadStore[posicao].nCiclo = 5
                        ufLoadStore[posicao].idRS = rs.index(x)
                        ufLoadStore[posicao].idDestino = x.idDestino

    return ufAddSub, ufLoadStore, ufMulDiv, loadStoreQueue