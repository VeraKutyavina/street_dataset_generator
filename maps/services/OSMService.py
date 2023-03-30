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
