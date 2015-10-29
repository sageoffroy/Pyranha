
def a(s,l):
    x = list()
    for e in l:
        if e.lower().startswith(s.lower()):
	    x.append(e)
    x.sort()
    return x



li = ['Abanico', 'Alo', 'Barco', 'Bueno', 'Zanahoria','buenos','Bullying']

li.sort()

sub = 'Bue'
subx=''
lix = li

for s in sub:
    subx = subx+s
    print("--------INICIO------")
    lix = a(subx,li)
    print lix
    li = lix
    print("--------FIN---------")

