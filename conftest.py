import pytest
import requests

from data.constants import BASE_URL_AUTHORIZE, BASE_URL_MEME, HEADERS
from data.payloads_for_meme_creation import CORRECT_PAYLOAD
from data.randomizer import get_random_string
from endpoints.post_token import PostToken
from endpoints.get_token import GetToken
from endpoints.get_all_meme import GetAllMemes
from endpoints.get_exact_meme import GetExactMeme
from endpoints.post_new_meme import PostMeme
from endpoints.put_existed_meme import PutMeme
from endpoints.delete_meme import DeleteMeme


@pytest.fixture(scope='function')
def create_new_token(post_token_endpoint):
    name = get_random_string()
    post_token_endpoint.create_new_token(name)
    post_token_endpoint.check_status_code(200)
    token = post_token_endpoint.get_token_from_response()
    return token, name


@pytest.fixture(scope='function')
def create_new_meme_without_deletion(post_new_meme, delete_meme):
    payload = CORRECT_PAYLOAD
    post_new_meme.post_new_meme_as_authorized_user(payload)
    new_meme = post_new_meme.response_json
    return new_meme


@pytest.fixture(scope='function')
def create_new_meme(post_new_meme, delete_meme):
    payload = CORRECT_PAYLOAD
    post_new_meme.post_new_meme_as_authorized_user(payload)
    new_meme = post_new_meme.response_json

    token = post_new_meme.session.headers.get('Authorization')

    delete_meme_with_token = DeleteMeme(token)

    assert 'Authorization' in delete_meme_with_token.session.headers, 'Authorization header is missing in delete session'

    yield new_meme, delete_meme_with_token, token

    meme_id = new_meme['id']
    delete_meme_with_token.as_authorized_user(meme_id)
    delete_meme_with_token.check_status_code(200)


@pytest.fixture(scope='function')
def post_token_endpoint():
    return PostToken()


@pytest.fixture(scope='function')
def get_token_endpoint():
    return GetToken()


@pytest.fixture(scope='function')
def get_all_memes(token):
    return GetAllMemes(token)


@pytest.fixture(scope='function')
def get_exact_meme(token):
    return GetExactMeme(token)


@pytest.fixture(scope='function')
def post_new_meme(name, token):
    return PostMeme(name, token)


@pytest.fixture(scope='function')
def put_existed_meme(name, token):
    return PutMeme(name, token)


@pytest.fixture(scope='function')
def delete_meme(token):
    return DeleteMeme(token)


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


@pytest.fixture(scope='function')
def get_created_meme_id(create_new_meme):
    new_meme, _, _ = create_new_meme
    return new_meme['id']


@pytest.fixture(scope='function')
def get_meme_id_without_deletion(create_new_meme_without_deletion):
    return create_new_meme_without_deletion['id']
