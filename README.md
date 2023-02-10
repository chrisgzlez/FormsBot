# TO-DO

## Coger Elementos (IMPORTANTE)

-   Leer las 'labels'
-   Detectar los distintos tipos de labels

## Modificar Inputs (IMPORTANTE)

-   Añadir información correspondiente a cada label
-   Añadir info correspondiente a cada tipo de input (texto, opcion multiple...)

## Optimizar Tiempos (SEMI-IMPORTANTE)

-   Usar libreria time
-   Diferencia de tiempo de '--headless' a no
-   Esperar solo por un input en vez de todos
-   Ponerlo fuera del for-loop

## Clases de Datos (POO) (SEMI-IMPORTANTE)

-   Crear la clase de datos (con modificador @dataclass)
-   Informacion de:
-   -   Nombre
-   -   Apellidos
-   -   Instagram
-   -   Numero de Personas
-   -   Correo
-   -   Info de otras personas
-   Guardarlo en un archivo o algo

## UI Introducir Datos (SEMI-IMPORTANTE)

-   Hacer un menu
-   Leer datos por terminal y guardarlos en la clase

## Base de Datos (PUEDE ESPERAR)

-   Guardar la info de las clases en una base de datos

# Varios

CLASS_NAME
CSS_SELECTOR
ID
LINK_TEXT
NAME
PARTIAL_LINK_TEXT
TAG_NAME
XPATH

# Referencias

## Tutorial Principal

https://medium.com/swlh/automatically-filling-multiple-responses-into-a-google-form-with-selenium-and-python-176340c5220d

## Documentacion de Selenium

https://www.selenium.dev/documentation/webdriver/
https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/chrome.html

## Explicacion del find_element y find_elements

https://stackoverflow.com/questions/30002313/selenium-finding-elements-by-class-name-in-python

# Explicacion Basica del Codigo

con find_element coges un unico elemento (el primero que encuentra)
con find_elements coges todos (luego lo puedes iterar)
el .find_element() se lo puedes aplicar a cualquier elementoWeb
el By.[tipo] te deja buscar por el tipo indicado (mostrados arriba)
el XPATH ponerlo entre comillas simples solo
para saber que elementos quieres, en la web, click derecho>inspeccionar y vas abriendo divs
hasta que encuentras el qeu quieres y le pillas la clase o el id

# Elementos de la Web (del DOM) (HTML basico)

clase: muchos elementos pueden tener la misma clase
id: unico en todo el DOM y para cada elemento, no hay 2 iguales
tag: tipo de etiqueta (entre <>): <p>, <div>, <input>, <form>
dentro de la tag, puedes tener atributos: <div class="clase" id="3452" name="Mortadelo"...></div>
las tags se abren y cierran (funcionan como parentesis). Ejemplo:

<div class="contenedor">
    ELementos dentro de la div
</div>

Las labels se cogen todas igual
Los inputs esta en field

## TIPOS DE INPUTS

### Text: type=input

### Multiple Choice (checkbox):

All the options buscar role="list" en field

Each option => role="listbox"
Esta opcion tiene su label y su checkbox:

-   Label: Única span
-   Checkbox: role="checkbox"

### Multiple choice (Dropdown):

caja de dropdown: role="listbox"
clicko en ella
opciones de dropdown: role="presentation" (solo 1 vez)
dentro de opciones, cada opcion: span (click en ella)

### Radial:

Todas las opciones: div role="radiogroup"
opciones>span> (todas las opciones) >div>label (especifica)

deberia de coger todas las opciones y hacer un for
opcion opciones.label
opcion:
*label: span
*radio: role="radio"
CASO ESPECIAL "otro"
pasos a seguir:

-   identificar que es la opcion otro
-   clickar su radio
    (Igual que en las otras opciones)
-   escribir en su text input type="text" (Easy)
