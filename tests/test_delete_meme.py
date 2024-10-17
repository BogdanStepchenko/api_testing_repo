import pytest
import allure

from data.payloads_for_meme_creation import CORRECT_PAYLOAD


@allure.feature("Delete Meme Feature")
class TestDeleteMeme:

    @allure.story("Authorized user deletes existing meme")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Delete existed meme as an authorized user")
    def test_delete_existed_meme_as_authorized_user(self, create_new_meme_without_deletion,
                                                    delete_meme, get_exact_meme):
        meme_id = create_new_meme_without_deletion["id"]
        delete_meme.delete_existed_meme_as_authorized_user(meme_id)
        delete_meme.check_status_code(200)
        get_exact_meme.check_get_exact_meme_as_authorized_user(meme_id, expect_deleted=True)

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

    @allure.story("Deletion of someone else's meme")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_meme_created_by_another_user(self, delete_meme, post_token_endpoint,
                                                 post_new_meme, get_authorized_headers):
        with allure.step('Authorization as another user'):
            another_user_token = post_token_endpoint.create_new_token('AnotherUser')['token']
            another_user_headers = {**get_authorized_headers, 'Authorization': another_user_token}
            post_new_meme.authorized_headers = another_user_headers
        with allure.step('Creation of new meme a another user'):
            post_new_meme.post_new_meme_as_authorized_user(CORRECT_PAYLOAD)
            meme_id = post_new_meme.response_json["id"]
        with allure.step('Trying to delete created meme as main user'):
            delete_meme.delete_existed_meme_as_authorized_user(meme_id)
        with allure.step('Check that status code is 403'):
            delete_meme.check_status_code(403)
