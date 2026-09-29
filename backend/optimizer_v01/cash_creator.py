import json
import os

from pydantic import TypeAdapter

import backend.data.data_schemas as schemas
import backend.data.json_bd as db
import backend.optimizer_v01.time_matrix as time
from backend.optimizer_v01.vrp_optimazer import optimize_vrptw, OptimizationResult


async def initialize_optimizer_cash(api_flag = False):
    # если api_flag = True, запрос пришел от фронтенда, необходимо пересчитать план
    db.initialize_database()
    type_adapter = TypeAdapter(OptimizationResult)

    file_path = 'backend/data/data_json/optimizer_cash.json'
    should_write = False

    # 1. Проверяем, существует ли файл и есть ли в нем данные
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

                # Если файл содержит только пустой словарь
                if content == '{}':
                    should_write = True
                else:
                    existing_data = json.loads(content)
                    # Если это словарь и он пустой (на всякий случай)
                    if isinstance(existing_data, dict) and not existing_data:
                        should_write = True
                    # Если там НЕ словарь (например, поврежденная структура или массив)
                    elif not isinstance(existing_data, dict):
                        should_write = True
                    else:
                        # В файле НЕ пустой словарь. Ничего не делаем.
                        should_write = False
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Если файл поврежден, разрешаем перезапись
            should_write = True
    else:
        # Если файл вообще пустой или не существует
        should_write = True
    # пересчет если запрос пришел из фронтенда
    if api_flag == True:
        should_write = True
    # 2. Записываем данные только если файл был пуст, поврежден или содержал {}, или запрос пришел из фронтенда
    if should_write:
        # ИСПРАВЛЕНО: добавлен await перед вызовом асинхронной функции
        optimization_result = await get_optimization()

        # Проверяем, что оптимизатор вернул данные, а не None из-за ошибки
        # Новый исправленный код
        if optimization_result is not None:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 1. Pydantic сам переведет datetime в строки и вернет JSON-строку байт
                json_bytes = type_adapter.dump_json(optimization_result, by_alias=True)
                # 2. Декодируем байты в обычный текст
                json_string = json_bytes.decode('utf-8')

                # 3. Дополнительно форматируем через встроенный json для красивых отступов (indent)
                parsed_json = json.loads(json_string)
                json.dump(parsed_json, f, ensure_ascii=False, indent=4)


async def get_optimization() -> OptimizationResult | None:
    # ИСПРАВЛЕНО: по умолчанию ставим None, чтобы не возвращать сам класс
    # OptimizationResult в случае ошибки внутри блока try
    result = None
    try:
        requests = db.get_all_requests()
        engineers = db.get_all_engineers()

        # 0 — депо, 1 и 2 — заявки
        positions = [(i.location.latitude, i.location.longitude) for i in requests]
        depot_location = schemas.Location(
            latitude=engineers[0].start_location.latitude,
            longitude=engineers[0].start_location.longitude,
        )
        positions = [(depot_location.latitude, depot_location.longitude)] + positions
        time_matrix = await time.build_time_matrix(positions)

        result = optimize_vrptw(
            requests=requests,
            engineers=engineers,
            time_matrix=time_matrix,
            depot_location=depot_location,
            solver_time_limit_seconds=30,
        )
    except Exception as e:
        print(f"Ошибка в работе оптимизатора: {e}")
    return result
