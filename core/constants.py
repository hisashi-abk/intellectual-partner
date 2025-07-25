"""
Common constants for the core application.
"""

# Time constants
DEFAULT_SESSION_DURATION = 25  # minutes
DEFAULT_BREAK_DURATION = 5  # minutes
MAX_STUDY_DURATION = 480  # 8 hours in minutes
MIN_STUDY_DURATION = 1  # 1 minute

# Concentration levels
MIN_CONCENTRATION_LEVEL = 1
MAX_CONCENTRATION_LEVEL = 10
GOOD_CONCENTRATION_THRESHOLD = 7

# Study environment ratings
MIN_ENVIRONMENT_RATING = 1
MAX_ENVIRONMENT_RATING = 5
GOOD_ENVIRONMENT_THRESHOLD = 4

# Achievement points
DEFAULT_ACHIEVEMENT_POINTS = 100
STREAK_ACHIEVEMENT_POINTS = 150
GOAL_COMPLETION_POINTS = 200
PERFECT_SCORE_POINTS = 300
CONSISTENCY_POINTS = 250

# Cache timeouts (in seconds)
CACHE_TIMEOUT_SHORT = 300  # 5 minutes
CACHE_TIMEOUT_MEDIUM = 3600  # 1 hour
CACHE_TIMEOUT_LONG = 86400  # 24 hours

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Colors
DEFAULT_TAG_COLOR = "#3b82f6"
DEFAULT_CATEGORY_COLOR = "#3b82f6"
DEFAULT_SUBJECT_COLOR = "#3b82f6"
DEFAULT_BADGE_COLOR = "#ffd700"

# File upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_FORMATS = ["JPEG", "PNG", "GIF", "WEBP"]
ALLOWED_DOCUMENT_FORMATS = ["PDF", "DOC", "DOCX", "TXT"]

# API rate limits
API_RATE_LIMIT_DEFAULT = "100/hour"
API_RATE_LIMIT_AUTHENTICATED = "1000/hour"
API_RATE_LIMIT_PREMIUM = "5000/hour"

# Study session states
SESSION_STATES = {
    "PLANNING": "planning",
    "ACTIVE": "active",
    "BREAK": "break",
    "COMPLETED": "completed",
    "CANCELLED": "cancelled",
}

# Notification types
NOTIFICATION_TYPES = {
    "STUDY_REMINDER": "study_reminder",
    "ACHIEVEMENT": "achievement",
    "GOAL_DEADLINE": "goal_deadline",
    "STREAK_BROKEN": "streak_broken",
    "TEACHER_MESSAGE": "teacher_message",
    "SYSTEM_UPDATE": "system_update",
}

# Error codes
ERROR_CODES = {
    "VALIDATION_ERROR": "VALIDATION_ERROR",
    "NOT_FOUND": "NOT_FOUND",
    "PERMISSION_DENIED": "PERMISSION_DENIED",
    "BUSINESS_LOGIC_ERROR": "BUSINESS_LOGIC_ERROR",
    "SOFT_DELETED": "SOFT_DELETED",
    "CONCENTRATION_LEVEL_ERROR": "CONCENTRATION_LEVEL_ERROR",
    "STUDY_ENVIRONMENT_ERROR": "STUDY_ENVIRONMENT_ERROR",
    "ACHIEVEMENT_ERROR": "ACHIEVEMENT_ERROR",
}
