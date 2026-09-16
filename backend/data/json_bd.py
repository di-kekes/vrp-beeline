import json

from pathlib import Path
from typing import TypeVar, Type

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


# Путь к папке с JSON-файлами
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data_json"


ENGINEERS_FILE = DATA_DIR / "engineers.json"
REQUESTS_FILE = DATA_DIR / "requests.json"


def initialize_database() -> None:
    """
    Создаёт папку data и JSON-файлы,
    если они ещё не существуют.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in (ENGINEERS_FILE, REQUESTS_FILE):
        if not file_path.exists():
            file_path.write_text(
                "[]",
                encoding="utf-8",
            )


def read_json(file_path: Path) -> list[dict]:
    """
    Читает JSON-файл и возвращает список словарей.
    """

    initialize_database()

    try:
        data = json.loads(
            file_path.read_text(encoding="utf-8")
        )

    except json.JSONDecodeError:
        raise ValueError(
            f"Некорректный JSON-файл: {file_path}"
        )

    if not isinstance(data, list):
        raise ValueError(
            f"JSON-файл должен содержать список: {file_path}"
        )

    return data


def write_json(
    file_path: Path,
    data: list[dict],
) -> None:
    """
    Записывает список словарей в JSON-файл.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=4,
        ),
        encoding="utf-8",
    )


def create_item(
    file_path: Path,
    item: BaseModel,
) -> dict:
    """
    Добавляет новый объект в JSON-файл.
    """

    data = read_json(file_path)

    item_data = item.model_dump(mode="json")

    if any(
        existing_item["id"] == item_data["id"]
        for existing_item in data
    ):
        raise ValueError(
            f"Объект с id={item_data['id']} уже существует"
        )

    data.append(item_data)

    write_json(file_path, data)

    return item_data


def get_all_items(
    file_path: Path,
    model: Type[T],
) -> list[T]:
    """
    Возвращает все объекты из JSON-файла
    в виде Pydantic-моделей.
    """

    data = read_json(file_path)

    return [
        model.model_validate(item)
        for item in data
    ]


def get_item_by_id(
    file_path: Path,
    model: Type[T],
    item_id: int,
) -> T | None:
    """
    Возвращает объект по id.
    Если объект не найден, возвращает None.
    """

    data = read_json(file_path)

    for item in data:
        if item["id"] == item_id:
            return model.model_validate(item)

    return None


def delete_item(
    file_path: Path,
    item_id: int,
) -> bool:
    """
    Удаляет объект по id.

    Возвращает:
    - True, если объект удалён.
    - False, если объект не найден.
    """

    data = read_json(file_path)

    filtered_data = [
        item
        for item in data
        if item["id"] != item_id
    ]

    if len(filtered_data) == len(data):
        return False

    write_json(file_path, filtered_data)

    return True


def update_item(
    file_path: Path,
    item: BaseModel,
) -> dict:
    """
    Обновляет существующий объект по id.
    """

    data = read_json(file_path)

    item_data = item.model_dump(mode="json")

    for index, existing_item in enumerate(data):
        if existing_item["id"] == item_data["id"]:
            data[index] = item_data

            write_json(file_path, data)

            return item_data

    raise ValueError(
        f"Объект с id={item_data['id']} не найден"
    )

from .data_schemas import Engineer
from .data_schemas import Request


# =========================
# Engineers
# =========================

def create_engineer(engineer: Engineer) -> dict:
    return create_item(
        ENGINEERS_FILE,
        engineer,
    )


def get_all_engineers() -> list[Engineer]:
    return get_all_items(
        ENGINEERS_FILE,
        Engineer,
    )


def get_engineer_by_id(
    engineer_id: int,
) -> Engineer | None:
    return get_item_by_id(
        ENGINEERS_FILE,
        Engineer,
        engineer_id,
    )


def update_engineer(engineer: Engineer) -> dict:
    return update_item(
        ENGINEERS_FILE,
        engineer,
    )


def delete_engineer(engineer_id: int) -> bool:
    return delete_item(
        ENGINEERS_FILE,
        engineer_id,
    )


# =========================
# Requests
# =========================

def create_request(request: Request) -> dict:
    return create_item(
        REQUESTS_FILE,
        request,
    )


def get_all_requests() -> list[Request]:
    return get_all_items(
        REQUESTS_FILE,
        Request,
    )


def get_request_by_id(
    request_id: int,
) -> Request | None:
    return get_item_by_id(
        REQUESTS_FILE,
        Request,
        request_id,
    )


def update_request(request: Request) -> dict:
    return update_item(
        REQUESTS_FILE,
        request,
    )


def delete_request(request_id: int) -> bool:
    return delete_item(
        REQUESTS_FILE,
        request_id,
    )