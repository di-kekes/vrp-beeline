import pprint

import requests
resp = requests.get('https://catalog.api.2gis.ru/3.0/items/geocode',
                    params={"key": '2d64e373-d8b2-4338-b90b-53939cd66d6c',
                            "type": "building",
                            "fields":'items.point',
                            "q": 'Город Москва, пр-кт.Волгоградский, д. 128 к 5, кв. 1'}).json()
coords = resp["result"]["items"][0]['point']
print(coords)