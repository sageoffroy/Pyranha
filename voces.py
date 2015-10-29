# -*- encoding: utf-8 -*-
from vox import Vox

COMANDOS = ['inicio','pesta','detener','recarga']

voz = Vox()
voz.record(3)
rta = voz.voz_a_texto()
exit = False
#print rta
for r in rta:
    for c in COMANDOS:
        if c in r:
            exit = True
            if c == 'pesta':
                print "Ejecutando comando: Pestaña"
            else:
                print "Ejecutando comando: " + c
            break

    if exit:
        break
