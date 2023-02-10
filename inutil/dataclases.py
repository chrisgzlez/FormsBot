from dataclasses import dataclass, field
import random
import string
from typing import Any

def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))

@dataclass
class Person:
    dni: str = Any
    name: str = Any
    surname1: str = Any
    surname2: str = Any
    email: str = Any
    instagram: str = Any

    def __repr__(self) -> str:
        self


    #OBLIGAR A QUE EL CAMPO DNI Y NOMBRE SEAN OBLIGATORIOS
    def deletePerson(self):
        del self

    def modificate_person(self, newAtributos): #HACER QUE NO SE PASE UN VECTOR DE LEN 6, Y QUE SE PASA CADA ATRIBUTO COMO UN ARGUMENTO -> OBLIGA A PASAR 6 ATRIBUTOS 
        if(len(newAtributos) == 6):
            self.dni = newAtributos[0]
            self.name = newAtributos[1]
            self.surname1 = newAtributos[2]
            self.surname2 = newAtributos[3]
            self.email = newAtributos[4]
            self.instagram = newAtributos[5]
        else:
            print("Error en modificatePerson. Numero de argumentos incorrecto...\n")


@dataclass
class Group:
    id_group: str = field(default_factory=generate_id)
    titular: Person = None #CAMBIAR NONE
    people: list[Person] = field(default_factory = list)

    def __is_member(self, persona) -> int:
        for i in self.people:
            if i.__eq__(persona):
                return 1
        return 0

    def add_person(self, persona): #FALTA COMPROBACION
        if self.__is_member(persona) == 0:
            self.people.append(persona)
        else:
            print('Esta persona ya esta en el grupo')

    def delete_person(self, persona): #FALTA COMPROBACION
        if self.__is_member(persona) == 1:
            self.people.remove(persona)
        else:
            print('Esta persona ya esta en el grupo')


    def change_titular(self, persona): #FALTA COMPROBACION -> CAMBIAR ERROR
        self.titular = persona
        if self.__is_member(persona) == 0:
            self.people.append(persona)
    
    def repr_person_group(self) -> str:
        text = ''
        for i in self.people:
            text+=(f'{i.name}; ')
        
        return text

    def __repr__(self) -> str:
        text = f'Group(id_group = {self.id_group}, titular = {self.titular.name}, people = {self.repr_person_group()})'
        return text

@dataclass
class Paso:
    paso_name: str
    linktree: str
    instagram: str


@dataclass
class Event:
    id_event: str
    cuentas_paso: list[Paso]
    link_forms: str


persona = Person("39499527V", "Adrian", "Martinez", "Balea", "aaaaaaaaaaa", "bbbbbbbbb")

grupo = Group(titular=persona)

grupo.add_person(persona)

persona.deletePerson()

print(grupo)

print(persona)


'''#persona.modificate_person("123456789A", "A", "M", "B", "a@gemail.com")

#print(persona)

grupo = Group(id_group="18347")

persona2 = Person(dni="1", name="Adri")

print(persona2)

#grupo.add_person(persona)

grupo.add_person(persona2)

print(persona2)

#grupo.change_titular(persona)

print(grupo)

#del persona -> Elimina la persona pero si la meto en un grupo sigue en él y no se elimina

#print(grupo)'''