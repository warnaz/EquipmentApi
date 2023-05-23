from django.apps import AppConfig


class EquapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equapi'
    
    def ready(self) -> None:
        import equapi.signals
