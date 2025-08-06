from django.apps import AppConfig


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'

    # importando signals para que sejam carregados quando o app for iniciado
    def ready(self):
        import service.signals
