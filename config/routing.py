"""
WebSocket routing configuration for Intellectual Partner
"""

from django.urls import re_path
from channels.routing import URLRouter

# WebSocket コンシューマのインポート
from notifications.consumers import (
    NotificationsConsumer,
    TeacherDashboardConsumer,
    StudySessionConsumer,
)
from analytics.consumers import (
    AnalyticsConsumer,
    RealTimeAnalyticsConsumer,
)

# WebSocket URLパターン
websocket_urlpatterns = [
    # 通知関連WebSocket
    re_path(
        r"ws/notifications/(?P<user_id>\w+)/$",
        NotificationsConsumer.as_asgi(),
        name="notifications_ws",
    ),
    # 教師ダッシュボード用WebSocket
    re_path(
        r"ws/teacher/dashboard/(?P<teacher_id>\w+)/$",
        TeacherDashboardConsumer.as_asgi(),
        name="teacher_dashboard_ws",
    ),
    # 学習セッション用WebSocket (リアルタイム進捗更新)
    re_path(
        r"ws/study-session/(?P<session_id>\w+)/$",
        StudySessionConsumer.as_asgi(),
        name="study_session_ws",
    ),
    # 分析データリアルタイム更新
    re_path(
        r"ws/analytics/(?P<user_id>\w+)/$",
        AnalyticsConsumer.as_asgi(),
        name="analytics_ws",
    ),
    # リアルタイム分析 (集中度など)
    re_path(
        r"ws/realtime-analytics/(?<user_id>\w+)/$",
        RealTimeAnalyticsConsumer.as_asgi(),
        name="realtime_analytics_ws",
    ),
]

# 開発環境用のWebSocketパス (デバッグ用)
development_websocket_patterns = [
    re_path(
        r"ws/debug/(?P<room_name>\w+)/$",
        NotificationsConsumer.as_asgi(),  # デバッグ用に流用
        name="debug_ws",
    ),
]

# 本番環境とテスト環境を分離
from django.conf import settings

if settings.DEBUG:
    websocket_urlpatterns.extend(development_websocket_patterns)


# WebSocketミドルウェア設定 (将来的な拡張用)
class WebSocketRateLimitMiddleware:
    """WebSocketの接続数制限ミドルウェア"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # レート制限ロジック (将来実装)
        # 現在はそのまま通す
        return await self.inner(scope, receive, send)


# カスタムWebSocketミドルウェアスタック
def WebSocketMiddlewareStack(inner):
    """カスタムWebSocketミドルウェアスタック"""
    return WebSocketRateLimitMiddleware(inner)
