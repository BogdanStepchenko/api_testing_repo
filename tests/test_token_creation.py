import pytest
import allure


@allure.feature('Token Creation Feature')
class TestTokenCreation:

    @allure.story('Creation correct authorization token')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("blabla", id="simple_name"),
            pytest.param("bla bla", id="name_with_spaces"),
            pytest.param("!@#", id="special_characters"),
            pytest.param("", id="empty_name"),
            pytest.param("    ", id="name_with_spaces_only"),
        ]
    )
    def test_correct_token_creation(self, post_token_endpoint, name):
        with allure.step('Check that it is possible to create correct token'):
            post_token_endpoint.create_new_token(name)
        with allure.step('Check that response contains correct token'):
            post_token_endpoint.check_is_token_in_response()
        with allure.step('Check that response contains name'):
            post_token_endpoint.check_is_name_in_response()
        with allure.step('Check that status code is 200'):
            post_token_endpoint.check_status_code(200)

    @allure.story("Create token with incorrect name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param(12345, id="int_name"),
            pytest.param(None, id='without_name'),
        ]
    )
    def test_incorrect_token_creation(self, post_token_endpoint, name):
        with allure.step(f"Attempt to create token with name: {name}"):
            post_token_endpoint.create_new_token(name)
        with allure.step("Check that the status code is 400"):
            post_token_endpoint.check_status_code(400)
        with allure.step("Check if token is present in response"):
            post_token_endpoint.check_is_token_in_response()

    @allure.story("Create token with duplicate name")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("name", ['hello'])
    def test_create_token_with_the_same_name(self, post_token_endpoint, name):
        with allure.step(f"Create token with name: {name}"):
            post_token_endpoint.create_new_token(name)
        with allure.step("Check that the status code is 200 for the first request"):
            post_token_endpoint.check_status_code(200)
        with allure.step("Attempt to create token with the same name again"):
            post_token_endpoint.create_new_token(name)
        with allure.step("Check that the status code is 409 for the duplicate request"):
            post_token_endpoint.check_status_code(200)
