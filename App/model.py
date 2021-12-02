"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def init(): #Comentar
    """ Inicializa el catálogo

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        catalog = {
                    'airports': None,
                    'cities': None,
                    'digraph': None,
                    'undigraph': None,
                    'edgeMap': None
                    }

        catalog['airports'] = mp.newMap(numelements=41001,
                                     maptype='PROBING')

        catalog['cities'] = mp.newMap(numelements=14000,
                                     maptype='PROBING')

        catalog['edgeMap'] = mp.newMap(numelements=92606,
                                     maptype='PROBING')

        catalog['digraph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10700,
                                              comparefunction=None)
        
        catalog['undigraph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=10700,
                                              comparefunction=None)

        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:init()')

# Funciones para agregar informacion al catalogo

def addAirport(catalog, airport): #NOT USING YET
    newairport = newAirport(airport['Name'], airport['City'], airport['Country'], airport['IATA'], airport['Latitude'], airport['Longitude'])
    if not mp.contains(catalog['airports'], airport['IATA']):
        mp.put(catalog['airports'], airport['IATA'], newairport)

def addCity(catalog, airport):
    try:
        city = airport['City']
        newairport = newAirport(airport['Name'], airport['City'], airport['Country'], airport['IATA'], airport['Latitude'], airport['Longitude'])
        if not mp.contains(catalog['cities'], city):
            mapCity = mp.newMap(maptype='PROBING')
            mp.put(mapCity, airport['IATA'], newairport)
            mp.put(catalog['cities'], city, mapCity)
        else:
            mapCity = me.getValue(mp.get(catalog['cities'],city))
            mp.put(mapCity, airport['IATA'], newairport)
    except Exception as exp:
        error.reraise(exp, 'model:addCity()')

def addNodeAirport(catalog, airport):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        if not gr.containsVertex(catalog['digraph'], airport):
            gr.insertVertex(catalog['digraph'], airport)
    except Exception as exp:
        error.reraise(exp, 'model:addNodeAirport')

def addNodeUndigraph(catalog, airport):
    try:
        if not gr.containsVertex(catalog['undigraph'], airport):
            gr.insertVertex(catalog['undigraph'], airport)
    except Exception as exp:
        error.reraise(exp, 'model:addNodeUndigraph')

def addConnection(catalog, departure, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos
    """
    edge = gr.getEdge(catalog['digraph'], departure, destination)
    if edge is None:
        gr.addEdge(catalog['digraph'], departure, destination, distance)

def addAirportConnection(catalog, route):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    """
    try:
        departure = route["Departure"] # IATA
        destination = route["Destination"] # IATA
        distance = route["distance_km"]
        cleanServiceDistance(distance)
        addNodeAirport(catalog, departure)
        addNodeAirport(catalog, destination)
        addConnection(catalog, departure, destination, distance)
    except Exception as exp:
        error.reraise(exp, 'model:addAirportConnection')

def addEdgeInfo(catalog, route):
    IataDeparture = route["Departure"]
    IataDestination = route["Destination"]
    if not mp.contains(catalog["edgeMap"], IataDeparture): 
        edges_list = lt.newList("ARRAY_LIST") 
        lt.addLast(edges_list, IataDestination) 
        mp.put(catalog["edgeMap"], IataDeparture, edges_list) 
    else:
        edges_list = me.getValue(mp.get(catalog["edgeMap"], IataDeparture)) #Se saca la lista que contiene la ciudad
        if not lt.isPresent(edges_list, IataDestination):
            lt.addLast(edges_list, IataDestination) #Se añade la información de dicho avistamiento

def createUndirectedGraph(catalog):
    for departure in lt.iterator(mp.keySet(catalog['edgeMap'])):
        for destination in lt.iterator(me.getValue(mp.get(catalog['edgeMap'], departure))):
            if dualConnection(catalog, destination=destination, departure=departure):
                addNodeUndigraph(catalog, destination)
                addNodeUndigraph(catalog, departure)
                edge = gr.getEdge(catalog['undigraph'], departure, destination)
                if edge is None:
                    gr.addEdge(catalog['undigraph'], departure, destination, weight=0)

# Funciones para creacion de datos
def newAirport(Name, City, Country, IATA, Latitude, Longitude):
    airport = {"Name": Name, "City": City, "Country": Country, "IATA": IATA, "Latitude":Latitude, "Longitude": Longitude}
    return airport

# Funciones de consulta

def giveCities(catalog, city):
    mapCity = me.getValue(mp.get(catalog['cities'], city))
    return mp.valueSet(mapCity)

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de ayuda

def cleanServiceDistance(distance):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if distance == '':
        distance = 0

def dualConnection(catalog, destination, departure):
    if mp.get(catalog['edgeMap'], destination) == None or mp.get(catalog['edgeMap'], departure) == None:
        return False
    if lt.isPresent(me.getValue(mp.get(catalog['edgeMap'], destination)), departure) != 0:
        if lt.isPresent(me.getValue(mp.get(catalog['edgeMap'], departure)), destination) != 0:
            return True
    return False 
