import dataBaseMenu
import bot
from dataBase import dataBase as db

# !HAY QUE CERRAR EL CONNECTION.CURSOR() CADA VEZ QUE SE CREA UNO
if __name__ == "__main__":
    global connection
    connection = db.connectDataBase()

    if connection == None:
        print('Error al conectarse a la base de datos...')
        exit()

    while(1):
        print('A - Ejecutar bot')
        print('B - Gestion de base de datos')
        print('S - Salir')
        op = input('Seleccione una opcion: ').upper()
        if op == 'A':
            bot.ejecutarBot(connection)
        elif op == 'B':
            dataBaseMenu.menuBaseDatos(connection)
        elif op == 'S':
            db.saveData(connection)
            db.disconnectDataBase(connection)
            exit()
        else:
            print('Opcion incorrecta')
    
