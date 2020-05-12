from .base import *

DEBUG = True

SENDGRID_API_KEY = (
    "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"
)

URL_PATH_PROJECT = "https://api.jussupov.me"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
