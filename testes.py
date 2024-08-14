import io

teste = open('testes.ias', 'r+')

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

print(load_ac(1, teste))

teste.close()