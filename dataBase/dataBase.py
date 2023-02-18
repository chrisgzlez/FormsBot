import psycopg2
import math

def connectDataBase():
    contrasena = 123456789

    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = str(int((contrasena+16493476) // (math.sqrt(2)*math.sqrt(3)*math.sqrt(4)*math.sqrt(5)*math.sqrt(6)*math.sqrt(7)*math.sqrt(8)))),
            database = 'forms'
        )

        print('Conexion exitosa con la base de datos')

        return connection
        
        
    except Exception as ex:
        print('Error al conectar con la base de datos: ' + ex)
        return None

def disconnectDataBase(connection):
    try:
        connection.close()
        print('Conexion cerrada')
    except Exception as ex:
        print(ex)





    '''if itemTitle == const.NOMBRE:
        cursor.execute("select nombre from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i where i.evento = 'inventado'")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return 'a' '''

'''connection = connectDataBase()
cursor = connection.cursor()
idEvento = '\'inventado\''
cursor.execute("select nombre from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = " + idEvento + " and p.dni = g.titular")
rows = cursor.fetchall()
prueba = ''
for row in rows:
    prueba+=str(row)
print(prueba.replace('\'', '').replace('(', '').replace(')', '').replace(',', ', ')[:-2])
disconnectDataBase(connection)'''