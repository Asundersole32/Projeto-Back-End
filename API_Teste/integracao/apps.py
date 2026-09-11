from django.apps import AppConfig


class IntegracaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integracao'

    def ready(self):
        from . import adapters      # noqa — registra adapters
        from . import auth          # noqa — registra auth strategies
        from . import transforms    # noqa — registra transforms
        from . import webhooks      # noqa — registra webhook auth strategies
    