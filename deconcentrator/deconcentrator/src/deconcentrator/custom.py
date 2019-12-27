import os

APPS = [
    'providers',
    'objectives',
]

with open(os.environ["SECRET_KEY_FILE"], 'r') as fd:
    SECRET_KEY = fd.read(1024).rstrip()

DEBUG = os.environ.get('DEBUG', False)
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
