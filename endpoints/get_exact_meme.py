import pytest
import requests

from json import JSONDecodeError
from pydantic import ValidationError
from endpoints.basic_class import BasicClass
from models.meme_data import MemeJson
from data.constants import BASE_URL_MEME, HEADERS


class GetExactMeme(BasicClass):

    def __init__(self, authorized_headers):
        super().__init__()
        self.response_json = None
        self.authorized_headers = authorized_headers

    def get_meme_by_id(self, meme_id, headers):
        self.response = requests.get(f"{BASE_URL_MEME}/{meme_id}", headers=headers)
        if self.response.status_code == 200:
            try:
                self.response_json = self.response.json()
                try:
                    MemeJson(**self.response_json)
                except ValidationError as e:
                    pytest.fail(f"Validation Error: {e}\nResponse: {self.response_json}")
            except JSONDecodeError:
                pytest.fail("Failed to decode JSON response")
        else:
            self.response_json = None

    def check_get_exact_meme_as_authorized_user(self, meme_id, expect_deleted=False):
        self.get_meme_by_id(meme_id, headers=self.authorized_headers)
        if self.response.status_code == 404:
            if expect_deleted:
                assert self.response_json is None, "Expected response JSON to be None for deleted meme."
            else:
                assert False, f"Meme with ID {meme_id} was not found, but it should exist."
            return None
        if self.response.status_code == 200:
            assert self.response_json is not None, "Response JSON is None for valid meme ID."
            assert 'id' in self.response_json, "Response JSON does not contain 'id'"
            assert self.response_json['id'] == meme_id, f"Expected ID {meme_id}, but got {self.response_json['id']}"
            assert 'url' in self.response_json, "Response JSON does not contain 'url'"
            assert self.response_json['url'].startswith('http'), 'URL should start with http or https'
        else:
            assert False, "Response JSON is None. Possibly invalid token or no JSON in the response."

    def check_meme_fields_in_response(self):
        try:
            MemeJson(**self.response_json)
        except ValidationError as e:
            print(f"Response: {self.response_json}")
            pytest.fail(f"Validation failed: {e}")

    def check_get_exact_meme_as_unauthorized_user(self, meme_id):
        self.get_meme_by_id(meme_id, headers=HEADERS)
        assert 'Not authorized' in self.response.text, 'Expected Not authorized message in response'

    def check_get_non_existed_meme(self, meme_id):
        self.get_meme_by_id(meme_id, headers=self.authorized_headers)
        assert 'Not Found' in self.response.text, 'Meme ID is not correct! Please, try with another id'
