from csv import DictReader

import requests

from backend.data.data_schemas import *
from backend.data.json_bd import create_request

translate = {
    'Подключение': Skill.CONNECTION_CLIENT,
    'Дозаказ': Skill.ADD_EQUIPMENT_ORDER,
    'Локальная заявка': Skill.LOCAL_APPLICATION,
    'Глобальная проблема': Skill.ACCIDENTS_ON_TKD
}
durations = {
    'Подключение': Duration.CONNECTION_CLIENT_T,
    'Дозаказ': Duration.ADD_EQUIPMENT_ORDER_T,
    'Локальная заявка': Duration.LOCAL_APPLICATION_T,
    'Глобальная проблема': Duration.ACCIDENTS_ON_TKD_T
}


def add_requests_from_csv(csv_dict: DictReader) -> None:
    sp = parse_csv(csv_dict)
    for request in sp:
        data = create_request(request)
        print(data)


def parse_csv(csv_dict: DictReader, have_column_names=True) -> list[Request]:
    result = []
    locations = get_locations(csv_dict)
    for i, row in enumerate(csv_dict):
        try:
            ##!!!УБРАТЬ ОГРАНИЧЕНИЕ В 2 СТРОКИ ПРИ ДЕПЛОЕ
            if i == 3:
                break
            request = Request(id=int(row['Заявка']),
                              required_skill=translate[row['Тип заявки BK']],
                              priority=Priority.DEFAULT,
                              location=locations[i],
                              time_window_start=get_datetime(row['Начало']),
                              time_window_end=get_datetime(row['Окончание']),
                              duration=durations[row['Тип заявки BK']]
                              )
            result.append(request)
        except Exception as e:
            break
    return result


def get_location(address: str) -> Location:
    # https://catalog.api.2gis.ru/3.0/items/geocode?key=YOUR_API_KEY&type=building%2Cstation_platform%2Cattraction%2Cadm_div.place%2Cstreet%2Cadm_div.district%2Cadm_div.city&fields=items.point&location=37.64%2C55.74&q=Город+Москва%2C+пр-кт.Волгоградский%2C+д.+128+к+5%2C+кв.+1
    resp = requests.get('https://catalog.api.2gis.ru/3.0/items/geocode',
                        params={"key": '2d64e373-d8b2-4338-b90b-53939cd66d6c',
                                "type": "building",
                                "fields": 'items.point',
                                "q": address}).json()
    coords = resp["result"]["items"][0]['point']
    lat, lon = coords['lat'], coords['lon']
    return Location(latitude=lat, longitude=lon, address=address)


def get_locations(csv_dict: DictReader) -> list[Location]:
    locations = []
    n = 0
    for i, row in enumerate(csv_dict):
        #УБРАТЬ ОГРАНИЧЕНИЕ В ДВЕ СТРОКИ ПРИ ДЕПЛОЕ
        if i == 3:
            break
        locations.append(get_location(row['Адрес']))
        n += 1
    while len(locations) != n:
        continue
    return locations


def get_datetime(str_date: str) -> datetime:
    # 17.08.2026 20:00
    str_date = str_date.split()
    date, time = str_date[0], str_date[1]
    date = date.split('.')
    year, month, day = int(date[2]), int(date[1]), int(date[0])
    time = time.split(':')
    hour = int(time[0])
    minute = int(time[1])
    return datetime(year, month, day, hour, minute)
