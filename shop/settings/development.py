from .base import *
import os

DEBUG = True

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

URL_PATH_PROJECT = "http://127.0.0.1:8000"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
