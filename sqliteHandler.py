import sqlite3


class sqliteHandler:
    
    def __init__(self):
        self.db = "db/pyranha_db"
    #----------------------------------------------------------------------
    #---CONEXION-----------------------------------------------------------
    #----------------------------------------------------------------------
    def connection(self):
        """Metodo que establece la conexion con la base de datos SQLITE """
        print "Iniciando conexion"
        self.con = sqlite3.connect(self.db)    
        self.cursor = self.con.cursor()
        print "Base de datos abierta correctamente..."
      
    def close_connection():
        """Metodo para cerrar la conexion de la base de datos"""
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
        "Metodo que retorna todas los Quick en forma de lista"
        self.cursor.execute('SELECT * FROM "main"."quick" ;')
        lista = self.cursor.fetchall()
        return lista
    
    def modify_quick(self, descrip, url):
        """Metod para modificar la url de un Quick, especificando tambien cual de ellos usando descrip """
        self.cursor.execute('UPDATE "main"."quick" set url ='+url+' where id_quick in (SELECT id_quick FROM "main"."quick" WHERE descrip ='+descrip+' );')
        self.con.commit()
    #----------------------------------------------------------------------
    
    def start(self):
        """Metodo que inicializa y establece la conexion con la base de datos """
        print "Iniciando handler de base de datos Sqlite"
        self.connection()