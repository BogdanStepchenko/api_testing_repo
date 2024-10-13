from data.randomizer import get_random_string

CORRECT_PAYLOAD = {
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

PAYLOAD_WITHOUT_INFO = {
    "tags": [
        get_random_string(),
        get_random_string()
    ],
    "text": get_random_string(),
    "url": get_random_string()
}

PAYLOAD_WITH_INCORRECT_INFO = {
    "info": None,
    "tags": [
        get_random_string(),
        get_random_string()
    ],
    "text": get_random_string(),
    "url": get_random_string()
}

PAYLOAD_WITHOUT_TAGS = {
    "info": {
        get_random_string(): get_random_string()
    },
    "text": get_random_string(),
    "url": get_random_string()
}

PAYLOAD_WITH_INCORRECT_TAGS = {
    "info": {
        get_random_string(): get_random_string()
    },
    "tags": None,
    "text": get_random_string(),
    "url": get_random_string()
}

PAYLOAD_WITHOUT_TEXT = {
    "info": {
        get_random_string(): get_random_string()
    },
    "tags": [
        get_random_string(),
        get_random_string()
    ],
    "url": get_random_string()
}

PAYLOAD_WITH_INCORRECT_TEXT = {
    "info": {
        get_random_string(): get_random_string()
    },
    "tags": [
        get_random_string(),
        get_random_string()
    ],
    "text": None,
    "url": get_random_string()
}

PAYLOAD_WITHOUT_URL = {
    "info": {
        get_random_string(): get_random_string()
    },
    "tags": [
        get_random_string(),
        get_random_string()
    ],
    "text": get_random_string()
}

PAYLOAD_WITH_INCORRECT_URL = {
    "info": {
        get_random_string(): get_random_string()
    },
    "tags": [
        get_random_string(),
        get_random_string()
    ],
    "text": get_random_string(),
    "url": None
}
