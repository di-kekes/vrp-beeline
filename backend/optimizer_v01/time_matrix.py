import httpx


OSRM_URL = "https://router.project-osrm.org"


async def build_time_matrix(
    coordinates: list[tuple[float, float]],
) -> list[list[int]]:
    """
    coordinates:
        [(latitude, longitude), ...]

    Возвращает матрицу времени в минутах.
    """

    # OSRM ожидает longitude,latitude
    coordinate_string = ";".join(
        f"{lon},{lat}"
        for lat, lon in coordinates
    )

    url = (
        f"{OSRM_URL}/table/v1/driving/"
        f"{coordinate_string}"
    )

    params = {
        "annotations": "duration",
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(
            url,
            params=params,
        )

        response.raise_for_status()
        data = response.json()

    if data["code"] != "Ok":
        raise RuntimeError(
            f"OSRM error: {data['code']}"
        )

    durations = data["durations"]

    return [
        [
            0 if duration is None
            else max(0, round(duration / 60))
            for duration in row
        ]
        for row in durations
    ]
