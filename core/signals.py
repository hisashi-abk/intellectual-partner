"""
Core signals for the intellectual partner application.
Contains signal handlers for common model operations.
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create initial user profile data when a new user is created.
    """
    if created:
        logger.info(f"新しいユーザーが作成されました。: {instance.username}")

        # Clear any cached user data
        cache.delete_many(cache.keys(f"ユーザー:{instance.id}:*"))

        # Here you would typically create related profile models
        # from apps.accounts.models import UserProfile
        # UserProfile.objects.create(user=instance)


@receiver(post_save)
def invalidate_user_cache(sender, instance, **kwargs):
    """
    Invalidate user-specific cache when user-related models are updated.
    """
    if hasattr(instance, "user_id"):
        user_id = instance.user_id
        cache.delete_many(cache.keys(f"ユーザー:{user_id}:*"))
        logger.debug(f"Invalidated cache for user {user_id}")


@receiver(post_delete)
def cleanup_soft_deleted_cache(sender, instance, **kwargs):
    """
    Clean up cache when soft-deleted items are actually deleted.
    """
    if hasattr(instance, "user_id"):
        user_id = instance.user_id
        cache.delete_many(cache.keys(f"ユーザー:{user_id}:*"))
        logger.debug(f"Cleaned up cache for deleted instance of user {user_id}")


@receiver(pre_save)
def validate_soft_delete(sender, instance, **kwargs):
    """
    Validate soft delete operations.
    """
    if hasattr(instance, "is_deleted") and instance.is_deleted:
        if not instance.deleted_at:
            instance.deleted_at = timezone.now()

        # Prevent modification of deleted items
        if instance.pk:
            try:
                original = sender.objects.get(pk=instance.pk)
                if original.is_deleted and not kwargs.get("force_update", False):
                    raise ValidationError("Cannot modify deleted items")
            except sender.DoesNotExist:
                pass


@receiver(post_save)
def log_model_changes(sender, instance, created, **kwargs):
    """
    Log important model changes for audit purposes.
    """
    if created:
        logger.info(f"Created new {sender.__name__}: {instance}")
    else:
        logger.info(f"Updated {sender.__name__}: {instance}")


@receiver(post_delete)
def log_model_deletions(sender, instance, **kwargs):
    """
    Log model deletions for audit purposes.
    """
    logger.info(f"Deleted {sender.__name__}: {instance}")
