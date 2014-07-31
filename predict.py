from sqliteHandler import *

class predict:
    def __init__(self):
        self.sql = sqliteHandler()

    def prediction(self,subword):
        """Metodo que retorna las palabras que coinciden con el comienzo de la subpalabra, ordenadas
        por el criterio de "mas utilizada" a "menos utilizada" """
	self.sql.start()
	dic = self.sql.get_dic()
	li = list()
	result = list()
	for d in dic.iteritems():
	    if d[0].startswith(subword):
		li.append(d)
	li.sort(reverse=True)
	self.sql.close_connection()
	for l in li:
	    result.append(l[0])
        return result


