import pytest


class TestGetExactMeme:

    def test_get_exact_meme_as_authorized_user(self, get_created_meme_id, get_exact_meme):
        get_exact_meme.check_get_exact_meme_as_authorized_user(get_created_meme_id)
        get_exact_meme.check_status_code(200)
        get_exact_meme.check_meme_fields_in_response()

    def test_get_exact_meme_as_unauthorized_user(self, get_exact_meme):
        get_exact_meme.check_get_exact_meme_as_unauthorized_user(1)
        get_exact_meme.check_status_code(401)

    @pytest.mark.parametrize(
        "incorrect_id",
        [
            None,
            'abc',
            19381038190381
        ]
    )
    def test_get_meme_with_incorrect_id(self, get_exact_meme, incorrect_id):
        get_exact_meme.check_get_non_existed_meme(incorrect_id)
        get_exact_meme.check_status_code(404)

    def test_get_exact_meme_with_invalid_token(self, get_created_meme_id, get_exact_meme):
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        get_exact_meme.authorized_headers = invalid_headers
        get_exact_meme.check_get_exact_meme_as_authorized_user(get_created_meme_id)
        get_exact_meme.check_status_code(401)
