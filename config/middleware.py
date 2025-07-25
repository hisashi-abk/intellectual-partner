"""
カスタムミドルウェア
"""

import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestTimingMiddleware(MiddlewareMixin):
    """リクエスト処理時間を測定"""

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            duration = time.time() - request.start_time
            response["X-Response-Time"] = f"{duration:.3f}s"

            if duration > 1.0:  # 1秒以上の場合ログ出力
                logger.warning(f"Slow request: {request.path} took {duration:.3f}s")

        return response


class IntellectualPartnerHeaderMiddleware(MiddlewareMixin):
    """アプリ固有のヘッダーを追加"""

    def process_response(self, request, response):
        response["X-Intellectual-Partner-Version"] = "1.0.0"
        return response
