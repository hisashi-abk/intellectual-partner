"""
カスタム例外ハンドラー
"""

from django.http import JsonResponse
from django.core.exceptions import ValidationError
from ninja.errors import HttpError
import logging

logger = logging.getLogger(__name__)


class IntellectualPartnerException(Exception):
    """アプリ固有の基底例外"""

    pass


class GoalLimitExceeded(IntellectualPartnerException):
    """目標数上限エラー"""

    pass


class TicketLimitExceeded(IntellectualPartnerException):
    """チケット数上限エラー"""

    pass


def custom_exception_handler(request, exception):
    """カスタム例外エラー"""
    logger.error(f"Exception occurred: {exception}", exc_info=True)

    if isinstance(exception, (GoalLimitExceeded, TicketLimitExceeded)):
        return JsonResponse(
            {
                "error": "limit_exceeded",
                "message": str(exception),
            },
            status=400,
        )

    return None
