import json
import requests

URL = "https://api.tomtom.com/search/2/batch/sync.json?key=AKsJwMrvQ4DrSMW4Gc1COArEByeDm256"


def split_array(original_array):
    subarrays = []
    temp = []

    for i in range(len(original_array)):
        temp.append(original_array[i])
        if len(temp) == 100:
            subarrays.append(temp)
            temp = []

    if len(temp) > 0:
        subarrays.append(temp)

    return subarrays


def get_addresses(coordinates):
    splited_coordinates = split_array(coordinates)
    address_coordinates_dict = {}
    i = 0

    for array in splited_coordinates:
        data = {"batchItems": []}
        for coord in array:
            lat, lon = coord
            query = "/reverseGeocode/{},{}.json".format(lat, lon)
            data["batchItems"].append({"query": query})

        response = requests.post(URL, json=data)
        data = json.loads(response.text)

        for item in data['batchItems']:
            address_coordinates_dict[coordinates[i]] = item['response']['addresses'][0]['address']['freeformAddress']
            i += 1

    return address_coordinates_dict


def get_street_name(latitude, longitude):
    url = f"https://api.tomtom.com/search/2/reverseGeocode/{latitude},{longitude}.json?key=AKsJwMrvQ4DrSMW4Gc1COArEByeDm256"

    response = requests.get(url)
    data = response.json()

    if 'addresses' in data and data['addresses']:
        street_name = data['addresses'][0]['address']['streetName'].replace('улица', '').replace('Улица', '').replace('Проспект', '').strip()
        return street_name
    else:
        return None


def get_city_name_coord(latitude, longitude):
    url = f"https://api.tomtom.com/search/2/reverseGeocode/{latitude},{longitude}.json?key=AKsJwMrvQ4DrSMW4Gc1COArEByeDm256"

    response = requests.get(url)
    data = response.json()

    if 'addresses' in data and data['addresses']:
        city_name = data['addresses'][0]['address']['municipality'].replace('город', '').strip()
        return city_name
    else:
        return None


def get_coordinates(address):
    url = f"https://api.tomtom.com/search/2/geocode/{address}.json?key=AKsJwMrvQ4DrSMW4Gc1COArEByeDm256"

    response = requests.get(url)
    data = response.json()

    if 'results' in data and data['results']:
        latitude = data['results'][0]['position']['lat']
        longitude = data['results'][0]['position']['lon']
        return [latitude, longitude]
    else:
        return None