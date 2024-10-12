import pytest
from data.constants import CORRECT_PAYLOAD, PAYLOAD_WITHOUT_INFO, PAYLOAD_WITHOUT_TEXT, \
    PAYLOAD_WITHOUT_TAGS, PAYLOAD_WITHOUT_URL, PAYLOAD_WITH_INCORRECT_TEXT, \
    PAYLOAD_WITH_INCORRECT_INFO, PAYLOAD_WITH_INCORRECT_TAGS, PAYLOAD_WITH_INCORRECT_URL


class TestPostMeme:

    def test_post_correct_meme_as_authorized_user(self, post_new_meme):
        payload = CORRECT_PAYLOAD
        post_new_meme.post_new_meme_as_authorized_user(payload)
        post_new_meme.check_status_code(200)
        post_new_meme.check_if_info_is_correct_in_response(payload['info'])
        post_new_meme.check_if_tags_is_correct_in_response(payload['tags'])
        post_new_meme.check_if_text_is_correct_in_response(payload['text'])
        post_new_meme.check_if_url_is_correct_in_response(payload['url'])
        post_new_meme.check_if_correct_username_in_response()

    def test_post_correct_meme_as_unauthorized_user(self, post_new_meme):
        post_new_meme.post_new_meme_as_unauthorized_user(CORRECT_PAYLOAD)
        post_new_meme.check_status_code(401)

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
    def test_post_incorrect_meme_as_authorized_user(self, post_new_meme, payload, description):
        post_new_meme.post_new_meme_as_authorized_user(payload)
        post_new_meme.check_status_code(400)
