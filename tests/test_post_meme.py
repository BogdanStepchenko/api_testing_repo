import pytest
import allure
from data.payloads_for_meme_creation import CORRECT_PAYLOAD, PAYLOAD_WITHOUT_INFO, PAYLOAD_WITHOUT_TEXT, \
    PAYLOAD_WITHOUT_TAGS, PAYLOAD_WITHOUT_URL, PAYLOAD_WITH_INCORRECT_TEXT, \
    PAYLOAD_WITH_INCORRECT_INFO, PAYLOAD_WITH_INCORRECT_TAGS, PAYLOAD_WITH_INCORRECT_URL


@allure.feature('Post Meme Feature')
class TestPostMeme:

    @pytest.mark.fast_smoke
    @allure.story('Post meme as authorized user')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_post_correct_meme_as_authorized_user(self, post_new_meme, get_authorized_headers):
        with allure.step('Check that possible to post new meme with correct payload'):
            post_new_meme.post_new_meme_as_authorized_user(CORRECT_PAYLOAD, get_authorized_headers)
        with allure.step('Checking status code is 200'):
            post_new_meme.check_status_code(200)
        with allure.step('Check that response contains all fields which were in payload'):
            post_new_meme.check_if_info_is_correct_in_response(CORRECT_PAYLOAD['info'])
            post_new_meme.check_if_tags_is_correct_in_response(CORRECT_PAYLOAD['tags'])
            post_new_meme.check_if_text_is_correct_in_response(CORRECT_PAYLOAD['text'])
            post_new_meme.check_if_url_is_correct_in_response(CORRECT_PAYLOAD['url'])
        with allure.step('Check that response contains correct usersname'):
            post_new_meme.check_if_correct_username_in_response()

    @pytest.mark.smoke
    @allure.story('Post meme as unauthorized user')
    @allure.severity(allure.severity_level.NORMAL)
    def test_post_correct_meme_as_unauthorized_user(self, post_new_meme):
        with allure.step('Check that impossible to post new meme with correct payload as unauthorized user'):
            post_new_meme.post_new_meme_as_unauthorized_user(CORRECT_PAYLOAD)
        with allure.step('Checking status code is 401'):
            post_new_meme.check_status_code(401)

    @pytest.mark.full_test
    @pytest.mark.parametrize("payload, description", [
        (PAYLOAD_WITHOUT_INFO, "Payload without 'info' field"),
        (PAYLOAD_WITHOUT_TAGS, "Payload without 'tags' field"),
        (PAYLOAD_WITHOUT_TEXT, "Payload without 'text' field"),
        (PAYLOAD_WITHOUT_URL, "Payload without 'url' field"),
        (PAYLOAD_WITH_INCORRECT_URL, "Payload with incorrect URL format"),
        (PAYLOAD_WITH_INCORRECT_TAGS, "Payload with incorrect tags"),
        (PAYLOAD_WITH_INCORRECT_TEXT, "Payload with incorrect text"),
        (PAYLOAD_WITH_INCORRECT_INFO, "Payload with incorrect info"),
    ])
    @allure.story('Post meme with incorrect payload as authorized user')
    @allure.severity(allure.severity_level.NORMAL)
    def test_post_incorrect_meme_as_authorized_user(self, post_new_meme, payload, description, get_authorized_headers):
        with allure.step('Check that impossible to post new meme with incorrect payload as authorized user'):
            post_new_meme.post_new_meme_as_authorized_user(payload, get_authorized_headers)
        with allure.step('Checking status code is 400'):
            post_new_meme.check_status_code(400)

    @pytest.mark.full_test
    @allure.story('Post meme with incorrect authorization token')
    @allure.severity(allure.severity_level.NORMAL)
    def test_post_meme_with_invalid_token(self, post_new_meme):
        with allure.step('Creation of invalid token'):
            invalid_headers = {"Authorization": "Bearer invalid_token"}
            post_new_meme.authorized_headers = invalid_headers
        with allure.step('Check that impossible to post meme with incorrect token'):
            post_new_meme.post_new_meme_as_authorized_user(CORRECT_PAYLOAD, invalid_headers)
        with allure.step('Checking status code is 401'):
            post_new_meme.check_status_code(401)
