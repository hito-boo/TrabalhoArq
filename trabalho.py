# Caetano Vendrame Mantovani, RA: 135846
# Matheus Cenerini Jacomini, RA 134700
# Vitor da Rocha Machado, RA: 132769

from sys import argv
import io

TAM_ENDERECO = 23
TAM_MAX_DADO = 16

# Abrir o arquivo da seguinte forma: python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao

'''
O programa dará origem a um arquivo chamado 'memoria_ajustada.ias', na qual ocorrerá o processamento dos
dados e instruções dispostas no arquivo de memória passado como argumento.
'''

'''
Foi criado um registrador de uso geral chamado 'NAR' (Next Adress Registrator), o qual armazena o endereço
que está logo após o endereço do MAR (foi utilizado no algoritmo de Selection Sort).
O endereço do MAR em questão não é de instrução no momento dessa atribuição.
'''

# Função principal ----------------------------------------------------------------------------------------

def main() -> None:
    # Esperando: python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao
    if len(argv) == 3:
        try:
            # memoria = open(nome_arquivo_memoria, 'r+')
            memoria_aberta = open(argv[1], 'r')
        except FileNotFoundError:
            print("\nERRO: Arquivo de memória não encontrado.")
        else:
            memoria = ajusta_memoria(memoria_aberta, TAM_ENDERECO)
            ciclo_ias(memoria, argv[2])
            memoria.close()
    else:
        print("\nERRO: Número de argumentos inválido.")
        print("Modo de uso: python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao\n")
    return None

# Função de processamento ---------------------------------------------------------------------------------

def ciclo_ias(memoria: io.TextIOWrapper, endereco_instrucao: str) -> None:
    # Registradores
    PC: str = endereco_instrucao
    AC: int = 0; MQ: int = 0; NAR: str = '';
    C: int = 0; Z: int = 0; R: int = 0
    MBR: str = ''; MAR: str = ''; IR: str = ''

    print('\nValores Iniciais:')
    imprime_registradores(AC, MQ, C, Z, R, PC, MBR, MAR, IR, NAR)
    prox = input('\nPara a execução de cada instrução, aperte [ENTER]')

    while IR != 'END':
        if not prox:
            # Interpretação da instrução:
            MAR = PC
            MBR = leitura_memoria(memoria, int(MAR, 0))
            IR = MBR.split()[1]
            if len(MBR.split()) > 2:
                if MBR.split()[2][0] == '(':
                    MAR = MBR.split()[2][1:5]

            # Incrementando PC:
            PC = hex(int(PC, 0) + 1)

            # Execução da instrução:
            # Transferência de Dados
            if IR == 'LOAD':
                C, AC = verifica_carry(int(MBR.split()[2]))
                Z = verifica_sinal(AC)

            if IR == 'LOAD_M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                C, AC = verifica_carry(int(MBR))
                Z = verifica_sinal(AC)
            
            elif IR == 'LOAD_-M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                C, AC = verifica_carry(-int(MBR))
                Z = verifica_sinal(AC)
            
            elif IR == 'LOAD_MQ':
                C, AC = verifica_carry(MQ)
                Z = verifica_sinal(AC)
            
            elif IR == 'LOAD_NAR':
                MAR = NAR
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                C, AC = verifica_carry(int(MBR))
                Z = verifica_sinal(AC)

            elif IR == 'LOAD_MQ_M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                MQ = int(MBR)

            elif IR == 'STORE_M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = AC
                store(memoria, int(MAR, 0), int(MBR))

            # Aritmética de Dados
            elif IR == 'ADD':
                AC = AC + int(MBR.split()[2])
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'ADD_M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                AC = AC + int(MBR)
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'SUB':
                AC = AC - int(MBR.split()[2])
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'SUB_M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                AC = AC - int(MBR)
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'MUL':
                MQ = MQ * int(MBR.split()[2])
                C, MQ = verifica_carry(MQ)

            elif IR == 'MUL_M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                MQ = MQ * int(MBR)
                C, MQ = verifica_carry(MQ)

            elif IR == 'DIV':
                R = AC % int(MBR.split()[2])
                AC = AC // int(MBR.split()[2])
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'DIV_M':
                NAR = hex((int(MAR, 0) + 1))
                MBR = load(memoria, int(MAR, 0))
                R = AC % int(MBR)
                AC = AC // int(MBR)
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)
            
            # Desvio
            elif IR == 'JUMP_M':
                PC = MAR

            elif IR == 'JUMP_+M':
                if AC >= 0:
                    PC = MAR

            # Fim das instruções
            elif IR == 'END':
                pass

            # Erro na Memória
            else:
                print('ERRO NA MEMÓRIA!')
            
            # Impressão de Registradores:
            imprime_registradores(AC, MQ, C, Z, R, PC, MBR, MAR, IR, NAR)

            # Continuar ciclo:
            prox = input('\nPara a execução da próxima instrução, aperte [ENTER]')

        else:
            prox = input('\nPara a execução da próxima instrução, aperte [ENTER]')
    return None

# Função que faz a leitura da memória ---------------------------------------------------------------------

def leitura_memoria(memoria: io.TextIOWrapper, endereco: int) -> str:
    memoria.seek(endereco * TAM_ENDERECO)
    leitura = memoria.readline().strip()
    if int(leitura[:4], 0) == endereco:
        return leitura
    else:
        return ''

# Funções que realizam as instruções ----------------------------------------------------------------------

def load(memoria: io.TextIOWrapper, endereco: int) -> str:
    ''' Instrução de carregamento de um valor no endereço fornecido em um registrador. '''
    leitura = leitura_memoria(memoria, endereco)
    if leitura:
        return leitura.split()[1]
    else:
        return '0'

def store(memoria: io.TextIOWrapper, endereco: int, dado: int) -> None:
    memoria.seek(endereco * TAM_ENDERECO)
    if int(memoria.read(4), 0) == endereco:
        memoria.seek(endereco * TAM_ENDERECO + 5)
        memoria.write((str(dado) + ' ' * TAM_MAX_DADO)[:TAM_MAX_DADO] + '\n')
    return None

def verifica_sinal(reg: int) -> int:
    ''' Função que verifica a polaridade de um registrador. '''
    if reg < 0:
        return -1
    elif reg == 0:
        return 0
    else:
        return 1

def verifica_carry(reg: int) -> tuple[int, int]:
    ''' Função que verifica se houve Carry Out em um registrador. '''
    if len(str(reg)) > TAM_MAX_DADO:
        return 1, int(str(reg)[:TAM_MAX_DADO])
    else:
        return 2, reg

# Função que imprime os registradores ----------------------------------------------------------------------

def imprime_registradores(ac: int, mq: int, c: int, z: int, r: int, pc: str, mbr: str, mar: str, ir: str, nar: str) -> None:
    ''' Função que imprime os registradores usados no ciclo de instrução. '''
    print('\nPC: ' + pc)
    print('MBR: ' + str(mbr) + ' | IR: ' + ir + ' | MAR: ' + mar )
    print('AC: ' + str(ac) + ' | MQ: ' + str(mq) + ' | NAR: ' + nar)
    print('C: ' + str(c) + ' | Z: ' + str(z) + ' | R: ' + str(r))
    return None

# Função que faz a formatação da memória processada --------------------------------------------------------

def ajusta_memoria(memoria_aberta: io.TextIOWrapper, tamanho_endereco: int) -> io.TextIOWrapper:
    memoria_ajustada = open('memoria_ajustada.ias', 'w+')
    linha = memoria_aberta.readline().strip()
    while linha:
        memoria_ajustada.write((linha + ' ' * (tamanho_endereco - 2))[:tamanho_endereco - 2] + '\n')
        linha = memoria_aberta.readline().strip()
    memoria_aberta.close()
    return memoria_ajustada

# Chamada da função principal ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()