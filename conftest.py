import pytest
import requests

from data.constants import BASE_URL_AUTHORIZE, HEADERS
from data.randomizer import get_random_string

from endpoints.post_token import PostToken
from endpoints.get_token import GetToken
from endpoints.get_all_meme import GetAllMemes


@pytest.fixture(scope='function')
def create_new_token():
    name = get_random_string()
    payload = {'name': name}
    creation_response = requests.post(BASE_URL_AUTHORIZE, json=payload, headers=HEADERS)
    assert creation_response.status_code == 200
    try:
        created_object = creation_response.json()
    except requests.exceptions.JSONDecodeError as e:
        pytest.fail(f"Failed to decode JSON: {e}")
    token = created_object['token']
    assert 'token' in created_object
    return token, name


@pytest.fixture(scope='function')
def post_token_endpoint():
    return PostToken()


@pytest.fixture(scope='function')
def get_token_endpoint():
    return GetToken()


@pytest.fixture(scope='function')
def get_all_memes(get_authorized_headers):
    return GetAllMemes(get_authorized_headers)


@pytest.fixture(scope='function')
def token(create_new_token):
    token, name = create_new_token
    return token


@pytest.fixture(scope='function')
def name(create_new_token):
    token, name = create_new_token
    return name


@pytest.fixture(scope='function')
def get_authorized_headers(token):
    headers = {**HEADERS, 'Authorization': token}
    return headers
