from django.apps import AppConfig


class QuestAnsConfig(AppConfig):
    name = 'uliza'

    def ready(self):
        import uliza.signals.listener