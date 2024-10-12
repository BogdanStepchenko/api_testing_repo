from json import JSONDecodeError

import pytest
import requests
from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_MEME, HEADERS


class PostMeme(BasicClass):
    def __init__(self, authorized_headers, username):
        super().__init__()
        self.response_json = None
        self.authorized_headers = authorized_headers
        self.username = username

    def post_new_meme_as_authorized_user(self, payload):
        self.response = requests.post(BASE_URL_MEME, json=payload, headers=self.authorized_headers)
        if self.response.status_code == 200:
            try:
                self.response_json = self.response.json()
            except JSONDecodeError:
                pytest.fail("Failed to decode JSON response")
        else:
            self.response_json = None

    def post_new_meme_as_unauthorized_user(self, payload):
        self.response = requests.post(BASE_URL_MEME, json=payload, headers=HEADERS)
        assert 'Not authorized' in self.response.text, 'Expected Not authorized message in response'

    def check_if_info_is_correct_in_response(self, expected_data):
        assert self.response_json['info'] == expected_data

    def check_if_tags_is_correct_in_response(self, expected_data):
        assert self.response_json['tags'] == expected_data

    def check_if_url_is_correct_in_response(self, expected_data):
        assert self.response_json['url'] == expected_data

    def check_if_text_is_correct_in_response(self, expected_data):
        assert self.response_json['text'] == expected_data

    def check_if_correct_username_in_response(self):
        assert self.username == self.response_json['updated_by']
