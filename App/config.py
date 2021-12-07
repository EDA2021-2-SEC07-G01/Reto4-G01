import os
import sys
file_path = os.path.join(os.path.dirname(__file__), '..')
file_dir = os.path.dirname(os.path.realpath('__file__'))
sys.path.insert(0, os.path.abspath(file_path))
data_airports = file_dir + '/Data/airports-utf8-small.csv'
data_routes = file_dir + '/Data/routes-utf8-small.csv'
data_worldcities = file_dir + '/Data/worldcities-utf8.csv'
