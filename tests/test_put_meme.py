import pytest
from data.payloads_for_meme_updation import generate_correct_payload, generate_payload_without_tags,  \
    generate_payload_without_info, generate_payload_without_url, \
    generate_payload_without_text, generate_payload_with_incorrect_id


class TestPutMeme:

    def test_update_meme_with_correct_payload_as_authorized_user(self, get_created_meme_id, put_existed_meme):
        correct_payload = generate_correct_payload(get_created_meme_id)
        put_existed_meme.update_meme_as_authorized_user_and_id(get_created_meme_id, correct_payload)
        put_existed_meme.check_status_code(200)
        put_existed_meme.check_if_id_was_changed_properly(correct_payload)
        put_existed_meme.check_if_info_was_changed_properly(correct_payload)
        put_existed_meme.check_if_tags_were_changed_properly(correct_payload)
        put_existed_meme.check_if_text_was_changed_properly(correct_payload)
        put_existed_meme.check_if_url_was_changed_properly(correct_payload)
        put_existed_meme.check_if_name_was_not_changed_properly()

    def test_update_meme_with_correct_payload_as_unauthorized_user(self, get_created_meme_id, put_existed_meme):
        correct_payload = generate_correct_payload(get_created_meme_id)
        put_existed_meme.update_meme_as_unauthorized_user_and_id(get_created_meme_id, correct_payload)
        put_existed_meme.check_status_code(401)

    @pytest.mark.parametrize("payload, description", [
        (generate_payload_without_tags, "Payload without 'tags' field"),
        (generate_payload_without_info, "Payload without 'info' field"),
        (generate_payload_without_url, "Payload without 'url' field"),
        (generate_payload_without_text, "Payload without 'text' field"),
        (generate_payload_with_incorrect_id, "Payload with incorrect ID")
    ])
    def test_update_meme_with_incorrect_payload_as_authorized_user(self, get_created_meme_id,
                                                                   put_existed_meme, payload, description):
        incorrect_payload = payload(get_created_meme_id)
        put_existed_meme.update_meme_as_authorized_user_and_id(get_created_meme_id, incorrect_payload)
        put_existed_meme.check_status_code(400)
