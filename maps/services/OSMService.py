import osmnx as ox
import requests
import osmapi
import shapely

from maps.services.TomTomService import get_addresses


def get_random_points(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"

    response = requests.get(url)
    data = response.json()

    if len(data) > 2:
        point1 = (float(data[0]['lon']), float(data[0]['lat']))
        point2 = (float(data[1]['lon']), float(data[1]['lat']))
    else:
        point1 = (float(data[0]['boundingbox'][0]), float(data[0]['boundingbox'][2]))
        point2 = (float(data[0]['boundingbox'][1]), float(data[0]['boundingbox'][3]))

    return [point1, point2]


def get_streets_name(graph):
    streets = []
    for u, v, k, data in graph.edges(keys=True, data=True):
        if 'highway' and 'name' in data.keys():
            street_name = data['name']
            if street_name not in streets and isinstance(street_name, str):
                streets.append(street_name)

    return streets


def get_street_in_city(place_name):
    graph = ox.graph_from_place(place_name, network_type='all')
    streets = get_streets_name(graph)

    print(streets)
    print(len(streets))


def get_street_in_place(north, south, east, west):
    graph = ox.graph_from_bbox(north, south, east, west, network_type="all")

    streets = get_streets_name(graph)

    return streets


def get_city_name(north, south, east, west):
    api = osmapi.OsmApi()
    print(float(east), float(north), float(west), float(south))
    bbox = (float(east), float(north), float(west), float(south))

    data = api.Map(*bbox)

    city_name = ''
    for elem in data:
        if 'tag' in elem['data']:
            if 'addr:city' in elem['data']['tag']:
                city_name = elem['data']['tag']['addr:city']
                break

    return city_name


def get_street_data(city_name, street_name, osm_item, final_data):
    tags = {}
    for key in osm_item.keys():
        tag_parts = key.split('=')
        tags = {tag_parts[1]: tag_parts[0]}
        final_data[street_name][tag_parts[0]] = []

        data = ox.geometries_from_place(city_name, tags)

        coordinates = []
        data_dict = {}
        for index, row in data.iterrows():
            if type(row['geometry']) == shapely.geometry.point.Point:
                current_coordinates = (row['geometry'].y, row['geometry'].x)
                coordinates.append(current_coordinates)
                data_dict[current_coordinates] = row['name']

        address_coordinates_dict = get_addresses(coordinates)

        result = {}
        for key in data_dict.keys():
            if street_name.lower() in address_coordinates_dict[key].lower():
                result[data_dict[key]] = address_coordinates_dict[key]
                current_obj = {
                    "address": address_coordinates_dict[key],
                    "coordinates": key,
                    "name": data_dict[key],
                }
                final_data[street_name][tag_parts[0]].append(current_obj)


def get_street_data1(city_name, street_name, osm_item, final_data, points):
    print(points)
    for key in osm_item.keys():
        tag_parts = key.split('=')
        tags = {tag_parts[1]: tag_parts[0]}
        final_data[street_name][tag_parts[0]] = []

        for point in points:
            data = ox.geometries_from_point(point, tags, 500)

            coordinates = []
            data_dict = {}
            for index, row in data.iterrows():
                if type(row['geometry']) == shapely.geometry.point.Point:
                    current_coordinates = (row['geometry'].y, row['geometry'].x)
                    coordinates.append(current_coordinates)
                    data_dict[current_coordinates] = row['name']

            address_coordinates_dict = get_addresses(coordinates)

            result = {}
            for key in data_dict.keys():
                if street_name.lower() in address_coordinates_dict[key].lower():
                    result[data_dict[key]] = address_coordinates_dict[key]
                    current_obj = {
                        "address": address_coordinates_dict[key],
                        "coordinates": key,
                        "name": data_dict[key],
                    }
                    final_data[street_name][tag_parts[0]].append(current_obj)
