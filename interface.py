'''
crear grupo (con personas existentes o no)
crear evento
ir a evento
listar personas
listar grupos
'''

from dataBase import dataBase as db

def existePersona(dni: str):
    cursor = connection.cursor() 
    cursor.execute("select dni from personas where dni = %s", (dni,))
    rows = cursor.fetchall()
    return len(rows)

#dni, nombre, apellido1, apellido2, email, instagram, telefono
#todo: tener en cuenta que el usuario puede querer poner a null un dato
def crearGrupo():
    while(1):
        op = input('¿El titular del grupo existe ya? [y/n] ').upper()
        if op == 'Y' or op == 'S' or op == 'YES' or op == 'SI':
            while(1):
                dni = input('DNI del titular del grupo: ')
                if existePersona(dni):
                    break
                else:
                    print('No existe una persona con ese DNI')
            idGrupo = input('ID del grupo: ')
            break
                
        elif op == 'N' or op == 'NO':
            print('Creando nueva persona para ser titular...')
            while(1):
                dni = input('DNI: ')
                if existePersona(dni):
                    print('Ya existe una persona con ese DNI')
                else:
                    break
            nombre = input('Nombre: ')
            apellido1 = input('Primer apellido: ')
            apellido2 = input('Segundo apellido: ')
            email = input('Email: ')
            instagram = input('Instagram: ')
            telefono = input('Telefono: ')
            idGrupo = input('ID del grupo: ')
            break

        else:
            print('Opcion incorrecta')

    while(1):
        confirmar = input('¿Desea confirmar la creación de un grupo con ID \''+idGrupo+'\' cuyo titular tiene el DNI \''+dni+'\'? [y/n] ').upper()
        if confirmar == 'Y' or confirmar == 'S' or confirmar == 'YES' or confirmar == 'SI':
            #todo: falta meter la persona en el grupo
            print('Creacion de grupo realizada correctamente')
            break
        elif confirmar == 'N' or confirmar == 'NO':
            print('Cambios no guardados')
            break
        else:
            print('Opcion incorrecta')
        
    return 

def insertarPersonasExistentes():
    pass

def insertarPersonasNuevas():
    pass

def crearEvento():
    pass

def irGrupo():
    pass

def listarPersonas():
    pass

def listarGrupos():
    pass



connection = db.connectDataBase()       
while(1):
    print('\n\nA - Crear grupo')
    print('B - Insertar personas existentes en grupos')
    print('C - Insertar personas nuevas en grupos')
    print('D - Crear evento')
    print('E - Ir grupo a evento')
    print('F - Listar personas')
    print('G - Listar grupos')
    print('S - Salir')
    opcion = input('Seleccione una opcion: ').upper()
    print('\n')

    if opcion == 'A':
        crearGrupo()
    elif opcion == 'B':
        insertarPersonasExistentes()
    elif opcion == 'C':
        insertarPersonasNuevas()
    elif opcion == 'D':
        crearEvento()
    elif opcion == 'E':
        irGrupo()
    elif opcion == 'F':
        listarPersonas()
    elif opcion == 'G':
        listarGrupos()
    elif opcion == 'S':
        db.disconnectDataBase(connection)
        exit()
    else:
        print('Opcion incorrecta')
    

