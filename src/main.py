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

    #Busca da instrucao
    IR, PC = Pipeline.BuscaInstrucoes(IR, listInstrucoes, PC)

    #Decodificacao da instrucao
    

