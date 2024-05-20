import requests
from prefs import preferences


def login(username: str, password: str) -> bool:
    print(username, password)
    response = requests.post(f"{preferences['API_URL']}/login/", data={"username": username, "password": password})
    return True if response.status_code == 200 and response.json()['status'] == "success" else False


def register(username: str, password: str) -> bool:
    response = requests.post(f"{preferences['API_URL']}/register/", data={"username": username, "password": password})
    return True if response.status_code == 200 and response.json()['status'] == "success" else False


def get_token() -> str:
    response = requests.get(f"{preferences['API_URL']}/getcsrf/")
    return response.json()["csrf_token"] if response.status_code == 200 else None


if __name__ == "__main__":
    print(get_token())
