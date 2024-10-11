import requests
from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_AUTHORIZE, HEADERS


class PostToken(BasicClass):

    def __init__(self):
        super().__init__()
        self.creation_response = None
        self.created_object = None

    def create_new_token(self, name):
        payload = {
            'name': name
        }
        self.creation_response = requests.post(BASE_URL_AUTHORIZE, json=payload, headers=HEADERS)
        self.response = self.creation_response
        if self.response.status_code == 200:
            try:
                self.created_object = self.creation_response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                raise
        else:
            self.created_object = None
        assert self.created_object is not None, "Failed to create the object"
        return self.created_object

    def check_is_token_was_created(self):
        assert self.created_object is not None, "Created object is None, token creation failed"

    def check_is_token_in_response(self):
        assert self.created_object is not None, "Created object is None, token creation failed"
        assert 'token' in self.created_object, "Response does not contain 'token'"

    def check_is_name_in_response(self):
        assert self.created_object is not None, "Created object is None, token creation failed"
        assert 'user' in self.created_object, "Response does not contain 'token'"
