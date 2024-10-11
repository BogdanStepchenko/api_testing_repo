import pytest


class TestGetToken:

    def test_correct_token_alive(self, get_token_endpoint, token):
        get_token_endpoint.check_is_token_valid(token)
        get_token_endpoint.check_status_code(200)

    def test_correct_name_in_response(self, get_token_endpoint, token, name):
        get_token_endpoint.check_is_token_valid(token)
        get_token_endpoint.check_is_name_in_token_correct(name)
        get_token_endpoint.check_status_code(200)

    @pytest.mark.parametrize(
        "invalid_token, expected_status_code",
        [
            (None, 400),
            ('', 400),
            ('invalid_format_of_token', 400)
        ]
    )
    def test_incorrect_token(self, get_token_endpoint, invalid_token, expected_status_code):
        get_token_endpoint.check_is_token_valid(invalid_token)
        get_token_endpoint.check_status_code(expected_status_code)
