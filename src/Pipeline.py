def BuscaInstrucoes(IR, listInstrucoes, PC):
    IR =  listInstrucoes[PC]
    PC += 1
    
    return IR, PC

def DecodificacaoInstrucoes(IR):
    