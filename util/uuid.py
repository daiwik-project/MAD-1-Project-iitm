import random
import string

def generate_uuid():
    characters = string.ascii_letters + string.digits
    uuid = ''.join(random.choices(characters, k=12))
    return uuid