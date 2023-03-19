from yandex_geocoder import Client

YANDEX_API_KEY = 'fe94c607-ccc3-4d84-a017-3082f44c2512'

client = Client(YANDEX_API_KEY)


def get_coord_by_address(address):
    coordinates = client.coordinates(address)
    print(coordinates[0])
    return coordinates

