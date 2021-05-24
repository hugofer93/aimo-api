from datetime import timedelta

from decouple import config


DEBUG = config('DEBUG', cast=bool, default=False)

HOST = config('HOST', default='127.0.0.1')

DATABASE = {
    'NAME': 'db.sqlite3',
}

JSON_WEB_TOKEN = {
    'AUTH_HEADER_NAME':     'AUTHORIZATION',
    'AUTH_HEADER_TYPES':    'Bearer',
    'ALGORITHM':            'HS256',
    'USER_FIELD_CLAIM':     'username',
    'TOKEN_LIFETIME':       timedelta(days=1),
}

SECRET_KEY = config('SECRET_KEY')
