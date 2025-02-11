from endpoints.basic_class import BasicClass
from data.constants import BASE_URL_MEME


class DeleteMeme(BasicClass):

    def __init__(self, token=None):
        super().__init__(token)

    def _delete_meme(self, meme_id):
        return self.session.delete(f'{BASE_URL_MEME}/{meme_id}')

    def as_authorized_user(self, meme_id):
        self.response = self._delete_meme(meme_id)
        if self.response.status_code == 200:
            self.response_text = self.response.text
            assert f'Meme with id {meme_id} successfully deleted' in self.response_text, 'Meme WAS NOT deleted'
        elif self.response.status_code == 404:
            print(f'Meme with id {meme_id} was already deleted.')
        else:
            assert False, f"Invalid status code: {self.response.status_code}"

    def as_authorized_user_but_with_incorrect_token(self, meme_id, headers):
        self.session.headers.update(headers)
        self.response = self._delete_meme(meme_id)
        if self.response.status_code == 401:
            print(self.response.text)
            assert 'Not authorized' in self.response.text, "Expected invalid token error message."
        else:
            assert False, f"Invalid status code: {self.response.status_code}"

    def as_authorized_user_but_now_owner(self, meme_id):
        self.response = self._delete_meme(meme_id)
        if self.response.status_code == 403:
            assert 'You are not the meme owner' in self.response.text, \
                "Expected permission error message, but got something else."
        else:
            assert False, f"Invalid status code: {self.response.status_code}"

    def as_unauthorized_user(self, meme_id):
        self.session.headers.pop('Authorization', None)  # Убираем заголовок Authorization
        self.response = self._delete_meme(meme_id)
        assert 'Not authorized' in self.response.text, 'Expected "Not authorized" message is NOT in response'
