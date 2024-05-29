from datetime import datetime
import requests
from prefs import preferences


def login(username: str, password: str) -> (bool, str, datetime):
    response = requests.post(f"{preferences['API_URL']}/login/", data={"username": username, "password": password})

    status = response.json()['status']
    code = response.status_code

    print(f"{response.json()['session_expiry']}")

    if status == "success" and code == 200:
        token = response.json().get('session_key', None)
        expiry = datetime.strptime(response.json()['session_expiry'], "%Y-%m-%dT%H:%M:%S.%fZ")
        return True, token, expiry

    return False, None, None


def register(username: str, password: str) -> (bool, str):
    response = requests.post(f"{preferences['API_URL']}/register/", data={"username": username, "password": password})

    status = response.json()['status']

    if status == "success":
        return True, None

    return False, response.json()['message']
