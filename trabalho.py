import io

def main() -> None:
    nome_arq = input('\nDigite o nome do arquivo que representa a memória: ')
    endereco = int((input('\nDigite o endereço da primeira instrução do programa: ')), 0)
    try:
        memoria = open(nome_arq, 'r+')
    except:
        print("ERRO: Arquivo de memória não encontrado.")
    else:
        ciclo_ias(memoria, endereco)
        memoria.close()
    return None

def ciclo_ias(memoria: io.TextIOWrapper, endereco: int) -> None:
    # Registradores 
    AC: int
    MQ: int
    PC: int
    MBR: int
    MIR: int
    MAR: int
    IR: int

    # Buscando o endereço da primeira instrução.
    ...

    # Interpretar a instrução, executar instrução e incrementar PC.
    ...

    # Imprimindo os registradores.
    ...

    return None

def load_ac(endereco: int, memoria: io.TextIOWrapper) -> int:
    memoria.seek(0)
    leitura = memoria.readline().split()
    endereco_atual = int(leitura[0], 0)
    dado = int(leitura[1])
    while endereco_atual != endereco:
        leitura = memoria.readline().split()
        endereco_atual = int(leitura[0], 0)
        dado = int(leitura[1])
    return dado

def add_ac(ac: int, endereco: int, memoria: io.TextIOWrapper) -> int:
    memoria.seek(0)
    leitura = memoria.readline().split()
    endereco_atual = int(leitura[0], 0)
    dado = int(leitura[1])
    while endereco_atual != endereco:
        leitura = memoria.readline().split()
        endereco_atual = int(leitura[0], 0)
        dado = int(leitura[1])
    return ac + dado

def sub_ac(ac: int, endereco: int, memoria: io.TextIOWrapper) -> int:
    memoria.seek(0)
    leitura = memoria.readline().split()
    endereco_atual = int(leitura[0], 0)
    dado = int(leitura[1])
    while endereco_atual != endereco:
        leitura = memoria.readline().split()
        endereco_atual = int(leitura[0], 0)
        dado = int(leitura[1])
    return ac - dado

def store(ac: int, endereco: int, memoria: io.TextIOWrapper) -> None:
    memoria.seek(0)
    offset = memoria.tell()
    endereco_atual = memoria.readline().split()[0]
    while endereco_atual != endereco:
        offset = memoria.tell()
        endereco_atual = memoria.readline.split()[0]
    memoria.seek(offset + 5)
    memoria.write(ac)
    # Tratar o tamanho do dado (adicionar espaço branco depois quando necessário)
    return None

if __name__ == '__main__':
    main()