import requests
from data.constants import HEADERS


class BasicClass:
    def __init__(self, token=None):
        self.response = None
        self.response_json = None
        self.response_text = None
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        if token:
            self.session.headers.update({'Authorization': token})

    def check_status_code(self, code):
        if self.response is None:
            raise ValueError("Response is None. Can not check status code.")
        if self.response.status_code != code:
            raise ValueError(f"Expected status code {code}, but we got {self.response.status_code}.")
