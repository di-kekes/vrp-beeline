import requests

req = requests.put("http://127.0.0.1:8000/api/generate_dataset")
print(req.json())