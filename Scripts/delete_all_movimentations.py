import requests
BASE_URL = "http://127.0.0.1:8000"

for i in range(40):
    delete = requests.delete(f"{BASE_URL}/movimentation/Delete_movimentation/{i}")
    