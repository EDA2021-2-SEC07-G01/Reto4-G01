import os
import sys
file_path = os.path.join(os.path.dirname(__file__), '..')
file_dir = os.path.dirname(os.path.realpath('__file__'))
sys.path.insert(0, os.path.abspath(file_path))
data_airports = file_dir + '/Data/airports_full.csv'
data_routes = file_dir + '/Data/routes_full.csv'
data_worldcities = file_dir + '/Data/worldcities.csv'
