import requests
from settings import Settings
DATABASE_URL = ""
settings = Settings()
import threading
import base64

def _gen_url(route):
    return f"{settings.chat_url}/{route}"


def _make_request(method, route, **kwargs):
    response = method(_gen_url(route), **kwargs)
    response.raise_for_status()
    return response.json()


def submit_edited_image(thread_id, file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    print(encoded_string)
    _make_request(requests.post, f"image-edit/{thread_id}", json={"base64": encoded_string})
