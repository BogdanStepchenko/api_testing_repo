import pytest
import allure


@allure.feature('Get Authorization Token Feature')
class TestGetToken:

    @allure.story('Getting correct token')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_correct_token_alive(self, get_token_endpoint, token):
        with allure.step('Check that possible to get correct token'):
            get_token_endpoint.check_is_token_valid(token)
        with allure.step('Checking status code is 200'):
            get_token_endpoint.check_status_code(200)

    @allure.story('Getting correct name in response of correct token')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_correct_name_in_response(self, get_token_endpoint, token, name):
        with allure.step('Check that possible to get correct token'):
            get_token_endpoint.check_is_token_valid(token)
        with allure.step('Check that there is correct name in response'):
            get_token_endpoint.check_is_name_in_token_correct(name)
        with allure.step('Checking status code is 200'):
            get_token_endpoint.check_status_code(200)

    @pytest.mark.parametrize(
        "invalid_token, expected_status_code",
        [
            (None, 404),
            ('', 404),
            ('invalid_format_of_token', 404)
        ]
    )
    @allure.story('Impossible to get incorrect token')
    @allure.severity(allure.severity_level.NORMAL)
    def test_incorrect_token(self, get_token_endpoint, invalid_token, expected_status_code):
        with allure.step('Check that possible to get invalid token'):
            get_token_endpoint.check_is_token_valid(invalid_token)
        with allure.step('Checking status code is 404'):
            get_token_endpoint.check_status_code(expected_status_code)
