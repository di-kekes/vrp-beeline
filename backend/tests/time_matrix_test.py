import pytest

from backend.optimizer_v01.time_matrix import *

@pytest.mark.asyncio
async def test():
    coordinates = [
        (55.751244, 37.618423),  # Депо
        (55.760000, 37.620000),  # Заявка 1
        (55.770000, 37.630000),  # Заявка 2
    ]
    matrix = await build_time_matrix(coordinates)
    # 1. Проверяем размер матрицы
    assert len(matrix) == 3
    assert all(len(row) == 3 for row in matrix)

    # 2. Проверяем диагональ
    for i in range(3):
        assert matrix[i][i] == 0

    # 3. Проверяем, что время неотрицательное
    for row in matrix:
        for duration in row:
            assert duration >= 0

    # 4. Выводим матрицу для просмотра
    for row in matrix:
        print(row)