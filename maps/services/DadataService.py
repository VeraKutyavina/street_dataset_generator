from dadata import Dadata

token = "8809edcac820bf5caaaa1ef4d8071259815212de"
secret = "fc0528818eb61d5947a3406e42982182e7e5027f"


def get_address_by_coord(x, y):
    dadata = Dadata(token)
    result = dadata.geolocate(name="address", lat=float(x), lon=float(y))
    return result


def get_coord_by_address(address):
    # dadata = Dadata(token, secret)
    # result = dadata.clean("address", address)
    token = "8809edcac820bf5caaaa1ef4d8071259815212de"
    secret = "fc0528818eb61d5947a3406e42982182e7e5027f"
    dadata = Dadata(token, secret)
    result = dadata.clean("address", "москва сухонская 11")
    print(result)
    return [result[0]['geo_lat'], result[0]['geo_lon']]