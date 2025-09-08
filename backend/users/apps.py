# backend/apps/users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        # import signals to register receivers
        from . import signals  # noqa
