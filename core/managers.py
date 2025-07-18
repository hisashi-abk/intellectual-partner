"""
Custom managers for the core application.
Provides common query methods and soft delete functionality.
"""

from django.db import models
from django.utils import timezone
from typing import Optional, Any
from django.db.models.query import QuerySet
from datetime import timedelta


class SoftDeleteQuerySet(QuerySet):
    """
    QuerySet for soft delete functionality.
    """

    def delete(self):
        """Soft delete all objects in the queryset."""
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        """Permanently delete all objects in the queryset."""
        return super().delete()

    def alive(self):
        """Return only non-deleted objects."""
        return self.filter(is_deleted=False)

    def dead(self):
        """Return only deleted objects."""
        return self.filter(is_deleted=True)

    def restore(self):
        """Restore soft-deleted objects."""
        return self.update(is_deleted=False, deleted_at=None)


class SoftDeleteManager(models.Manager):
    """
    Manager for soft delete functionality.
    """

    def get_queryset(self):
        """Return only non-deleted objects by default."""
        return SoftDeleteQuerySet(self.model, using=self._db).alive()

    def all_with_deleted(self):
        """Return all objects including soft-deleted ones."""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def deleted_only(self):
        """Return only soft-deleted objects."""
        return SoftDeleteQuerySet(self.model, using=self._db).dead()

    def restore_by_id(self, id: Any):
        """Restore a soft-deleted object by ID."""
        return self.all_with_deleted().filter(id=id).restore()


class TimeStampedManager(models.Manager):
    """
    Manager for timestamped models with common date queries.
    """

    def created_today(self):
        """Return objects created today."""
        today = timezone.now().date()
        return self.filter(created_at__date=today)

    def created_this_week(self):
        """Return objects created this week."""
        week_start = timezone.now().date() - timedelta(days=7)
        return self.filter(created_at__date__gte=week_start)

    def created_this_month(self):
        """Return objects created this month."""
        month_start = timezone.now().replace(day=1).date()
        return self.filter(created_at__date__gte=month_start)

    def updated_today(self):
        """Return objects updated today."""
        today = timezone.now().date()
        return self.filter(updated_at__date=today)

    def recent(self, days: int = 7):
        """Return objects created within the last N days."""
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)


class UserRelatedManager(models.Manager):
    """
    Manager for user-related models.
    """

    def for_user(self, user):
        """Return objects for a specific user."""
        return self.filter(user=user)

    def active_for_user(self, user):
        """Return active objects for a specific user."""
        queryset = self.filter(user=user)
        if hasattr(self.model, "is_active"):
            queryset = queryset.filter(is_active=True)
        return queryset


class BaseModelManager(SoftDeleteManager, TimeStampedManager):
    """
    Combined manager for base models with soft delete and timestamp functionality.
    """

    def get_queryset(self):
        """Return only non-deleted objects by default."""
        return SoftDeleteQuerySet(self.model, using=self._db).alive()


class TagManager(models.Manager):
    """
    Manager for tag models.
    """

    def get_or_create_by_name(self, name: str, defaults: Optional[dict] = None):
        """Get or create a tag by name."""
        defaults = defaults or {}
        return self.get_or_create(name=name.lower().strip(), defaults=defaults)

    def popular(self, limit: int = 10):
        """Get most popular tags based on usage."""
        # This would need to be implemented based on actual usage tracking
        return self.all()[:limit]


class CategoryManager(models.Manager):
    """
    Manager for category models.
    """

    def root_categories(self):
        """Get all root categories (no parent)."""
        return self.filter(parent=None)

    def get_descendants(self, category):
        """Get all descendants of a category."""
        descendants = []
        children = self.filter(parent=category)
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_descendants(child))
        return descendants


class SubjectManager(models.Manager):
    """
    Manager for subject models.
    """

    def active(self):
        """Return only active subjects."""
        return self.filter(is_active=True)

    def by_code(self, code: str):
        """Get subject by code."""
        return self.filter(code=code).first()


class AchievementManager(models.Manager):
    """
    Manager for achievement models.
    """

    def for_user(self, user):
        """Get achievements for a specific user."""
        return self.filter(user=user)

    def by_type(self, achievement_type: str):
        """Get achievements by type."""
        return self.filter(type=achievement_type)

    def recent_for_user(self, user, days: int = 30):
        """Get recent achievements for a user."""
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(user=user, achieved_at__gte=cutoff)


class ConcentrationLevelManager(models.Manager):
    """
    Manager for concentration level models.
    """

    def for_user(self, user):
        """Get concentration levels for a specific user."""
        return self.filter(user=user)

    def for_session(self, session_id):
        """Get concentration levels for a specific session."""
        return self.filter(session_id=session_id)

    def average_for_user(self, user, days: int = 7):
        """Get average concentration level for a user over N days."""
        cutoff = timezone.now() - timedelta(days=days)
        result = self.filter(user=user, timestamp__gte=cutoff).aggregate(avg_level=models.Avg("level"))
        return result["avg_level"] or 0


class StudyEnvironmentManager(models.Manager):
    """
    Manager for study environment models.
    """

    def for_user(self, user):
        """Get study environments for a specific user."""
        return self.filter(user=user)

    def high_rated(self, user, rating_threshold: int = 4):
        """Get high-rated study environments for a user."""
        return self.filter(user=user, effective_rating__gte=rating_threshold)

    def by_location(self, location: str):
        """Get study environments by location."""
        return self.filter(location__icontains=location)
