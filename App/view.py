"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config as cf
assert cf
import threading
import time
from App import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from DISClib.ADT.graph import gr

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar ruta más corta entre ciudades")
    print("5- Utilizar millas de viajero")
    print("6- Cuantificar efecto aeropuerto cerrado")

catalog = None

"""
Menu principal
"""

def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ...")
            catalog = controller.init()
            controller.loadCSVs(catalog)
            print("Grafos cargados!")
        elif int(inputs[0]) == 2:
            pass

        elif int(inputs[0]) == 3:
            pass

        elif int(inputs[0]) == 4:
            departure_city = input("Ingrese la ciudad de salida: ")
            destination_city = input("Ingrese la ciudad de destino: ")
            cities_departure = controller.giveCities(catalog, departure_city)
            cities_destination = controller.giveCities(catalog, destination_city)

        elif int(inputs[0]) == 5:
            pass

        elif int(inputs[0]) == 6:
            pass

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

