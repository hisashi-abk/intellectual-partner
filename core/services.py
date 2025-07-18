"""
Core business logic services.
"""

from typing import List, Optional, Dict, Any
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Tag, Category, Subject, Achievement, ConcentrationLevel, StudyEnvironment
from .exceptions import NotFoundError, ValidationError, BusinessLogicError
from .utils import StudySessionGenerator, ProgressCalculator
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class TagService:
    """Service for tag operations."""

    @staticmethod
    def get_or_create_tag(name: str, color: str = "#3b82f6", description: str = "") -> Tag:
        """Get or create a tag by name."""
        tag, created = Tag.objects.get_or_create(
            name=name.lower().strip(), defaults={"color": color, "description": description}
        )
        return tag

    @staticmethod
    def get_popular_tags(limit: int = 10) -> List[Tag]:
        """Get popular tags."""
        # TODO: Implement based on actual usage
        return list(Tag.objects.filter(is_deleted=False)[:limit])


class CategoryService:
    """Service for category operations."""

    @staticmethod
    def get_category_tree(parent_id: Optional[str] = None) -> List[Category]:
        """Get category tree structure."""
        queryset = Category.objects.filter(parent_id=parent_id)
        categories = []

        for category in queryset:
            category_dict = {"category": category, "children": CategoryService.get_category_tree(category.id)}
            categories.append(category_dict)

        return categories


class SubjectService:
    """Service for subject operations."""

    @staticmethod
    def get_active_subjects() -> QuerySet:
        """Get all active subjects."""
        return Subject.objects.filter(is_active=True)

    @staticmethod
    def get_subject_by_code(code: str) -> Subject:
        """Get subject by code."""
        try:
            return Subject.objects.get(code=code, is_active=True)
        except Subject.DoesNotExist:
            raise NotFoundError(f"Subject with code '{code}' not found")


class ConcentrationService:
    """Service for concentration tracking."""

    @staticmethod
    def record_concentration(user: User, level: int, session_id: str, notes: str = "") -> ConcentrationLevel:
        """Record concentration level."""
        if not (1 <= level <= 10):
            raise ValidationError("Concentration level must be between 1 and 10")

        concentration = ConcentrationLevel.objects.create(user=user, level=level, session_id=session_id, notes=notes)

        logger.info(f"Recorded concentration level {level} for user {user.id}")
        return concentration

    @staticmethod
    def get_user_concentration_trend(user: User, days: int = 7) -> Dict[str, Any]:
        """Get user's concentration trend."""
        cutoff = timezone.now() - timedelta(days=days)
        concentrations = ConcentrationLevel.objects.filter(user=user, timestamp__gte=cutoff).order_by("timestamp")

        if not concentrations.exists():
            return {"trend": "no_data", "average": 0, "improvement": 0, "sessions": 0}

        levels = [c.level for c in concentrations]
        average = sum(levels) / len(levels)

        # Calculate improvement (compare first half vs second half)
        if len(levels) >= 4:
            mid = len(levels) // 2
            first_half = levels[:mid]
            second_half = levels[mid:]
            improvement = (sum(second_half) / len(second_half)) - (sum(first_half) / len(first_half))
        else:
            improvement = 0

        return {
            "trend": "improving" if improvement > 0 else "declining" if improvement < 0 else "stable",
            "average": round(average, 2),
            "improvement": round(improvement, 2),
            "sessions": len(levels),
        }


class StudyEnvironmentService:
    """Service for study environment tracking."""

    @staticmethod
    def record_environment(
        user: User,
        location: str,
        effective_rating: int,
        background_music: str = "",
        lighting: str = "moderate",
        temperature: str = "comfortable",
        noise_level: str = "silent",
    ) -> StudyEnvironment:
        """Record study environment."""
        if not (1 <= effective_rating <= 5):
            raise ValidationError("Effective rating must be between 1 and 5")

        environment = StudyEnvironment.objects.create(
            user=user,
            location=location,
            background_music=background_music,
            lighting=lighting,
            temperature=temperature,
            noise_level=noise_level,
            effective_rating=effective_rating,
        )

        logger.info(f"Recorded study environment for user {user.id}")
        return environment

    @staticmethod
    def get_optimal_environments(user: User, min_rating: int = 4) -> List[StudyEnvironment]:
        """Get user's optimal study environments."""
        return list(
            StudyEnvironment.objects.filter(user=user, effective_rating__gte=min_rating).order_by(
                "-effective_rating", "-timestamp"
            )
        )


class AchievementService:
    """Service for achievement operations."""

    ACHIEVEMENT_TYPES = {
        "study_time": {"title": "学習時間達成", "description": "目標学習時間を達成しました", "points": 100},
        "streak": {"title": "連続学習達成", "description": "連続学習記録を達成しました", "points": 150},
        "goal_completion": {"title": "目標完了", "description": "設定した目標を完了しました", "points": 200},
        "perfect_score": {"title": "満点獲得", "description": "テストで満点を獲得しました", "points": 300},
        "consistency": {"title": "継続性", "description": "継続的な学習を実現しました", "points": 250},
    }

    @staticmethod
    def create_achievement(
        user: User,
        achievement_type: str,
        custom_title: str = None,
        custom_description: str = None,
        custom_points: int = None,
    ) -> Achievement:
        """Create an achievement for a user."""
        if achievement_type not in AchievementService.ACHIEVEMENT_TYPES:
            raise ValidationError(f"Invalid achievement type: {achievement_type}")

        template = AchievementService.ACHIEVEMENT_TYPES[achievement_type]

        achievement = Achievement.objects.create(
            user=user,
            title=custom_title or template["title"],
            description=custom_description or template["description"],
            type=achievement_type,
            points=custom_points or template["points"],
        )

        logger.info(f"Created achievement '{achievement.title}' for user {user.id}")
        return achievement

    @staticmethod
    def get_user_achievements(user: User, achievement_type: str = None) -> QuerySet:
        """Get user's achievements."""
        queryset = Achievement.objects.filter(user=user)
        if achievement_type:
            queryset = queryset.filter(type=achievement_type)
        return queryset.order_by("-achieved_at")


class StudySessionService:
    """Service for study session operations."""

    @staticmethod
    def generate_session_name(subject: str = None, mood: str = None, difficulty: str = None) -> str:
        """Generate a unique session name."""
        from .utils import get_time_of_day

        time_of_day = get_time_of_day()

        return StudySessionGenerator.generate_operation_name(
            subject=subject, time_of_day=time_of_day, mood=mood, difficulty=difficulty
        )

    @staticmethod
    def suggest_study_strategy(
        goal_type: str, difficulty: str, available_time: int, learning_style: str
    ) -> Dict[str, Any]:
        """Suggest study strategy based on parameters."""
        return StudySessionGenerator.generate_study_strategy(
            goal_type=goal_type, difficulty=difficulty, time_available=available_time, learning_style=learning_style
        )


class AnalyticsService:
    """Service for analytics operations."""

    @staticmethod
    def calculate_user_progress(user: User, days: int = 30) -> Dict[str, Any]:
        """Calculate comprehensive user progress."""
        cutoff = timezone.now() - timedelta(days=days)

        # Get concentration data
        concentrations = ConcentrationLevel.objects.filter(user=user, timestamp__gte=cutoff).order_by("timestamp")

        # Get study environments
        environments = StudyEnvironment.objects.filter(user=user, timestamp__gte=cutoff).order_by("timestamp")

        # Get achievements
        achievements = Achievement.objects.filter(user=user, achieved_at__gte=cutoff).order_by("-achieved_at")

        # Calculate metrics
        concentration_sessions = [
            {
                "date": c.timestamp,
                "concentration": c.level,
                "duration": 30,  # Default duration, should come from actual session data
            }
            for c in concentrations
        ]

        weekly_progress = ProgressCalculator.calculate_weekly_progress(concentration_sessions)

        return {
            "period_days": days,
            "total_sessions": len(concentration_sessions),
            "total_achievements": achievements.count(),
            "total_points": sum(a.points for a in achievements),
            "weekly_progress": weekly_progress,
            "concentration_trend": ConcentrationService.get_user_concentration_trend(user, days),
            "optimal_environments": len(StudyEnvironmentService.get_optimal_environments(user)),
            "recent_achievements": [
                {"title": a.title, "type": a.type, "points": a.points, "achieved_at": a.achieved_at}
                for a in achievements[:5]
            ],
        }
