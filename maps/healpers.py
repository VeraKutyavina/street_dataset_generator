from maps.services.MLService import detect_objects
from maps.services.VideoServices import create_map_video
from maps.services.YandexService import get_coord_by_address
from maps.services.DadataService import get_street_by_coord, get_city_by_coord
from maps.services.OSMService import get_city_name, get_street_in_place, get_street_data

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

    screens_addresses_dict = {'video-images-opencv/Пряженникова/image0.png': 'Пряженникова', 'video-images-opencv/Пряженникова/image1.png': 'Удмуртская Респ, г Глазов, ул Пряженникова, д 49/21', 'video-images-opencv/Пряженникова/image2.png': 'Удмуртская Респ, г Глазов, ул Пряженникова, д 51', 'video-images-opencv/Пряженникова/image3.png': 'Удмуртская Респ, г Глазов, ул Пряженникова, д 53/22', 'video-images-opencv/Пряженникова/image4.png': 'Удмуртская Респ, г Глазов, ул Пряженникова, д 53/22', 'video-images-opencv/Пряженникова/image5.png': 'Удмуртская Респ, г Глазов, ул Пряженникова, д 55/19', 'video-images-opencv/Пряженникова/image6.png': 'Пряженникова:, ', 'video-images-opencv/Пряженникова/image7.png': 'Удмуртская Респ, г Глазов, ул Пряженникова, д 49/21:58.13758299999783, 52.64627599999999', 'video-images-opencv/Качалова/image0.png': 'Качалова', 'video-images-opencv/Качалова/image1.png': 'г Казань, ул Качалова, д 95', 'video-images-opencv/Качалова/image2.png': 'г Казань, ул Качалова, д 84', 'video-images-opencv/Качалова/image3.png': 'г Казань, ул Качалова, д 84', 'video-images-opencv/Качалова/image4.png': 'г Казань, ул Ипподромная, д 15/86', 'video-images-opencv/Качалова/image5.png': 'г Казань, ул Ипподромная, д 15/86', 'video-images-opencv/Качалова/image6.png': 'г Казань, ул Качалова, д 86', 'video-images-opencv/Качалова/image7.png': 'г Казань, ул Качалова, д 104/2', 'video-images-opencv/Качалова/image8.png': 'г Казань, ул Качалова, д 104', 'video-images-opencv/Качалова/image9.png': 'г Казань, ул Газовая, д 2/104', 'video-images-opencv/Качалова/image10.png': 'г Казань, ул Газовая, д 7', 'video-images-opencv/Качалова/image11.png': 'г Казань, ул Газовая, д 7', 'video-images-opencv/Качалова/image12.png': 'г Казань, ул Газовая, д 7', 'video-images-opencv/Качалова/image13.png': 'г Казань, ул Газовая, д 6', 'video-images-opencv/Качалова/image14.png': 'Качалова:, ', 'video-images-opencv/Качалова/image15.png': 'г Казань, ул Качалова, д 89:55.773848999996304, 49.14576699999999', 'video-images-opencv/Качалова/image16.png': 'г Казань, ул Шаляпина, д 14/83:55.77396699999632, 49.145435', 'video-images-opencv/Качалова/image17.png': 'г Казань, ул Шаляпина, д 14/83:55.7740969999963, 49.14518199999999', 'video-images-opencv/Качалова/image18.png': 'г Казань, ул Качалова, д 78:55.774190999996314, 49.144979', 'video-images-opencv/Качалова/image19.png': 'г Казань, ул Качалова, д 78:55.774276999996324, 49.14479299999999', 'video-images-opencv/Качалова/image20.png': 'г Казань, ул Качалова, д 77:55.774353999996315, 49.144628', 'video-images-opencv/Качалова/image21.png': 'г Казань, ул Качалова, д 77:55.77444499999633, 49.144435', 'video-images-opencv/Качалова/image22.png': 'г Казань, ул Качалова, д 77:55.77454499999631, 49.14422199999999', 'video-images-opencv/Качалова/image23.png': 'г Казань, ул Качалова, д 77:55.774619999996304, 49.144060999999994', 'video-images-opencv/Качалова/image24.png': 'г Казань, ул Качалова, д 75:55.77471699999631, 49.14387099999999', 'video-images-opencv/Качалова/image25.png': 'г Казань, ул Качалова, д 75:55.774816999996325, 49.143686', 'video-images-opencv/Качалова/image26.png': 'г Казань, ул Нурсултана Назарбаева, д 21:55.77491399999632, 49.14349899999999', 'video-images-opencv/Качалова/image27.png': 'г Казань, ул Нурсултана Назарбаева, д 21:55.77498499999631, 49.143361', 'video-images-opencv/Качалова/image28.png': 'г Казань, ул Нурсултана Назарбаева, д 21:55.77508699999631, 49.143148999999994', 'video-images-opencv/Качалова/image29.png': 'г Казань, ул Нурсултана Назарбаева, д 21/64:55.77518799999631, 49.14293099999999', 'video-images-opencv/Качалова/image30.png': 'г Казань, ул Нурсултана Назарбаева, д 21/64:55.77529399999632, 49.142671'}
    # screens_addresses_dict = {}

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
        # create_map_video(address, screens_addresses_dict)

        # osm
        coordinates = get_coord_by_address(address)
        street = get_street_by_coord(coordinates[1], coordinates[0])
        # city = get_city_by_coord(coordinates[1], coordinates[0])

        # get_street_data(city, street, result_objects_osm)
        final_data[street] = {}
        print(screens_addresses_dict)
        detect_objects(result_objects_map, street, screens_addresses_dict, final_data)
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


