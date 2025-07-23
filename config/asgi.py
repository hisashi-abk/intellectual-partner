"""
ASGI config for Intellectual Partner project.

WebSocket (Django Channels) 対応のASGI設定
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Django設定を読み込み
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Django ASGIアプリケーション (HTTP用)
django_asgi_app = get_asgi_application()

# WebSocketルーティングをインポート
from .routing import websocket_urlpatterns

# ASGI アプリケーション設定
application = ProtocolTypeRouter(
    {
        # HTTP リクエスト (通常のDjango)
        "http": django_asgi_app,
        # WebSocket リクエスト
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)

# 開発環境でのデバッグ設定
import django
from django.conf import settings

if settings.DEBUG:
    # 開発環境での詳細ログ
    import logging

    logging.getLogger("channels").setLevel(logging.DEBUG)
    logging.getLogger("channels.routing").setLevel(logging.DEBUG)
