from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
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
    """
    Позволяет работать как с обычными значениями,
    так и с Enum.
    """

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
    # 1. Собираем точки
    #
    # Первые N точек — стартовые позиции инженеров.
    # Затем идут заявки.
    # ---------------------------------------------------------

    locations = []

    for engineer in engineers:
        locations.append(
            (
                engineer.start_location.latitude,
                engineer.start_location.longitude,
            )
        )

    for request in requests:
        locations.append(
            (
                request.location.latitude,
                request.location.longitude,
            )
        )


    num_engineers = len(engineers)
    num_requests = len(requests)

    # ---------------------------------------------------------
    # 2. Индексы заявок
    # ---------------------------------------------------------

    request_node_by_index = {
        request_index: num_engineers + request_index
        for request_index in range(num_requests)
    }

    # ---------------------------------------------------------
    # 3. Временная шкала
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

    # ---------------------------------------------------------
    # 4. OR-Tools Manager
    #
    # Для каждого инженера start/end — его собственная
    # стартовая точка.
    # ---------------------------------------------------------

    starts = list(range(num_engineers))
    ends = list(range(num_engineers))

    manager = pywrapcp.RoutingIndexManager(
        len(locations),
        num_engineers,
        starts,
        ends,
    )

    routing = pywrapcp.RoutingModel(manager)

    # ---------------------------------------------------------
    # 5. Travel callback
    # ---------------------------------------------------------

    def time_callback(from_index: int, to_index: int) -> int:

        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        travel_time = time_matrix[from_node][to_node]

        # Добавляем обслуживание заявки в момент,
        # когда инженер уезжает из неё.
        if from_node >= num_engineers:
            request_index = from_node - num_engineers
            service_time = requests[request_index].duration

            return travel_time + service_time

        return travel_time

    transit_callback_index = routing.RegisterTransitCallback(
        time_callback
    )

    # Основная стоимость маршрута —
    # суммарное время движения.
    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_callback_index
    )

    # ---------------------------------------------------------
    # 6. Time Dimension
    # ---------------------------------------------------------

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

    routing.AddDimension(
        transit_callback_index,
        planning_horizon,  # разрешённое ожидание
        planning_horizon,  # максимум времени маршрута
        False,
        "Time",
    )

    time_dimension = routing.GetDimensionOrDie("Time")

    # ---------------------------------------------------------
    # 7. Shift каждого инженера
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

        # OR-Tools старается определить разумное
        # начало/окончание маршрута.
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(start_index)
        )

        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(end_index)
        )

    # ---------------------------------------------------------
    # 8. Time Window каждой заявки
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
    # 9. Совместимость инженер <-> заявка
    #
    # skill
    # ---------------------------------------------------------

    for request_index, request in enumerate(requests):

        required_skill = enum_value(
            request.required_skill
        )

        if required_skill is None:
            continue

        required_skill = str(required_skill)

        allowed_engineers = []

        for engineer_id, engineer in enumerate(engineers):

            engineer_skills = normalize_skills(
                engineer.skills
            )

            if required_skill in engineer_skills:
                allowed_engineers.append(engineer_id)

        node = request_node_by_index[request_index]
        index = manager.NodeToIndex(node)

        if not allowed_engineers:
            # Ни один инженер не умеет выполнять заявку.
            # Разрешаем ей быть пропущенной через disjunction.
            continue

        routing.SetAllowedVehiclesForIndex(
            allowed_engineers,
            index,
        )

    # ---------------------------------------------------------
    # 10. Приоритеты
    #
    # Добавляем возможность пропускать заявки.
    # Чем выше priority — тем выше штраф.
    # ---------------------------------------------------------

    for request_index, request in enumerate(requests):

        priority = getattr(request, "priority", 1)

        try:
            priority = int(
                enum_value(priority)
            )
        except (ValueError, TypeError):
            priority = 1

        priority = max(1, priority)

        penalty = 100_000 * priority

        node = request_node_by_index[request_index]
        index = manager.NodeToIndex(node)

        routing.AddDisjunction(
            [index],
            penalty,
        )

    # ---------------------------------------------------------
    # 11. Алгоритм поиска
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
    # 12. Решение
    # ---------------------------------------------------------

    solution = routing.SolveWithParameters(
        search_parameters
    )

    if solution is None:
        raise RuntimeError(
            "OR-Tools не смог найти допустимое решение"
        )

    # ---------------------------------------------------------
    # 13. Разбираем результат
    # ---------------------------------------------------------

    routes = []

    assigned_request_ids = set()

    total_travel_all = 0

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

            if node >= num_engineers:

                request_index = node - num_engineers
                request = requests[request_index]

                time_var = time_dimension.CumulVar(
                    index
                )

                visit_minutes = solution.Value(
                    time_var
                )

                visit_datetime = (
                    planning_start
                    + __import__("datetime").timedelta(
                        minutes=visit_minutes
                    )
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

        total_travel_all += route_travel

    # ---------------------------------------------------------
    # 14. Невыполненные заявки
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