import Helpers
import Pipeline

listRegisters, memoriaDados, memoriaInstrucoes, ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore = Helpers.getStructures()
clock = 0
PC = 0
IR = "" 


def main():
    global IR, PC
    fileName = input("Nome do arquivo de entrada: ")

    instructionFile = open(fileName, "r")

    listInstrucoes = instructionFile.readlines()

    # escrita

    # execucao

    #Despacho da instrucao
    Pipeline.Despacho(IR, rsAddSub, rsMulDiv, rsLoadStore, listRegisters)
    #Busca da instrucao
    IR, PC = Pipeline.BuscaInstrucoes(IR, listInstrucoes, PC)
    

