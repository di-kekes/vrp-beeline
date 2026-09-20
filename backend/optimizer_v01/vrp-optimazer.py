
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2,
)


@dataclass
class StopResult:
    request_id: str
    visit_time: datetime
    duration_minutes: int


@dataclass
class RouteResult:
    engineer_id: str
    stops: list[StopResult]
    total_travel_minutes: int
    total_route_minutes: int


@dataclass
class OptimizationResult:
    routes: list[RouteResult]
    unassigned_requests: list[str]


def enum_value(value: Any) -> Any:
    if hasattr(value, "value"):
        return value.value
    return value


def normalize_skills(skills: list[Any] | None) -> set[str]:
    if not skills:
        return set()

    return {
        str(enum_value(skill))
        for skill in skills
    }


def parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value

    return datetime.fromisoformat(value)


def optimize_vrptw(
    requests: list[Any],
    engineers: list[Any],
    time_matrix: list[list[int]],
    depot_location: Any,
    solver_time_limit_seconds: int = 10,
) -> OptimizationResult:

    if not engineers:
        raise ValueError("Список инженеров пуст")

    if not requests:
        return OptimizationResult(
            routes=[],
            unassigned_requests=[],
        )

    # ---------------------------------------------------------
    # 1. Проверка матрицы и создание точек
    # ---------------------------------------------------------

    num_engineers = len(engineers)
    num_requests = len(requests)

    locations = [
        (
            depot_location.latitude,
            depot_location.longitude,
        )
    ]

    for request in requests:
        locations.append(
            (
                request.location.latitude,
                request.location.longitude,
            )
        )

    expected_size = num_requests + 1

    if len(time_matrix) != expected_size:
        raise ValueError("Неверный размер time_matrix")

    if any(len(row) != expected_size for row in time_matrix):
        raise ValueError("Матрица времени должна быть квадратной")

    # Узел заявки: 1 ... N
    request_node_by_index = {
        request_index: request_index + 1
        for request_index in range(num_requests)
    }

    # ---------------------------------------------------------
    # 2. Временная шкала
    # ---------------------------------------------------------

    all_start_times = []

    for engineer in engineers:
        all_start_times.append(
            parse_datetime(engineer.shift_start)
        )

    for request in requests:
        all_start_times.append(
            parse_datetime(request.time_window_start)
        )

    planning_start = min(all_start_times)

    def to_minutes(value: datetime) -> int:
        return int(
            (value - planning_start).total_seconds() / 60
        )

    planning_horizon = max(
        to_minutes(
            max(
                parse_datetime(request.time_window_end)
                for request in requests
            )
        ),
        max(
            to_minutes(
                parse_datetime(engineer.shift_end)
            )
            for engineer in engineers
        ),
    )

    # ---------------------------------------------------------
    # 3. OR-Tools Manager
    # Все инженеры начинают и заканчивают в одном депо
    # ---------------------------------------------------------

    starts = [0] * num_engineers
    ends = [0] * num_engineers

    manager = pywrapcp.RoutingIndexManager(
        len(locations),
        num_engineers,
        starts,
        ends,
    )

    routing = pywrapcp.RoutingModel(manager)

    # ---------------------------------------------------------
    # 4. Travel callback
    # Время обслуживания добавляется после посещения узла
    # ---------------------------------------------------------

    def time_callback(
        from_index: int,
        to_index: int,
    ) -> int:

        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        travel_time = time_matrix[from_node][to_node]

        if from_node > 0:
            request_index = from_node - 1
            service_time = int(
                requests[request_index].duration
            )

            return travel_time + service_time

        return travel_time

    transit_callback_index = routing.RegisterTransitCallback(
        time_callback
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_callback_index
    )

    # ---------------------------------------------------------
    # 5. Time Dimension
    # ---------------------------------------------------------

    routing.AddDimension(
        transit_callback_index,
        planning_horizon,  # Разрешённое ожидание
        planning_horizon,  # Максимальное время
        False,
        "Time",
    )

    time_dimension = routing.GetDimensionOrDie("Time")

    # ---------------------------------------------------------
    # 6. Смены инженеров
    # ---------------------------------------------------------

    for vehicle_id, engineer in enumerate(engineers):

        start_index = routing.Start(vehicle_id)
        end_index = routing.End(vehicle_id)

        shift_start = to_minutes(
            parse_datetime(engineer.shift_start)
        )

        shift_end = to_minutes(
            parse_datetime(engineer.shift_end)
        )

        time_dimension.CumulVar(start_index).SetRange(
            shift_start,
            shift_end,
        )

        time_dimension.CumulVar(end_index).SetRange(
            shift_start,
            shift_end,
        )

        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(start_index)
        )

        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(end_index)
        )

    # ---------------------------------------------------------
    # 7. Временные окна заявок
    # CumulVar заявки = начало обслуживания
    # ---------------------------------------------------------

    for request_index, request in enumerate(requests):

        node = request_node_by_index[request_index]
        index = manager.NodeToIndex(node)

        window_start = to_minutes(
            parse_datetime(request.time_window_start)
        )

        window_end = to_minutes(
            parse_datetime(request.time_window_end)
        )

        time_dimension.CumulVar(index).SetRange(
            window_start,
            window_end,
        )

    # ---------------------------------------------------------
    # 8. Совместимость навыков и транспорта
    # ---------------------------------------------------------

    for request_index, request in enumerate(requests):

        required_skill = enum_value(
            request.required_skill
        )

        required_skill = (
            str(required_skill)
            if required_skill is not None
            else None
        )

        required_vehicle = enum_value(
            getattr(
                request,
                "required_vehicle",
                None,
            )
        )

        required_vehicle = (
            str(required_vehicle)
            if required_vehicle is not None
            else None
        )

        allowed_engineers = []

        for engineer_id, engineer in enumerate(engineers):

            engineer_skills = normalize_skills(
                engineer.skills
            )

            engineer_vehicle = str(
                enum_value(engineer.vehicle_type)
            )

            skill_match = (
                required_skill is None
                or required_skill in engineer_skills
            )

            vehicle_match = (
                required_vehicle is None
                or engineer_vehicle == required_vehicle
            )

            if skill_match and vehicle_match:
                allowed_engineers.append(engineer_id)

        node = request_node_by_index[request_index]
        index = manager.NodeToIndex(node)

        routing.SetAllowedVehiclesForIndex(
            allowed_engineers,
            index,
        )

    # ---------------------------------------------------------
    # 9. Приоритеты и необслуженные заявки
    #
    # NORMAL -> можно не выполнять, но за это большой штраф
    # URGENT -> обязательна к выполнению
    # ---------------------------------------------------------

    for request_index, request in enumerate(requests):

        priority = enum_value(
            getattr(request, "priority", "default")
        )

        priority = str(priority).lower()

        node = request_node_by_index[request_index]
        index = manager.NodeToIndex(node)

        if priority == "urgent":
            # Срочная заявка ОБЯЗАТЕЛЬНА.
            # Не добавляем Disjunction -> OR-Tools не может её пропустить.
            continue

        elif priority == "default":
            # Обычную заявку можно не выполнять,
            # но это будет сильно штрафоваться.
            penalty = 100_000

            routing.AddDisjunction(
                [index],
                penalty,
            )

        else:
            raise ValueError(
                f"Неизвестный приоритет заявки: {priority}"
            )

    # ---------------------------------------------------------
    # 10. Алгоритм поиска
    # ---------------------------------------------------------

    search_parameters = (
        pywrapcp.DefaultRoutingSearchParameters()
    )

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.FromSeconds(
        solver_time_limit_seconds
    )

    # ---------------------------------------------------------
    # 11. Решение
    # ---------------------------------------------------------

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if solution is None:
        raise RuntimeError(
            "OR-Tools не смог найти допустимое решение"
        )

    # ---------------------------------------------------------
    # 12. Разбор маршрутов
    # ---------------------------------------------------------

    routes = []
    assigned_request_ids = set()

    for vehicle_id, engineer in enumerate(engineers):

        if not routing.IsVehicleUsed(
            solution,
            vehicle_id,
        ):
            continue

        index = routing.Start(vehicle_id)

        route_stops = []
        route_travel = 0

        while not routing.IsEnd(index):

            node = manager.IndexToNode(index)

            if node > 0:

                request_index = node - 1
                request = requests[request_index]

                time_var = time_dimension.CumulVar(index)

                visit_minutes = solution.Value(time_var)

                visit_datetime = (
                    planning_start
                    + timedelta(minutes=visit_minutes)
                )

                route_stops.append(
                    StopResult(
                        request_id=str(request.id),
                        visit_time=visit_datetime,
                        duration_minutes=int(
                            request.duration
                        ),
                    )
                )

                assigned_request_ids.add(
                    str(request.id)
                )

            next_index = solution.Value(
                routing.NextVar(index)
            )

            route_travel += time_matrix[
                node
            ][
                manager.IndexToNode(next_index)
            ]

            index = next_index

        end_time = solution.Value(
            time_dimension.CumulVar(index)
        )

        start_time = solution.Value(
            time_dimension.CumulVar(
                routing.Start(vehicle_id)
            )
        )

        total_route_time = end_time - start_time

        routes.append(
            RouteResult(
                engineer_id=str(engineer.id),
                stops=route_stops,
                total_travel_minutes=route_travel,
                total_route_minutes=total_route_time,
            )
        )

    # ---------------------------------------------------------
    # 13. Невыполненные заявки
    # ---------------------------------------------------------

    unassigned = [
        str(request.id)
        for request in requests
        if str(request.id) not in assigned_request_ids
    ]

    return OptimizationResult(
        routes=routes,
        unassigned_requests=unassigned,
    )