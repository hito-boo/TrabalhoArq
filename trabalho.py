'''
# Trabalho de Arquitetura e Organização de Computadores - Simulação Instruções de Máquina

# Caetano Vendrame Mantovani, RA: 135846
# Matheus Cenerini Jacomini, RA 134700
# Vitor da Rocha Machado, RA: 132769

Abrir o arquivo da seguinte forma: python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao tamanho_vetor

O programa dará origem a um arquivo chamado 'memoria_ajustada.ias', no qual ocorrerá o processamento dos dados e instruções
dispostas no arquivo de memória passado como argumento.

# python trabalho.py selection_sort.ias 0x1D 10
O algoritmo de Selection Sort está disposto no arquivo 'selection_sort.ias', o qual possui sua primeira instrução no
endereço 0x1D e um vetor de tamanho 10.

# python trabalho.py fibonacci.ias 0x05 0
O segundo algoritmo implementado foi um que fornece o elemento n = 7 da Sequência de Fibonacci e está disposto no arquivo
'fibonacci.ias', o qual não exige vetor e possui o seu resultado sendo o último dado disposto dos endereços de dados.
'''

from sys import argv
import io

TAM_ENDERECO = 23
TAM_MAX_DADO = 16

# Função principal ----------------------------------------------------------------------------------------------------------

def main() -> None:
    '''
    Função principal do programa.
    '''
    # Esperando: python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao tamanho_vetor
    if len(argv) == 4:
        try:
            # memoria = open(nome_arquivo_memoria, 'r+')
            memoria_aberta = open(argv[1], 'r', encoding="utf8")
        except FileNotFoundError:
            print("\nERRO: Arquivo de memória não encontrado.")
        else:
            memoria = ajusta_memoria(memoria_aberta, TAM_ENDERECO)
            lista = cria_vetor_enderecos(int(argv[3]))
            ciclo_ias(memoria, argv[2], lista)
            memoria.close()
    else:
        print("\nERRO: Número de argumentos inválido.")
        print("Modo de uso: python trabalho.py nome_arquivo_memoria endereco_primeira_instrucao tamanho_vetor\n")
    return None

# Função de processamento ---------------------------------------------------------------------------------------------------

def ciclo_ias(memoria: io.TextIOWrapper, endereco_instrucao: str, vetor: list[str]) -> None:
    '''
    Função que realiza a interpretação da memória de forma a simular o ciclo do Computador IAS.
    '''
    # Registradores
    PC: str = endereco_instrucao
    AC: int = 0; MQ: int = 0;
    C: int = 0; Z: int = 0; R: int = 0
    MBR: str = ''; MAR: str = ''; IR: str = ''

    # Impressão dos valores iniciais
    print('\nValores Iniciais:')
    imprime_registradores(AC, MQ, C, Z, R, PC, MBR, MAR, IR)
    prox = input('\nPara a execução de cada instrução, aperte [ENTER]')

    while IR != 'END':
        if not prox:
            # Interpretação da instrução:
            MAR = PC
            MBR = leitura_memoria(memoria, int(MAR, 0))
            IR = MBR.split()[1]
            if len(MBR.split()) > 2:
                # Acesso ao endereço de memória
                if MBR.split()[2][0] == '(':
                    MAR = MBR.split()[2][1:-1]
                # Acesso à referência dada pelo vetor
                elif MBR.split()[2][0] == '*':
                    MAR = vetor[int(leitura_memoria(memoria, int(MBR.split()[2][1:-1], 0)).split()[1])]

            # Incrementando PC:
            PC = hex(int(PC, 0) + 1)

            # Execução da instrução:
            # Transferência de Dados
            if IR == 'LOAD':
                # Carregar no AC um valor de forma imediata
                C, AC = verifica_carry(int(MBR.split()[2]))
                Z = verifica_sinal(AC)

            if IR == 'LOAD_M':
                # Carregar no AC um valor da memória
                MBR = load(memoria, int(MAR, 0))
                C, AC = verifica_carry(int(MBR))
                Z = verifica_sinal(AC)
            
            elif IR == 'LOAD_-M':
                # Carregar no AC o oposto de um valor da memória
                MBR = load(memoria, int(MAR, 0))
                C, AC = verifica_carry(-int(MBR))
                Z = verifica_sinal(AC)
            
            elif IR == 'LOAD_MQ':
                # Carregar no AC o valor em MQ
                C, AC = verifica_carry(MQ)
                Z = verifica_sinal(AC)

            elif IR == 'LOAD_MQ_M':
                # Carregar no MQ um valor da memória
                MBR = load(memoria, int(MAR, 0))
                MQ = int(MBR)

            elif IR == 'STORE_M':
                # Guardar o valor de AC em um endereço de memória
                MBR = AC
                store(memoria, int(MAR, 0), int(MBR))

            # Aritmética de Dados
            elif IR == 'ADD':
                # Adicionar um valor ao AC de forma imediata
                AC = AC + int(MBR.split()[2])
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'ADD_M':
                # Adicionar ao AC um valor da memória
                MBR = load(memoria, int(MAR, 0))
                AC = AC + int(MBR)
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'SUB':
                # Subtrair do AC um valor de forma imediata
                AC = AC - int(MBR.split()[2])
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'SUB_M':
                # Subtrair do AC um valor da memória
                MBR = load(memoria, int(MAR, 0))
                AC = AC - int(MBR)
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'MUL':
                # Multiplicar o MQ com um valor de forma imediata
                MQ = MQ * int(MBR.split()[2])
                C, MQ = verifica_carry(MQ)

            elif IR == 'MUL_M':
                # Multiplicar o MQ com um valor da memória
                MBR = load(memoria, int(MAR, 0))
                MQ = MQ * int(MBR)
                C, MQ = verifica_carry(MQ)

            elif IR == 'DIV':
                # Dividir o AC por um valor de forma imediata
                R = AC % int(MBR.split()[2])
                AC = AC // int(MBR.split()[2])
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)

            elif IR == 'DIV_M':
                # Dividir o AC por um valor da memória
                MBR = load(memoria, int(MAR, 0))
                R = AC % int(MBR)
                AC = AC // int(MBR)
                C, AC = verifica_carry(AC)
                Z = verifica_sinal(AC)
            
            # Desvio
            elif IR == 'JUMP_M':
                # Desvio incondicional
                PC = MAR

            elif IR == 'JUMP_+M':
                # Desvio condicional; caso AC não seja negativo
                if AC >= 0:
                    PC = MAR

            # Fim das instruções
            elif IR == 'END':
                # Fim das instruções
                pass

            # Erro na Memória
            else:
                print('ERRO NA MEMÓRIA!')
            
            # Impressão de Registradores:
            imprime_registradores(AC, MQ, C, Z, R, PC, MBR, MAR, IR)

            # Continuar ciclo:
            prox = input('\nPara a execução da próxima instrução, aperte [ENTER]')

        else:
            prox = input('\nPara a execução da próxima instrução, aperte [ENTER]')
    return None

# Função que faz a leitura da memória ---------------------------------------------------------------------------------------

def leitura_memoria(memoria: io.TextIOWrapper, endereco: int) -> str:
    '''
    Realiza a leitura de um endereço de memória.
    '''
    memoria.seek(endereco * TAM_ENDERECO)
    leitura = memoria.readline().strip()
    if int(leitura[:4], 0) == endereco:
        return leitura
    else:
        return ''

# Funções que realizam as instruções ----------------------------------------------------------------------------------------

def load(memoria: io.TextIOWrapper, endereco: int) -> str:
    '''
    Instrução de carregamento de um valor no endereço fornecido em um registrador.
    '''
    leitura = leitura_memoria(memoria, endereco)
    if leitura:
        return leitura.split()[1]
    else:
        return '0'

def store(memoria: io.TextIOWrapper, endereco: int, dado: int) -> None:
    '''
    Instrução de armazenar um valor no endereço fornecido.
    '''
    memoria.seek(endereco * TAM_ENDERECO)
    if int(memoria.read(4), 0) == endereco:
        memoria.seek(endereco * TAM_ENDERECO + 5)
        memoria.write((str(dado) + ' ' * TAM_MAX_DADO)[:TAM_MAX_DADO] + '\n')
    return None

def verifica_sinal(reg: int) -> int:
    '''
    Função que verifica a polaridade de um registrador.
    '''
    if reg < 0:
        return -1
    elif reg == 0:
        return 0
    else:
        return 1

def verifica_carry(reg: int) -> tuple[int, int]:
    '''
    Função que verifica se houve Carry Out em um registrador.
    '''
    if len(str(reg)) > TAM_MAX_DADO:
        return 1, int(str(reg)[:TAM_MAX_DADO])
    else:
        return 2, reg

# Função que imprime os registradores ---------------------------------------------------------------------------------------

def imprime_registradores(ac: int, mq: int, c: int, z: int, r: int, pc: str, mbr: str, mar: str, ir: str) -> None:
    '''
    Função que imprime os registradores usados no ciclo de instrução.
    '''
    print('\nPC: ' + pc)
    print('MBR: ' + str(mbr) + ' | IR: ' + ir + ' | MAR: ' + mar )
    print('AC: ' + str(ac) + ' | MQ: ' + str(mq))
    print('C: ' + str(c) + ' | Z: ' + str(z) + ' | R: ' + str(r))
    return None

# Função que faz a formatação da memória processada -------------------------------------------------------------------------

def ajusta_memoria(memoria_aberta: io.TextIOWrapper, tamanho_endereco: int) -> io.TextIOWrapper:
    '''
    Formata o arquivo da memória para ser lido pelo simulador.
    '''
    memoria_ajustada = open('memoria_ajustada.ias', 'w+')
    linha = memoria_aberta.readline().strip()
    while linha:
        memoria_ajustada.write((linha + ' ' * (tamanho_endereco - 2))[:tamanho_endereco - 2] + '\n')
        linha = memoria_aberta.readline().strip()
    memoria_aberta.close()
    return memoria_ajustada

# Função que cria o vetor utilizado pelo ciclo ------------------------------------------------------------------------------
def cria_vetor_enderecos(tamanho: int) -> list[str]:
    '''
    Função que cria o vetor utilizado pelo ciclo, de forma a armazenar os endereços do vetor da memória.
    Vetor da memória começa sempre em 0x00 e é ocupado pelos espaços seguintes.
    '''
    vetor = []
    i = 0
    while i < tamanho:
        vetor.append(hex(i))
        i += 1
    return vetor

# Chamada da função principal ------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()