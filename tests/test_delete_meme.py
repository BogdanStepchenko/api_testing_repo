import pytest


class TestDeleteMeme:

    def test_delete_existed_meme_as_authorized_user(self, get_created_meme_id, delete_meme):
        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(200)

    def test_delete_existed_meme_as_unauthorized_user(self, get_created_meme_id, delete_meme):
        delete_meme.delete_existed_meme_as_unauthorized_user(get_created_meme_id)
        delete_meme.check_status_code(401)

    @pytest.mark.parametrize("meme_id, description", [
        ("", "Empty meme id"),
        (123456789, "Non-existed meme id"),
        ('abcd', "Incorrect meme id")
    ])
    def test_delete_non_existed_meme_as_authorized_user(self, meme_id, description, delete_meme):
        delete_meme.delete_existed_meme_as_authorized_user(meme_id)
        delete_meme.check_status_code(400)

    def test_deletion_already_deleted_meme(self, get_created_meme_id, delete_meme):
        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(200)

        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(404)

    def test_delete_meme_with_invalid_token(self, get_created_meme_id, delete_meme):
        invalid_headers = {"Authorization": "BlaBlaBla"}
        delete_meme.authorized_headers = invalid_headers
        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(401)
