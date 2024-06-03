from requests import Session
from prefs import preferences
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import os


def upload_file(file_path, var, session: Session) -> str | None:
    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'rb') as f:
        file_size = os.path.getsize(file_path)
        filename = file_path.split('/')[-1]

        def progress_callback(monitor):
            progress = monitor.bytes_read / file_size
            var.set(progress)

        encoder = MultipartEncoder(
            fields={'file': (filename, f, 'application/octet-stream')}
        )
        monitor = MultipartEncoderMonitor(encoder, progress_callback)

        response = session.post(f'{preferences["API_URL"]}/upload/', data=monitor,
                                headers={'Content-Type': monitor.content_type,
                                         'filename': filename,
                                         'filesize': str(file_size)})
        return preferences["API_URL"] + response.json()['url']


def delete_file(file_token, session: Session) -> str | None:
    response = session.post(f'{preferences["API_URL"]}/delete/', data={'file_token': file_token})

    return response.json()['message']


def share_file(file_token, user, session: Session) -> str | None:
    response = session.post(f'{preferences["API_URL"]}/share/',
                            data={'file_token': file_token, 'username': user})

    return response.json()['message']


def private_file(file_token, session: Session) -> str | None:
    response = session.post(f'{preferences["API_URL"]}/private/', data={'file_token': file_token})

    return response.json()['message']
