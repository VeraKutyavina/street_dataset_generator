from maps.services.DadataService import get_street_by_coord, get_city_by_coord
from maps.services.OSMService import get_city_name, get_street_in_place, get_street_data
from maps.services.VideoServices import create_map_video
from maps.services.YandexService import get_coord_by_address


def collect_screenshots(request):
    north = request.POST['north']
    south = request.POST['south']
    east = request.POST['east']
    west = request.POST['west']
    address = request.POST['address']

    if bool(address):
        create_map_video(address)
    elif bool(north) and bool(south) and bool(east) and bool(west):
        city = get_city_name(north, south, east, west)
        streets = get_street_in_place(north, south, east, west)

        for street in streets:
            full_address = city + ', ' + street
            create_map_video(full_address)


def collect_osm_data(request):
    address = request.POST['address']
    osm_item = request.POST['osm_item']

    coordinates = get_coord_by_address(address)
    street = get_street_by_coord(coordinates[1], coordinates[0])
    city = get_city_by_coord(coordinates[1], coordinates[0])

    get_street_data(city, street, osm_item)
