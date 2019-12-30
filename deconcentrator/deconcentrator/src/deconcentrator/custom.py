import os

APPS = [
    'rest_framework',
    'providers',
    'objectives',
]

with open(os.environ["SECRET_KEY_FILE"], 'r') as fd:
    SECRET_KEY = fd.read(1024).rstrip()

DEBUG = os.environ.get('DEBUG', str(False)) == str(True)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', "").split(" ")

with open(os.environ['POSTGRES_PASSWORD_FILE'], 'r') as fd:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'deconcentrator',
            'HOST': 'postgres',
            'USER': 'postgres',
            'PASSWORD': fd.read(1024).rstrip(),
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    'memcached': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached',
    },
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis://redis/0",
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'redis'
STATIC_ROOT = '/mnt/static'

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'


# noinspection PyPep8
from django.utils.log import DEFAULT_LOGGING
from deepmerge import always_merger
LOGGING = always_merger.merge(DEFAULT_LOGGING, {
    'loggers': {
        'deconcentrator': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
})