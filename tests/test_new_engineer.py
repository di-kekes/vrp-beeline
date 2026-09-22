import requests
#Создание новой задачи
data = {
    "id":2,
    "name":"Петя",
    "start_location":{"latitude":87.542,
                "longitude":43.452,
                "address":"какойто адресс24"},
    "skills":["connection_client","accidents_on_tkd"],
    "shift_start":"2008-06-17",
    "shift_end" :"2008-06-18",
    "vehicle_type":"bicycle"
}
#Создание новой задачи
req = requests.post("http://127.0.0.1:8000/api/add_engineer",json=data)
print(req.json())