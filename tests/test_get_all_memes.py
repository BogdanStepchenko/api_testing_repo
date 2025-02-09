import allure
import pytest


@allure.feature('Get All Memes Feature')
class TestGetAllMemes:

    @pytest.mark.fast_smoke
    @allure.story('Authorized user can get all memes')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_memes_as_authorized_user(self, get_all_memes):
        with allure.step('Checking that authorized user can get all memes'):
            get_all_memes.check_get_all_memes_with_valid_token()
        with allure.step('Checking the status code is 200'):
            get_all_memes.check_status_code(200)

    @pytest.mark.smoke
    @allure.story('Unauthorized user can not get all memes')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_unauthorized_user_cant_get_all_memes(self, get_all_memes):
        with allure.step('Checking that unauthorized user cannot get memes'):
            get_all_memes.check_get_all_memes_as_unauthorized_user()
        with allure.step('Checking the status code is 401'):
            get_all_memes.check_status_code(401)

    @pytest.mark.smoke
    @allure.story('Check that all memes have unique IDs')
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_memes_have_unique_id(self, get_all_memes):
        with allure.step('Getting all memes as an authorized user'):
            get_all_memes.check_get_all_memes_with_valid_token()
        with allure.step('Checking the status code is 200'):
            get_all_memes.check_status_code(200)
        with allure.step('Verifying that all memes have unique IDs'):
            get_all_memes.check_all_memes_have_unique_id()

    @pytest.mark.full_test
    @allure.story('Check that all memes have required fields')
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_memes_have_required_fields(self, get_all_memes):
        with allure.step('Getting all memes as an authorized user'):
            get_all_memes.check_get_all_memes_with_valid_token()
        with allure.step('Checking the status code is 200'):
            get_all_memes.check_status_code(200)
        with allure.step('Verifying that all memes have the required fields'):
            get_all_memes.check_all_memes_have_id_field()
            get_all_memes.check_all_memes_have_tags_field()
            get_all_memes.check_all_memes_have_info_field()
            get_all_memes.check_all_memes_have_text_field()
            get_all_memes.check_all_memes_have_updated_by_field()
            get_all_memes.check_all_memes_have_url_field()

    @pytest.mark.full_test
    @allure.story('Unauthorized user with Authorization header but without token can not get memes')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_memes_as_unauthorized_user_but_with_authorization_in_headers(self, get_all_memes):
        with allure.step('Attempt to get memes with authorization header but without token'):
            get_all_memes.check_get_all_memes_with_authorization_but_without_token()
        with allure.step('Checking the status code is 401'):
            get_all_memes.check_status_code(401)

    @pytest.mark.full_test
    @allure.story('Check that user can not get memes with invalid token')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_memes_with_invalid_token(self, get_all_memes):
        with allure.step('Set invalid authorization token'):
            invalid_headers = {"Authorization": "Bearer invalid_token"}
        with allure.step('Attempt to get memes with invalid token'):
            get_all_memes.check_get_all_memes_with_invalid_token(invalid_headers)
        with allure.step('Checking the status code is 401'):
            get_all_memes.check_status_code(401)
