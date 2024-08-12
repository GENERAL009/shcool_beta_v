from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'

    def ready(self):
        import authapp.signals  # Импортируйте ваши сигналы

# myapp/apps.py
