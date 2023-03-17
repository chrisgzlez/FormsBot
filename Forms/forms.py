"""
AUTORES:
    Adrian Martinez Balea
    Cristian Novoa Gonzalez
VERSION: 0.5
FECHA CREACION: 5/10/2022

"""

""" IMPORTS """
# Navigate the Website
from tokenize import String
from selenium.webdriver.common.by import By  # used to select web elements

# Used to interact with elements
# indicates state of web element
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # used to wait for condition
from selenium.webdriver.remote.webelement import WebElement  # WebElement class

import re
import time
# Want to use time library to check execution times and look for the fastest way

from . import constantes as const

## STATUS: WORKING
def autoCompleteShortAnswer(driver: WebElement, xpath: str, itemTitle: str):
    # cambiado el tiempo de espera
    input = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, f'{xpath}//input')))

    if (input == None):
        print("Este tipo no era, saliendo")
        raise Exception

    input.clear()
    input.click()
    entrada = getInput(itemTitle)
    input.send_keys(entrada)
    print('Respuesta: '+str(entrada))
    return

## TODO: Cambiar los 'String' por 'str' estamos malitos
## TODO: Añadir type 'connection' a los parametros connection
## TODO: Quiza cambiar parametro connection a conn
## TODO: Use context wraps with teh connection?? (usando 'with')
## STATUS: HAS NOT BEING TESTED, BUT SHOULD WORK
def autoCompleteTextArea(driver: WebElement, xpath: str, itemTitle: str):
    input = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, f'{xpath}//textarea')))
    
    if (input == None):
        print("Este tipo no era, saliendo")
        raise Exception
        
    input.clear()
    input.click()
    entrada = getInput(itemTitle)
    print('Respuesta: '+str(entrada))
    input.send_keys(entrada)
    return

## TODO: Empaquetar los argumentos y desempaquetarlos posteriormente? Ya que hay tantos??
## TODO: Cambiar 'apaño'
## TODO: Añadir excepciones a los autocomplete individuales más concretas y raisearlar
## TODO: Mejor excepciones
## TODO: AÑADIR ARGUMENTOS NECESARIOS AL RESTO DE FUNCIONES
## WORK IN PROGRESS
def autoCompleteField(driver: WebElement, xpath: String, itemTitle: str, evento: str, conn):
    global connection
    connection = conn

    global idEvento
    idEvento = evento
    """We try different types of input types until we find the right one

    Args:
        driver (WebElement): chromedriver with the webpage
        xpath (String): xpath of the current item
        itemTitle (str): its label
        idEvento (str): event identifier for the database
        connection (_type_): connection to the database
    """
    try:
        autoCompleteShortAnswer(driver, xpath, itemTitle)
    except Exception:
        try:
            autoCompleteTextArea(driver, xpath, itemTitle)
        except Exception:
                try:
                    autoCompleteCheckBox(driver, xpath, itemTitle)
                except Exception:
                    try:
                        autoCompleteRadial(driver, xpath, itemTitle)
                    except Exception:
                        try:
                            autoCompleteDropDown(driver, xpath, itemTitle)
                        except Exception as ex:
                            print(ex)

    return                                                                                                                                                                                                                  



## STATUS: WORKING
## TODO: Gestionar numero entradas / personas
def autoCompleteCheckBox(driver: WebElement, xpath: String, itemTitle: str):
    div = driver.find_element(By.XPATH, f'{xpath}//*[@role="list"]')
    labels = div.text.split("\n")
    print(f'Labels: {labels}')

    entrada = getInput(itemTitle)
    print(entrada)
    indexOfRightEntry = labels.index(str(entrada))

    checkboxes = driver.find_elements(By.XPATH, f'{xpath}//*[@role="list"]/*[@role="listitem"]//*[@role="checkbox"]')
    
    entrada = getInput(itemTitle)
    indexOfRightEntry = labels.index(str(entrada))

    if (indexOfRightEntry == ValueError):
        """checkboxes[-1].click()
        input = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, f'{xpath}//input')))

        if (input == None):
            print("Este tipo no era, saliendo")
            raise Exception

        input.clear()
        input.click()
        entrada = getInput(itemTitle, idEvento, connection)
        input.send_keys(entrada)

        ## Esto tendría un pequeno espacio de texto, haberia que pasarlle un novo path 
        ## e usar a función de autocompleteShortAnswer
        ##autocompleteShortAnswer(driver, newXpath, itemTitle, idEvento, connection)"""
        return
    else:
        checkboxes[indexOfRightEntry].click()  # deberia de valer
        print('Respuesta: '+str(entrada))
    
    return

## STATUS: NEEDS UPDATE
def autoCompleteDropDown(driver: WebElement, xpath: String, itemTitle: str):
  
    wait = WebDriverWait(driver,1)

    # Click in the dropdown option to show the options
    pagination = wait.until(EC.element_to_be_clickable((By.XPATH, f'{xpath}//*[@role="listbox"]')))
    pagination.click()

    # We wait until the options are loaded
    wait.until(EC.element_to_be_clickable((By.XPATH,f'{xpath}//*[@role="listbox"]/*[@role="presentation"][2]/*[@role="option"]')))
    
    # we exclude the first one (index 0) because it is repeated
    labels = pagination.text.split("\n")

    entrada = getInput(itemTitle)
    indexOfRightEntry = labels.index(str(entrada))
    if (indexOfRightEntry == ValueError):
        return


    # WE CLICK THE OPTION THAT WE LIKE
    # HERE WE ARE GETTING THE 2nd OPTION (The index starts at 1, not 0)
    option = driver.find_element(By.XPATH,f'{xpath}//*[@role="listbox"]/*[@role="presentation"][2]/*[@role="option"][{indexOfRightEntry}]')
    option.click()
    print('Respuesta: '+str(entrada))
    time.sleep(1) ## Necesario para no clickar fuera
    return

# STATUS: WORKING
# todo: añadir campo otro
def autoCompleteRadial(driver: WebElement, xpath: str, itemTitle: str):
    div = driver.find_element(By.XPATH, f'{xpath}//*[@role="radiogroup"]')
    labels = div.text.split("\n")
    print(f'Labels: {labels}')


    ###
    entrada = getInput(itemTitle)
    print(entrada)
    indexOfRightEntry = labels.index(str(entrada))

    radios = driver.find_elements(By.XPATH, f'{xpath}//*[@role="radiogroup"]//*[@role="radio"]')

    
    entrada = getInput(itemTitle)
    indexOfRightEntry = labels.index(str(entrada))

    if (indexOfRightEntry == ValueError):
        radios[-1].click()
        ## Esto tendría un pequeno espacio de texto, haberia que pasarlle un novo path 
        ## e usar a función de autocompleteShortAnswer
        ##autocompleteShortAnswer(driver, newXpath, itemTitle, idEvento, connection)
    else:
        print('Respuesta: '+str(entrada))
        radios[indexOfRightEntry].click()  # deberia de valer
    return


"""
    @param driver: WebElement in which we want to look for the button
    @param button_name: The name of the button we want to look for
    @param searchBy: tuple -> (Selector: By.SELECTOR, value: str)
    @param searchBy: needs to be unpacked to find_elements()
    @return: The WebElement button we looked for
"""
def findButton(driver: WebElement, button_name: str, searchBy: tuple) -> WebElement:
    # Find all the buttons in the WebElement
    buttons = driver.find_elements(*searchBy)  # We unpack searchBy here
    # Iterate through all the buttons until we find the one we want
    for button in buttons:
        if (button.text == button_name):
            send_button = button
            break
    return send_button






## TODO: TODO DE AQUÍ PARA ABAJO EN SU PROPIO ARCHIVO??
"""
badCharacters = set([" ", ":", "-", "~", "|", ";", "(", ")", "[", "]"])

# Cambiar, usar regex, que solo coja characters [A-Z], [a-z]
def filterBadCharacters(char: str) -> bool:
    return not char in badCharacters

# Mirar re.escape 
def preProcessLabel(label: str) -> list: 
    listWords = list(map(lambda w: re.sub(" ", "", w), label.split(" ")))
    listWords = list(filter(lambda w: w, listWords))
    #listWords = label.split(" ")
    listWords = ["".join(filter(filterBadCharacters, [*word])) for word in listWords]
    return listWords
"""

def selectField(label: str) -> int:   #TODO: NUMERO DE ENTRADAS PUEDE SER LIMITADO => Número de entradas (escribir de 1 a 5)
    #ordenados por prioridad para que no haya problemas
    labelToUpper = label.upper()
    if 'NOMBRE' in labelToUpper or 'NOME' in labelToUpper: #TODO: Añadir nombres completos en plural
        if 'DNI' in labelToUpper:
            if 'TODO' in labelToUpper or 'TODA' in labelToUpper or 'TOD@' in labelToUpper or 'NOMBRES' in labelToUpper:
                return const.NOMBRES_COMPLETOS_TODOS_DNI #Nombres completos y DNIs de todos
            else:
                return const.NOMBRE_COMPLETO_DNI #Nombre completo y DNI
        else:
            if 'TODO' in labelToUpper or 'TODA' in labelToUpper or 'TOD@' in labelToUpper:
                return const.NOMBRES_COMPLETOS_TODOS #Nombres completos y DNIs de todos
            else:
                if 'COMPLETO' in labelToUpper or 'APELLIDO' in labelToUpper or 'APELIDO' in labelToUpper:
                    return const.NOMBRE_COMPLETO #Nombre completo
                else:
                    return const.NOMBRE #Nombre

    elif 'DNI' in labelToUpper:
        return const.DNI

    elif 'APELLIDO' in labelToUpper or 'APELIDO' in labelToUpper:
        if 'PRIMER' in labelToUpper or '1' in labelToUpper:
            return const.PRIMER_APELLIDO #Primer apellido
        elif 'SEGUNDO' in labelToUpper or '2' in labelToUpper:
            return const.SEGUNDO_APELLIDO #Segundo apellido
        else:
            return const.APELLIDOS #Apellidos

    elif 'TEL' in labelToUpper or 'TÉL' in labelToUpper:
        return const.TELEFONO #Telefono

    elif 'CORREO' in labelToUpper or 'MAIL' in labelToUpper or 'ELECTRONICO' in labelToUpper or 'ELECTRÓNICO' in labelToUpper:
        return const.CORREO #Correo 

    elif 'INSTA' in labelToUpper or 'IG' in labelToUpper:
        return const.INSTAGRAM #Instagram

    elif 'CONDICION' in labelToUpper or 'CONDICIÓN' in labelToUpper or 'ACEPT' in labelToUpper or 'TERMINOS' in labelToUpper or 'TÉRMINOS' in labelToUpper or 'NORMA' in labelToUpper:
        return const.CONDICIONES #Aceptar condiciones

    elif 'ENTRADA' in labelToUpper or 'NUMERO' in labelToUpper or 'NÚMERO' in labelToUpper or 'Nº':
        return const.NUM_ENTRADAS #Numero de entradas

    else:
        return const.ERROR #Error


def getInput(itemTitle : str) -> str:
    cursor = connection.cursor()
    field = selectField(itemTitle)
    if field == const.NOMBRE:
        cursor.execute("select nombre from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])
        

    elif field == const.NOMBRE_COMPLETO:
        cursor.execute("select nombre, apellido1, apellido2 from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.NOMBRE_COMPLETO_DNI:
        cursor.execute("select nombre, apellido1, apellido2, dni from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.NOMBRES_COMPLETOS_TODOS:
        cursor.execute("select nombre, apellido1, apellido2 from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i where i.evento = '" + idEvento + "'")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.NOMBRES_COMPLETOS_TODOS_DNI:
        cursor.execute("select nombre, apellido1, apellido2, dni from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i where i.evento = '" + idEvento + "'")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.DNI:
        cursor.execute("select dni from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.PRIMER_APELLIDO:
        cursor.execute("select apellido1 from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.SEGUNDO_APELLIDO:
        cursor.execute("select apellido2 from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])
    
    elif field == const.APELLIDOS:
        cursor.execute("select apellido1, apellido2 from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.NUM_ENTRADAS:
        cursor.execute("select count(*) from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i where i.evento = '" + idEvento + "'")
        rows = cursor.fetchall()
        return rows[0][0]

    elif field == const.CORREO:
        cursor.execute("select email from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.INSTAGRAM:
        cursor.execute("select instagram from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    elif field == const.TELEFONO:
        cursor.execute("select telefono from personas p inner join pertenecer p2 on (p2.persona = p.dni) natural join irevento i inner join grupos g on (g.id = i.grupo) where i.evento = '" + idEvento + "' and p.dni = g.titular")
        rows = cursor.fetchall()
        return ', '.join([' '.join(row) for row in rows])

    else:
        return ''

