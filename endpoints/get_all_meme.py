from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_MEME, HEADERS


class GetAllMemes(BasicClass):

    def __init__(self, token=None):
        super().__init__(token)

    def check_get_all_memes_with_valid_token(self):
        self.response = self.session.get(BASE_URL_MEME)
        assert self.response.status_code == 200, f"Expected status code 200, but got {self.response.status_code}"
        self.response_json = self.response.json()
        assert isinstance(self.response_json, dict), 'Expected response is dict'
        assert 'data' in self.response_json, 'Key "data" is expected in response'
        memes = self.response_json['data']
        assert len(memes) > 0, 'Expected at least one meme in list'

    def check_get_all_memes_with_invalid_token(self, invalid_headers):
        self.response = self.session.get(BASE_URL_MEME, headers=invalid_headers)
        assert self.response.status_code == 401, f"Expected status code 401, but got {self.response.status_code}"
        if self.response.text:
            assert "error" in self.response.text.lower() or "unauthorized" in self.response.text.lower(), \
                "Expected an error message in response when using an invalid token"

    def check_all_memes_have_id_field(self):
        memes = self.response_json['data']
        for meme in memes:
            assert 'id' in meme, f'Field "id" is missing in {meme}'

    def check_all_memes_have_info_field(self):
        memes = self.response_json['data']
        for meme in memes:
            assert 'info' in meme, f'Field "info" is missing in {meme}'

    def check_all_memes_have_tags_field(self):
        memes = self.response_json['data']
        for meme in memes:
            assert 'tags' in meme, f'Field "tags" is missing in {meme}'

    def check_all_memes_have_text_field(self):
        memes = self.response_json['data']
        for meme in memes:
            assert 'text' in meme, f'Field "text" is missing in {meme}'

    def check_all_memes_have_updated_by_field(self):
        memes = self.response_json['data']
        for meme in memes:
            assert 'updated_by' in meme, f'Field "updated_by" is missing in {meme}'

    def check_all_memes_have_url_field(self):
        memes = self.response_json['data']
        for meme in memes:
            assert 'url' in meme, f'Field "url" is missing in {meme}'

    def check_all_memes_have_unique_id(self):
        memes = self.response_json['data']
        ids = set(map(lambda meme: meme['id'], memes))
        assert len(ids) == len(memes), 'Not all IDs are unique'

    def check_get_all_memes_as_unauthorized_user(self):
        self.session.headers.pop('Authorization', None)
        self.response = self.session.get(BASE_URL_MEME, headers=HEADERS)
        assert 'Not authorized' in self.response.text, 'Expected Not authorized message in response'

    def check_get_all_memes_with_authorization_but_without_token(self):
        headers = {**HEADERS, 'Authorization': ""}
        self.session.headers.update(headers)
        self.response = self.session.get(BASE_URL_MEME, headers=headers)
        assert self.response.status_code == 401, f'Response status code is incorrect: {self.response.status_code}'
        assert 'Not authorized' in self.response.text, 'Expected Not authorized message in response'
