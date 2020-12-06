import Helpers
import Pipeline

listRegisters, memoriaDados, memoriaInstrucoes, ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore = Helpers.getStructures()
clock = 0
PC = 0
IR = ""
flagOcorreuDespacho = True
listaDeInstrucoes = []

def main():
    global IR, PC, listRegisters, memoriaDados, memoriaInstrucoes, ufAddSub, ufMulDiv, ufLoadStore, rsAddSub, rsMulDiv, rsLoadStore, flagOcorreuDespacho, clock
    fileName = input("Nome do arquivo de entrada: ")

    instructionFile = open(fileName, "r")

    listInstrucoes = instructionFile.readlines()

    while(PC < len(listInstrucoes)):
        # escrita

        # execucao

        #Despacho da instrucao
        if (flagOcorreuDespacho):
            instruction = listaDeInstrucoes[PC]
        
        rsMulDiv, rsAddSub, rsLoadStore, listRegisters, flagOcorreuDespacho = Pipeline.Despacho(instruction, rsAddSub, rsMulDiv, rsLoadStore, listRegisters, flagOcorreuDespacho)
        
        #Busca da instrucao
        IR, PC = Pipeline.BuscaInstrucoes(IR, listInstrucoes, PC)
        listaDeInstrucoes.append(IR)
    

