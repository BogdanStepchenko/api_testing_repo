class BasicClass:
    def __init__(self):
        self.response = None

    def check_status_code(self, code):
        if self.response is None:
            raise ValueError("Response is None. Can not check status code.")
        if self.response.status_code != code:
            raise ValueError(f"Expected status code {code}, but we got {self.response.status_code}.")
