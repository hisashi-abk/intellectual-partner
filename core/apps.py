from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "コア機能"

    def ready(self):
        """
        Called when the application is ready.
        Register any signals here.
        """
        import core.signals
