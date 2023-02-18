import dataBaseMenu
import bot
from dataBase import dataBase as db

if __name__ == "__main__":
    global connection
    connection = db.connectDataBase()

    if connection == None:
        print('Error al conectarse a la base de datos...')
        exit()

    while(1):
        print('1 - Ejecutar bot')
        print('2 - Gestion de base de datos')
        print('3 - Salir')
        op = input('Seleccione una opcion: ')
        if op == '1':
            bot.ejecutarBot(connection)
        elif op == '2':
            dataBaseMenu.menuBaseDatos(connection)
        elif op == '3':
            db.disconnectDataBase(connection)
            exit()
        else:
            print('Opcion incorrecta')
    
