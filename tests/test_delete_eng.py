import requests
#Создание новой задачи
data = {
        "id": 1,
        "name": "Иван Сидоров",
        "start_location": {
            "latitude": 55.7558,
            "longitude": 37.6173,
            "address": "Москва"
        },
        "shift_start": "2026-09-17T09:00:00+03:00",
        "shift_end": "2026-09-17T18:00:00+03:00",
        "skills": [
            "connection_client",
            "accidents_on_tkd"
        ],
        "vehicle_type": "car"
    }
#Создание новой задачи
req = requests.delete("http://127.0.0.1:8000/api/engineer_unavailable",json=data)
print(req.json())