
# todo: modularizar el codigo:
''' - funcion confirmar(mensajePregunta: str, mensajeRespuesta: str) -> bool
    - funcion pedir dni() -> str (DNI o None)...
    - funcion obtenerNombrePersona(dni: str) -> list[]'''

def transaction(func):
    def wrapper(*args, **kwargs):
        cursor = connection.cursor()
        cursor.execute('begin')
        check = func(*args, **kwargs)
        if check:
            cursor.execute('commit')
        else:
            cursor.execute('rollback') 
        return check
    return wrapper


def existePersona(dni: str) -> int:
    cursor = connection.cursor() 
    cursor.execute("select dni from personas where dni = %s", (dni,))
    rows = cursor.fetchall()
    return len(rows)

def existeGrupo(idGrupo: str) -> int:
    cursor = connection.cursor() 
    cursor.execute("select * from grupos")
    cursor = connection.cursor()
    rows = cursor.fetchall()
    return len(rows)

def isInGroup(dni: str, idGrupo: str) -> int:
    cursor = connection.cursor()
    cursor.execute("select * from pertenecer where persona = %s and grupo = %s", (dni, idGrupo))
    rows = cursor.fetchall()
    return len(rows)

def _insertarPersonaEnGrupo(dni: str, idGrupo: str):
    cursor = connection.cursor()
    cursor.execute("insert into pertenecer values(%s, %s)", (dni, idGrupo))
    cursor.execute("select nombre, apellido1, apellido2 from personas where dni = %s", (dni,))
    rows = cursor.fetchall()
    for row in rows:
        persona = row
    cursor.close()
    print(persona[0] + ' ' + persona[1]+ ' añadid@ correctamente al grupo con ID '+idGrupo)
    return


@transaction
def crearPersona() -> str:
    while(1):
        dni = input('DNI: ')
        if existePersona(dni):
            print('Ya existe una persona con ese DNI\n')
        elif dni.upper() == 'NULL' or dni=='':
            print('La clave primaria DNI no puede ser NULL')
        else:
            break
    nombre = input('Nombre: ')
    apellido1 = input('Primer apellido: ')
    apellido2 = input('Segundo apellido: ')
    email = input('Email: ')
    instagram = input('Instagram: ')
    telefono = input('Telefono: ')
    datos = [nombre, apellido1, apellido2, email, instagram, telefono]

    for i in range(len(datos)): # para poner un dato a null tiene que ser = None
        if datos[i].upper() == 'NULL' or datos[i]  == '': # si escribimos null lo convierte a None
            datos[i] = None

    while(1):
        confirmar = input('Confirmar la creación de esta persona? [y/n]: ').upper()
        if confirmar == 'Y' or confirmar == 'S' or confirmar == 'YES' or confirmar == 'SI':
            cursor = connection.cursor()
            cursor.execute("insert into personas values(%s, %s, %s, %s, %s, %s, %s)", (dni, *datos)) # unpacking de datos
            print('Persona creada correctamente')
            return dni
        elif confirmar == 'N' or confirmar == 'NO':
            print('Cambios no guardados')
            return None
        else:
            print('Opcion incorrecta')

@transaction
def crearGrupo() -> str:
    while(1):
        op = input('¿El titular del grupo existe ya? [y/n]: ').upper()
        if op == 'Y' or op == 'S' or op == 'YES' or op == 'SI':
            op = 'Y'
            while(1):
                dni = input('DNI del titular del grupo: ')
                if existePersona(dni):
                    break
                else:
                    print('No existe una persona con ese DNI')
            idGrupo = input('ID del grupo: ')
            break
                
        elif op == 'N' or op == 'NO':
            op = 'N'
            print('Creando nueva persona para ser titular...')
            dni = crearPersona()
            idGrupo = input('ID del grupo: ')
            break

        else:
            print('Opcion incorrecta')

    cursor = connection.cursor()
    cursor.execute('select nombre, apellido1, apellido2 from personas where dni = %s', (dni,))
    rows = cursor.fetchall()
    for row in rows:
        persona = row

    while(1):
        confirmar = input('¿Desea confirmar la creación de un grupo con ID \''+idGrupo+'\' cuyo titular es \''+persona[0]+' '+persona[1]+ '\' ? [y/n]: ').upper()
        if confirmar == 'Y' or confirmar == 'S' or confirmar == 'YES' or confirmar == 'SI':
            cursor = connection.cursor()
            cursor.execute("insert into grupos values(%s, %s)", (idGrupo, dni))
            cursor.execute("insert into pertenecer values(%s, %s)", (dni, idGrupo))
            print('Creacion de grupo realizada correctamente')
            return idGrupo
        elif confirmar == 'N' or confirmar == 'NO':
            print('Cambios no guardados')
            return None
        else:
            print('Opcion incorrecta')
        
    return 

@transaction
def insertarPersonasExistentes():
    while(1):
        idGrupo = input('Inserte el ID del grupo en el que desee insertar las personas: ')
        if not existeGrupo(idGrupo):
            print('No existe ningun grupo con ese ID')
            op = input('Pulse \'S\' para volver al menu o cualquier otra tecla para introducir otro ID: ').upper()
            if op == 'S':
                return
        else:
            break
            
    while(1):
        dni = input('Introduzca el DNI de la persona que desea insertar en el grupo: ')
        if not existePersona(dni):
            print('La persona con DNI '+dni+' no existe')
            op2 = input('Pulse \'S\' para volver al menu o cualquier otra tecla para introducir otro DNI: ').upper()
            if op2 == 'S':
                return
            else:
                continue
        
        elif isInGroup(dni, idGrupo):
            cursor = connection.cursor()
            cursor.execute("select nombre, apellido1, apellido2 from personas where dni = %s", (dni,))
            rows = cursor.fetchall()
            for row in rows:
                persona = row
            cursor.close()
            print(persona[0] + ' ' + persona[1]+ ' ya esta en el grupo')
            op2 = input('Pulse \'S\' para volver al menu o cualquier otra tecla para introducir otro DNI: ').upper()
            if op2 == 'S':
                return
            else:
                continue
        else:
            cursor = connection.cursor()
            cursor.execute("insert into pertenecer values(%s, %s)", (dni, idGrupo))
            cursor.execute("select nombre, apellido1, apellido2 from personas where dni = %s", (dni,))
            rows = cursor.fetchall()
            for row in rows:
                persona = row
            cursor.close()
            print(persona[0] + ' ' + persona[1]+ ' añadid@ correctamente al grupo con ID '+idGrupo)


@transaction
def insertarPersonasNuevas():
    while(1):
        idGrupo = input('Inserte el ID del grupo en el que desee insertar las personas: ')
        if not existeGrupo(idGrupo):
            print('No existe ningun grupo con ese ID')
            op = input('Pulse \'S\' para volver al menu o cualquier otra tecla para introducir otro ID: ').upper()
            if op == 'S':
                return
        else:
            break
    
    dni = crearPersona()

    if dni == None:
        return

    cursor = connection.cursor()
    cursor.execute("insert into pertenecer values(%s, %s)", (dni, idGrupo))
    cursor.execute("select nombre, apellido1, apellido2 from personas where dni = %s", (dni,))
    rows = cursor.fetchall()
    for row in rows:
        persona = row
    cursor.close()

    while(1):
        confirmar = input('Desea insertar a ' +persona[0] +' '+ persona[1]+' en el grupo con ID '+idGrupo+'? [y/n]: ').upper()
        if confirmar == 'Y' or confirmar == 'S' or confirmar == 'YES' or confirmar == 'SI':
            _insertarPersonaEnGrupo(dni, idGrupo)
            return
        elif confirmar == 'N' or confirmar == 'NO':
            print('Cambios no guardados')
            return
        else:
            print('Opcion incorrecta')



@transaction
def crearEvento():
    pass

@transaction
def irGrupo():
    pass

def listarPersonas():
    cursor = connection.cursor()
    cursor.execute('select * from personas')
    rows = cursor.fetchall()
    if len(rows) == 0:
        print('No existen personas en la base de datos...')
        return
    for row in rows:
        print(row)
    return

def listarGrupos():
    cursor = connection.cursor()
    cursor.execute('select * from grupos')
    rows = cursor.fetchall()
    if len(rows) == 0:
        print('No existen grupos en la base de datos...')
        return
    for row in rows:
        print(row)
    return

@transaction
def borrarPersona() -> bool:
    while(1):
        dni = input('DNI de la persona que desea eliminar: ')
        if not existePersona(dni):
            print('No existe una persona con ese DNI')
            op = input('Pulse \'S\' para salir o cualquier otra tecla para introducir otro dni: ').upper()
            if op == 'S':
                return
        else:
            while(1):
                cursor = connection.cursor()
                cursor.execute('select nombre, apellido1, apellido2 from personas where dni = %s', (dni,))
                rows = cursor.fetchall()
                for row in rows:
                    persona = row
                confirmar = input('Desea eliminar a '+persona[0]+ ' '+persona[1]+' ' +persona[2]+' de la base de datos? [y/n]: ').upper()
                if confirmar == 'Y' or confirmar == 'S' or confirmar == 'YES' or confirmar == 'SI':
                    cursor.execute('delete from personas where dni = %s', (dni,))
                    print(persona[0]+ ' '+persona[1]+' ' +persona[2]+' eliminad@ correctamente de la base de datos')
                    return True
                elif confirmar == 'N' or confirmar == 'NO':
                    print('Cambios no guardados')
                    return False
                else:
                    print('Opcion incorrecta')
            break

@transaction
def borrarGrupo() -> bool:
    while(1):
        idGrupo = input('ID del grupo que desea eliminar: ')
        if not existeGrupo(idGrupo):
            print('No existe un grupo con ese ID')
            op = input('Pulse \'S\' para salir o cualquier otra tecla para introducir otro ID: ').upper()
            if op == 'S':
                return
        else:
            while(1):
                cursor = connection.cursor()
                cursor.execute('select nombre, apellido1, apellido2 from grupos as g inner join personas as p on (g.titular = p.dni) where g.id = %s', (idGrupo,))
                rows = cursor.fetchall()
                for row in rows:
                    persona = row
                confirmar = input('Desea eliminar al grupo cuyo ID es '+idGrupo+' y su titular es '+persona[0]+ ' '+persona[1]+' de la base de datos? [y/n]: ').upper()
                if confirmar == 'Y' or confirmar == 'S' or confirmar == 'YES' or confirmar == 'SI':
                    cursor.execute('delete from grupos where id = %s', (idGrupo,))
                    print('Grupo con ID \''+idGrupo+'\' eliminad@ correctamente de la base de datos')
                    return True
                elif confirmar == 'N' or confirmar == 'NO':
                    print('Cambios no guardados')
                    return False
                else:
                    print('Opcion incorrecta')
            break


def verInfoGrupo():
    while(1):
        idGrupo = input('ID del grupo: ')
        if not existeGrupo(idGrupo):
            print('No existe un grupo con ID '+idGrupo)
            op = input('Pulse \'S\' para salir o cualquier otra tecla para introducir otro ID: ').upper()
            if op == 'S':
                return
            break
            
    cursor = connection.cursor()
    cursor.execute("select p2.dni, p2.nombre, p2.apellido1, p2.apellido2, p2.email, p2.instagram, p2.telefono from pertenecer as p inner join personas as p2 on (p2.dni = p.persona) where p.grupo = %s", (idGrupo,))
    print('\n')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return

def verInfoPersona():
    dni = input('DNI de la persona: ')
    cursor = connection.cursor()
    cursor.execute("select * from personas as p where p.dni = %s", (dni,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return



def menuBaseDatos(conn):
    global connection
    connection = conn    
    while(1):
        print('\n\n-----------------------------------------------------------------------')
        print('A - Crear persona')
        print('B - Borrar persona')
        print('C - Listar personas')
        print('D - Ver info de persona\n')

        print('E - Crear grupo')
        print('F - Borrar grupo')
        print('G - Listar grupos')
        print('H - Insertar personas existentes en grupos')
        print('I - Insertar personas nuevas en grupos')
        print('J - Ver info de grupo\n')

        print('K - Crear evento')
        print('L - Ir grupo a evento\n')

        print('S - Salir\n')

        opcion = input('Seleccione una opcion: ').upper()
        print('\n')

        if opcion == 'A':
            crearPersona()
        elif opcion == 'B':
            borrarPersona()
        elif opcion == 'C':
            listarPersonas()
        elif opcion == 'D':
            verInfoPersona()

        elif opcion == 'E':
            crearGrupo()
        elif opcion == 'F':
            borrarGrupo()
        elif opcion == 'G':
            listarGrupos()
        elif opcion == 'H':
            insertarPersonasExistentes()
        elif opcion == 'I':
            insertarPersonasNuevas()
        elif opcion == 'J':
            verInfoGrupo()

        elif opcion == 'K':
            crearEvento()
        elif opcion == 'L':
            irGrupo()

        elif opcion == 'S':
            print('Volviendo al menu principal...')
            break
        else:
            print('Opcion incorrecta')
        print('-----------------------------------------------------------------------')
    return
    

