from datetime import datetime

from backend.data.data_schemas import (
    Engineer,
    Location,
    Skill,
    VehicleType,
)

from backend.data.json_bd import (
    create_engineer,
    get_all_engineers,
    get_engineer_by_id,
    update_engineer,
    delete_engineer,
)


def main():
    # 1. Создаём инженера
    engineer = Engineer(
        id=1,
        name="Иван Петров",
        start_location=Location(
            latitude=55.7558,
            longitude=37.6173,
            address="Москва",
        ),
        shift_start=datetime.fromisoformat(
            "2026-09-17T09:00:00+03:00"
        ),
        shift_end=datetime.fromisoformat(
            "2026-09-17T18:00:00+03:00"
        ),
        skills=[
            Skill.CONNECTION_CLIENT,
            Skill.ACCIDENTS_ON_TKD,
        ],
        vehicle_type=VehicleType.CAR,
    )

    # 2. Записываем инженера
    print("\n1. Создание инженера")

    try:
        result = create_engineer(engineer)
        print("Инженер создан:")
        print(result)

    except ValueError as error:
        print(f"Ошибка: {error}")

    # 3. Читаем всех инженеров
    print("\n2. Чтение всех инженеров")

    engineers = get_all_engineers()

    for item in engineers:
        print(item)

    # 4. Читаем инженера по ID
    print("\n3. Поиск инженера по ID")

    found_engineer = get_engineer_by_id(1)

    if found_engineer:
        print(found_engineer)
    else:
        print("Инженер не найден")

    # 5. Обновляем инженера
    print("\n4. Обновление инженера")

    engineer.name = "Иван Сидоров"

    updated_engineer = update_engineer(engineer)

    print(updated_engineer)

    # 6. Проверяем обновление
    print("\n5. Проверка обновления")

    found_engineer = get_engineer_by_id(1)

    if found_engineer:
        print(found_engineer.name)

    # 7. Удаляем инженера
    # print("\n6. Удаление инженера")
    #
    # is_deleted = delete_engineer(1)
    #
    # print(f"Удалён: {is_deleted}")
    #
    # # 8. Проверяем удаление
    # print("\n7. Проверка удаления")
    #
    # found_engineer = get_engineer_by_id(1)
    #
    # print(f"Результат поиска: {found_engineer}")


if __name__ == "__main__":
    main()