import requests
from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_AUTHORIZE, HEADERS


class GetToken(BasicClass):

    def __init__(self):
        super().__init__()
        self.text_response = None

    def check_is_token_valid(self, token):
        self.response = requests.get(f"{BASE_URL_AUTHORIZE}/{token}", headers=HEADERS)
        if self.response.status_code == 200:
            self.text_response = self.response.text
            assert "Token is alive" in self.text_response, 'Token is not alive'
            return True
        else:
            return False, f"Invalid status code: {self.response.status_code}"

    def check_is_name_in_token_correct(self, name):
        assert self.response is not None, 'Response is not available'
        assert self.response.status_code == 200, f"Response status code is not correct: {self.response.status_code}"
        assert self.text_response is not None, "No JSON response available"
        assert 'Username is ' in self.text_response, 'Username is not in response'
        assert self.text_response.split('Username is ')[-1] == name
