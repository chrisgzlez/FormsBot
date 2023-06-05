import psycopg2
import math
import os

def connectDataBase():
    contrasena = 123456789
    password = str(int((contrasena+16493476) // (math.sqrt(2)*math.sqrt(3)*math.sqrt(4)*math.sqrt(5)*math.sqrt(6)*math.sqrt(7)*math.sqrt(8))))

    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'adrian',
            password = password,
            database = 'forms'
        )

        print('Conexion exitosa con la base de datos')

        return connection
        
        
    except Exception as ex:
        print('Error al conectar con la base de datos: ' + str(ex))
        return None

def disconnectDataBase(connection):
    try:
        connection.close()
        print('Conexion cerrada')
    except Exception as ex:
        print(ex)

def saveFile(connection, path: str, table: str):
    cursor = connection.cursor()
    file_name = (table+'.csv')
    query = ("copy (select * from "+table+") to stdout with csv delimiter ';'")
    with open(os.path.join(path, file_name), 'w') as fp:
        cursor.copy_expert(query, fp)
    cursor.close()



def saveData(connection):
    try:
        path = r'/home/adrian/formsBot/DatosCSV'
        tables = ['personas', 'grupos', 'eventos', 'pasos', 'pertenecer', 'irevento']
        for table in tables:
            saveFile(connection, path, table)
        print('Datos guardados correctamente en csv')
    except Exception as ex:
        print('Error al guardar los datos: '+ex)