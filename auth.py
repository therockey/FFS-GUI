from datetime import datetime
import requests
from requests import Session
from prefs import preferences


def login(username: str, password: str) -> (bool, Session | str, datetime):
    response = requests.post(f"{preferences['API_URL']}/login/", data={"username": username, "password": password})

    response_dict = response.json()

    status = response_dict['status']
    code = response.status_code

    if status == "success" and code == 200:
        token = response_dict['session_key']
        session = Session()
        session.cookies['sessionid'] = token
        expiry = datetime.strptime(response_dict['session_expiry'], "%Y-%m-%dT%H:%M:%S.%fZ")

        return True, session, expiry

    return False, response_dict['message'], None


def register(username: str, password: str) -> (bool, str):
    response = requests.post(f"{preferences['API_URL']}/register/", data={"username": username, "password": password})

    status = response.json()['status']

    if status == "success":
        return True, None

    return False, response.json()['message']


def get_file_list(session: Session) -> list:
    response = session.get(f"{preferences['API_URL']}/user_filenames/")

    return response.json()


def check_connection():
    try:
        response = requests.get(preferences['API_URL'])
    except requests.exceptions.ConnectionError:
        return False

    return True
