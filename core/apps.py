from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    from django.apps import AppConfig

    def ready(self):
        import core.signals  #register the signal for notification on console.
