from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings


def hash_raw_password(password: str) -> str:
    return make_password(password)



