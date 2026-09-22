from pprint import pprint

import requests

req = requests.get("http://127.0.0.1:8000/api/get_requests")
pprint(req.json())