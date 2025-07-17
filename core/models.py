"""
Core models for the intellectual partner application.
Contains base models and common mixins.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides created_at and updated_at fields.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base class that provides soft delete functionally.
    """

    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="削除日時")

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete by setting is_deleted=True and deleted_at timestamp."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        """Restore soft deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class BaseModel(TimeStampedModel, SoftDeleteModel):
    """
    Base model that combines timestamp and soft delete functionally.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)

    class Meta:
        abstract = True


class UserRelatedModel(BaseModel):
    """
    Abstract base class for models that are related to a user.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="ユーザー")

    class Meta:
        abstract = True


class PriorityChoices(models.TextChoices):
    """Common Priority choices for tasks and goals."""

    LOW = "low", "低"
    MEDIUM = "medium", "中"
    HIGH = "high", "高"
    URGENT = "urgent", "緊急"
    HOMEWORK = "homework", "宿題"


class DifficultyChoices(models.TextChoices):
    """Common difficulty choices for tasks and goals."""

    VERY_EASY = "very_easy", "とても簡単"
    EASY = "easy", "簡単"
    MEDIUM = "medium", "普通"
    HARD = "hard", "難しい"
    VERY_HARD = "very_hard", "とても難しい"
    TROUBLESOME = "troublesome", "面倒臭い"


class StatusChoices(models.TextChoices):
    """Common status choices for tasks and goals."""

    NOT_STARTED = "not_started", "未着手"
    IN_PROGRESS = "in_progress", "進行中"
    INACTIVE = "inactive", "放置中"
    COMPLETED = "completed", "完了"
    PAUSED = "paused", "中断"
    CANCELLED = "cancelled", "キャンセル"


class EmotionChoices(models.TextChoices):
    """Common emotion choices for mood tracking."""

    VERY_HAPPY = "very_happy", "😄"
    HAPPY = "happy", "😊"
    NEUTRAL = "neutral", "😐"
    SAD = "sad", "😢"
    VERY_SAD = "very_sad", "😭"
    EXCITED = "excited", "🤩"
    FRUSTRATED = "frustrated", "😤"
    TIRED = "tired", "😴"
    STRESSED = "stressed", "😰"
    RELAXED = "relaxed", "😌"


class ConcentrationLevel(models.Model):
    """Model to track concentration levels during study sessions."""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="concentration_levels")
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="集中度レベル")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="記録時刻")
    session_id = models.UUIDField(verbose_name="セッションID")
    notes = models.TextField(blank=True, verbose_name="メモ")

    class Meta:
        verbose_name = "集中度記録"
        verbose_name_plural = "集中度記録"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} - Level {self.level} at {self.timestamp}"


class StudyEnvironment(models.Model):
    """
    Model to track study environment preferences and conditions.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="study_environment")
    location = models.CharField(max_length=100, verbose_name="場所")
    background_music = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="BGM",
    )
    lighting = models.CharField(
        max_length=50,
        choices=[
            ("bright", "明るい"),
            ("moderate", "普通"),
            ("dim", "暗い"),
        ],
        default="moderate",
        verbose_name="明るさ",
    )
    temperature = models.CharField(
        max_length=50,
        choices=[
            ("hot", "暑い"),
            ("warm", "暖かい"),
            ("comfortable", "快適"),
            ("cool", "涼しい"),
            ("cold", "寒い"),
        ],
        default="comfortable",
        verbose_name="温度",
    )
    noise_level = models.CharField(
        max_length=50,
        choices=[
            ("silent", "静か"),
            ("low", "小さな音"),
            ("moderate", "普通"),
            ("loud", "うるさい"),
        ],
        default="silent",
        verbose_name="環境音",
    )
    effective_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="自己評価"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="記録時刻")

    class Meta:
        verbose_name = "学習環境"
        verbose_name_plural = "学習環境"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} - {self.location} ({self.effectiveness_rating}/5)"


class Tag(BaseModel):
    """
    Generic tag model for categorizing content.
    """

    name = models.CharField(max_length=50, unique=True, verbose_name="タグ名")
    color = models.CharField(max_length=7, default="#3b82F6", verbose_name="色")
    description = models.TextField(blank=True, verbose_name="説明")

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(BaseModel):
    """
    Generic category model for organizing content.
    """

    name = models.CharField(max_length=100, verbose_name="カテゴリ名")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name="親カテゴリ"
    )
    description = models.TextField(blank=True, verbose_name="説明")
    color = models.CharField(max_length=7, default="#3B83F6", verbose_name="色")
    icon = models.CharField(max_length=50, blank=True, verbose_name="アイコン")
    order = models.IntegerField(default=0, verbose_name="表示順序")

    class Meta:
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ"
        ordering = ["order", "name"]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    @property
    def full_path(self):
        """Get the full path of the category."""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class Subject(BaseModel):
    """
    Model to represent academic subjects.
    """

    name = models.CharField(max_length=100, verbose_name="科目名")
    code = models.CharField(max_length=20, unique=True, verbose_name="科目コード")
    color = models.CharField(max_length=7, default="#3B82F6")
    icon = models.CharField(max_length=50, blank=True, verbose_name="アイコン")
    description = models.TextField(blank=True, verbose_name="説明")
    is_active = models.BooleanField(default=True, verbose_name="有効")

    class Meta:
        verbose_name = "科目"
        verbose_name_plural = "科目"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Achievement(BaseModel):
    """
    Model to track user achievements and milestones.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="achievements")
    title = models.CharField(max_length=200, verbose_name="達成タイトル")
    description = models.TextField(verbose_name="説明")
    type = models.CharField(
        max_length=50,
        choices=[
            ("study_time", "学習時間"),
            ("streak", "連続学習"),
            ("goal_completion", "目標達成"),
            ("perfect_score", "満点"),
            ("consistency", "継続性"),
        ],
        verbose_name="達成タイプ",
    )
    points = models.ImageField(default=0, verbose_name="獲得ポイント")
    badge_icon = models.CharField(max_length=50, blank=True, verbose_name="バッジアイコン")
    badge_color = models.CharField(max_length=7, default="#FFD700", verbose_name="バッジカラー")
    achieved_at = models.DateTimeField(auto_now_add=True, verbose_name="達成日時")

    class Meta:
        verbose_name = "達成記録"
        verbose_name_plural = "達成記録"
        ordering = ["-achieved_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"
