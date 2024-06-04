from requests import Session
from prefs import preferences
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import os


def upload_file(file_path, var, session: Session, password: str | None) -> (bool, (str | None)):
    # Check if file exists
    if not os.path.isfile(file_path):
        return None

    # Check if session is provided, if it isn't assume a guest upload and create a new, unauthenticated one
    if not session:
        session = Session()

    with open(file_path, 'rb') as f:
        # Get file size and name
        file_size = os.path.getsize(file_path)
        filename = file_path.split('/')[-1]


        def progress_callback(monitor):
            progress = monitor.bytes_read / file_size
            var.set(progress)

        encoder = MultipartEncoder(
            fields={'file': (filename, f, 'application/octet-stream')}
        )
        monitor = MultipartEncoderMonitor(encoder, progress_callback)

        response = session.post(f'{preferences["API_URL"]}/file/', data=monitor,
                                headers={'Content-Type': monitor.content_type,
                                         'filename': filename,
                                         'filesize': str(file_size),
                                         'password': password})

        if response.status_code == 200:  # If the file was uploaded successfully return the download link
            return True, preferences["API_URL"] + response.json()['url']

        return False, response.json()['error']  # If the file wasn't uploaded successfully return the error message


def delete_file(file_token, session: Session) -> str | None:
    response = session.delete(f'{preferences["API_URL"]}/file/{file_token}/')

    return response.json()['message']


def share_file(file_token, user, session: Session) -> (bool, (str | None)):
    response = session.post(f'{preferences["API_URL"]}/share/{file_token}/{user}/')

    if response.status_code == 200:
        return True, response.json()['message']  # If the file was shared successfully return the success message

    return False, response.json()['error']  # If the file wasn't shared successfully return the error message


def private_file(file_token, session: Session) -> (bool, (str | None)):
    response = session.delete(f'{preferences["API_URL"]}/share/{file_token}')

    if response.status_code == 200:
        return True, response.json()['message']  # If the file was made private successfully return the success message

    return False, response.json()['error']  # If the file wasn't made private successfully return the error message
