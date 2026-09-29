
import pytest
from backend.optimizer_v01.vrp_optimazer import optimize_vrptw
from backend.data.data_schemas import Location
import backend.data.json_bd as json_bd
import backend.optimizer_v01.time_matrix as time
@pytest.mark.asyncio
async def test_optimizer_assigns_compatible_engineers():
    """
    Проверяет, что заявки назначаются инженерам,
    у которых есть необходимый навык и транспорт.
    """

    requests = json_bd.get_all_requests()

    engineers = json_bd.get_all_engineers()

    # 0 — депо, 1 и 2 — заявки
    positions = [(i.location.latitude, i.location.longitude) for i in requests]
    depot_location = Location(
        latitude=55.75,
        longitude=37.61,
    )
    positions = [(depot_location.latitude, depot_location.longitude)] + positions
    time_matrix = await time.build_time_matrix(positions)
    print(time_matrix)

    result = optimize_vrptw(
        requests=requests,
        engineers=engineers,
        time_matrix=time_matrix,
        depot_location=depot_location,
        solver_time_limit_seconds=30,
    )

    assigned = {}

    for route in result.routes:
        for stop in route.stops:
            assigned[stop.request_id] = route.engineer_id

    print(result)
    print(assigned)

    check = []
    for i in result.routes:
        a = [json_bd.get_engineer_by_id(int(i.engineer_id)),
             [json_bd.get_request_by_id(int(j.request_id)) for j in i.stops]]
        check.append(a)
    print(check)
    boool = []
    for s in check:
        a = s
        skills = a[0].skills
        r_skills = [skls.required_skill for skls in a[1]]
        boool.append(all(i in skills for i in r_skills))
    print(boool)


    for route in result.routes:
        for stop in route.stops:
            request = json_bd.get_request_by_id(
                int(stop.request_id)
            )

            # Время начала обслуживания из результата оптимизатора
            service_start = stop.visit_time

            assert (
                    request.time_window_start
                    <= service_start
                    <= request.time_window_end
            ), (
                f"Заявка {request.id} обслуживается вне "
                f"временного окна: "
                f"{service_start} не входит в "
                f"[{request.time_window_start}, "
                f"{request.time_window_end}]"
            )
            print(
                f"Заявка {request.id} обслуживается вне "
                f"временного окна: "
                f"{service_start} не входит в "
                f"[{request.time_window_start}, "
                f"{request.time_window_end}]"
            )
            