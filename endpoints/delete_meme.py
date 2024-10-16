import requests
from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_MEME, HEADERS


class DeleteMeme(BasicClass):

    def __init__(self, authorized_headers):
        super().__init__()
        self.response_text = None
        self.authorized_headers = authorized_headers

    def delete_existed_meme_as_authorized_user(self, meme_id):
        self.response = requests.delete(f'{BASE_URL_MEME}/{meme_id}', headers=self.authorized_headers)
        if self.response.status_code == 200:
            self.response_text = self.response.text
            assert f'Meme with id {meme_id} successfully deleted' in self.response_text, 'Meme WAS NOT deleted'
        else:
            assert False, f"Invalid status code: {self.response.status_code}"

    def delete_existed_meme_as_unauthorized_user(self, meme_id):
        self.response = requests.delete(f'{BASE_URL_MEME}/{meme_id}', headers=HEADERS)
        assert 'Not authorized' in self.response.text, 'Expected "Not authorized" message is NOT in response'
