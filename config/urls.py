"""
URL configuration for Intellectual Partner
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth

# Django Ninja API インスタンス
api = NinjaAPI(
    title="学習支援アプリ API",
    version="1.0.0",
    description="知的な伴奏者 - 学習支援アプリのRESTful API",
    auth=JWTAuth(),
    docs_url="api/docs" if settings.DEBUG else None,
)

# 各アプリのAPI エンドポイントを登録
api.add_router("/auth", "accounts.api.router")
api.add_router("/goals", "goals.api.router")
api.add_router("/tickets", "tickets.api.router")
api.add_router("/emotions", "emotions.api.router")
api.add_router("/journal", "journal.api.router")
api.add_router("/analytics", "analytics.api.router")
api.add_router("/teacher", "teacher_support.api.router")
api.add_router("/notifications", "notifications.api.router")
api.add_router("/gamification", "gamification.api.router")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

# 開発環境でのstatic/mediaファイル配信
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # デバッグツール
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__", include(debug_toolbar.urls))] + urlpatterns

    if "silk" in settings.INSTALLED_APPS:
        urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
