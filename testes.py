import io

teste = open('teste.ias', 'r+')

endereco = '0x0F'

def load(memoria: io.TextIOWrapper, endereco: int) -> str:
    memoria.seek(endereco * 23)
    leitura = memoria.readline().strip()
    if int(leitura[:4], 0) == endereco:
        return leitura
    else:
        return ''

def store(memoria: io.TextIOWrapper, endereco: int, dado: int) -> None:
    memoria.seek(endereco * 23)
    if int(memoria.read(4), 0) == endereco:
        memoria.seek(endereco * 23 + 5)
        memoria.write(trata_tam_dado(dado))
    return None

def trata_tam_dado(dado: int) -> str:
    return (str(dado) + ' ' * 16)[:16] + '\n'

store(teste, int(endereco, 0), 99999999999999999999999999999999999999999)

teste.close()