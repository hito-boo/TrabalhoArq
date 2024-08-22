oiee = open('novo.ias', 'wt')

i = 0
while i < 246:
    hexa = hex(i)
    oiee.write(hexa.split(sep='x')[0] + 'x' + hexa.split(sep='x')[1].upper() + ' \n')
    i += 1

oiee.close()