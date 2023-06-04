import json

from maps.services.MLService import detect_objects
from maps.services.TomTomService import get_street_name, get_city_name_coord
from maps.services.VideoServices import create_map_video
from maps.services.YandexService import get_coord_by_address
from maps.services.OSMService import get_city_name, get_street_in_place, get_street_data, get_street_data1

MAPS_OBJECT = 'maps-object-'
OSM_OBJECT = 'osm-object-'


def collect_screenshots(request):
    # parse query
    north = request.POST['north']
    south = request.POST['south']
    east = request.POST['east']
    west = request.POST['west']
    address = request.POST['address']

    result_objects_osm = {}
    result_objects_map = {}

    screens_addresses_dict = {}

    final_data = {}

    # prepare objects and properties
    for key in request.POST.keys():
        if MAPS_OBJECT in key:
            for child_key in request.POST.keys():
                if key in child_key and key != child_key:
                    result_objects_map[request.POST[key]] = request.POST[child_key]

        if OSM_OBJECT in key:
            for child_key in request.POST.keys():
                if key in child_key and key != child_key:
                    result_objects_osm[request.POST[key]] = request.POST[child_key]

    # collect screenshots and collect osm data

    if bool(address):
        # screens
        points = []
        create_map_video(address, screens_addresses_dict, points)

        coordinates = get_coord_by_address(address)
        street = get_street_name(coordinates[1], coordinates[0])
        city = get_city_name_coord(coordinates[1], coordinates[0])

        final_data[street] = {}
        detect_objects(result_objects_map, street, screens_addresses_dict, final_data)

        # osm
        get_street_data1(city, street, result_objects_osm, final_data, points)
    elif bool(north) and bool(south) and bool(east) and bool(west):
        city = get_city_name(north, south, east, west)
        streets = get_street_in_place(north, south, east, west)

        # screens
        for street in streets:
            full_address = city + ', ' + street
            create_map_video(full_address)

        # osm
        for street in streets:
            get_street_data(city, street, result_objects_osm)

        # detect objects
        for street in streets:
            detect_objects(result_objects_map, street, screens_addresses_dict)

    with open("data.json", "w") as json_file:
        json.dump(final_data, json_file, ensure_ascii=False)
