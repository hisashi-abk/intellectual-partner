"""
Common middleware for the core application.
"""

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
import logging
import time
import json

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log API requests."""

    def process_request(self, request):
        """Log incoming request."""
        request.start_time = time.time()

        # Log API requests
        if request.path.startswith("/api/"):
            logger.info(f"API Request: {request.method} {request.path}")

    def process_response(self, request, response):
        """Log request completion."""
        if hasattr(request, "start_time") and request.path.startswith("/api/"):
            duration = time.time() - request.start_time
            logger.info(f"API Response: {request.method} {request.path} - {response.status_code} - {duration:.3f}s")

        return response


class UserActivityMiddleware(MiddlewareMixin):
    """Middleware to track user activity."""

    def process_request(self, request):
        """Track user activity."""
        if request.user.is_authenticated:
            cache_key = f"user_activity:{request.user.id}"
            cache.set(cache_key, timezone.now(), timeout=settings.CACHE_TIMEOUT_MEDIUM)


class RateLimitMiddleware(MiddlewareMixin):
    """Simple rate limiting middleware."""

    def process_request(self, request):
        """Check rate limits."""
        if not request.path.startswith("/api/"):
            return None

        # Get client IP
        client_ip = self.get_client_ip(request)

        # Check if user is authenticated
        if request.user.is_authenticated:
            rate_limit_key = f"rate_limit:user:{request.user.id}"
            rate_limit = getattr(settings, "API_RATE_LIMIT_AUTHENTICATED", "1000/hour")
        else:
            rate_limit_key = f"rate_limit:ip:{client_ip}"
            rate_limit = getattr(settings, "API_RATE_LIMIT_DEFAULT", "100/hour")

        # Simple rate limiting logic
        current_requests = cache.get(rate_limit_key, 0)
        limit, period = self.parse_rate_limit(rate_limit)

        if current_requests >= limit:
            return JsonResponse(
                {"error": "Rate limit exceeded", "message": f"Too many requests. Limit: {rate_limit}"}, status=429
            )

        # Increment counter
        cache.set(rate_limit_key, current_requests + 1, timeout=period)

        return None

    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def parse_rate_limit(self, rate_limit):
        """Parse rate limit string like '100/hour'."""
        limit_str, period_str = rate_limit.split("/")
        limit = int(limit_str)

        period_map = {"second": 1, "minute": 60, "hour": 3600, "day": 86400}

        period = period_map.get(period_str, 3600)
        return limit, period


class ExceptionHandlingMiddleware(MiddlewareMixin):
    """Middleware for handling exceptions."""

    def process_exception(self, request, exception):
        """Handle exceptions globally."""
        if request.path.startswith("/api/"):
            logger.error(f"API Exception: {request.method} {request.path} - {str(exception)}")

            # Return JSON error response for API endpoints
            return JsonResponse(
                {
                    "error": "Internal Server Error",
                    "message": "An error occurred while processing your request.",
                    "timestamp": timezone.now().isoformat(),
                },
                status=500,
            )

        return None
