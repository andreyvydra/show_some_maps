import sys
from io import BytesIO

import requests
from PIL import Image
from spn_finder import get_spn


def geocode(address, kind=None):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    if kind is not None:
        geocoder_params['kind'] = kind

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym


def get_coordinates(address):
    toponym = geocode(address)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_points(address):
    toponym = geocode(address)
    toponym_dots = toponym["boundedBy"]["Envelope"]
    left_point, right_point = toponym_dots['lowerCorner'], toponym_dots['upperCorner']
    left_point = list(map(float, left_point.split()))
    right_point = list(map(float, right_point.split()))
    return left_point, right_point


def get_district_name(address):
    response = geocode(address, kind='district')
    dist = response["metaDataProperty"]["GeocoderMetaData"]["Address"]["district"]
    print(dist)
    return dist


def show_map(ll, spn, l='map', pt=None):
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": l
    }
    if pt is not None:
        map_params['pt'] = pt

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()


toponym_to_find = " ".join(sys.argv[1:])

district = get_district_name(toponym_to_find)



