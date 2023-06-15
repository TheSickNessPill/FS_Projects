from django.apps import AppConfig


class AnnouncementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'announcement'

    def ready(self):
        from announcement import signals  # выполнение модуля -> регистрация сигналов
