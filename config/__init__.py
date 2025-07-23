"""
Celeryアプリケーションの初期化
Djangoの起動時にCeleryアプリケーションがロードされるようにする
"""

# Celeryアプリケーションのインポートにより, Django起動時にCeleryが自動的に初期化される

from .celery import app as celery_app

__all__ = ("celery_app",)
