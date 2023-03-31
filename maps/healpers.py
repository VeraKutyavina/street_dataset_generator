from maps.services.OSMService import get_city_name, get_street_in_place
from maps.services.VideoServices import create_map_video


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
