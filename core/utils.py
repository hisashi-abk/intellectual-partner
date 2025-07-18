"""
Common utilities for the intellectual partner application.
"""

import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


class StudySessionGenerator:
    """
    Utility class for generating study session names and strategies.
    """

    OPERATION_PREFIXES = ["作戦", "戦略", "計画", "プロジェクト", "ミッション", "チャレンジ", "挑戦"]

    ADJECTIVES = [
        "集中",
        "完璧",
        "効率",
        "持続",
        "突破",
        "克服",
        "達成",
        "成功",
        "継続",
        "向上",
        "飛躍",
        "成長",
        "発展",
        "進歩",
        "改善",
        "強化",
        "徹底",
        "完全",
        "最高",
        "優秀",
    ]

    NOUNS = [
        "学習",
        "勉強",
        "習得",
        "理解",
        "記憶",
        "復習",
        "予習",
        "演習",
        "練習",
        "実践",
        "探求",
        "研究",
        "分析",
        "思考",
        "考察",
        "検討",
        "学びの道",
        "知識の扉",
        "理解の橋",
    ]

    TIME_BASED_MODIFIERS = {
        "morning": ["朝の", "早朝の", "午前の"],
        "afternoon": ["午後の", "昼の", "日中の"],
        "evening": ["夕方の", "夜の", "夜間の"],
        "late_night": ["深夜の", "夜更けの", "夜中の"],
    }

    SUBJECT_MODIFIERS = {
        "数学": ["数理", "計算", "論理", "証明"],
        "国語": ["文学", "言語", "表現", "読解"],
        "英語": ["英文", "語学", "コミュニケーション", "国際"],
        "理科": ["科学", "実験", "観察", "発見"],
        "社会": ["歴史", "地理", "公民", "世界"],
        "物理": ["物理学", "力学", "電磁気", "波動"],
        "化学": ["化学", "分子", "反応", "実験"],
        "生物": ["生命", "生物学", "遺伝", "進化"],
    }

    @classmethod
    def generate_operation_name(
        cls,
        subject: Optional[str] = None,
        time_of_day: Optional[str] = None,
        mood: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> str:
        """
        Generate a unique operation name based on context.

        Args:
            subject: Academic subject
            time_of_day: Time period (morning, afternoon, evening, late_night)
            mood: User's current mood
            difficulty: Task difficulty level

        Returns:
            Generated operation name
        """
        prefix = random.choice(cls.OPERATION_PREFIXES)
        adjective = random.choice(cls.ADJECTIVES)
        noun = random.choice(cls.NOUNS)

        # Add subject modifier if provided
        if subject and subject in cls.SUBJECT_MODIFIERS:
            noun = random.choice(cls.SUBJECT_MODIFIERS[subject])

        # Add time-based modifier if provided
        time_modifier = ""
        if time_of_day and time_of_day in cls.TIME_BASED_MODIFIERS:
            time_modifier = random.choice(cls.TIME_BASED_MODIFIERS[time_of_day])

        # Add difficulty modifier
        difficulty_modifier = ""
        if difficulty:
            difficulty_map = {
                "very_easy": "簡単",
                "easy": "基礎",
                "medium": "標準",
                "hard": "上級",
                "very_hard": "超難関",
            }
            difficulty_modifier = difficulty_map.get(difficulty, "")

        # Combine components
        components = [prefix, time_modifier, difficulty_modifier, adjective, noun]
        components = [c for c in components if c]  # Remove empty strings

        return "".join(components)

    @classmethod
    def generate_study_strategy(
        cls, goal_type: str, difficulty: str, time_available: int, learning_style: str
    ) -> Dict[str, Any]:
        """
        Generate study strategy recommendations based on user preferences.

        Args:
            goal_type: Type of goal (exam, skill, knowledge, etc.)
            difficulty: Task difficulty level
            time_available: Available study time in minutes
            learning_style: User's learning style preference

        Returns:
            Strategy recommendations dictionary
        """
        strategies = {
            "pomodoro": {
                "name": "ポモドーロ・テクニック",
                "description": "25分の集中学習と5分の休憩を繰り返す",
                "work_duration": 25,
                "break_duration": 5,
                "cycles": min(time_available // 30, 4),
            },
            "time_blocking": {
                "name": "タイムブロッキング",
                "description": "集中的な学習時間を確保",
                "work_duration": min(time_available, 90),
                "break_duration": 15,
                "cycles": 1,
            },
            "spaced_repetition": {
                "name": "間隔反復学習",
                "description": "復習間隔を徐々に延ばす学習法",
                "work_duration": 20,
                "break_duration": 10,
                "cycles": time_available // 30,
            },
        }

        # Learning style based recommendations
        if learning_style == "visual":
            strategies["mind_mapping"] = {
                "name": "マインドマップ学習",
                "description": "視覚的な関連付けで理解を深める",
                "work_duration": 45,
                "break_duration": 15,
                "cycles": 1,
            }
        elif learning_style == "auditory":
            strategies["active_recall"] = {
                "name": "音読・復唱学習",
                "description": "声に出して記憶を定着させる",
                "work_duration": 30,
                "break_duration": 10,
                "cycles": time_available // 40,
            }
        elif learning_style == "kinesthetic":
            strategies["practice_based"] = {
                "name": "実践型学習",
                "description": "手を動かしながら学習する",
                "work_duration": 60,
                "break_duration": 15,
                "cycles": 1,
            }

        # Select best strategy based on available time and difficulty
        if time_available < 30:
            recommended = "pomodoro"
        elif difficulty in ["hard", "very_hard"]:
            recommended = "spaced_repetition"
        else:
            recommended = "time_blocking"

        return {
            "recommended": recommended,
            "strategy": strategies[recommended],
            "alternatives": [s for s in strategies.keys() if s != recommended],
        }


class ProgressCalculator:
    """
    Utility class for calculating progress and analytics.
    """

    @staticmethod
    def calculate_completion_percentage(completed: int, total: int) -> float:
        """Calculate completion percentage."""
        if total == 0:
            return 100.0
        return min((completed / total) * 100, 100.0)

    @staticmethod
    def calculate_study_streak(study_dates: List[datetime]) -> int:
        """Calculate current study streak."""
        if not study_dates:
            return 0

        study_dates = sorted(study_dates, reverse=True)
        current_date = timezone.now().date()
        streak = 0

        for i, study_date in enumerate(study_dates):
            expected_date = current_date - timedelta(days=i)
            if study_date.date() == expected_date:
                streak += 1
            else:
                break

        return streak

    @staticmethod
    def calculate_weekly_progress(sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate weekly progress metrics."""
        if not sessions:
            return {
                "total_time": 0,
                "average_concentration": 0,
                "sessions_count": 0,
                "most_productive_day": None,
                "improvement_trend": 0,
            }

        total_time = sum(session.get("duration", 0) for session in sessions)
        concentrations = [session.get("concentration", 0) for session in sessions if session.get("concentration")]
        average_concentration = sum(concentrations) / len(concentrations) if concentrations else 0

        # Group by day of week
        daily_sessions = {}
        for session in sessions:
            day = session.get("date", timezone.now()).strftime("%A")
            if day not in daily_sessions:
                daily_sessions[day] = []
            daily_sessions[day].append(session)

        # Find most productive day
        most_productive_day = (
            max(daily_sessions.keys(), key=lambda day: sum(s.get("duration", 0) for s in daily_sessions[day]))
            if daily_sessions
            else None
        )

        # Calculate improvement trend
        if len(concentrations) > 1:
            first_half = concentrations[: len(concentrations) // 2]
            second_half = concentrations[len(concentrations) // 2 :]
            improvement_trend = (sum(second_half) / len(second_half)) - (sum(first_half) / len(first_half))
        else:
            improvement_trend = 0

        return {
            "total_time": total_time,
            "average_concentration": round(average_concentration, 2),
            "sessions_count": len(sessions),
            "most_productive_day": most_productive_day,
            "improvement_trend": round(improvement_trend, 2),
        }


class CacheManager:
    """
    Utility class for managing cache operations.
    """

    @staticmethod
    def get_cache_key(prefix: str, *args) -> str:
        """Generate cache key with prefix and arguments."""
        key_parts = [prefix] + [str(arg) for arg in args]
        return ":".join(key_parts)

    @staticmethod
    def cache_user_data(user_id: int, data_type: str, data: Any, timeout: int = 3600) -> None:
        """Cache user-specific data."""
        cache_key = CacheManager.get_cache_key("user", user_id, data_type)
        cache.set(cache_key, data, timeout)

    @staticmethod
    def get_cached_user_data(user_id: int, data_type: str) -> Optional[Any]:
        """Retrieve cached user data."""
        cache_key = CacheManager.get_cache_key("user", user_id, data_type)
        return cache.get(cache_key)

    @staticmethod
    def invalidate_user_cache(user_id: int, data_type: Optional[str] = None) -> None:
        """Invalidate user cache."""
        if data_type:
            cache_key = CacheManager.get_cache_key("user", user_id, data_type)
            cache.delete(cache_key)
        else:
            # Invalidate all user cache (requires pattern matching)
            pattern = CacheManager.get_cache_key("user", user_id, "*")
            cache.delete_many(cache.keys(pattern))


class ValidationUtils:
    """
    Utility class for common validation operations.
    """

    @staticmethod
    def validate_study_time(duration: int) -> bool:
        """Validate study time duration."""
        return 1 <= duration <= 480  # 1 minute to 8 hours

    @staticmethod
    def validate_concentration_level(level: int) -> bool:
        """Validate concentration level."""
        return 1 <= level <= 10

    @staticmethod
    def validate_priority(priority: str) -> bool:
        """Validate priority level."""
        valid_priorities = ["low", "medium", "high", "urgent"]
        return priority in valid_priorities

    @staticmethod
    def validate_difficulty(difficulty: str) -> bool:
        """Validate difficulty level."""
        valid_difficulties = ["very_easy", "easy", "medium", "hard", "very_hard"]
        return difficulty in valid_difficulties


class NotificationHelper:
    """
    Utility class for notification operations.
    """

    @staticmethod
    def create_notification_payload(
        user_id: int, title: str, message: str, type: str = "info", data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create notification payload."""
        return {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": type,
            "data": data or {},
            "timestamp": timezone.now().isoformat(),
        }

    @staticmethod
    def format_study_reminder(session_name: str, start_time: datetime) -> Tuple[str, str]:
        """Format study reminder notification."""
        title = "学習時間のお知らせ"
        message = f"「{session_name}」の開始時間です。頑張りましょう！"
        return title, message

    @staticmethod
    def format_achievement_notification(achievement_title: str, points: int) -> Tuple[str, str]:
        """Format achievement notification."""
        title = "🎉 達成おめでとうございます！"
        message = f"「{achievement_title}」を達成しました！{points}ポイント獲得！"
        return title, message


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data using SHA-256."""
    return hashlib.sha256(data.encode()).hexdigest()


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable format."""
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes}分"
        return f"{minutes}分{remaining_seconds}秒"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        if remaining_minutes == 0:
            return f"{hours}時間"
        return f"{hours}時間{remaining_minutes}分"


def get_time_of_day() -> str:
    """Get current time of day category."""
    current_hour = timezone.now().hour

    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    elif 17 <= current_hour < 22:
        return "evening"
    else:
        return "late_night"


def calculate_next_study_time(
    current_time: datetime, interval_minutes: int, user_preferences: Optional[Dict[str, Any]] = None
) -> datetime:
    """
    Calculate next optimal study time based on interval and user preferences.
    """
    next_time = current_time + timedelta(minutes=interval_minutes)

    # If user preferences are provided, adjust for preferred study times
    if user_preferences and "preferred_study_hours" in user_preferences:
        preferred_hours = user_preferences["preferred_study_hours"]
        if next_time.hour not in preferred_hours:
            # Find next preferred hour
            for hour in preferred_hours:
                if hour > next_time.hour:
                    next_time = next_time.replace(hour=hour, minute=0, second=0)
                    break
            else:
                # If no preferred hour found today, use first preferred hour tomorrow
                next_time = next_time.replace(hour=preferred_hours[0], minute=0, second=0) + timedelta(days=1)

    return next_time
