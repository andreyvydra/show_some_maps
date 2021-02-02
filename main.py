import sys
from io import BytesIO

import requests
from PIL import Image
from distance import lonlat_distance


def get_organization(ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "d7e2a7d3-32d5-44db-ad56-43b741226da0"
    ll = ','.join([str(ll[0]), str(ll[1])])
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass

    json_response = response.json()
    organization = json_response["features"][0]
    return organization


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

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


def print_info_about_pharmacy(organization, point):
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    org_working_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    point_org = organization["geometry"]["coordinates"]
    ln = lonlat_distance(point_org, point)
    print(org_name, org_address, org_working_time, str(ln) + ' м', sep='\n')


def show_map(spn=None, ll=None, l='map', add_params=None):
    map_params = {
        "l": l
    }
    if spn is not None:
        map_params['spn'] = spn
    if ll is not None:
        map_params['ll'] = ll
    if add_params is not None:
        map_params['pt'] = '~'.join(add_params)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    print(response.url)
    Image.open(BytesIO(
        response.content)).show()


if __name__ == '__main__':
    address = ' '.join(sys.argv[1:])
    address_ll = get_coordinates(address)
    organization = get_organization(address_ll)

    org_point = organization["geometry"]["coordinates"]

    print_info_about_pharmacy(organization, address_ll)

    address_ll = ','.join([str(i) for i in address_ll])
    org_point = ','.join([str(i) for i in org_point])

    show_map(add_params=[address_ll, org_point])
