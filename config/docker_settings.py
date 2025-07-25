"""
Docker環境用設定
"""

from .settings import *

# Docker内でのデータベース設定
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "intellectual_partner",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432",
    }
}

# Docker内でのRedis設定
REDIS_URL = "redis://redis:6379/0"
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://redis:6379/2"],
        },
    },
}

# 静的ファイル設定
STATIC_ROOT = "/app/staticfiles"
MEDIA_ROOT = "/app/media"
