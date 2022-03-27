from django.apps import AppConfig


class CritiqueConfig(AppConfig):
    name = 'critique'

    def ready(self):
        import critique.signals
