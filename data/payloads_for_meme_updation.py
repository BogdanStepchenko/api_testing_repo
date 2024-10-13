from data.randomizer import get_random_string


def generate_correct_payload(meme_id):
    payload = {
        "id": meme_id,
        "info": {
            get_random_string(): get_random_string()
        },
        "tags": [
            get_random_string(),
            get_random_string()
        ],
        "text": get_random_string(),
        "url": get_random_string()
    }
    return payload


def generate_payload_with_incorrect_id(meme_id):
    payload = {
        "id": 1234567890,
        "info": {
            get_random_string(): get_random_string()
        },
        "tags": [
            get_random_string(),
            get_random_string()
        ],
        "text": get_random_string(),
        "url": get_random_string()
    }
    return payload


def generate_payload_without_info(meme_id):
    payload = {
        "id": meme_id,
        "tags": [
            get_random_string(),
            get_random_string()
        ],
        "text": get_random_string(),
        "url": get_random_string()
    }
    return payload


def generate_payload_without_tags(meme_id):
    payload = {
        "id": meme_id,
        "info": {
            get_random_string(): get_random_string()
        },
        "text": get_random_string(),
        "url": get_random_string()
    }
    return payload


def generate_payload_without_text(meme_id):
    payload = {
        "id": meme_id,
        "info": {
            get_random_string(): get_random_string()
        },
        "tags": [
            get_random_string(),
            get_random_string()
        ],
        "url": get_random_string()
    }
    return payload


def generate_payload_without_url(meme_id):
    payload = {
        "id": meme_id,
        "info": {
            get_random_string(): get_random_string()
        },
        "tags": [
            get_random_string(),
            get_random_string()
        ],
        "text": get_random_string(),
    }
    return payload
