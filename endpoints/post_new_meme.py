from json import JSONDecodeError

import pytest
from pydantic import ValidationError
from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_MEME
from models.meme_data import MemeJson


class PostMeme(BasicClass):
    def __init__(self, username, token=None):
        super().__init__(token)
        self.username = username

    def post_new_meme_as_authorized_user(self, payload, headers=None):
        if headers:
            self.session.headers.update(headers)
        self.response = self.session.post(BASE_URL_MEME, json=payload)
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

    def post_new_meme_as_unauthorized_user(self, payload):
        self.session.headers.pop('Authorization', None)
        self.response = self.session.post(BASE_URL_MEME, json=payload)
        assert 'Not authorized' in self.response.text, 'Expected Not authorized message in response'

    def check_if_info_is_correct_in_response(self, expected_data):
        assert 'info' in self.response_json, "Field 'info' not found in response"
        assert self.response_json['info'] == expected_data, f"Expected 'info': {expected_data}, " \
                                                            f"got: {self.response_json['info']}"

    def check_if_tags_is_correct_in_response(self, expected_data):
        assert 'tags' in self.response_json, "Field 'tags' not found in response"
        assert self.response_json['tags'] == expected_data, f"Expected 'tags': {expected_data}, " \
                                                            f"got: {self.response_json['tags']}"

    def check_if_url_is_correct_in_response(self, expected_data):
        assert 'url' in self.response_json, "Field 'url' not found in response"
        assert self.response_json['url'] == expected_data, f"Expected 'url': {expected_data}, " \
                                                           f"got: {self.response_json['url']}"

    def check_if_text_is_correct_in_response(self, expected_data):
        assert 'text' in self.response_json, "Field 'text' not found in response"
        assert self.response_json['text'] == expected_data, f"Expected 'text': {expected_data}, " \
                                                            f"got: {self.response_json['text']}"

    def check_if_correct_username_in_response(self):
        assert 'updated_by' in self.response_json, "Field 'updated_by' not found in response"
        assert self.username == self.response_json['updated_by'], f"Expected username: {self.username}, " \
                                                                  f"got: {self.response_json['updated_by']}"

    def check_all_fields_in_response(self, expected_data):
        self.check_if_info_is_correct_in_response(expected_data['info'])
        self.check_if_tags_is_correct_in_response(expected_data['tags'])
        self.check_if_url_is_correct_in_response(expected_data['url'])
        self.check_if_text_is_correct_in_response(expected_data['text'])
        self.check_if_correct_username_in_response()
