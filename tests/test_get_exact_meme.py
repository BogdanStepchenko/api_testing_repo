import pytest
import allure


@allure.feature('Get Exact Meme Feature')
class TestGetExactMeme:

    @pytest.mark.fast_smoke
    @allure.story('Check that authorized user can get exact meme')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_exact_meme_as_authorized_user(self, get_created_meme_id, get_exact_meme):
        with allure.step('Getting exact meme by ID'):
            get_exact_meme.check_all_fields_in_meme_response(get_created_meme_id)
        with allure.step('Checking status code is 200'):
            get_exact_meme.check_status_code(200)
        with allure.step('Checking that all fields in response are correct'):
            get_exact_meme.check_all_fields_in_meme_response(get_created_meme_id)

    @pytest.mark.smoke
    @allure.story('Check that unauthorized user can not get exact meme')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_exact_meme_as_unauthorized_user(self, get_exact_meme):
        with allure.step('Check that unauthorized user can not get exact meme by ID'):
            get_exact_meme.get_meme_by_id(1)
        with allure.step('Checking status code is 401'):
            get_exact_meme.check_status_code(401)

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "incorrect_id",
        [
            None,
            'abc',
            19381038190381
        ]
    )
    @allure.story('Impossible to get exact meme with incorrect meme ID')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_meme_with_incorrect_id(self, get_exact_meme, incorrect_id):
        with allure.step('Check that authorized user can not get exact meme with incorrect ID'):
            get_exact_meme.check_get_non_existed_meme(incorrect_id)
        with allure.step('Checking status code is 404'):
            get_exact_meme.check_status_code(404)

    @pytest.mark.full_test
    @allure.story('Getting exact meme with incorrect authorization token')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_exact_meme_with_invalid_token(self, get_created_meme_id, get_exact_meme):
        with allure.step('Creation invalid token'):
            invalid_headers = {"Authorization": "Bearer invalid_token"}
            get_exact_meme.authorized_headers = invalid_headers
        with allure.step('Check that impossible to get exact meme with incorrect authorization token'):
            get_exact_meme.get_meme_by_id(get_created_meme_id, invalid_headers)
        with allure.step('Checking status code is 401'):
            get_exact_meme.check_status_code(401)
