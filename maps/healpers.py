from maps.services.DadataService import get_street_by_coord, get_city_by_coord
from maps.services.OSMService import get_city_name, get_street_in_place, get_street_data
from maps.services.VideoServices import create_map_video
from maps.services.YandexService import get_coord_by_address

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
        print(result_objects_osm)
        print(result_objects_map)

    # collect screenshots and collect osm data
    if bool(address):
        # screens
        # create_map_video(address)

        # osm
        coordinates = get_coord_by_address(address)
        street = get_street_by_coord(coordinates[1], coordinates[0])
        city = get_city_by_coord(coordinates[1], coordinates[0])

        get_street_data(city, street, result_objects_osm)
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

