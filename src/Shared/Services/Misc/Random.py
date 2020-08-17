import random
import string


def get_random_string(length):
    """
    Generates a random string
    """
    letters = string.ascii_lowercase
    rnd_string = ''.join(random.choice(letters) for i in range(length))
    return rnd_string
