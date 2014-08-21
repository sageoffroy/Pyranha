from sqliteHandler import *

class predict:
    def __init__(self):
        self.sql = sqliteHandler()


    def dictToList(self,dic,subword):
        """Metodo que retorna en una lista los valores """
        li = list()
        if subword != '':
            for d in dic.iteritems():
                if d[0].startswith(subword):
                    li.append(d)
        else:
            li = list(dic.items())
        return li
    
    def getPodium(self,li):
        return li[:3]
    
    def prediction(self,subword):
        """Metodo que retorna las palabras que coinciden con el comienzo de la subpalabra, ordenadas
        por el criterio de "mas utilizada" a "menos utilizada" """
        self.sql.start()
        dic = self.sql.get_dic()#diccionario 'completo' de la rae, no ordenado
        li = list()
        result = list()
        subword = str(subword).lower()
        li = self.dictToList(dic,subword)
        li = sorted(li, key=lambda score: score[1], reverse=True)#ordena las palabras por valor
        li = self.getPodium(li)
        
        self.sql.close_connection()#cierra conexion sql
        for l in li:
            result.append(l[0])
        return result