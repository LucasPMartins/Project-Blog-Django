import random
import string
from django.utils.text import slugify

def random_letters(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def new_slugify(string,k=5):
    return slugify(string) + '-' + random_letters(k)