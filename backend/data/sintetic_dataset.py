import random
from datetime import datetime, timedelta

from data_schemas import (
    Engineer,
    Request,
    Location,
    Priority,
    VehicleType,
    Skill,
    Duration,
)

from backend.data.json_bd import (
    initialize_database,
    create_engineer,
    create_request,
)
from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent / "data_json"

ENGINEERS_FILE = DATA_DIR / "engineers.json"
REQUESTS_FILE = DATA_DIR / "requests.json"


def clear_dataset():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    ENGINEERS_FILE.write_text("[]", encoding="utf-8")
    REQUESTS_FILE.write_text("[]", encoding="utf-8")

# ============================================================
# НАСТРОЙКИ ГЕНЕРАЦИИ
# ============================================================

NUM_ENGINEERS = 10
NUM_REQUESTS = 60

# Центральная точка района генерации
CENTER_LATITUDE = 55.7558
CENTER_LONGITUDE = 37.6173

# Максимальное отклонение координат от центра
COORDINATE_RADIUS = 0.08

# Начало рабочего дня
WORKING_DAY_START = datetime(
    2026,
    9,
    21,
    8,
    0,
)

# Продолжительность смены
SHIFT_DURATION_HOURS = 9


# ============================================================
# НАСТРОЙКИ
# ============================================================

ALL_SKILLS = list(Skill)

ALL_VEHICLES = list(VehicleType)

ALL_DURATIONS = [
    Duration.CONNECTION_CLIENT_T,
    Duration.ACCIDENTS_ON_TKD_T,
    Duration.ADD_EQUIPMENT_ORDER_T,
    Duration.LOCAL_APPLICATION_T,
]


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def random_location() -> Location:
    """
    Создаёт случайную координату
    рядом с центральной точкой.
    """

    latitude = (
        CENTER_LATITUDE
        + random.uniform(
            -COORDINATE_RADIUS,
            COORDINATE_RADIUS,
        )
    )

    longitude = (
        CENTER_LONGITUDE
        + random.uniform(
            -COORDINATE_RADIUS,
            COORDINATE_RADIUS,
        )
    )

    return Location(
        latitude=latitude,
        longitude=longitude,
    )


def random_priority() -> Priority:
    """
    Генерирует приоритет заявки.

    Срочных заявок немного меньше обычных.
    """

    if random.random() < 0.13:
        return Priority.URGENT

    return Priority.DEFAULT


def random_engineer_skills() -> list[Skill]:
    """
    Генерирует от 1 до 3 уникальных навыков инженера.
    """

    number_of_skills = random.randint(
        1,
        min(3, len(ALL_SKILLS)),
    )

    return random.sample(
        ALL_SKILLS,
        number_of_skills,
    )


def random_time_window(
    day_start: datetime,
    day_end: datetime,
) -> tuple[datetime, datetime]:
    """
    Создаёт случайное временное окно заявки.
    """

    total_minutes = int(
        (day_end - day_start).total_seconds()
        / 60
    )

    # Длительность окна:
    # от 1 до 3 часов
    window_duration = random.choice(
        [60, 90, 120, 180]
    )

    max_start = total_minutes - window_duration

    start_offset = random.randint(
        0,
        max_start,
    )

    window_start = (
        day_start
        + timedelta(minutes=start_offset)
    )

    window_end = (
        window_start
        + timedelta(minutes=window_duration)
    )

    return window_start, window_end


# ============================================================
# ГЕНЕРАЦИЯ ИНЖЕНЕРОВ
# ============================================================

def generate_engineers(
    count: int,
) -> list[Engineer]:

    engineers = []

    shift_start = WORKING_DAY_START

    shift_end = (
        shift_start
        + timedelta(
            hours=SHIFT_DURATION_HOURS
        )
    )

    for engineer_id in range(1, count + 1):

        engineer = Engineer(
            id=engineer_id,

            name=f"Engineer {engineer_id}",

            start_location=random_location(),

            shift_start=shift_start,

            shift_end=shift_end,

            skills=random_engineer_skills(),

            vehicle_type=random.choice(
                ALL_VEHICLES
            ),
        )

        engineers.append(engineer)

    return engineers


# ============================================================
# ГЕНЕРАЦИЯ ЗАЯВОК
# ============================================================

def generate_requests(
    count: int,
    engineers: list[Engineer],
) -> list[Request]:

    requests = []

    day_start = WORKING_DAY_START

    day_end = (
        day_start
        + timedelta(
            hours=SHIFT_DURATION_HOURS
        )
    )

    for request_id in range(1, count + 1):

        # Выбираем случайный навык,
        # который действительно есть хотя бы
        # у одного инженера.
        available_skills = set()

        for engineer in engineers:
            available_skills.update(
                engineer.skills
            )

        required_skill = random.choice(
            list(available_skills)
        )

        # Иногда ограничиваем тип транспорта.
        if random.random() < 0.3:
            required_vehicle = random.choice(
                ALL_VEHICLES
            )
        else:
            required_vehicle = None

        priority = random_priority()

        duration = random.choice(
            ALL_DURATIONS
        )

        time_window_start, time_window_end = (
            random_time_window(
                day_start,
                day_end,
            )
        )

        request = Request(
            id=request_id,

            location=random_location(),

            priority=priority,

            required_skill=required_skill,

            required_equipment=None,

            required_vehicle=required_vehicle,

            time_window_start=time_window_start,

            time_window_end=time_window_end,

            duration=duration,
        )

        requests.append(request)

    return requests


# ============================================================
# СОХРАНЕНИЕ
# ============================================================

def save_dataset(
    engineers: list[Engineer],
    requests: list[Request],
) -> None:

    initialize_database()
    clear_dataset()

    for engineer in engineers:
        create_engineer(engineer)

    for request in requests:
        create_request(request)


# ============================================================
# MAIN
# ============================================================

def main():

    print("Генерация датасета...")

    engineers = generate_engineers(
        NUM_ENGINEERS
    )

    requests = generate_requests(
        NUM_REQUESTS,
        engineers,
    )

    save_dataset(
        engineers,
        requests,
    )

    print()
    print("Датасет создан.")
    print(f"Инженеров: {len(engineers)}")
    print(f"Заявок:    {len(requests)}")

    urgent_count = sum(
        request.priority == Priority.URGENT
        for request in requests
    )

    default_count = sum(
        request.priority == Priority.DEFAULT
        for request in requests
    )

    print()
    print(f"Обычных заявок:  {default_count}")
    print(f"Срочных заявок:  {urgent_count}")


if __name__ == "__main__":
    main()