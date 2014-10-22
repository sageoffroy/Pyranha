import sqlite3


class PyranhaSqliteHandler:
    
    def __init__(self):
        print("Pyranha Sqlite Handler: iniciando base de datos")
        self.db = "db/pyranha_db"
    #----------------------------------------------------------------------
    #---CONEXION-----------------------------------------------------------
    #----------------------------------------------------------------------
    """Metodo que establece la conexion con la base de datos SQLITE """
    def open_connection(self):
        print "Iniciando conexion"
        print("Pyranha Sqlite Handler - connection: conectando a la base de datos")
        self.con = sqlite3.connect(self.db)    
        self.cursor = self.con.cursor()
        print("Pyranha Sqlite Handler - connection: base de datos abierta correctamente")
      
    """Metodo para cerrar la conexion de la base de datos"""
    def close_connection(self):
        self.con.close()
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    #---FAVORITE-----------------------------------------------------------
    #----------------------------------------------------------------------
    def add_favorite(self,url,descrip):
        """Metodo para agregar favoritos """
        self.cursor.execute('INSERT INTO "main"."favorites" (url,descrip) VALUES ('+url+', '+descrip+');')
        self.con.commit()
        print "Almacenado favorito.."
    
    def get_favorites(self):
        """Metodo que retorna todos los favoritos que cargo el usuario en forma de lista"""
        self.cursor.execute('SELECT * FROM "main"."favorites" ;')
        lista = self.cursor.fetchall()
        return lista
      
        
    def remove_favorite(self, id, url):
        """Metodo que borra de la base de datos la ocurrencia de un favorito que coincida con el id especificado """
        self.cursor.execute('DELETE FROM "main"."favorites" WHERE id_fav = '+id+';')
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    #---QUICK--------------------------------------------------------------
    #----------------------------------------------------------------------
    def modify_quick(self, id, descrip, url):
        """Metodo para modificar un favorito """
        if descrip == '':
            self.cursor.execute('UPDATE "main"."favorites" set url ='+url+' where id_fav ='+id+';')
        else:
            self.cursor.execute('UPDATE "main"."favorites" set url ='+url+', descrip ='+descrip+' where id_fav ='+id+';')
        self.con.commit()
        
    def get_quick(self):
        """Metodo que retorna todas los Quick en forma de lista"""
        self.cursor.execute('SELECT descrip, url FROM "main"."quick" ;')
        lista = self.cursor.fetchall()
        return lista
    
    def modify_quick(self, descrip, url):
        """Metodo para modificar la url de un Quick, especificando tambien cual de ellos usando descrip """
        self.cursor.execute('UPDATE "main"."quick" set url ='+url+' where id_quick in (SELECT id_quick FROM "main"."quick" WHERE descrip ='+descrip+' );')
        self.con.commit()
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    #---DIC----------------------------------------------------------------
    #----------------------------------------------------------------------
    def get_dic(self):
        """Metodo que retorna todo el diccionario"""
        result = self.cursor.execute('SELECT word,value FROM "main"."dic" ;')
        result = result.fetchall()
        dic = dict(result)
        return dic

    def update_dic(self, word):
        """Metodo que actualiza el valor de las palabras del diccionario"""
        oldvalue = self.cursor.execute('SELECT value FROM "main"."dic" WHERE word ='+word+';')
        newvalue = oldvalue.fetchone()
        newvalue = newvalue[0]+1
        self.cursor.execute('UPDATE "main"."dic" SET value ='+newvalue+' WHERE word ='+word+' ;')
        self.con.commit()
        
    #----------------------------------------------------------------------
    
    def start(self):
        """Metodo que inicializa y establece la conexion con la base de datos """
        print "Iniciando handler de base de datos Sqlite"
        self.open_connection()
