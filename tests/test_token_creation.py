import pytest


class TestTokenCreation:

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("blabla", id="simple_name"),
            pytest.param("bla bla", id="name_with_spaces"),
            pytest.param("!@#", id="special_characters")
        ]
    )
    def test_correct_token_creation(self, post_token_endpoint, name):
        post_token_endpoint.create_new_token(name)
        post_token_endpoint.check_is_token_in_response()
        post_token_endpoint.check_is_name_in_response()
        post_token_endpoint.check_status_code(200)

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("", id="empty_name"),
            pytest.param("    ", id="name_with_spaces_only"),
            pytest.param(12345, id="int_name"),
            pytest.param(None, id='without_name'),
            pytest.param('f'*300, id='too_long_name')
        ]
    )
    def test_incorrect_token_creation(self, post_token_endpoint, name):
        post_token_endpoint.create_new_token(name)
        post_token_endpoint.check_status_code(400)
        post_token_endpoint.check_is_token_in_response()
        post_token_endpoint.check_is_name_in_response()

    @pytest.mark.parametrize("name", ['hello'])
    def test_create_token_with_the_same_name(self, post_token_endpoint, name):
        post_token_endpoint.create_new_token(name)
        post_token_endpoint.check_status_code(200)
        post_token_endpoint.create_new_token(name)
        post_token_endpoint.check_status_code(409)

