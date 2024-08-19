old = open('testes_old.ias', 'r')
novo = open('teste.ias', 'w')

linha = old.readline().strip()
while linha:
    novo.write((linha + ' ' * 21)[:21] + '\n')
    linha = old.readline().strip()

old.close()
novo.close()