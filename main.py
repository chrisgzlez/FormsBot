""" IMPORTS """
# Navigate the Website
from selenium import webdriver  # driver
from selenium.webdriver.common.by import By  # used to select web elements

# Want to use time library to check execution times and look for the fastest way
import time
from Forms import forms
from dataBase import dataBase as db

# XPATH Syntax
# https://www.w3schools.com/xml/xpath_syntax.asp

if __name__ == "__main__":

    connection = db.connectDataBase()

    option = webdriver.ChromeOptions() # pa decir que es de chrome
    # option.add_argument("-incognito")
    # option.add_argument("--headless") # runs in background, doesn't use GUI, faster
    # option.add_argument("disable-gpu") # similar to --headless

    browser = webdriver.Chrome(executable_path='./chromedriver', options=option)
    browser.get("https://docs.google.com/forms/d/1J6hrsxtT-QsD7PCaMP5Ek0QjZ4_7yx6FTg_ITWJ6Jfs/edit")

    """ OBTENER Y MODIFICAR ELEMENTOS DE LA PAGINA"""
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
            forms.autoCompleteField(browser, itemPath, itemTitle.text, 'inventado', connection)

            """if (i == 1):
                print("---------------TEXTBOX-----------------")
                forms.autoCompleteTextBox(browser, itemPath)
            
            if (i == 2):
                print("---------------CHECKBOX-----------------")
                forms.autoCompleteCheckBox(browser, itemPath)
            
            if (i == 3):
                print("---------------DROPDOWN-----------------")
                forms.autoCompleteDropDown(browser, itemPath)

            if (i == 4):
                print("---------------RADIAL-----------------")
                forms.autoCompleteRadial(browser, itemPath)"""

    finally:
        # Enviar
        send_button.click()
        time.sleep(2)
        # Closes the browser after submitting form
        browser.close()
        #Disconnects the database
        db.disconnectDataBase(connection)


