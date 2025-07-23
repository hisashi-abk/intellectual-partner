"""
Celery configuration for Intellectual Partner application
"""

import os
from celery import Celery
from django.conf import settings

# Django設定モジュールを設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Celeryアプリケーションのインスタンス作成
app = Celery("intellectual_partner")

# Django設定からCelery設定を読み込み
app.config_from_object("django.conf:settings", namespace="CELERY")

# タスクの自動検出
app.autodiscover_tasks()

# タスクの設定
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tokyo",
    enable_utc=True,
    # タスクのルーティング
    task_routes={
        "analytics.tasks.*": {"queue": "analytics"},
        "notifications.tasks.*": {"queue": "notifications"},
        "teacher_support.tasks.*": {"queue": "teacher_support"},
    },
    # ワーカー設定
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    # タスクの実行時間制限
    task_sort_time_limit=300,  # 5分
    task_time_limit=600,  # 10分
    # 結果の保存期間
    result_expires=3600,  # 1時間
    # 定期タスクのスケジュール (Celery Beat)
    beat_schedule={
        # 放置チケット検出 (毎日午前9時)
        "defeat-abandoned-tickets": {
            "task": "tickets.tasks.detect_abandoned_tickets",
            "schedule": 60.0 * 60.0 * 24.0,  # 24時間ごと
            "options": {"queue": "notifications"},
        },
        # 学習データ分析 (毎日午前2時)
        "daily_analytics": {
            "task": "analytics.tasks.daily_analytics_processing",
            "schedule": 60.0 * 60.0 * 24.0,  # 24時間ごと
            "options": {"queue": "analytics"},
        },
        # 週次レポート生成 (毎週月曜日午前8時)
        "weekly-reports": {
            "task": "teacher_support.tasks.generate_weekly_reports",
            "schedule": 60.0 * 60.0 * 24.0 * 7.0,  # 週1回
            "options": {"queue": "teacher_support"},
        },
        # 通知クリーンアップ(毎日午前3時)
        "cleanup-old-notifications": {
            "task": "notifications.tasks.cleanup_old_notifications",
            "schedule": 60.0 * 60.0 * 24.0,  # 24時間ごと
            "options": {"queue": "notifications"},
        },
        # 感情データ集計 (毎時)
        "hourly-emotion-aggregation": {
            "task": "emotions.tasks.aggregation_emotion_data",
            "schedule": 60.0 * 60.0,  # 1時間ごと
            "options": {"queue": "analytics"},
        },
    },
)


@app.task(bind=True)
def debug_task(self):
    """デバッグ用タスク"""
    print(f"Request: {self.request!r}")


# エラーハンドリング設定
@app.task(bind=True)
def handle_task_failure(self, exc, task_id, args, kwargs, traceback):
    """タスク失敗時の処理"""
    print(f"Task {task_id} failed: {exc}")

    # Sentryなどの監視システムに送信
    if hasattr(settings, "SENTRY_DSN") and settings.SENTRY_DSN:
        import sentry_sdk

        sentry_sdk.capture_exception(exc)


# カスタムタスククラス
class CallbackTask(app.Task):
    """コールバック付きタスク基底クラス"""

    def on_success(self, retval, task_id, args, kwargs):
        """タスク成功時のコールバック"""
        print(f"Task {task_id} succeeded with result: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """タスク失敗時のコールバック"""
        print(f"Task {task_id} failed: {exc}")
        handle_task_failure.delay(exc, task_id, args, kwargs, str(einfo))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """ "タスクリトライ時のコールバック"""
        print(f"Task {task_id} is being retried: {exc}")


# デフォルトタスククラスを設定
app.Task = CallbackTask

if __name__ == "__main__":
    app.start()
