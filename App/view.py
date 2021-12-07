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
from tabulate import tabulate
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
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

def printLoadData(catalog, data, first, last):
    if data == 'digraph':
        print("=== Aiports-Routes DiGraph ===")
        print("Nodes: "+str(gr.numVertices(catalog[data]))+ " loaded airports.")
        print("Edges: "+str(gr.numEdges(catalog[data]))+ " loaded routes.")
        print("First & Last Airport loaded in the DiGraph")
        headers = ["IATA", "Name", "City", "Country", "Latitude","Longitude"]
        table1 = []
        first_element = me.getValue(mp.get(catalog['airports'], first))
        last_element = me.getValue(mp.get(catalog['airports'], first))
        table1.append([first, first_element['Name'], first_element['City'], first_element['Country'], first_element['Latitude'], first_element['Longitude']])
        table1.append([last, last_element['Name'], last_element['City'], last_element['Country'], last_element['Latitude'], last_element['Longitude']])
        print(tabulate(table1,headers, tablefmt="grid"))
        
    elif data == 'undigraph':
        print("=== Aiports-Routes Graph ===")
        print("Nodes: "+str(gr.numVertices(catalog[data]))+ " loaded airports.")
        print("Edges: "+str(gr.numEdges(catalog[data]))+ " loaded routes.")
        print("First & Last Airport loaded in the DiGraph")
        headers = ["IATA", "Name", "City", "Country", "Latitude","Longitude"]
        table1 = []
        first_element = me.getValue(mp.get(catalog['airports'], first))
        last_element = me.getValue(mp.get(catalog['airports'], last))
        table1.append([first, first_element['Name'], first_element['City'], first_element['Country'], first_element['Latitude'], first_element['Longitude']])
        table1.append([last, last_element['Name'], last_element['City'], last_element['Country'], last_element['Latitude'], last_element['Longitude']])
        print(tabulate(table1,headers, tablefmt="grid"))

def printIATAS(list_cities):
    headers = ["Name", "City", "Country", "IATA","Latitude","Longitude"]
    table1 = []
    for airport in lt.iterator(list_cities):
        table1.append([airport['Name'], airport['City'], airport['Country'], airport['IATA'], airport['Latitude'], airport['Longitude']])
    print(tabulate(table1,headers, tablefmt="grid"))

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
            IATA_first, IATA_last = controller.loadCSVs(catalog)
            printLoadData(catalog, "digraph", IATA_first, IATA_last)
            printLoadData(catalog, "undigraph", IATA_first, IATA_last)
            #printLoadData(catalog, "cities")
            #AÑADIR CITY NETWORK
        elif int(inputs[0]) == 2:
            pass

        elif int(inputs[0]) == 3:
            pass

        elif int(inputs[0]) == 4:
            departure_city = input("Ingrese la ciudad de salida: ")
            destination_city = input("Ingrese la ciudad de destino: ")
            cities_departure = controller.giveCities(catalog, departure_city)
            cities_destination = controller.giveCities(catalog, destination_city)
            printIATAS(cities_departure)
            departureIATA = input('Ingrese el IATA del lugar salida de interés: ')
            printIATAS(cities_destination)
            departureIATA = input('Ingrese el IATA del lugar destino de interés: ')

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

