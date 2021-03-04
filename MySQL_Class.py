import mysql.connector
import DBConfig

class MySQL():
    # ---------------------------------------------------------
    def connect(self):

        conn = mysql.connector.connect(**DBConfig.dbConfig)

        # Crear Cursor
        cursor = conn.cursor()

        # Retornar Coneccion y Cursor
        return conn, cursor
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    def close(self, cursor, conn):
        # Cerrar el cursor
        cursor.close()

        # Cerrar coneccion con MySQL
        conn.close()
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    def insertdata(self, alarma):

        # Conectar con MySQL
        conn, cursor = self.connect()

        # Insertar los datos
        cursor.execute("INSERT INTO parpadeos (id,alarma) VALUES ({},{})".format("NULL",alarma))

        conn.commit()

        # Cerrar el cursor y la coneccion
        self.close(cursor,conn)
    # ---------------------------------------------------------
    def ConsultData(self):
        # connect to MySQL
        conn, cursor = self.connect()   
            
        # execute command
        cursor.execute("select * from parpadeos order by id desc limit 1;")
        respuesta = cursor.fetchall()

        # close cursor and connection
        self.close(cursor, conn) 

        return respuesta

