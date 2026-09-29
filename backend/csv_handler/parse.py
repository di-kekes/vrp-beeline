from csv import DictReader

import requests

from backend.data.data_schemas import *
from backend.data.json_bd import create_request
from backend.data.sintetic_dataset import clear_dataset


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

def is_empty_row(row: dict) -> bool:
    return not any(
        str(value).strip()
        for value in row.values()
    )

def add_requests_from_csv(csv_dict: DictReader) -> None:
    requests_list = parse_csv(csv_dict)

    # Очищаем старый датасет только после успешного парсинга
    clear_dataset()

    for request in requests_list:
        data = create_request(request)
        print(data)


def parse_csv(csv_dict: DictReader) -> list[Request]:
    # DictReader — итератор, поэтому сохраняем строки
    rows = []
    
    for row in csv_dict:
        if is_empty_row(row):
            break
        rows.append(row)

    locations = get_locations(rows)

    result = []

    for i, row in enumerate(rows):
        try:
            request = Request(
                id=int(row['Заявка']),
                required_skill=translate[row['Тип заявки BK']],
                priority=Priority.DEFAULT,
                location=locations[i],
                time_window_start=get_datetime(row['Начало']),
                time_window_end=get_datetime(row['Окончание']),
                duration=durations[row['Тип заявки BK']]
            )

            result.append(request)

        except Exception as e:
            print(f"Ошибка в строке CSV №{i + 2}: {e}")
            print(f"Данные строки: {row}")
            raise

    return result


def get_location(address: str) -> Location:
    address = address.strip()

    if not address:
        raise ValueError("Пустой адрес")

    response = requests.get(
        'https://catalog.api.2gis.ru/3.0/items/geocode',
        params={
            "key": "1e36bf3c-fadf-4a6c-9f48-255481765ebd",
            "type": "building",
            "fields": "items.point",
            "q": address
        }
    )

    response.raise_for_status()

    resp = response.json()

    if "result" not in resp:
        raise ValueError(
            f"2ГИС не вернул result для адреса '{address}': {resp}"
        )

    items = resp["result"].get("items", [])

    if not items:
        raise ValueError(
            f"2ГИС не нашёл адрес '{address}'"
        )

    coords = items[0].get("point")

    if not coords:
        raise ValueError(
            f"2ГИС не вернул координаты для адреса '{address}'"
        )

    return Location(
        latitude=coords['lat'],
        longitude=coords['lon'],
        address=address
    )


def get_locations(rows: list[dict]) -> list[Location]:
    locations = []

    for i, row in enumerate(rows):
        address = row.get('Адрес', '').strip()

        if not address:
            raise ValueError(
                f"Пустой адрес в строке CSV №{i + 2}. "
                f"Данные строки: {row}"
            )

        print(f"Геокодирование строки {i + 2}: {address}")

        locations.append(
            get_location(address)
        )

    return locations


def get_datetime(str_date: str) -> datetime:
    # 17.08.2026 20:00

    date_part, time_part = str_date.strip().split()

    day, month, year = map(int, date_part.split('.'))
    hour, minute = map(int, time_part.split(':'))

    return datetime(year,month,day,hour,minute)