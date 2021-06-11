from fastapi.security import HTTPBasic
from jwt import encode
from time import time
from os import environ

SECRET_KEY = environ['SECRET_KEY']
TOKEN_EXPIRE = 5 * 60

security_login = HTTPBasic()


def create_token(user: str) -> str:
    """Creates JWT for user with given name."""
    payload = {'name': user,
               'iat': round(time()),
               'exp': round(time() + TOKEN_EXPIRE)}

    return encode(payload, SECRET_KEY, algorithm='HS256')
