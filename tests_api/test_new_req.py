import requests
#Создание новой задачи
data = {
    "id":4,
    "location":{"latitude":87.542,
                "longitude":43.452,
                "address":"какойто адресс24"},
    "priority": "default",
    "required_skill":"connection_client",
    "time_window_start":"2008-06-17",
    "time_window_end" :"2008-06-18",
    "duration":[20, 80,  0]
}
#Создание новой задачи
req = requests.post("http://127.0.0.1:8000/api/urgent_request",json=data)
print(req.json())