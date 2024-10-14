import pytest
import requests

from json import JSONDecodeError
from pydantic import ValidationError
from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_MEME, HEADERS
from models.meme_data import MemeJson


class PutMeme(BasicClass):
    def __init__(self, authorized_headers, username):
        super().__init__()
        self.response_json = None
        self.authorized_headers = authorized_headers
        self.username = username

    def update_meme_as_authorized_user_and_id(self, create_new_meme, payload):
        meme_id = create_new_meme
        self.response = requests.put(f'{BASE_URL_MEME}/{meme_id}', json=payload, headers=self.authorized_headers)
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

    def check_if_id_was_changed_properly(self, expected_data):
        if self.response_json is None:
            raise ValueError("Response JSON is None, cannot check ID.")
        assert 'id' in self.response_json, "Response JSON does not contain 'id'"
        assert expected_data['id'] == int(self.response_json['id']), 'ID was changed!'

    def check_if_info_was_changed_properly(self, expected_data):
        if self.response_json is None:
            raise ValueError("Response JSON is None, cannot check 'info'.")
        assert 'info' in self.response_json, "Response JSON does not contain 'info'"
        assert expected_data['info'] == self.response_json['info'], 'INFO was not changed!'

    def check_if_tags_were_changed_properly(self, expected_data):
        if self.response_json is None:
            raise ValueError("Response JSON is None, cannot check 'tags'.")
        assert 'tags' in self.response_json, "Response JSON does not contain 'tags'"
        assert expected_data['tags'] == self.response_json['tags'], 'TAGS were not changed!'

    def check_if_text_was_changed_properly(self, expected_data):
        assert 'text' in self.response_json, "Response JSON does not contain 'text'"
        assert expected_data['text'] == self.response_json['text'], 'TEXT was not changed!'

    def check_if_url_was_changed_properly(self, expected_data):
        if self.response_json is None:
            raise ValueError("Response JSON is None, cannot check 'url'.")
        assert 'url' in self.response_json, "Response JSON does not contain 'url'"
        assert expected_data['url'] == self.response_json['url'], 'URL was not changed!'

    def check_if_name_was_not_changed_properly(self):
        if self.response_json is None:
            raise ValueError("Response JSON is None, cannot check 'updated_by'.")
        assert 'updated_by' in self.response_json, "Response JSON does not contain 'updated_by'"
        assert self.response_json['updated_by'] == self.username, 'UPDATED_BY was changed!'

    def update_meme_as_unauthorized_user_and_id(self, create_new_meme, payload):
        meme_id = create_new_meme
        self.response = requests.put(f'{BASE_URL_MEME}/{meme_id}', json=payload, headers=HEADERS)
        assert 'Not authorized' in self.response.text, 'Expected Not authorized message in response'
