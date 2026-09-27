import requests
with open("../dataset/Восток Синтетические данные.csv") as file:
    files = {"file":file}
    req = requests.post("http://127.0.0.1:8000/api/upload_csv",files=files)
    print(req.json())