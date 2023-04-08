import requests

GEOCODIO_API_KEY = '9630c113d44338440c168341d08d6481169937c'

url = "https://api.geocod.io/v1.7/reverse?api_key=" + GEOCODIO_API_KEY


def convert_to_payload(arr):
    payload_arr = []
    for tup in arr:
        lat = str(tup[0])
        lon = str(tup[1])
        payload_arr.append(lat + "," + lon)
    return str(payload_arr)


def get_address_pool(coord):
    # payload = '["35.9746000,-77.9658000","32.8793700,-96.6303900","33.8337100,-117.8362320","35.4171240,-80.6784760"]'
    payload = convert_to_payload(coord)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)
