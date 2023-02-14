"""" IMPORTS """
# Navigate the Website
from selenium import webdriver  # driver
from selenium.webdriver.common.by import By  # used to select web elements

# Want to use time library to check execution times and look for the fastest way
from Forms import forms
from dataBase import dataBase as db

import time

import sys #para pasar por linea de comandos

# XPATH Syntax
# https://www.w3schools.com/xml/xpath_syntax.asp

def getLugaryFecha(connection, idEvento) -> dict:
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

def selectEvent(connection) -> list[str]:
    
    return

def linktree(connection, idEvento, browser, link):
    browser.get(link)
    data = getLugaryFecha(connection, idEvento)
    print(data)
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

            print('ITEM = ' + itemPath)

            # ITEM TITLE
            print("\n---------------ITEMS-----------------")
            itemTitle = browser.find_element(By.XPATH, f'{itemPath}//span[1]')
            print(itemTitle.text)
            print(f"This is the connection type: {type(connection)}")
            #forms.autoCompleteShortAnswer(browser, itemPath, itemTitle.text, 'inventado', connection)
            forms.autoCompleteField(browser, itemPath, itemTitle.text, idEvento, connection)

    finally:
        # Enviar
        send_button.click()
        time.sleep(2)
        # Closes the browser after submitting form
        browser.close()
        #Disconnects the database
        db.disconnectDataBase(connection)
        return

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Error. Debes pasar como parametro el id del evento")
        exit()

    idEvento = str(sys.argv[1])

    connection = db.connectDataBase()

    option = webdriver.ChromeOptions() # pa decir que es de chrome
    # option.add_argument("-incognito")
    # option.add_argument("--headless") # runs in background, doesn't use GUI, faster
    # option.add_argument("disable-gpu") # similar to --headless

    browser = webdriver.Chrome(executable_path='./chromedriver', options=option)
    
    browser.get("https://www.instagram.com/pasoinformatica.2223/")

    #time.sleep(5)

    try:
        #XPATH: //*[@id="mount_0_0_87"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]
        #FULL-XPATH: /html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]
        #role = "dialog"

        #No es necesario aceptar las cookies, puede trabajar por detras
        '''cookies = forms.findButton(browser, 'Permitir solo cookies necesarias', (By.XPATH, '//button'))
        if(cookies != None):
            cookies.click()'''
        while(1):
            time.sleep(2)
            prueba = browser.find_elements(By.XPATH, '//main//header/section//a')
            if len(prueba) <= 0:
                browser.refresh()
            else:
                browser2 = webdriver.Chrome(executable_path='./chromedriver', options=option)

                link = prueba[0].text
                if 'https' not in prueba[0].text:
                    link = f"https://{prueba[0].text}"
                    print('LINK = '+link)
                if 'forms' in link or 'google' in link:
                    autoCompleteForms(browser2, link)
                else:
                    linktree(connection, idEvento, browser2, link)
                break
            


    except Exception as ex:
        print('EXCEPCION: '+str(ex))
    finally:
        db.disconnectDataBase(connection)
        browser.close()
        exit()