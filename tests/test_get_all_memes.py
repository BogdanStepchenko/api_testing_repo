class TestGetAllMemes:

    def test_get_all_memes_as_authorized_user(self, get_all_memes):
        get_all_memes.check_get_all_memes_as_authorized_user()
        get_all_memes.check_status_code(200)

    def test_unauthorized_user_cant_get_all_memes(self, get_all_memes):
        get_all_memes.check_get_all_memes_as_unauthorized_user()
        get_all_memes.check_status_code(401)

    def test_all_memes_have_unique_id(self, get_all_memes):
        get_all_memes.check_get_all_memes_as_authorized_user()
        get_all_memes.check_status_code(200)
        get_all_memes.check_all_memes_have_unique_id()

    def test_all_memes_have_required_fields(self, get_all_memes):
        get_all_memes.check_get_all_memes_as_authorized_user()
        get_all_memes.check_status_code(200)
        get_all_memes.check_all_memes_have_id_field()
        get_all_memes.check_all_memes_have_tags_field()
        get_all_memes.check_all_memes_have_info_field()
        get_all_memes.check_all_memes_have_text_field()
        get_all_memes.check_all_memes_have_updated_by_field()
        get_all_memes.check_all_memes_have_url_field()

    def test_get_all_memes_as_unauthorized_user_but_with_authorization_in_headers(self, get_all_memes):
        get_all_memes.check_get_all_memes_with_authorization_but_without_token()
        get_all_memes.check_status_code(401)
