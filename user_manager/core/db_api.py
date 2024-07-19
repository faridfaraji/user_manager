import requests
from settings import Settings
DATABASE_URL = ""
settings = Settings()


def _gen_url(route):
    return f"{settings.database_url}/{route}"


def _make_request(method, route, **kwargs):
    response = method(_gen_url(route), **kwargs)
    response.raise_for_status()
    return response.json()


def get_prompt():
    return _make_request(requests.get, "prompts")["prompt"]
