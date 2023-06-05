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
        print('A - Ejecutar bot')
        print('B - Gestion de base de datos')
        print('S - Salir')
        op = input('Seleccione una opcion: ').upper()
        if op == 'A':
            while(1):
                print('\n\nDonde va a estar el link?')
                print('A - Link en stories')
                print('B - Link en la bio')
                link = input('Seleccione una opcion: ').upper()
                if link=='A' or link=='B':
                    print('\n\n')
                    break
                else:
                    print('Opcion incorrecta')
            bot.ejecutarBot(connection, link)
        elif op == 'B':
            dataBaseMenu.menuBaseDatos(connection)
        elif op == 'S':
            db.saveData(connection)
            db.disconnectDataBase(connection)
            exit()
        else:
            print('Opcion incorrecta')
    
