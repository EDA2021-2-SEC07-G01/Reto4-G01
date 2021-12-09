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
        print("First & Last Airport loaded in the Graph")
        headers = ["IATA", "Name", "City", "Country", "Latitude","Longitude"]
        table1 = []
        first_element = me.getValue(mp.get(catalog['airports'], first))
        last_element = me.getValue(mp.get(catalog['airports'], last))
        table1.append([first, first_element['Name'], first_element['City'], first_element['Country'], first_element['Latitude'], first_element['Longitude']])
        table1.append([last, last_element['Name'], last_element['City'], last_element['Country'], last_element['Latitude'], last_element['Longitude']])
        print(tabulate(table1,headers, tablefmt="grid"))

    elif data == 'cities':
        print("=== City Network ===")
        print("The number of cities are: "+str(mp.size(catalog[data])))
        print("First & Last City loaded in data structure.")
        headers = ["City", "Country", "Latitude", "Longitude", "Population"]
        table1 = []
        first_element = lt.getElement(me.getValue(mp.get(catalog[data], first)), 1)
        last_element = lt.getElement(me.getValue(mp.get(catalog[data], last)), 1)
        table1.append([first, first_element['country'], first_element['lat'], first_element['lng'], first_element['population']])
        table1.append([last, last_element['country'], last_element['lat'], last_element['lng'], last_element['population']])
        print(tabulate(table1,headers, tablefmt="grid"))

def printREQ1(list_iatas, catalog):
    if lt.size(list_iatas) < 5:
        headers = ["Name", "City", "Country", "IATA", "connections", "inbound", "outbound"]
        table1 = []
        for iata in lt.iterator(list_iatas):
            airport = me.getValue(mp.get(catalog['airports'], iata))
            table1.append([airport['Name'], airport['City'], airport['Country'], airport['IATA'], gr.indegree(catalog['digraph'], iata)+gr.outdegree(catalog['digraph'], iata), gr.indegree(catalog['digraph'], iata), gr.outdegree(catalog['digraph'], iata)])
        print(tabulate(table1,headers, tablefmt="grid"))       
    elif lt.size(list_iatas) >= 5:
        contador = 0
        headers = ["Name", "City", "Country", "IATA", "connections", "inbound", "outbound"]
        table1 = []
        for iata in lt.iterator(list_iatas):
            airport = me.getValue(mp.get(catalog['airports'], iata))
            table1.append([airport['Name'], airport['City'], airport['Country'], airport['IATA'], gr.indegree(catalog['digraph'], iata)+gr.outdegree(catalog['digraph'], iata), gr.indegree(catalog['digraph'], iata), gr.outdegree(catalog['digraph'], iata)])
            contador += 1
            if contador == 5:
                break
        print(tabulate(table1,headers, tablefmt="grid")) 

def printREQ2(iata, catalog):
    airport = me.getValue(mp.get(catalog['airports'], iata))
    headers = ["IATA", "Name", "City", "Country"]
    table1 = []
    table1.append([iata, airport['Name'], airport['City'], airport['Country']])
    print(tabulate(table1,headers, tablefmt="grid")) 

def printIATAS(list_cities):
    headers = ["City", "Latitude", "Longitude", "Country", "Admin-Name"]
    table1 = []
    for city in lt.iterator(list_cities):
        table1.append([city['city'], city['lat'], city['lng'], city['country'], city['admin_name']])
    print(tabulate(table1,headers, tablefmt="grid"))

def printREQ5(list_IATAS, airports):
    headers = ["IATA", "Name", "City", "Country"]
    table1 = []
    if lt.size(list_IATAS) < 6:
        for iata in lt.iterator(list_IATAS):
            airport = me.getValue(mp.get(airports, iata))
            table1.append([iata, airport['Name'], airport['City'], airport['Country']])    
        print(tabulate(table1,headers, tablefmt="grid"))
    elif lt.size(list_IATAS) >= 6:
        i = 1
        while i < 4:
            iata = lt.getElement(list_IATAS, i)
            airport = me.getValue(mp.get(airports, iata))
            table1.append([iata, airport['Name'], airport['City'], airport['Country']])
            i += 1    
        j = -2
        while j < 1:
            iata = lt.getElement(list_IATAS, lt.size(list_IATAS)+j)
            airport = me.getValue(mp.get(airports, iata))
            table1.append([iata, airport['Name'], airport['City'], airport['Country']])
            j += 1    
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
            IATA_first, IATA_last, first_city, last_city = controller.loadCSVs(catalog)
            printLoadData(catalog, "digraph", IATA_first, IATA_last)
            printLoadData(catalog, "undigraph", IATA_first, IATA_last)
            printLoadData(catalog, "cities", first_city, last_city)
    
        elif int(inputs[0]) == 2:
            print("=============== Req No. 1 Inputs ===============")
            print("most connected airports in network (TOP 5)")
            print("Number of aiports in network: "+str(gr.numVertices(catalog['digraph']))+'\n')
            print("=============== Req No. 1 Answer ===============")
            print("Connected airports inside network: "+str(gr.numEdges(catalog['undigraph'])))
            print("TOP 5 most connected airports...")
            iatas_connect = controller.interconexion(catalog)
            printREQ1(iatas_connect, catalog)

        elif int(inputs[0]) == 3:
            iata1 = input("Ingrese el IATA del primer aeropuerto: ")
            iata2 = input("Ingrese el IATA del segundo aeropuerto: ")
            print("=============== Req No. 2 Inputs ===============")
            print("Airport-1 IATA Code: "+iata1)
            print("Airport-2 IATA Code: "+iata2+'\n')
            print("=============== Req No. 2 Answers ===============")
            print("+++ Airport 1 IATA Code: "+iata1+" +++")
            printREQ2(iata1, catalog)
            print("+++ Airport 1 IATA Code: "+iata2+" +++")
            printREQ2(iata2, catalog)
            '\n'
            airport1 = me.getValue(mp.get(catalog['airports'], iata1))["Name"]
            airport2 = me.getValue(mp.get(catalog['airports'], iata2))["Name"]
            total, connected = controller.clusters(catalog, iata1, iata2)
            print("Number of SCC in Airport-Route network: " + str(total))
            print("Does the "+airport1+" and the "+airport2+" belong together?\n"+"ANSWER: "+str(connected))

        elif int(inputs[0]) == 4:
            departure_city = input("Ingrese la ciudad de salida: ")
            destination_city = input("Ingrese la ciudad de destino: ")
            all_departures = me.getValue(mp.get(catalog['cities'], departure_city))
            all_destinations = me.getValue(mp.get(catalog['cities'], destination_city))
            printIATAS(all_departures)
            departureCoordinates = input('Ingrese la latidud y longitud de salida separada por coma: ')
            printIATAS(all_destinations)
            destinationCoordinates = input('Ingrese la latidud y longitud de llegada separada por coma: ')

        elif int(inputs[0]) == 5:
            init = input("Ingrese la ciudad de origen como IATA: ")
            millas = input("Cantidad de millas disponibles: ")
            km = float(millas)*1.6
            mst = controller.mst(catalog, km, init)

        elif int(inputs[0]) == 6:
            IATA_useless = input("Ingrese el IATA del aeropuerto fuera de funcionamiento: ")
            print("=============== Req No. 5 Inputs ===============")
            print("Closing the airport with IATA code: "+IATA_useless+'\n')
            airports = gr.numVertices(catalog['digraph'])
            routes_directed = gr.numEdges(catalog['digraph'])
            routes_undirected = gr.numEdges(catalog['undigraph'])
            print("--- Airport-Routes Digraph ---")
            print("Original number of the Airports: "+str(airports)+' and Routes: '+str(routes_directed))
            print("--- Airport-Routes Graph ---")
            print("Original number of the Airports: "+str(airports)+' and Routes: '+str(routes_undirected)+'\n')
            print("+++ Removing Airport with IATA code: "+IATA_useless+' +++\n')
            directedfinal_nodes, directedroutes, directed_affected = controller.deleteIATA(catalog['digraph'], IATA_useless)
            print("--- Airport-Routes Digraph ---")
            print("Resulting number of the Airports: "+str(directedfinal_nodes)+' and Routes: '+str(directedroutes))
            print("--- Airport-Routes Graph ---")
            print("Original number of the Airports: "+str(directedfinal_nodes)+' and Routes: '+str(routes_undirected-lt.size(directed_affected))+'\n')
            print("=============== Req No. 5 Answer ===============")
            print("There are "+str(lt.size(directed_affected))+" Airports affected by the removal of "+IATA_useless)
            print("The first & last 3 Airports affected are: ")
            printREQ5(directed_affected, catalog['airports'])

        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()

