import osmnx as ox
import numpy as np
import requests


def osm_query(tag, city):
    gdf = ox.geometries_from_place(city, tag).reset_index()
    gdf['city'] = np.full(len(gdf), city.split(',')[0])
    gdf['object'] = np.full(len(gdf), list(tag.keys())[0])
    gdf['type'] = np.full(len(gdf), tag[list(tag.keys())[0]])
    gdf = gdf[['city', 'object', 'type', 'geometry']]
    print(gdf)
    return gdf


def get_random_points(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"

    response = requests.get(url)
    data = response.json()

    point1 = (float(data[0]['lon']), float(data[0]['lat']))
    point2 = (float(data[1]['lon']), float(data[1]['lat']))

    return [point1, point2]


def get_street_in_city(place_name):
    # получаем граф дорог города
    graph = ox.graph_from_place(place_name, network_type='all')

    # получаем список всех улиц города
    streets = []
    for u, v, k, data in graph.edges(keys=True, data=True):
        if 'highway' and 'name' in data.keys():
            street_name = data['name']
            if street_name not in streets and isinstance(street_name, str):
                streets.append(street_name)

    print(streets)
    print(len(streets))


def get_street_in_place():
    # координаты прямоугольника
    north, south, east, west = 55.79, 55.82, 49.16, 49.11

    tags = {"highway": True}

    # Получение графа дорожной сети области
    G = ox.graph_from_bbox(north, south, east, west, network_type="all")

    print('HI')

    # Получение списка всех улиц области
    streets = []
    for u, v, k, data in G.edges(keys=True, data=True):
        if 'highway' and 'name' in data.keys():
            street_name = data['name']
            if street_name not in streets and isinstance(street_name, str):
                streets.append(street_name)

    # Вывод списка улиц
    print(streets)

