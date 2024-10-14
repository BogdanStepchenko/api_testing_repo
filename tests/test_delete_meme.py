import pytest
import allure


@allure.feature("Delete Meme Feature")
class TestDeleteMeme:

    @allure.story("Authorized user deletes existing meme")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Delete existed meme as an authorized user")
    def test_delete_existed_meme_as_authorized_user(self, get_created_meme_id, delete_meme):
        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(200)

    @allure.story("Unauthorized user tries to delete existed meme")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("Delete existed meme as an unauthorized user")
    def test_delete_existed_meme_as_unauthorized_user(self, get_created_meme_id, delete_meme):
        delete_meme.delete_existed_meme_as_unauthorized_user(get_created_meme_id)
        delete_meme.check_status_code(401)

    @allure.story("Authorized user deletes non-existed meme")
    @allure.severity(allure.severity_level.MINOR)
    @allure.step("Delete meme with invalid meme ID")
    @pytest.mark.parametrize("meme_id, description", [
        ("", "Empty meme id"),
        (123456789, "Non-existed meme id"),
        ('abcd', "Incorrect meme id")
    ])
    def test_delete_non_existed_meme_as_authorized_user(self, meme_id, description, delete_meme):
        delete_meme.delete_existed_meme_as_authorized_user(meme_id)
        delete_meme.check_status_code(400)

    @allure.story("Check re-deletion of already deleted meme")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("Attempt to delete already deleted meme")
    def test_deletion_already_deleted_meme(self, get_created_meme_id, delete_meme):
        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(200)

        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(404)

    @allure.story("Delete meme with invalid authorization token")
    @allure.severity(allure.severity_level.MINOR)
    @allure.step("Attempt to delete a meme with invalid token")
    def test_delete_meme_with_invalid_token(self, get_created_meme_id, delete_meme):
        invalid_headers = {"Authorization": "BlaBlaBla"}
        delete_meme.authorized_headers = invalid_headers
        delete_meme.delete_existed_meme_as_authorized_user(get_created_meme_id)
        delete_meme.check_status_code(401)
