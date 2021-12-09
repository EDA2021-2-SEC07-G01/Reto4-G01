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
 """

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    return model.init()

# Funciones para la carga de datos
def loadCSVs(catalog):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    airportsfile = cf.data_airports
    airports_file = csv.DictReader(open(airportsfile, encoding="utf-8"), delimiter=",")
    contador = 0
    for airport in airports_file:
        model.addAirport(catalog, airport)
        model.addNodeAirport(catalog['digraph'], airport['IATA'])
        model.addNodeAirport(catalog['undigraph'], airport['IATA'])
        if contador == 0:
            first_IATA = airport['IATA']
        last_IATA = airport['IATA']
        contador += 1
            
    routesfile = cf.data_routes
    routes_file = csv.DictReader(open(routesfile, encoding="utf-8"), delimiter=",")
    for route in routes_file:
        model.addAirportConnection(catalog, route) # digrapgh connection
        model.addEdgeInfo(catalog, route) # undirected-graph connection
    model.createUndirectedGraph(catalog)

    worldcities = cf.data_worldcities
    worldcities_file = csv.DictReader(open(worldcities, encoding="utf-8"), delimiter=",")
    contador_cities = 0
    for city in worldcities_file:
        model.addCity(catalog, city)
        if contador_cities == 0:
            first_city = city['city_ascii']
        last_city = city['city_ascii']
        contador_cities += 1

    return first_IATA, last_IATA, first_city, last_city

# Funciones de consulta sobre el catálogo

def interconexion(catalog):
    return model.get_interconexion(catalog)

def clusters(catalog, iata1, iata2):
    return model.clusters(catalog, iata1, iata2)

def mst(catalog, km, init):
    return model.mst(catalog, km, init)

def deleteIATA(graph, IATA_useless):
    return model.deleteIATA(graph, IATA_useless)

def distanceDijkstra(catalog, iata1, iata2):
    return model.distanceDijkstra(catalog, iata1, iata2)