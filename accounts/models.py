"""
Accounts models for the intellectual partner application.
Contains use authentication and profile related models.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import (
    BaseModel,
    TimeStampedModel,
    DifficultyChoices,
    EmotionChoices,
)
import uuid


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    email = models.EmailField(_("email address"), unique=True)
    is_teacher = models.BooleanField(default=False, verbose_name="教師フラグ")
    is_student = models.BooleanField(default=True, verbose_name="生徒フラグ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    def __str__(self):
        return self.email or self.username


class UserProfile(BaseModel):
    """
    Extended use profile with learning preferences and personal information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Basic Information
    display_name = models.CharField(max_length=100, blank=True, verbose_name="表示名")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="アバター")
    birth_date = models.DateField(blank=True, null=True, verbose_name="生年月日")
    bio = models.TextField(max_length=500, blank=True, verbose_name="自己紹介")

    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="電話番号")
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name="緊急連絡先")

    # Learning Preferences
    preferred_study_time_start = models.TimeField(blank=True, null=True, verbose_name="希望学習開始時間")
    preferred_study_time_end = models.TimeField(blank=True, null=True, verbose_name="希望学習終了時間")
    daily_study_goal_minutes = models.IntegerField(
        default=60,
        validators=[MinValueValidator(1), MaxValueValidator(1440)],
        verbose_name="1日の学習目標時間(分)",
    )

    # Learning Style Preferences
    learning_style = models.CharField(
        max_length=20,
        choices=[
            ("visual", "視覚型"),
            ("auditory", "聴覚型"),
            ("kinesthetic", "体感型"),
            ("mixed", "混合型"),
        ],
        default="mixed",
        verbose_name="学習スタイル",
    )

    concentration_duration = models.IntegerField(
        default=25,
        validators=[MinValueValidator(5), MaxValueValidator(180)],
        verbose_name="集中可能時間(分)",
    )

    preferred_difficulty = models.CharField(
        max_length=20, choices=DifficultyChoices.choices, default=DifficultyChoices.MEDIUM, verbose_name="好みの難易度"
    )

    # Notification Settings
    email_notifications = models.BooleanField(default=True, verbose_name="メール通知")
    push_notifications = models.BooleanField(default=True, verbose_name="プッシュ通知")
    reminder_enabled = models.BooleanField(default=True, verbose_name="リマインダー有効")
    reminder_time = models.TimeField(blank=True, null=True, verbose_name="リマインダー時刻")

    # Gamification Preferences
    show_achievements = models.BooleanField(default=True, verbose_name="達成表示")
    show_leaderboard = models.BooleanField(default=False, verbose_name="ランキング表示")

    # Privacy Settings
    profile_public = models.BooleanField(default=False, verbose_name="プロフィール公開")
    progress_public = models.BooleanField(default=False, verbose_name="進捗公開")

    class Meta:
        verbose_name = "ユーザープロフィール"
        verbose_name_plural = "ユーザープロフィール"

    def __str__(self):
        return f"{self.user.username}さんのプロフィール"

    @property
    def display_name_or_username(self):
        """Return display name if set, otherwise username."""
        return self.display_name or self.user.username


class LearningStyle(BaseModel):
    """
    Detailed learning style assessment and preferences.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="learning_style")

    # Learning Modality Scores (0-10)
    visual_score = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="視覚学習スコア",
    )
    auditory_score = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="聴覚学習スコア",
    )
    kinesthetic_score = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="体感学習スコア",
    )

    # Study Environment Preferences
    prefers_quiet = models.BooleanField(default=True, verbose_name="静かな方が好き")
    prefers_background_music = models.BooleanField(default=False, verbose_name="BGMがある方が好き")
    prefers_group_study = models.BooleanField(default=False, verbose_name="グループ学習が好き")
    prefers_breaks = models.BooleanField(default=False, verbose_name="休憩が好き")

    # Task Management Preferences
    prefers_small_tasks = models.BooleanField(default=True, verbose_name="小さなタスクが好き")
    prefers_deadlines = models.BooleanField(default=True, verbose_name="締切がある方が好き")
    prefers_routine = models.BooleanField(default=True, verbose_name="ルーティンワークが好き")

    # Motivation Preferences
    motivation_type = models.CharField(
        max_length=20,
        choices=[
            ("intrinsic", "自発的"),
            ("extrinsic", "受動的"),
            ("mixed", "混合"),
        ],
        default="mixed",
        verbose_name="動機タイプ",
    )

    feedback_preferences = models.CharField(
        max_length=20,
        choices=[
            ("immediate", "すぐに"),
            ("delayed", "後から"),
            ("weekly", "毎週"),
        ],
        default="immediate",
        verbose_name="フィードバック時期の希望",
    )

    # Assessment Date
    assessed_at = models.DateTimeField(auto_now=True, verbose_name="評価日時")

    class Meta:
        verbose_name = "学習スタイル"
        verbose_name_plural = "学習スタイル"

    def __str__(self):
        return f"{self.user.username}さんの学習スタイル"

    @property
    def dominant_learning_style(self):
        """Determine the dominant learning style based on scores."""
        scores = {
            "visual": self.visual_score,
            "auditory": self.auditory_score,
            "kinesthetic": self.kinesthetic_score,
        }
        return max(scores, key=scores.get)


class StudentTeacherRelation(BaseModel):
    """
    Model to manage teacher-student relationships.
    """

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="students",
        limit_choices_to={"is_teacher": True},
        verbose_name="教師",
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teachers",
        limit_choices_to={"is_student": True},
        verbose_name="生徒",
    )

    # Relationship Details
    subject = models.CharField(max_length=100, blank=True, verbose_name="担当科目")
    class_name = models.CharField(max_length=100, blank=True, verbose_name="クラス名")
    academic_year = models.CharField(max_length=10, blank=True, verbose_name="学年")

    # Permission Levels
    can_assign_tasks = models.BooleanField(default=True, verbose_name="タスク割当権限")
    can_view_progress = models.BooleanField(default=True, verbose_name="進捗閲覧権限")
    can_view_emotions = models.BooleanField(default=False, verbose_name="感情ログ閲覧権限")
    can_send_messages = models.BooleanField(default=True, verbose_name="メッセージ送信権限")

    # Relationship Status
    is_active = models.BooleanField(default=True, verbose_name="関係有効")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="開始日時")
    ended_at = models.DateTimeField(blank=True, null=True, verbose_name="終了日時")

    class Meta:
        verbose_name = "関係性"
        verbose_name_plural = "関係性"
        unique_together = ["teacher", "student", "subject"]

    def __str__(self):
        subject_str = f" ({self.subject})" if self.subject else ""
        return f"{self.teacher.username} -> {self.student.username}{subject_str}"


class UserSettings(BaseModel):
    """
    User-specific application settings and preferences.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")

    # Theme and UI Preferences
    theme = models.CharField(
        max_length=10,
        choices=[
            ("light", "ライト"),
            ("dark", "ダーク"),
            ("auto", "自動"),
        ],
        default="auto",
        verbose_name="テーマ",
    )

    language = models.CharField(
        max_length=10,
        choices=[
            "ja",
            "日本語",
            "en",
            "English",
        ],
        default="ja",
        verbose_name="言語",
    )

    timezone = models.CharField(
        max_length=50,
        default="Asia/Tokyo",
        verbose_name="タイムゾーン",
    )

    # Analytics and Privacy
    analytics_enabled = models.BooleanField(default=True, verbose_name="分析権限")
    data_sharing_enabled = models.BooleanField(default=False, verbose_name="データ共有権限")

    # Accessibility
    high_contrast = models.BooleanField(default=False, verbose_name="高コントラスト")
    large_text = models.BooleanField(default=False, verbose_name="大きな文字")
    screen_reader_support = models.BooleanField(default=False, verbose_name="スクリーンリーダー対応")

    # Advanced Features
    beta_features_enabled = models.BooleanField(default=False, verbose_name="ベータ機能有効")
    advanced_analytics = models.BooleanField(default=False, verbose_name="高度な分析")

    class Meta:
        verbose_name = "ユーザー設定"
        verbose_name_plural = "ユーザー設定"

    def __str__(self):
        return f"{self.user.username}さんの設定"


class UserStatistics(TimeStampedModel):
    """
    Cached user statistics for performance optimization.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="statistics")

    # Study Statistics
    total_study_time_minutes = models.IntegerField(default=0, verbose_name="総学習時間(分)")
    current_streak_days = models.IntegerField(default=0, verbose_name="現在の連続継続日数")
    longest_streak_days = models.IntegerField(default=0, verbose_name="最長連続継続日数")

    # Task Statistics
    total_task_completed = models.IntegerField(default=0, verbose_name="完了タスク総数")
    total_task_created = models.IntegerField(default=0, verbose_name="作成タスク総数")
    average_task_completion_time = models.FloatField(default=0.0, verbose_name="平均タスク完了時間")

    # Goal Statistics
    total_goals_achieved = models.IntegerField(default=0, verbose_name="達成目標総数")
    current_active_goals = models.IntegerField(default=0, verbose_name="現在の活動目標数")

    # Engagement Statistics
    total_login_days = models.IntegerField(default=0, verbose_name="総ログイン日数")
    last_login_date = models.DateField(blank=True, null=True, verbose_name="最終ログイン日")
    average_session_duration = models.FloatField(default=0.0, verbose_name="平均セッション時間")

    # Emotional State
    most_common_emotion = models.CharField(
        max_length=20, choices=EmotionChoices.choices, blank=True, verbose_name="最頻出感情"
    )
    average_concentration_level = models.FloatField(default=5.0, verbose_name="平均集中レベル")

    # Cache TimeStamp
    last_calculated_at = models.DateTimeField(auto_now=True, verbose_name="最終計算日時")

    class Meta:
        verbose_name = "ユーザー統計"
        verbose_name_plural = "ユーザー統計"

    def __str__(self):
        return f"{self.user.username}さんの統計"

    @property
    def completion_rate(self):
        """Calculate task completion rate."""
        if self.total_task_created == 0:
            return 0.0
        return (self.total_task_completed / self.total_task_created) * 100
