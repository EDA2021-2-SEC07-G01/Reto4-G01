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

from DISClib.ADT.indexminpq import size
import config as cf
import copy
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as omap
from DISClib.ADT import stack as pila
from DISClib.ADT import queue as cola
from DISClib.ADT.graph import edges, gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import scc as kosaraju
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
from DISClib.ADT import stack
from DISClib.Algorithms.Graphs import dijsktra as dj
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def init(): 
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

        catalog['cities'] = mp.newMap(numelements=41100,
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
        
        catalog['connections'] = omap.newMap(omaptype='RBT')

        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:init()')

# Funciones para agregar informacion al catalogo

def addAirport(catalog, airport):
    newairport = newAirport(airport['Name'], airport['City'], airport['Country'], airport['IATA'], airport['Latitude'], airport['Longitude'])
    if not mp.contains(catalog['airports'], airport['IATA']):
        mp.put(catalog['airports'], airport['IATA'], newairport)

def addCity(catalog, city):
    try:
        city_name = city['city_ascii']
        newcity = newCity(city['city'], city['city_ascii'], city['lat'], city['lng'], city['country'], city['capital'], city['population'], city['admin_name'])
        if not mp.contains(catalog['cities'], city_name):
            mapList = lt.newList("ARRAY_LIST")
            lt.addLast(mapList, newcity)
            mp.put(catalog['cities'], city_name, mapList)
        else:
            mapList = me.getValue(mp.get(catalog['cities'], city_name))
            lt.addLast(mapList, newcity)
    except Exception as exp:
        error.reraise(exp, 'model:addCity()')

def addNodeAirport(graph, airport):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        if not gr.containsVertex(graph, airport):
            gr.insertVertex(graph, airport)
    except Exception as exp:
        error.reraise(exp, 'model:addNodeAirport')

def addConnection(catalog, departure, destination, distance):
    """
    Adiciona un arco entre dos aeropuertos
    """
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
        addConnection(catalog, departure, destination, float(distance))
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
                weight = gr.getEdge(catalog['digraph'], departure, destination)['weight']
                gr.addEdge(catalog['undigraph'], departure, destination, weight=weight)

# Funciones para creacion de datos

def newAirport(Name, City, Country, IATA, Latitude, Longitude):
    airport = {"Name": Name, "City": City, "Country": Country, "IATA": IATA, "Latitude":Latitude, "Longitude": Longitude}
    return airport

def newCity(city, citi_ascii, lat, lng, country, capital, population, admin_name):
    city = {"city": city, "city_ascii": citi_ascii, "lat": lat, "lng": lng, "country": country, "capital":capital, "population": population, "admin_name": admin_name}
    return city

# Funciones de consulta

def interconexion(catalog):
    vertices = gr.vertices(catalog['digraph'])
    for iata in lt.iterator(vertices):
        connections = gr.indegree(catalog['digraph'], iata) + gr.outdegree(catalog['digraph'], iata)
        if not omap.contains(catalog['connections'], connections):
            connect_list = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(connect_list, iata)
            omap.put(catalog['connections'], connections, connect_list) # the number of connections is the key
        else:
            connect_list = me.getValue(omap.get(catalog['connections'], connections))
            lt.addLast(connect_list, iata)
    return catalog['connections']

def get_interconexion(catalog): #omap with values as list of iatas
    omap_connect = interconexion(catalog)
    iatas = lt.newList(datastructure='ARRAY_LIST')
    contador = 0
    while contador < 5:
        for iata in lt.iterator(me.getValue(omap.get(omap_connect,(omap.maxKey(omap_connect))))):
            lt.addLast(iatas, iata)
            contador += 1
        omap.deleteMax(omap_connect)
    return iatas

def clusters(catalog, iata1, iata2):
    scc = kosaraju.KosarajuSCC(catalog['digraph'])
    return kosaraju.connectedComponents(scc), kosaraju.stronglyConnected(scc, iata1, iata2)

def mst(catalog, km, init):
    mst = prim.PrimMST(catalog['undigraph']) # search
    edges_mst = prim.edgesMST(catalog['undigraph'], mst) # search
    kilometers= prim.weightMST(catalog['undigraph'], edges_mst)
    grafo_mst = gr.newGraph(datastructure='ADJ_LIST', directed=False, size=1000, comparefunction=None)
    i = 1
    while i <= lt.size(edges_mst["mst"]):
        arista = lt.getElement(edges_mst["mst"], i)
        vertexA = arista["vertexA"]
        vertexB = arista["vertexB"]
        weight = arista["weight"]
        if not gr.containsVertex(grafo_mst, vertexA):
            gr.insertVertex(grafo_mst, vertexA)
        if not gr.containsVertex(grafo_mst, vertexB):
            gr.insertVertex(grafo_mst, vertexB)
        if gr.getEdge(grafo_mst, vertexA, vertexB) == None:
            gr.addEdge(grafo_mst, vertexA, vertexB, weight)
        i += 1
    end = lt.lastElement(edges_mst['mst'])["vertexB"]
    dfs_str = dfs.DepthFirstSearch(grafo_mst, init)
    path = dfs.pathTo(dfs_str, end)
    vertex_path = dfs.dfsVertex(dfs_str, grafo_mst, init)
    return gr.numVertices(grafo_mst), kilometers/2 , path

def deleteIATA(graph, IATA_useless):
    final_nodes = gr.numVertices(graph)-1
    routes = gr.numEdges(graph) - (gr.outdegree(graph, IATA_useless) + gr.indegree(graph, IATA_useless))
    affected_airports = gr.adjacents(graph, IATA_useless)
    final_affected = lt.newList("ARRAY_LIST")
    for aiport in lt.iterator(affected_airports):        
        if lt.isPresent(final_affected, aiport) == 0:
            lt.addLast(final_affected, aiport)
    return final_nodes, routes, final_affected

def distanceDijkstra(catalog, iata1, iata2):
    search = dj.Dijkstra(catalog['digraph'], iata1)
    path = dj.pathTo(search, iata2)
    while not stack.isEmpty(path):
        edge = stack.pop(path)
        print(edge['vertexA'] + "-->" +
            edge['vertexB'] + "costo: " +
            str(edge['weight']))
    num = str(dj.distTo(search, iata2))
    return num

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
