"""" IMPORTS """
# Navigate the Website
from selenium import webdriver  # driver
from selenium.webdriver.common.by import By  # used to select web elements

# Want to use time library to check execution times and look for the fastest way
from Forms import forms
from Forms import constantes as const

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # used to wait for condition

import time


# XPATH Syntax
# https://www.w3schools.com/xml/xpath_syntax.asp

def checkStories(browser):
    storieExists = False
    try:
        WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="_aarf _aarg"]')))
        browser.find_elements(By.XPATH, '//*[@class="_aarf _aarg"]')
        storieExists = True
    except Exception:
        storieExists = False

    if storieExists:
        try:
            browser.find_elements(By.XPATH, '//*[@height="166"]')
            return const.STORIES_VISTAS
        except Exception:
            return const.STORIES_NO_VISTAS
    else:
        return const.NO_STORIES
    
def clickStorie(browser):
    while(1):
        try:
            WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="_aarf _aarg"]')))
            browser.find_elements(By.XPATH, '//*[@class="_aarf _aarg"]')
        except Exception:
            browser.refresh()
            continue


def getLugaryFecha() -> dict:
    cursor = connection.cursor()
    # Un unico evento
    cursor.execute("""select lugar, fecha from eventos where id = %s""", (idEvento,))
    row = cursor.fetchall()[0]

    return {
        "lugar" : str(row[0]),
        "dia"   : str(row[1].day),
        "mes"   : str(row[1].month),
        "year"   : str(row[1].year)
    }

def linktree(browser, link):
    browser.get(link)
    data = getLugaryFecha()
    #
    browser.close()
    return

    
def autoCompleteForms(browser, link):
    """ OBTENER Y MODIFICAR ELEMENTOS DE LA PAGINA"""
    browser.get(link)

    #/html/body/div/div[3]/form/div[2]/div/div[3]/div[1]/div[1]/div
    send_button = forms.findButton(browser, 'Enviar', (By.XPATH, '//form//*[@role="button"]'))

    # XPATH to the list of items
    listItemsPath = '//form//*[@role="list"][1]/*[@role="listitem"]'

    # Number of items in the form
    nItems = len(browser.find_elements(By.XPATH, listItemsPath))

    # from each field we want to get the label and the input
    try:
        for i in range(1, nItems+1):

            # XPATH to the corresponding item
            itemPath = f'{listItemsPath}[{i}]'

            # ITEM TITLE
            print("\n---------------ITEMS-----------------")
            itemTitle = browser.find_element(By.XPATH, f'{itemPath}//span[1]')
            print(itemTitle.text)
            forms.autoCompleteField(browser, itemPath, itemTitle.text, idEvento, connection)

    finally:
        # Enviar
        send_button.click()
        time.sleep(2)
        # Closes the browser after submitting form
        browser.close()
        return
    

def ejecutarBot(conn, link):
    if link=='A':
        ejecutarBotBio(conn)
    elif link=='B':
        ejecutarBotStorie(conn)
    else:
        return
    

def ejecutarBotBio(conn):
    global connection
    connection = conn
    global idEvento
    idEvento = input('ID del evento: ')
    global linkInsta
    linkInsta = input('Link del paso: ')

    try:
        option = webdriver.ChromeOptions() # para decir que es de chrome
        # option.add_argument("-incognito")
        # option.add_argument("--headless") # runs in background, doesn't use GUI, faster
        # option.add_argument("disable-gpu") # similar to --headless

        browser = webdriver.Chrome(executable_path='./chromedriver', options=option)
        
        browser.get(linkInsta)

    except Exception as ex:
        print('Error al abrir la pagina: '+str(ex))
        exit()

    try:
        #No es necesario aceptar las cookies, puede trabajar por detras
        '''cookies = forms.findButton(browser, 'Permitir solo cookies necesarias', (By.XPATH, '//button'))
        if(cookies != None):
            cookies.click()'''
        
        while(1):
            # Refrescar en página si no se encuentra el elemento hasta que se encuentre
            # TODO: Meterlo en una función con el while 1
            try:
                WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//main//header/section/div/a href')))
                elements = browser.find_elements(By.XPATH, '//main//header/section/div/a href')
            except Exception as ex:
                browser.refresh()
                continue


            # Trabajamos con el link
            if len(elements) <= 0:
                browser.refresh()
            else:
                browser2 = webdriver.Chrome(executable_path='./chromedriver', options=option)

                if 'https' not in elements[0].text:
                    link = f"https://{elements[0].text}"
                    print('LINK = '+link)
                if 'forms' in link or 'google' in link:
                    autoCompleteForms(browser2, link)
                else:
                    linktree(browser2, link)
            
                break

    except Exception as ex:
        print('Excepcion: '+ex)
    finally:
        browser.close()
        exit()


def ejecutarBotStorie(conn):
    global connection
    connection = conn
    global idEvento
    idEvento = input('ID del evento: ')
    global linkInsta
    linkInsta = input('Link del paso: ')

    try:
        option = webdriver.ChromeOptions() # para decir que es de chrome
        # option.add_argument("-incognito")
        # option.add_argument("--headless") # runs in background, doesn't use GUI, faster
        # option.add_argument("disable-gpu") # similar to --headless

        browser = webdriver.Chrome(executable_path='./chromedriver', options=option)
        
        browser.get(linkInsta)

    except Exception as ex:
        print('Error al abrir la pagina: '+str(ex))
        exit()

    try:
        #No es necesario aceptar las cookies, puede trabajar por detras
        '''cookies = forms.findButton(browser, 'Permitir solo cookies necesarias', (By.XPATH, '//button'))
        if(cookies != None):
            cookies.click()'''
        
        while(1):
            # Refrescar en página si no se encuentra el elemento hasta que se encuentre
            # TODO: Meterlo en una función con el while 1
            try:
                WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, '//main//header/section/div/a href')))
                elements = browser.find_elements(By.XPATH, '//main//header/section/div/a href')
            except Exception as ex:
                browser.refresh()
                continue


            # Trabajamos con el link
            if len(elements) <= 0:
                browser.refresh()
            else:
                browser2 = webdriver.Chrome(executable_path='./chromedriver', options=option)

                if 'https' not in elements[0].text:
                    link = f"https://{elements[0].text}"
                    print('LINK = '+link)
                if 'forms' in link or 'google' in link:
                    autoCompleteForms(browser2, link)
                else:
                    linktree(browser2, link)
            
                break

    except Exception as ex:
        print('Excepcion: '+ex)
    finally:
        browser.close()
        exit()