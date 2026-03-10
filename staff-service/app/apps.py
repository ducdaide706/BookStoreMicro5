from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from .models import Staff
        try:
            Staff.create_root()
        except Exception:
            pass