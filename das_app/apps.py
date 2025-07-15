from django.apps import AppConfig


class DasAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'das_app'
    verbose_name = "Das And Partners"


    def ready(self):
        import das_app.signals


