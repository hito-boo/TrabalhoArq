from sys import argv
import io

# Abrir o arquivo da seguinte forma: python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao

# Função principal ----------------------------------------------------------------------------------------

def main() -> None:
    if len(argv) == 3:
        try:
            memoria = open(argv[1], 'r+')
        except:
            print("\nERRO: Arquivo de memória não encontrado.")
        else:
            # Constante que guarda o Offset da primeira instrução, para que a busca sequencial de instruções se reduza apenas a elas
            global OFFSET_PRIMEIRA_INSTRUCAO
            OFFSET_PRIMEIRA_INSTRUCAO = offset_instrucao(memoria, int(argv[2], 0), 0)
            ciclo_ias(memoria, argv[2])
            memoria.close()
    return None

# Função de processamento ---------------------------------------------------------------------------------

def ciclo_ias(memoria: io.TextIOWrapper, endereco_instrucao: str) -> None:
    # Registradores 
    PC: str = endereco_instrucao
    AC: int = 0; MQ: int = 0; C: int = 2; Z: int = 1; R: int = 0
    MBR: str = ' '; MAR: str = ''; IR: str = ''

    while MBR != '':
        # Interpretação da instrução:
        MAR = PC
        MBR = leitura_instrucao(memoria, int(MAR, 0))
        IR = MBR.split()[1]
        MAR = MBR.split()[2][1:5]

        # Incrementando PC:
        PC = hex(int(PC, 0) + 1)

        # Execução da instrução:
        # Transferência de Dados
        if IR == 'LOAD_M':
            MBR = load(memoria, int(MAR, 0))
            AC = int(MBR)
        
        elif IR == 'LOAD_-M':
            MBR = load(memoria, int(MAR, 0))
            AC = -int(MBR)
        
        elif IR == 'LOAD_MQ':
            AC = MQ

        elif IR == 'LOAD_MQ_M':
            MBR = load(memoria, int(MAR, 0))
            MQ = int(MBR)

        elif IR == 'STORE_M':
            MBR = AC
            store(memoria, int(MAR, 0), MBR)

        # Aritmética de Dados
        elif IR == 'ADD_M':
            MBR = load(memoria, int(MAR, 0))
            AC = AC + int(MBR)
            AC, C = verifica_carry(AC)
            Z = verifica_sinal(AC)

        elif IR == 'SUB_M':
            MBR = load(memoria, int(MAR, 0))
            AC = AC - int(MBR)
            AC, C = verifica_carry(AC)
            Z = verifica_sinal(AC)

        elif IR == 'MUL_M':
            MBR = load(memoria, int(MAR, 0))
            MQ = MQ * int(MBR)
            AC, C = verifica_carry(AC)
            Z = verifica_sinal(AC)

        elif IR == 'DIV_M':
            MBR = load(memoria, int(MAR, 0))
            AC = AC / int(MBR)
            R = AC % int(MBR)
            AC, C = verifica_carry(AC)
            Z = verifica_sinal(AC)
        
        # Desvio
        elif IR == 'JUMP_M':
            PC = MAR

        elif IR == 'JUMP_+M':
            if AC >= 0:
                PC = MAR

    # Imprimindo os registradores.
    imprime_registradores(AC, MQ, C, Z, R, PC, MBR, MAR, IR)

    return None

# Função que faz a leitura das instruções -----------------------------------------------------------------

def leitura_instrucao(memoria:io.TextIOWrapper, endereco_instrucao: int) -> str:
    instrucao = ''
    offset = offset_instrucao(memoria, endereco_instrucao, OFFSET_PRIMEIRA_INSTRUCAO)
    memoria.seek(offset)
    return memoria.readline().strip()

def offset_instrucao(memoria: io.TextIOWrapper, endereco_instrucao: int, primeira_instrucao: int) -> int:
    # Função que retorna o Offset de uma instrução
    memoria.seek(primeira_instrucao)
    offset = memoria.tell()
    endereco_atual = int(memoria.readline().split()[0], 0)
    while endereco_atual != endereco_instrucao and endereco_atual != '':
        offset = memoria.tell()
        endereco_atual = int(memoria.readline().split()[0], 0)
    return offset

# Funções que realizam as instruções ----------------------------------------------------------------------

def load(memoria: io.TextIOWrapper, endereco: int) -> str:
    # Instrução de carregamento de um valor no endereço fornecido em um registrador.
    memoria.seek(0)
    leitura = memoria.readline().split()
    endereco_atual = int(leitura[0], 0)
    dado = leitura[1]
    while endereco_atual != endereco:
        leitura = memoria.readline().split()
        endereco_atual = int(leitura[0], 0)
        dado = leitura[1]
    return dado

def store(memoria: io.TextIOWrapper, endereco: int, ac: int) -> None:
    # Instrução de escrita na memória, no endereço fornecido.
    memoria.seek(0)
    offset = memoria.tell()
    endereco_atual = memoria.readline().split()[0]
    while endereco_atual != endereco:
        offset = memoria.tell()
        endereco_atual = memoria.readline.split()[0]
    memoria.seek(offset + 5)
    memoria.write(tratamento_store_ac(ac))
    return None

def tratamento_store_ac(ac: int) -> str:
    # Trata a quantidade de bytes a ser escrita na memória, para manter a estrutura do arquivo correta.
    if ac < -9 or ac > 99:
        acrescimo = ' '
    elif ac < 0 or ac > 9:
        acrescimo = '  '
    elif ac >= 0:
        acrescimo = '   '
    return str(ac) + acrescimo

def verifica_sinal(reg: int) -> int:
    # Função que verifica a polaridade de um registrador.
    if reg < 0:
        return -1
    elif reg == 0:
        return 0
    else:
        return 1

def verifica_carry(reg: int) -> tuple[int, int]:
    # Função que verifica se houve Carry Out em um registrador.
    if str(reg) > 4:
        return 1, reg[:4]
    else:
        return 2, reg

# Função que imprime os registradores ----------------------------------------------------------------------

def imprime_registradores(ac: int, mq: int, c: int, z: int, r: int, pc: str, mbr: str, mar: str, ir: str) -> None:
    # Função que imprime os registradores usados no ciclo de instrução.
    print('\nPC atual: ' + pc)
    print('Registrador do Buffer de Memória: ' + mbr + ' | Registrador do Endereço de Memória: ' + mar + ' | Registrador de Instrução: ' + ir)
    print('Acumulador: ' + str(ac) + ' | Multiplicador: ' + str(mq) + ' | Resto da divisão: ' + str(r))
    print('Carry Out: ' + str(c) + ' | Resultado Zero: ' + str(z))
    return None

# Chamada da função principal ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()