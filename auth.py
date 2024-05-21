import requests
from prefs import preferences


def login(username: str, password: str) -> (bool, str):
    response = requests.post(f"{preferences['API_URL']}/login/", data={"username": username, "password": password})
    return (True, "success") if response.status_code == 200 and response.json()['status'] == "success" else (
        False, response.json()['message'])


def register(username: str, password: str) -> (bool, str):
    response = requests.post(f"{preferences['API_URL']}/register/", data={"username": username, "password": password})
    return (True, "success") if response.status_code == 200 and response.json()['status'] == "success" else (
        False, response.json()['message'])


def get_token() -> str:
    response = requests.get(f"{preferences['API_URL']}/getcsrf/")
    return response.json()["csrf_token"] if response.status_code == 200 else None
