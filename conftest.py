import pytest
import requests

from data.constants import BASE_URL, HEADERS
from data.randomizer import get_random_string
from endpoints.post_token import PostToken


@pytest.fixture(scope='function')
def create_new_token():
    payload = {
        'name': get_random_string()
    }
    creation_response = requests.post(f'{BASE_URL}/authorize', json=payload, headers=HEADERS)
    assert creation_response.status_code == 200
    try:
        created_object = creation_response.json()
    except requests.exceptions.JSONDecodeError as e:
        pytest.fail(f"Failed to decode JSON: {e}")
    return created_object['token']


@pytest.fixture(scope='function')
def post_token_endpoint():
    return PostToken()
