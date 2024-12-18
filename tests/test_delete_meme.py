import pytest
import allure

from data.payloads_for_meme_creation import CORRECT_PAYLOAD


@allure.feature("Delete Meme Feature")
class TestDeleteMeme:

    @pytest.mark.fast_smoke
    @allure.story("Authorized user deletes existing meme")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Delete existed meme as an authorized user")
    def test_delete_existed_meme_as_authorized_user(self, create_new_meme_without_deletion,
                                                    delete_meme, get_exact_meme):
        meme_id = create_new_meme_without_deletion["id"]
        delete_meme.as_authorized_user(meme_id)
        delete_meme.check_status_code(200)
        get_exact_meme.check_if_meme_was_deleted(meme_id)

    @pytest.mark.smoke
    @allure.story("Unauthorized user tries to delete existed meme")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("Delete existed meme as an unauthorized user")
    def test_delete_existed_meme_as_unauthorized_user(self, get_created_meme_id, delete_meme):
        delete_meme.as_unauthorized_user(get_created_meme_id)
        delete_meme.check_status_code(401)

    @pytest.mark.smoke
    @allure.story("Authorized user deletes non-existed meme")
    @allure.severity(allure.severity_level.MINOR)
    @allure.step("Delete meme with invalid meme ID")
    @pytest.mark.parametrize("meme_id, description", [
        ("", "Empty meme id"),
        (123456789, "Non-existed meme id"),
        ('abcd', "Incorrect meme id")
    ])
    def test_delete_non_existed_meme_as_authorized_user(self, meme_id, description, delete_meme):
        delete_meme.as_authorized_user(meme_id)
        delete_meme.check_status_code(404)

    @pytest.mark.full_test
    @allure.story("Check re-deletion of already deleted meme")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.step("Attempt to delete already deleted meme")
    def test_deletion_already_deleted_meme(self, get_meme_id_without_deletion, delete_meme):
        delete_meme.as_authorized_user(get_meme_id_without_deletion)
        delete_meme.check_status_code(200)

        delete_meme.as_authorized_user(get_meme_id_without_deletion)
        delete_meme.check_status_code(404)

    @pytest.mark.full_test
    @allure.story("Delete meme with invalid authorization token")
    @allure.severity(allure.severity_level.MINOR)
    @allure.step("Attempt to delete a meme with invalid token")
    def test_delete_meme_with_invalid_token(self, get_meme_id_without_deletion, delete_meme):
        invalid_headers = {"Authorization": "BlaBlaBla"}
        delete_meme.authorized_headers = invalid_headers
        delete_meme.as_authorized_user_but_with_incorrect_token(get_meme_id_without_deletion)
        delete_meme.check_status_code(401)

    @pytest.mark.full_test
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
            delete_meme.as_authorized_user_but_now_owner(meme_id)
        with allure.step('Check that status code is 403'):
            delete_meme.check_status_code(403)
