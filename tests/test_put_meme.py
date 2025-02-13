import pytest
import allure
from data.payloads_for_meme_updation import generate_correct_payload, generate_payload_without_tags,  \
    generate_payload_without_info, generate_payload_without_url, \
    generate_payload_without_text, generate_payload_with_incorrect_id
from data.payloads_for_meme_creation import CORRECT_PAYLOAD


@allure.epic("Meme Update Feature")
class TestPutMeme:

    @pytest.mark.fast_smoke
    @allure.story("Update meme with correct payload as authorized user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_meme_with_correct_payload_as_authorized_user(self, get_created_meme_id,
                                                                 put_existed_meme):
        correct_payload = generate_correct_payload(get_created_meme_id)
        with allure.step("Update meme with correct payload as authorized user"):
            put_existed_meme.update_meme_as_authorized_user_and_id(get_created_meme_id,
                                                                   correct_payload)
        with allure.step("Check status code 200"):
            put_existed_meme.check_status_code(200)
        with allure.step("Check if fields are updated properly"):
            put_existed_meme.check_if_id_was_changed_properly(correct_payload)
            put_existed_meme.check_if_info_was_changed_properly(correct_payload)
            put_existed_meme.check_if_tags_were_changed_properly(correct_payload)
            put_existed_meme.check_if_text_was_changed_properly(correct_payload)
            put_existed_meme.check_if_url_was_changed_properly(correct_payload)
            put_existed_meme.check_if_name_was_not_changed_properly()

    @pytest.mark.smoke
    @allure.story("Attempt to update meme as unauthorized user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_meme_with_correct_payload_as_unauthorized_user(self, get_created_meme_id, put_existed_meme):
        correct_payload = generate_correct_payload(get_created_meme_id)
        with allure.step("Attempt to update meme with correct payload as unauthorized user"):
            put_existed_meme.update_meme_as_unauthorized_user_and_id(get_created_meme_id, correct_payload)
        with allure.step("Check status code 401"):
            put_existed_meme.check_status_code(401)

    @pytest.mark.smoke
    @allure.story("Test various incorrect payloads for meme update")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("payload, description", [
        (generate_payload_without_tags, "Payload without 'tags' field"),
        (generate_payload_without_info, "Payload without 'info' field"),
        (generate_payload_without_url, "Payload without 'url' field"),
        (generate_payload_without_text, "Payload without 'text' field"),
        (generate_payload_with_incorrect_id, "Payload with incorrect ID")
    ])
    def test_update_meme_with_incorrect_payload_as_authorized_user(self, get_created_meme_id, put_existed_meme,
                                                                   payload, description):
        incorrect_payload = payload(get_created_meme_id)
        with allure.step(f"Update meme with: {description}"):
            put_existed_meme.update_meme_as_authorized_user_and_id(get_created_meme_id,
                                                                   incorrect_payload)
        with allure.step("Check status code 400"):
            put_existed_meme.check_status_code(400)

    @pytest.mark.full_test
    @allure.story("Attempt to update meme with invalid token")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_meme_with_incorrect_token(self, get_created_meme_id, put_existed_meme):
        with allure.step("Creation invalid token"):
            invalid_headers = {"Authorization": "Bearer invalid_token"}
            correct_payload = generate_correct_payload(get_created_meme_id)
        with allure.step("Update meme with invalid token"):
            put_existed_meme.update_meme_as_authorized_user_and_id(get_created_meme_id,
                                                                   correct_payload, invalid_headers)
        with allure.step("Check status code 401"):
            put_existed_meme.check_status_code(401)

    @pytest.mark.full_test
    @allure.story("Attempt to update meme created by another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_meme_created_by_another_user(self, post_new_meme, put_existed_meme,
                                                 post_token_endpoint, get_authorized_headers):
        with allure.step('Authorization as another user'):
            another_user_token = post_token_endpoint.create_new_token('AnotherUser')['token']
            another_user_headers = {**get_authorized_headers, 'Authorization': another_user_token}
        with allure.step('Create a new meme as another user'):
            post_new_meme.post_new_meme_as_authorized_user(CORRECT_PAYLOAD, another_user_headers)
            meme_id = post_new_meme.response_json["id"]
        with allure.step('Attempt to update meme as main user'):
            correct_payload = generate_correct_payload(meme_id)
            put_existed_meme.update_meme_as_authorized_user_and_id(meme_id, correct_payload)
        with allure.step('Check status code 403'):
            put_existed_meme.check_status_code(403)
