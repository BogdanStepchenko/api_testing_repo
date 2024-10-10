import string
from random import randint, choice


def get_random_string():
    random_len = randint(1, 10)
    random_string = ''.join(choice(string.ascii_letters) for _ in range(random_len))
    return random_string
